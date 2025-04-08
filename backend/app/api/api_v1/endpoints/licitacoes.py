"""
Módulo de endpoints de licitações para o Sistema de Gestão de Licitações Governamentais.
Este módulo implementa as rotas para gerenciamento de licitações.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ....core.security import get_current_active_user, check_user_role
from ....db.session import get_db
from ....models.user import User, UserRole
from ....models.licitacao import Licitacao, StatusLicitacao
from ....schemas.licitacao import (
    Licitacao as LicitacaoSchema,
    LicitacaoCreate,
    LicitacaoUpdate,
    LicitacaoWithPropostas
)

router = APIRouter()

@router.get("/", response_model=List[LicitacaoSchema])
def read_licitacoes(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    status: StatusLicitacao = None,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Recupera lista de licitações com filtro opcional por status.
    
    Args:
        db: Sessão do banco de dados
        skip: Número de registros para pular (paginação)
        limit: Número máximo de registros a retornar
        status: Filtro opcional por status da licitação
        current_user: Usuário autenticado
        
    Returns:
        List[Licitacao]: Lista de licitações
    """
    query = db.query(Licitacao)
    
    # Aplica filtro por status se fornecido
    if status:
        query = query.filter(Licitacao.status == status)
    
    # Aplica filtro por usuário se não for admin ou gestor
    if current_user.role not in [UserRole.ADMIN, UserRole.GESTOR, UserRole.ANALISTA]:
        query = query.filter(Licitacao.created_by_id == current_user.id)
    
    licitacoes = query.offset(skip).limit(limit).all()
    return licitacoes

@router.post("/", response_model=LicitacaoSchema)
def create_licitacao(
    *,
    db: Session = Depends(get_db),
    licitacao_in: LicitacaoCreate,
    current_user: User = Depends(check_user_role([UserRole.ADMIN, UserRole.GESTOR]))
) -> Any:
    """
    Cria uma nova licitação.
    
    Args:
        db: Sessão do banco de dados
        licitacao_in: Dados da licitação a ser criada
        current_user: Usuário autenticado com permissão de administrador ou gestor
        
    Returns:
        Licitacao: Licitação criada
        
    Raises:
        HTTPException: Se o número da licitação já estiver em uso
    """
    # Verifica se já existe uma licitação com o mesmo número
    licitacao = db.query(Licitacao).filter(Licitacao.numero == licitacao_in.numero).first()
    if licitacao:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Número de licitação já está em uso"
        )
    
    # Cria a nova licitação
    licitacao_data = licitacao_in.dict()
    licitacao = Licitacao(**licitacao_data, created_by_id=current_user.id)
    db.add(licitacao)
    db.commit()
    db.refresh(licitacao)
    return licitacao

