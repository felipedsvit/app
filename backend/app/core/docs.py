"""
Documentação da API do Sistema de Gestão de Licitações Governamentais.
Este arquivo configura a documentação OpenAPI (Swagger) para a API.
"""

from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI

def custom_openapi(app: FastAPI):
    """
    Configura a documentação OpenAPI personalizada para o sistema.
    
    Args:
        app: Instância do FastAPI
        
    Returns:
        dict: Esquema OpenAPI personalizado
    """
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Sistema de Gestão de Licitações Governamentais",
        version="1.0.0",
        description="""
        # API do Sistema de Gestão de Licitações Governamentais
        
        Esta API fornece acesso ao Sistema de Gestão de Licitações Governamentais, uma plataforma completa para gerenciamento de processos licitatórios com recursos de IA para recomendação de fornecedores.
        
        ## Recursos Principais
        
        * **Autenticação e Autorização**: Sistema seguro com OAuth2, JWT e RBAC
        * **Gestão de Licitações**: CRUD completo para licitações e propostas
        * **Gestão de Fornecedores**: Cadastro e avaliação de fornecedores
        * **Recomendações de IA**: Sugestão inteligente de fornecedores para licitações
        * **Painel Kanban**: Visualização e gerenciamento do fluxo de licitações
        * **Automação de Processos**: Tarefas em background com Celery
        
        ## Perfis de Usuário
        
        * **Administrador**: Acesso completo ao sistema
        * **Gestor**: Gerenciamento de licitações e aprovações
        * **Analista**: Análise de propostas e recomendações
        * **Fornecedor**: Visualização de licitações e envio de propostas
        
        ## Conformidade
        
        O sistema está em conformidade com a LGPD (Lei Geral de Proteção de Dados) e implementa criptografia PGP para documentos sensíveis.
        """,
        routes=app.routes,
    )
    
    # Adiciona informações de segurança
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/api/v1/auth/login",
                    "scopes": {}
                }
            }
        },
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    # Adiciona tags com descrições
    openapi_schema["tags"] = [
        {
            "name": "auth",
            "description": "Operações de autenticação e autorização"
        },
        {
            "name": "users",
            "description": "Gerenciamento de usuários do sistema"
        },
        {
            "name": "licitacoes",
            "description": "Gerenciamento de licitações governamentais"
        },
        {
            "name": "fornecedores",
            "description": "Gerenciamento de fornecedores"
        },
        {
            "name": "propostas",
            "description": "Gerenciamento de propostas para licitações"
        },
        {
            "name": "recomendacoes",
            "description": "Recomendações de fornecedores baseadas em IA"
        },
        {
            "name": "kanban",
            "description": "Visualização e gerenciamento do fluxo de licitações"
        },
        {
            "name": "status",
            "description": "Verificação de status do sistema"
        }
    ]
    
    # Adiciona exemplos para endpoints principais
    if "paths" in openapi_schema:
        if "/api/v1/auth/login" in openapi_schema["paths"]:
            openapi_schema["paths"]["/api/v1/auth/login"]["post"]["requestBody"]["content"]["application/json"]["example"] = {
                "username": "admin@example.com",
                "password": "password"
            }
        
        if "/api/v1/licitacoes/" in openapi_schema["paths"]:
            openapi_schema["paths"]["/api/v1/licitacoes/"]["post"]["requestBody"]["content"]["application/json"]["example"] = {
                "numero": "2025/001",
                "titulo": "Aquisição de Equipamentos de TI",
                "descricao": "Aquisição de computadores, servidores e equipamentos de rede para modernização do parque tecnológico.",
                "objeto": "Computadores desktop, notebooks, servidores e switches de rede",
                "tipo": "pregao_eletronico",
                "valor_estimado": 1500000.0,
                "orgao_responsavel": "Ministério da Educação",
                "criterio_julgamento": "menor_preco",
                "palavras_chave": "computadores, servidores, TI, tecnologia, informática"
            }
        
        if "/api/v1/recomendacoes/recomendar/{licitacao_id}" in openapi_schema["paths"]:
            openapi_schema["paths"]["/api/v1/recomendacoes/recomendar/{licitacao_id}"]["get"]["responses"]["200"]["content"]["application/json"]["example"] = {
                "licitacao_id": "123",
                "licitacao_titulo": "Aquisição de Equipamentos de TI",
                "recomendacoes": [
                    {
                        "fornecedor_id": "1",
                        "razao_social": "TechSolutions Informática Ltda",
                        "cnpj": "12.345.678/0001-90",
                        "area_atuacao": "Tecnologia da Informação",
                        "avaliacao_media": 4.8,
                        "pontuacao_ia": 92.5,
                        "ranking": 1
                    },
                    {
                        "fornecedor_id": "2",
                        "razao_social": "DevPro Desenvolvimento de Software",
                        "cnpj": "98.765.432/0001-10",
                        "area_atuacao": "Desenvolvimento de Software",
                        "avaliacao_media": 4.2,
                        "pontuacao_ia": 78.3,
                        "ranking": 2
                    }
                ]
            }
    
    # Adiciona informações de contato e licença
    openapi_schema["info"]["contact"] = {
        "name": "Equipe de Desenvolvimento",
        "email": "suporte@licitagov.gov.br",
        "url": "https://licitagov.gov.br/suporte"
    }
    
    openapi_schema["info"]["license"] = {
        "name": "Licença Pública Geral",
        "url": "https://www.gnu.org/licenses/gpl-3.0.html"
    }
    
    # Adiciona logo
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png",
        "altText": "Logo do Sistema de Gestão de Licitações Governamentais"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema
