"""
Módulo de modelos de banco de dados para usuários do Sistema de Gestão de Licitações Governamentais.
Este módulo define o modelo de usuário com seus atributos e relacionamentos.
"""

from sqlalchemy import Boolean, Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import enum

from ..db.session import Base

class UserRole(str, enum.Enum):
    """
    Enumeração para os papéis de usuário no sistema.
    Define os diferentes níveis de acesso e permissões.
    """
    ADMIN = "admin"           # Administrador com acesso total
    GESTOR = "gestor"         # Gestor de licitações
    ANALISTA = "analista"     # Analista de licitações
    FORNECEDOR = "fornecedor" # Fornecedor externo
    USUARIO = "usuario"       # Usuário básico

class User(Base):
    """
    Modelo de usuário para o Sistema de Gestão de Licitações Governamentais.
    
    Attributes:
        id: Identificador único do usuário (UUID)
        email: Email do usuário (único)
        nome: Nome completo do usuário
        hashed_password: Senha criptografada
        role: Papel/função do usuário no sistema
        is_active: Indica se o usuário está ativo
        created_at: Data e hora de criação do usuário
        updated_at: Data e hora da última atualização
        last_login: Data e hora do último login
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nome = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USUARIO, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)
    
    def __repr__(self):
        """Representação em string do objeto User."""
        return f"<User {self.email}>"
