"""
Módulo de inicialização da API para o Sistema de Gestão de Licitações Governamentais.
Este módulo configura os roteadores para os diferentes endpoints da API.
"""

from fastapi import APIRouter

from .endpoints import users, auth, licitacoes, fornecedores, propostas

# Criação do roteador principal da API
api_router = APIRouter()

# Inclusão dos roteadores específicos para cada recurso
api_router.include_router(auth.router, prefix="/auth", tags=["autenticação"])
api_router.include_router(users.router, prefix="/users", tags=["usuários"])
api_router.include_router(licitacoes.router, prefix="/licitacoes", tags=["licitações"])
api_router.include_router(fornecedores.router, prefix="/fornecedores", tags=["fornecedores"])
api_router.include_router(propostas.router, prefix="/propostas", tags=["propostas"])
