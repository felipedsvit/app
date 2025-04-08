"""
Módulo de endpoints de usuários para o Sistema de Gestão de Licitações Governamentais.
Este módulo implementa as rotas para gerenciamento de usuários.
"""

from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ....core.security import get_current_active_user, get_password_hash, verify_password, check_user_role
from ....db.session import get_db
from ....models.user import User, UserRole
from ....schemas.user import User as UserSchema, UserCreate, UserUpdate, ChangePassword

router = APIRouter()

@router.get("/", response_model=List[UserSchema])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(check_user_role([UserRole.ADMIN, UserRole.GESTOR]))
) -> Any:
    """
    Recupera lista de usuários.
    
    Args:
        db: Sessão do banco de dados
        skip: Número de registros para pular (paginação)
        limit: Número máximo de registros a retornar
        current_user: Usuário autenticado com permissão de administrador ou gestor
        
    Returns:
        List[User]: Lista de usuários
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.post("/", response_model=UserSchema)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
    current_user: User = Depends(check_user_role([UserRole.ADMIN]))
) -> Any:
    """
    Cria um novo usuário.
    
    Args:
        db: Sessão do banco de dados
        user_in: Dados do usuário a ser criado
        current_user: Usuário autenticado com permissão de administrador
        
    Returns:
        User: Usuário criado
        
    Raises:
        HTTPException: Se o email já estiver em uso
    """
    # Verifica se já existe um usuário com o mesmo email
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já está em uso"
        )
    
    # Cria o novo usuário
    user = User(
        email=user_in.email,
        nome=user_in.nome,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/me", response_model=UserSchema)
def read_user_me(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Recupera informações do usuário autenticado.
    
    Args:
        current_user: Usuário autenticado
        
    Returns:
        User: Dados do usuário autenticado
    """
    return current_user

@router.put("/me", response_model=UserSchema)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Atualiza informações do usuário autenticado.
    
    Args:
        db: Sessão do banco de dados
        user_in: Dados a serem atualizados
        current_user: Usuário autenticado
        
    Returns:
        User: Usuário atualizado
    """
    # Converte o objeto para dicionário
    user_data = jsonable_encoder(current_user)
    
    # Atualiza apenas os campos fornecidos
    update_data = user_in.dict(exclude_unset=True)
    
    # Não permite que o usuário altere seu próprio papel
    if "role" in update_data:
        del update_data["role"]
    
    # Atualiza os dados
    for field in user_data:
        if field in update_data:
            setattr(current_user, field, update_data[field])
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/me/change-password", response_model=UserSchema)
def change_password(
    *,
    db: Session = Depends(get_db),
    password_data: ChangePassword,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Altera a senha do usuário autenticado.
    
    Args:
        db: Sessão do banco de dados
        password_data: Senha atual e nova senha
        current_user: Usuário autenticado
        
    Returns:
        User: Usuário atualizado
        
    Raises:
        HTTPException: Se a senha atual estiver incorreta
    """
    # Verifica se a senha atual está correta
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha atual incorreta"
        )
    
    # Atualiza a senha
    current_user.hashed_password = get_password_hash(password_data.new_password)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/{user_id}", response_model=UserSchema)
def read_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_user_role([UserRole.ADMIN, UserRole.GESTOR]))
) -> Any:
    """
    Recupera informações de um usuário específico.
    
    Args:
        user_id: ID do usuário a ser recuperado
        db: Sessão do banco de dados
        current_user: Usuário autenticado com permissão de administrador ou gestor
        
    Returns:
        User: Dados do usuário
        
    Raises:
        HTTPException: Se o usuário não for encontrado
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return user

@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: str,
    user_in: UserUpdate,
    current_user: User = Depends(check_user_role([UserRole.ADMIN]))
) -> Any:
    """
    Atualiza informações de um usuário específico.
    
    Args:
        db: Sessão do banco de dados
        user_id: ID do usuário a ser atualizado
        user_in: Dados a serem atualizados
        current_user: Usuário autenticado com permissão de administrador
        
    Returns:
        User: Usuário atualizado
        
    Raises:
        HTTPException: Se o usuário não for encontrado
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Converte o objeto para dicionário
    user_data = jsonable_encoder(user)
    
    # Atualiza apenas os campos fornecidos
    update_data = user_in.dict(exclude_unset=True)
    
    # Atualiza os dados
    for field in user_data:
        if field in update_data:
            setattr(user, field, update_data[field])
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", response_model=UserSchema)
def delete_user(
    *,
    db: Session = Depends(get_db),
    user_id: str,
    current_user: User = Depends(check_user_role([UserRole.ADMIN]))
) -> Any:
    """
    Desativa um usuário (não exclui do banco de dados).
    
    Args:
        db: Sessão do banco de dados
        user_id: ID do usuário a ser desativado
        current_user: Usuário autenticado com permissão de administrador
        
    Returns:
        User: Usuário desativado
        
    Raises:
        HTTPException: Se o usuário não for encontrado ou se tentar desativar a si mesmo
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Impede que o usuário desative a si mesmo
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível desativar seu próprio usuário"
        )
    
    # Desativa o usuário
    user.is_active = False
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
