"""
Configurações centrais da aplicação.
Este módulo contém as configurações globais para o Sistema de Gestão de Licitações Governamentais.
"""

import secrets
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Classe de configurações da aplicação usando Pydantic BaseSettings.
    Permite carregar configurações de variáveis de ambiente ou arquivo .env.
    """
    # Configurações da API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Sistema de Gestão de Licitações Governamentais"
    
    # Segurança
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 dias
    ALGORITHM: str = "HS256"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """
        Validador para configurar origens CORS a partir de string ou lista.
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Banco de dados
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "bids_db"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        """
        Validador para montar a URI de conexão com o banco de dados.
        """
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"{values.get('POSTGRES_DB') or ''}",
        )

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    
    # LGPD e Retenção de Dados
    DATA_ANONYMIZATION_MONTHS: int = 6  # Anonimizar dados após 6 meses de inatividade
    DATA_DELETION_YEARS: int = 5  # Excluir dados após 5 anos
    
    class Config:
        case_sensitive = True
        env_file = ".env"

# Instância global das configurações
settings = Settings()
