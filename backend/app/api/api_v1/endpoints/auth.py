"""
Módulo de endpoints de autenticação para o Sistema de Gestão de Licitações Governamentais.
Este módulo implementa as rotas para login, logout e gerenciamento de tokens.
"""

from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ...core.config import settings
from ...core.security import create_access_token, get_password_hash, verify_password
from ...db.session import get_db
from ...models.user import User
from ...schemas.user import Token, User as UserSchema

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Endpoint para autenticação de usuários e geração de token JWT.
    
    Args:
        db: Sessão do banco de dados
        form_data: Formulário com credenciais de login
        
    Returns:
        Token: Token de acesso JWT
        
    Raises:
        HTTPException: Se as credenciais forem inválidas
    """
    # Busca o usuário pelo email
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # Verifica se o usuário existe e se a senha está correta
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verifica se o usuário está ativo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    
    # Gera o token de acesso
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user.id), expires_delta=access_token_expires
    )
    
    # Atualiza o último login do usuário
    from datetime import datetime
    user.last_login = datetime.utcnow()
    db.commit()
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/test-token", response_model=UserSchema)
def test_token(current_user: User = Depends(get_current_active_user)) -> Any:
    """
    Endpoint para testar a validade do token JWT.
    
    Args:
        current_user: Usuário autenticado
        
    Returns:
        User: Dados do usuário autenticado
    """
    return current_user
