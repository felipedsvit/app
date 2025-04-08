"""
Módulo de endpoints de fornecedores para o Sistema de Gestão de Licitações Governamentais.
Este módulo implementa as rotas para gerenciamento de fornecedores.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ....core.security import get_current_active_user, check_user_role
from ....db.session import get_db
from ....models.user import User, UserRole
from ....models.fornecedor import Fornecedor, AvaliacaoFornecedor
from ....schemas.fornecedor import (
    Fornecedor as FornecedorSchema,
    FornecedorCreate,
    FornecedorUpdate,
    FornecedorWithPropostas,
    AvaliacaoFornecedor as AvaliacaoFornecedorSchema,
    AvaliacaoFornecedorCreate
)

router = APIRouter()

@router.get("/", response_model=List[FornecedorSchema])
def read_fornecedores(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    area_atuacao: str = None,
    is_active: bool = True,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Recupera lista de fornecedores com filtros opcionais.
    
    Args:
        db: Sessão do banco de dados
        skip: Número de registros para pular (paginação)
        limit: Número máximo de registros a retornar
        area_atuacao: Filtro opcional por área de atuação
        is_active: Filtro por status ativo/inativo
        current_user: Usuário autenticado
        
    Returns:
        List[Fornecedor]: Lista de fornecedores
    """
    query = db.query(Fornecedor).filter(Fornecedor.is_active == is_active)
    
    # Aplica filtro por área de atuação se fornecido
    if area_atuacao:
        query = query.filter(Fornecedor.area_atuacao.ilike(f"%{area_atuacao}%"))
    
    fornecedores = query.offset(skip).limit(limit).all()
    return fornecedores

@router.post("/", response_model=FornecedorSchema)
def create_fornecedor(
    *,
    db: Session = Depends(get_db),
    fornecedor_in: FornecedorCreate,
    current_user: User = Depends(check_user_role([UserRole.ADMIN, UserRole.GESTOR, UserRole.FORNECEDOR]))
) -> Any:
    """
    Cria um novo fornecedor.
    
    Args:
        db: Sessão do banco de dados
        fornecedor_in: Dados do fornecedor a ser criado
        current_user: Usuário autenticado com permissão adequada
        
    Returns:
        Fornecedor: Fornecedor criado
        
    Raises:
        HTTPException: Se o CNPJ já estiver em uso
    """
    # Verifica se já existe um fornecedor com o mesmo CNPJ
    fornecedor = db.query(Fornecedor).filter(Fornecedor.cnpj == fornecedor_in.cnpj).first()
    if fornecedor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CNPJ já está em uso"
        )
    
    # Cria o novo fornecedor
    fornecedor_data = fornecedor_in.dict()
    
    # Se o usuário for do tipo fornecedor, associa o fornecedor ao usuário
    if current_user.role == UserRole.FORNECEDOR and not fornecedor_in.user_id:
        fornecedor_data["user_id"] = current_user.id
    
    fornecedor = Fornecedor(**fornecedor_data)
    db.add(fornecedor)
    db.commit()
    db.refresh(fornecedor)
    return fornecedor

