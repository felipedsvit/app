// Arquivo de configuração para integração do módulo de IA no backend
// Este arquivo configura a integração do módulo de IA com o restante do sistema

from fastapi import FastAPI, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.api.api_v1.endpoints import recomendacoes
from app.api.api_v1.api import api_router
from app.db.session import get_db
from app.services.recomendador import RecomendadorFornecedores
from app.models.fornecedor import Fornecedor

# Instância global do recomendador
recomendador = RecomendadorFornecedores()

def configurar_modulo_ia(app: FastAPI):
    """
    Configura o módulo de IA no aplicativo FastAPI.
    
    Args:
        app: Instância do aplicativo FastAPI
    """
    # Registra as rotas de recomendações
    api_router.include_router(
        recomendacoes.router,
        prefix="/recomendacoes",
        tags=["recomendacoes"]
    )
    
    # Configura eventos de inicialização
    @app.on_event("startup")
    async def carregar_modelo_ia():
        """
        Tenta carregar o modelo de IA durante a inicialização do aplicativo.
        Se o modelo não existir, cria um modelo vazio.
        """
        try:
            # Tenta carregar o modelo salvo
            recomendador.carregar_modelo("modelo_recomendador.joblib")
            print("Modelo de IA carregado com sucesso.")
        except Exception as e:
            print(f"Não foi possível carregar o modelo de IA: {str(e)}")
            print("Um novo modelo será treinado quando solicitado.")
            
            # Cria um modelo vazio
            recomendador.fornecedores_dados = []
            recomendador.fornecedores_vetores = None
    
    # Configura tarefa de treinamento inicial
    @app.on_event("startup")
    async def agendar_treinamento_inicial(background_tasks: BackgroundTasks = BackgroundTasks(), db: Session = Depends(get_db)):
        """
        Agenda um treinamento inicial do modelo de IA se não houver um modelo treinado.
        
        Args:
            background_tasks: Tarefas em background do FastAPI
            db: Sessão do banco de dados
        """
        async def treinar_modelo_inicial():
            # Verifica se o modelo já está treinado
            if not recomendador.fornecedores_vetores:
                try:
                    # Busca todos os fornecedores ativos
                    fornecedores = db.query(Fornecedor).filter(Fornecedor.is_active == True).all()
                    
                    if fornecedores:
                        # Converte para lista de dicionários
                        fornecedores_dados = []
                        for f in fornecedores:
                            fornecedores_dados.append({
                                'id': f.id,
                                'razao_social': f.razao_social,
                                'descricao': f.descricao,
                                'area_atuacao': f.area_atuacao,
                                'especialidades': f.especialidades,
                                'palavras_chave': f.palavras_chave
                            })
                        
                        # Treina o modelo
                        recomendador.treinar(fornecedores_dados)
                        
                        # Salva o modelo
                        recomendador.salvar_modelo("modelo_recomendador.joblib")
                        print(f"Modelo de IA treinado inicialmente com {len(fornecedores_dados)} fornecedores.")
                except Exception as e:
                    print(f"Erro no treinamento inicial do modelo de IA: {str(e)}")
        
        # Agenda a tarefa para execução em background
        background_tasks.add_task(treinar_modelo_inicial)
    
    return app
