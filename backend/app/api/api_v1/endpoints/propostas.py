"""
Módulo de endpoints de propostas para o Sistema de Gestão de Licitações Governamentais.
Este módulo implementa as rotas para gerenciamento de propostas.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ....core.security import get_current_active_user, check_user_role
from ....db.session import get_db
from ....models.user import User, UserRole
from ....models.licitacao import Licitacao, Proposta, StatusLicitacao
from ....models.fornecedor import Fornecedor
from ....schemas.licitacao import (
    Proposta as PropostaSchema,
    PropostaCreate,
    PropostaUpdate,
    PropostaWithDetails
)

router = APIRouter()

@router.get("/", response_model=List[PropostaWithDetails])
def read_propostas(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    licitacao_id: str = None,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Recupera lista de propostas com filtro opcional por licitação.
    
    Args:
        db: Sessão do banco de dados
        skip: Número de registros para pular (paginação)
        limit: Número máximo de registros a retornar
        licitacao_id: Filtro opcional por ID da licitação
        current_user: Usuário autenticado
        
    Returns:
        List[PropostaWithDetails]: Lista de propostas com detalhes
    """
    query = db.query(Proposta)
    
    # Aplica filtro por licitação se fornecido
    if licitacao_id:
        query = query.filter(Proposta.licitacao_id == licitacao_id)
    
    # Filtra por fornecedor se o usuário for do tipo fornecedor
    if current_user.role == UserRole.FORNECEDOR:
        fornecedor = db.query(Fornecedor).filter(Fornecedor.user_id == current_user.id).first()
        if fornecedor:
            query = query.filter(Proposta.fornecedor_id == fornecedor.id)
        else:
            return []  # Retorna lista vazia se o usuário fornecedor não tiver um fornecedor associado
    
    propostas = query.offset(skip).limit(limit).all()
    
    # Adiciona detalhes do fornecedor para cada proposta
    result = []
    for proposta in propostas:
        fornecedor = db.query(Fornecedor).filter(Fornecedor.id == proposta.fornecedor_id).first()
        proposta_dict = jsonable_encoder(proposta)
        proposta_dict["fornecedor_nome"] = fornecedor.razao_social
        proposta_dict["fornecedor_avaliacao"] = fornecedor.avaliacao_media
        result.append(proposta_dict)
    
    return result

@router.post("/", response_model=PropostaSchema)
def create_proposta(
    *,
    db: Session = Depends(get_db),
    proposta_in: PropostaCreate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Cria uma nova proposta para uma licitação.
    
    Args:
        db: Sessão do banco de dados
        proposta_in: Dados da proposta a ser criada
        current_user: Usuário autenticado
        
    Returns:
        Proposta: Proposta criada
        
    Raises:
        HTTPException: Se a licitação não for encontrada, não estiver aberta para propostas,
                      ou o usuário não tiver um fornecedor associado
    """
    # Verifica se a licitação existe e está aberta para propostas
    licitacao = db.query(Licitacao).filter(Licitacao.id == proposta_in.licitacao_id).first()
    if not licitacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Licitação não encontrada"
        )
    
    if licitacao.status != StatusLicitacao.PUBLICADA:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta licitação não está aberta para propostas"
        )
    
    # Identifica o fornecedor associado ao usuário
    fornecedor = None
    if current_user.role == UserRole.FORNECEDOR:
        fornecedor = db.query(Fornecedor).filter(Fornecedor.user_id == current_user.id).first()
        if not fornecedor:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário não tem um fornecedor associado"
            )
    elif current_user.role in [UserRole.ADMIN, UserRole.GESTOR]:
        # Administradores e gestores podem criar propostas para qualquer fornecedor
        fornecedor_id = proposta_in.dict().get("fornecedor_id")
        if fornecedor_id:
            fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
            if not fornecedor:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Fornecedor não encontrado"
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID do fornecedor é obrigatório"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão insuficiente para criar propostas"
        )
    
    # Verifica se o fornecedor já enviou uma proposta para esta licitação
    proposta_existente = db.query(Proposta).filter(
        Proposta.licitacao_id == proposta_in.licitacao_id,
        Proposta.fornecedor_id == fornecedor.id
    ).first()
    
    if proposta_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este fornecedor já enviou uma proposta para esta licitação"
        )
    
    # Cria a nova proposta
    proposta_data = proposta_in.dict()
    proposta_data["fornecedor_id"] = fornecedor.id
    proposta = Proposta(**proposta_data)
    db.add(proposta)
    db.commit()
    db.refresh(proposta)
    return proposta

@router.get("/{proposta_id}", response_model=PropostaWithDetails)
def read_proposta(
    proposta_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Recupera informações de uma proposta específica.
    
    Args:
        proposta_id: ID da proposta a ser recuperada
        db: Sessão do banco de dados
        current_user: Usuário autenticado
        
    Returns:
        PropostaWithDetails: Dados da proposta com detalhes do fornecedor
        
    Raises:
        HTTPException: Se a proposta não for encontrada ou o usuário não tiver permissão
    """
    proposta = db.query(Proposta).filter(Proposta.id == proposta_id).first()
    if not proposta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proposta não encontrada"
        )
    
    # Verifica permissão para acessar a proposta
    if current_user.role == UserRole.FORNECEDOR:
        fornecedor = db.query(Fornecedor).filter(Fornecedor.user_id == current_user.id).first()
        if not fornecedor or fornecedor.id != proposta.fornecedor_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissão insuficiente para acessar esta proposta"
            )
    
    # Adiciona detalhes do fornecedor
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == proposta.fornecedor_id).first()
    proposta_dict = jsonable_encoder(proposta)
    proposta_dict["fornecedor_nome"] = fornecedor.razao_social
    proposta_dict["fornecedor_avaliacao"] = fornecedor.avaliacao_media
    
    return proposta_dict