@router.get("/{fornecedor_id}", response_model=FornecedorWithPropostas)
def read_fornecedor(
    fornecedor_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Recupera informações de um fornecedor específico com suas propostas.
    
    Args:
        fornecedor_id: ID do fornecedor a ser recuperado
        db: Sessão do banco de dados
        current_user: Usuário autenticado
        
    Returns:
        FornecedorWithPropostas: Dados do fornecedor com propostas
        
    Raises:
        HTTPException: Se o fornecedor não for encontrado
    """
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
    if not fornecedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fornecedor não encontrado"
        )
    
    return fornecedor

@router.put("/{fornecedor_id}", response_model=FornecedorSchema)
def update_fornecedor(
    *,
    db: Session = Depends(get_db),
    fornecedor_id: str,
    fornecedor_in: FornecedorUpdate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Atualiza informações de um fornecedor específico.
    
    Args:
        db: Sessão do banco de dados
        fornecedor_id: ID do fornecedor a ser atualizado
        fornecedor_in: Dados a serem atualizados
        current_user: Usuário autenticado
        
    Returns:
        Fornecedor: Fornecedor atualizado
        
    Raises:
        HTTPException: Se o fornecedor não for encontrado ou o usuário não tiver permissão
    """
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
    if not fornecedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fornecedor não encontrado"
        )
    
    # Verifica permissão para atualizar o fornecedor
    if (current_user.role not in [UserRole.ADMIN, UserRole.GESTOR] and 
        (not fornecedor.user_id or fornecedor.user_id != current_user.id)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão insuficiente para atualizar este fornecedor"
        )
    
    # Converte o objeto para dicionário
    fornecedor_data = jsonable_encoder(fornecedor)
    
    # Atualiza apenas os campos fornecidos
    update_data = fornecedor_in.dict(exclude_unset=True)
    
    # Atualiza os dados
    for field in fornecedor_data:
        if field in update_data:
            setattr(fornecedor, field, update_data[field])
    
    db.add(fornecedor)
    db.commit()
    db.refresh(fornecedor)
    return fornecedor

@router.post("/{fornecedor_id}/avaliacoes", response_model=AvaliacaoFornecedorSchema)
def create_avaliacao(
    *,
    db: Session = Depends(get_db),
    fornecedor_id: str,
    avaliacao_in: AvaliacaoFornecedorCreate,
    current_user: User = Depends(check_user_role([UserRole.ADMIN, UserRole.GESTOR, UserRole.ANALISTA]))
) -> Any:
    """
    Cria uma nova avaliação para um fornecedor.
    
    Args:
        db: Sessão do banco de dados
        fornecedor_id: ID do fornecedor a ser avaliado
        avaliacao_in: Dados da avaliação
        current_user: Usuário autenticado com permissão adequada
        
    Returns:
        AvaliacaoFornecedor: Avaliação criada
        
    Raises:
        HTTPException: Se o fornecedor não for encontrado
    """
    # Verifica se o fornecedor existe
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
    if not fornecedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fornecedor não encontrado"
        )
    
    # Cria a nova avaliação
    avaliacao_data = avaliacao_in.dict()
    avaliacao = AvaliacaoFornecedor(**avaliacao_data, avaliador_id=current_user.id)
    db.add(avaliacao)
    db.commit()
    db.refresh(avaliacao)
    
    # Atualiza a avaliação média do fornecedor
    avaliacoes = db.query(AvaliacaoFornecedor).filter(AvaliacaoFornecedor.fornecedor_id == fornecedor_id).all()
    total_pontuacao = sum(a.pontuacao for a in avaliacoes)
    fornecedor.avaliacao_media = total_pontuacao / len(avaliacoes)
    db.add(fornecedor)
    db.commit()
    
    return avaliacao

@router.get("/{fornecedor_id}/avaliacoes", response_model=List[AvaliacaoFornecedorSchema])
def read_avaliacoes(
    fornecedor_id: str,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Recupera avaliações de um fornecedor específico.
    
    Args:
        fornecedor_id: ID do fornecedor
        db: Sessão do banco de dados
        skip: Número de registros para pular (paginação)
        limit: Número máximo de registros a retornar
        current_user: Usuário autenticado
        
    Returns:
        List[AvaliacaoFornecedor]: Lista de avaliações
        
    Raises:
        HTTPException: Se o fornecedor não for encontrado
    """
    # Verifica se o fornecedor existe
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
    if not fornecedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fornecedor não encontrado"
        )
    
    avaliacoes = db.query(AvaliacaoFornecedor).filter(
        AvaliacaoFornecedor.fornecedor_id == fornecedor_id
    ).offset(skip).limit(limit).all()
    
    return avaliacoes
