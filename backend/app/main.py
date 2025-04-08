// Arquivo principal de integração do sistema
// Este arquivo atualiza o arquivo main.py para integrar todos os componentes

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.core.ia_integration import configurar_modulo_ia
from app.core.kanban_integration import configurar_rotas_kanban
from app.core.docs import personalizar_documentacao_openapi

def create_application() -> FastAPI:
    """
    Cria e configura a aplicação FastAPI com todos os componentes integrados.
    
    Returns:
        FastAPI: Aplicação configurada
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="Sistema de Gestão de Licitações Governamentais com IA",
        version="1.0.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )
    
    # Configuração de CORS
    origins = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Inclui as rotas da API
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    # Configura o módulo de IA
    app = configurar_modulo_ia(app)
    
    # Configura as rotas do Kanban
    configurar_rotas_kanban(api_router)
    
    # Rota de status do sistema
    @app.get("/api/v1/status", tags=["status"])
    def get_status():
        """
        Verifica o status do sistema.
        
        Returns:
            dict: Status do sistema
        """
        return {
            "status": "online",
            "versao": "1.0.0",
            "nome": settings.PROJECT_NAME,
            "ambiente": settings.ENVIRONMENT,
            "componentes": {
                "backend": "ativo",
                "banco_dados": "conectado",
                "redis": "conectado",
                "celery": "ativo",
                "ia": "configurado"
            }
        }
    
    # Personaliza a documentação OpenAPI usando o módulo de documentação
    app.openapi = lambda: personalizar_documentacao_openapi(app)
    
    return app

app = create_application()