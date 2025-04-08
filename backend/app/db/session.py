"""
Configuração da sessão do banco de dados para o Sistema de Gestão de Licitações Governamentais.
Este módulo configura a conexão com o PostgreSQL usando SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..core.config import settings

# Criação do engine do SQLAlchemy com a URI do PostgreSQL
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,  # Verifica a conexão antes de usar
    pool_size=10,        # Tamanho do pool de conexões
    max_overflow=20,     # Máximo de conexões extras permitidas
    pool_recycle=3600,   # Recicla conexões após 1 hora
)

# Criação da fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para modelos ORM
Base = declarative_base()

def get_db():
    """
    Função de dependência para obter uma sessão do banco de dados.
    
    Yields:
        Session: Sessão do banco de dados
        
    Note:
        A sessão é fechada automaticamente após o uso, mesmo em caso de exceção.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