@router.get("/{licitacao_id}", response_model=LicitacaoWithPropostas)
def read_licitacao(
    licitacao_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Recupera informações de uma licitação específica com suas propostas.
    
    Args:
        licitacao_id: ID da licitação a ser recuperada
        db: Sessão do banco de dados
        current_user: Usuário autenticado
        
    Returns:
        LicitacaoWithPropostas: Dados da licitação com propostas
        
    Raises:
        HTTPException: Se a licitação não for encontrada ou o usuário não tiver permissão
    """
    licitacao = db.query(Licitacao).filter(Licitacao.id == licitacao_id).first()
    if not licitacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Licitação não encontrada"
        )
    
    # Verifica permissão para acessar a licitação
    if (current_user.role not in [UserRole.ADMIN, UserRole.GESTOR, UserRole.ANALISTA] and 
        licitacao.created_by_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão insuficiente para acessar esta licitação"
        )
    
    return licitacao

@router.put("/{licitacao_id}", response_model=LicitacaoSchema)
def update_licitacao(
    *,
    db: Session = Depends(get_db),
    licitacao_id: str,
    licitacao_in: LicitacaoUpdate,
    current_user: User = Depends(check_user_role([UserRole.ADMIN, UserRole.GESTOR]))
) -> Any:
    """
    Atualiza informações de uma licitação específica.
    
    Args:
        db: Sessão do banco de dados
        licitacao_id: ID da licitação a ser atualizada
        licitacao_in: Dados a serem atualizados
        current_user: Usuário autenticado com permissão de administrador ou gestor
        
    Returns:
        Licitacao: Licitação atualizada
        
    Raises:
        HTTPException: Se a licitação não for encontrada
    """
    licitacao = db.query(Licitacao).filter(Licitacao.id == licitacao_id).first()
    if not licitacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Licitação não encontrada"
        )
    
    # Converte o objeto para dicionário
    licitacao_data = jsonable_encoder(licitacao)
    
    # Atualiza apenas os campos fornecidos
    update_data = licitacao_in.dict(exclude_unset=True)
    
    # Atualiza os dados
    for field in licitacao_data:
        if field in update_data:
            setattr(licitacao, field, update_data[field])
    
    db.add(licitacao)
    db.commit()
    db.refresh(licitacao)
    return licitacao

@router.delete("/{licitacao_id}", response_model=LicitacaoSchema)
def delete_licitacao(
    *,
    db: Session = Depends(get_db),
    licitacao_id: str,
    current_user: User = Depends(check_user_role([UserRole.ADMIN, UserRole.GESTOR]))
) -> Any:
    """
    Cancela uma licitação (não exclui do banco de dados).
    
    Args:
        db: Sessão do banco de dados
        licitacao_id: ID da licitação a ser cancelada
        current_user: Usuário autenticado com permissão de administrador ou gestor
        
    Returns:
        Licitacao: Licitação cancelada
        
    Raises:
        HTTPException: Se a licitação não for encontrada ou já estiver concluída
    """
    licitacao = db.query(Licitacao).filter(Licitacao.id == licitacao_id).first()
    if not licitacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Licitação não encontrada"
        )
    
    # Verifica se a licitação já está concluída
    if licitacao.status in [StatusLicitacao.CONCLUIDA, StatusLicitacao.HOMOLOGADA]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível cancelar uma licitação concluída ou homologada"
        )
    
    # Cancela a licitação
    licitacao.status = StatusLicitacao.CANCELADA
    db.add(licitacao)
    db.commit()
    db.refresh(licitacao)
    return licitacao

@router.put("/{licitacao_id}/status", response_model=LicitacaoSchema)
def update_licitacao_status(
    *,
    db: Session = Depends(get_db),
    licitacao_id: str,
    status: StatusLicitacao,
    current_user: User = Depends(check_user_role([UserRole.ADMIN, UserRole.GESTOR]))
) -> Any:
    """
    Atualiza o status de uma licitação.
    
    Args:
        db: Sessão do banco de dados
        licitacao_id: ID da licitação
        status: Novo status da licitação
        current_user: Usuário autenticado com permissão de administrador ou gestor
        
    Returns:
        Licitacao: Licitação atualizada
        
    Raises:
        HTTPException: Se a licitação não for encontrada ou a transição de status for inválida
    """
    licitacao = db.query(Licitacao).filter(Licitacao.id == licitacao_id).first()
    if not licitacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Licitação não encontrada"
        )
    
    # Verifica transições de status válidas
    if licitacao.status == StatusLicitacao.CANCELADA:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível alterar o status de uma licitação cancelada"
        )
    
    if licitacao.status == StatusLicitacao.CONCLUIDA and status != StatusLicitacao.CONCLUIDA:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível alterar o status de uma licitação concluída"
        )
    
    # Atualiza o status
    licitacao.status = status
    
    # Se estiver publicando, define a data de publicação
    if status == StatusLicitacao.PUBLICADA and not licitacao.data_publicacao:
        from datetime import datetime
        licitacao.data_publicacao = datetime.utcnow()
    
    # Se estiver concluindo, define a data de encerramento
    if status == StatusLicitacao.CONCLUIDA and not licitacao.data_encerramento:
        from datetime import datetime
        licitacao.data_encerramento = datetime.utcnow()
    
    db.add(licitacao)
    db.commit()
    db.refresh(licitacao)
    return licitacao