@router.put("/{proposta_id}", response_model=PropostaSchema)
def update_proposta(
    *,
    db: Session = Depends(get_db),
    proposta_id: str,
    proposta_in: PropostaUpdate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Atualiza informações de uma proposta específica.
    
    Args:
        db: Sessão do banco de dados
        proposta_id: ID da proposta a ser atualizada
        proposta_in: Dados a serem atualizados
        current_user: Usuário autenticado
        
    Returns:
        Proposta: Proposta atualizada
        
    Raises:
        HTTPException: Se a proposta não for encontrada, a licitação não estiver aberta,
                      ou o usuário não tiver permissão
    """
    proposta = db.query(Proposta).filter(Proposta.id == proposta_id).first()
    if not proposta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proposta não encontrada"
        )
    
    # Verifica se a licitação ainda está aberta para propostas
    licitacao = db.query(Licitacao).filter(Licitacao.id == proposta.licitacao_id).first()
    if licitacao.status != StatusLicitacao.PUBLICADA and current_user.role not in [UserRole.ADMIN, UserRole.GESTOR]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta licitação não está mais aberta para alterações em propostas"
        )
    
    # Verifica permissão para atualizar a proposta
    if current_user.role == UserRole.FORNECEDOR:
        fornecedor = db.query(Fornecedor).filter(Fornecedor.user_id == current_user.id).first()
        if not fornecedor or fornecedor.id != proposta.fornecedor_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissão insuficiente para atualizar esta proposta"
            )
    
    # Converte o objeto para dicionário
    proposta_data = jsonable_encoder(proposta)
    
    # Atualiza apenas os campos fornecidos
    update_data = proposta_in.dict(exclude_unset=True)
    
    # Administradores e gestores podem atualizar o status e a pontuação da IA
    if current_user.role not in [UserRole.ADMIN, UserRole.GESTOR]:
        if "status" in update_data:
            del update_data["status"]
        if "pontuacao_ia" in update_data:
            del update_data["pontuacao_ia"]
        if "is_vencedora" in update_data:
            del update_data["is_vencedora"]
    
    # Atualiza os dados
    for field in proposta_data:
        if field in update_data:
            setattr(proposta, field, update_data[field])
    
    db.add(proposta)
    db.commit()
    db.refresh(proposta)
    return proposta

@router.put("/{proposta_id}/vencedora", response_model=PropostaSchema)
def set_proposta_vencedora(
    *,
    db: Session = Depends(get_db),
    proposta_id: str,
    current_user: User = Depends(check_user_role([UserRole.ADMIN, UserRole.GESTOR]))
) -> Any:
    """
    Define uma proposta como vencedora da licitação.
    
    Args:
        db: Sessão do banco de dados
        proposta_id: ID da proposta a ser definida como vencedora
        current_user: Usuário autenticado com permissão de administrador ou gestor
        
    Returns:
        Proposta: Proposta atualizada
        
    Raises:
        HTTPException: Se a proposta não for encontrada ou a licitação não estiver em análise
    """
    proposta = db.query(Proposta).filter(Proposta.id == proposta_id).first()
    if not proposta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proposta não encontrada"
        )
    
    # Verifica se a licitação está em análise
    licitacao = db.query(Licitacao).filter(Licitacao.id == proposta.licitacao_id).first()
    if licitacao.status != StatusLicitacao.EM_ANALISE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A licitação deve estar em análise para definir uma proposta vencedora"
        )
    
    # Remove o status de vencedora de todas as propostas desta licitação
    propostas = db.query(Proposta).filter(Proposta.licitacao_id == proposta.licitacao_id).all()
    for p in propostas:
        p.is_vencedora = False
    
    # Define a proposta atual como vencedora
    proposta.is_vencedora = True
    proposta.status = "vencedora"
    
    # Atualiza o status da licitação para adjudicada
    licitacao.status = StatusLicitacao.ADJUDICADA
    
    db.add_all(propostas + [proposta, licitacao])
    db.commit()
    db.refresh(proposta)
    return proposta
