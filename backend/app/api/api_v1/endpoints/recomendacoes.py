"""
Endpoint de API para o módulo de recomendação de fornecedores do Sistema de Gestão de Licitações Governamentais.
Este módulo implementa as rotas para o serviço de recomendação baseado em IA.
"""

from typing import Any, List, Dict

from fastapi import APIRouter, Depends, HTTPException, Query, status, BackgroundTasks
from sqlalchemy.orm import Session

from ....core.security import get_current_active_user, check_user_role
from ....db.session import get_db
from ....models.user import User, UserRole
from ....models.licitacao import Licitacao
from ....models.fornecedor import Fornecedor
from ....services.recomendador import RecomendadorFornecedores
from ....worker.tasks import calculate_supplier_scores

router = APIRouter()

# Instância global do recomendador
recomendador = RecomendadorFornecedores()

@router.post("/treinar", status_code=status.HTTP_202_ACCEPTED)
def treinar_recomendador(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_user_role([UserRole.ADMIN, UserRole.GESTOR]))
) -> Dict[str, Any]:
    """
    Treina o modelo de recomendação com os dados atuais de fornecedores.
    Esta operação é executada em background.
    
    Args:
        background_tasks: Tarefas em background do FastAPI
        db: Sessão do banco de dados
        current_user: Usuário autenticado com permissão de administrador ou gestor
        
    Returns:
        Dict[str, Any]: Mensagem de confirmação
    """
    # Função para executar em background
    def treinar_modelo():
        # Busca todos os fornecedores ativos
        fornecedores = db.query(Fornecedor).filter(Fornecedor.is_active == True).all()
        
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
    
    # Adiciona a tarefa para execução em background
    background_tasks.add_task(treinar_modelo)
    
    return {
        "message": "Treinamento do modelo de recomendação iniciado em background",
        "status": "processando"
    }

@router.get("/recomendar/{licitacao_id}", status_code=status.HTTP_200_OK)
def recomendar_fornecedores(
    licitacao_id: str,
    top_n: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_user_role([UserRole.ADMIN, UserRole.GESTOR, UserRole.ANALISTA]))
) -> Dict[str, Any]:
    """
    Recomenda fornecedores para uma licitação específica.
    
    Args:
        licitacao_id: ID da licitação
        top_n: Número de recomendações a retornar (entre 1 e 20)
        db: Sessão do banco de dados
        current_user: Usuário autenticado com permissão adequada
        
    Returns:
        Dict[str, Any]: Lista de fornecedores recomendados com pontuações
    """
    # Verifica se o modelo foi treinado
    if not hasattr(recomendador, 'fornecedores_dados') or not recomendador.fornecedores_dados:
        # Tenta carregar o modelo salvo
        try:
            recomendador.carregar_modelo("modelo_recomendador.joblib")
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Modelo de recomendação não treinado. Execute o endpoint de treinamento primeiro."
            )
    
    # Busca a licitação
    licitacao = db.query(Licitacao).filter(Licitacao.id == licitacao_id).first()
    if not licitacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Licitação não encontrada"
        )
    
    # Prepara os dados da licitação
    licitacao_dados = {
        'id': licitacao.id,
        'titulo': licitacao.titulo,
        'descricao': licitacao.descricao,
        'objeto': licitacao.objeto,
        'palavras_chave': licitacao.palavras_chave
    }
    
    # Gera recomendações
    recomendacoes = recomendador.recomendar(licitacao_dados, top_n=top_n)
    
    # Formata o resultado
    resultado = {
        "licitacao_id": licitacao_id,
        "licitacao_titulo": licitacao.titulo,
        "recomendacoes": []
    }
    
    for rec in recomendacoes:
        fornecedor_id = rec['fornecedor']['id']
        # Busca dados adicionais do fornecedor no banco de dados
        fornecedor_db = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
        
        if fornecedor_db:
            resultado["recomendacoes"].append({
                "fornecedor_id": fornecedor_id,
                "razao_social": fornecedor_db.razao_social,
                "cnpj": fornecedor_db.cnpj,
                "area_atuacao": fornecedor_db.area_atuacao,
                "avaliacao_media": fornecedor_db.avaliacao_media,
                "pontuacao_ia": rec['pontuacao'],
                "ranking": rec['ranking']
            })
    
    return resultado

@router.post("/calcular-pontuacoes/{licitacao_id}", status_code=status.HTTP_202_ACCEPTED)
def calcular_pontuacoes(
    licitacao_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_user_role([UserRole.ADMIN, UserRole.GESTOR]))
) -> Dict[str, Any]:
    """
    Calcula pontuações de IA para todas as propostas de uma licitação.
    Esta operação é executada em background usando Celery.
    
    Args:
        licitacao_id: ID da licitação
        background_tasks: Tarefas em background do FastAPI
        db: Sessão do banco de dados
        current_user: Usuário autenticado com permissão de administrador ou gestor
        
    Returns:
        Dict[str, Any]: Mensagem de confirmação
    """
    # Verifica se a licitação existe
    licitacao = db.query(Licitacao).filter(Licitacao.id == licitacao_id).first()
    if not licitacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Licitação não encontrada"
        )
    
    # Inicia a tarefa Celery em background
    background_tasks.add_task(calculate_supplier_scores, licitacao_id)
    
    return {
        "message": f"Cálculo de pontuações iniciado para a licitação {licitacao_id}",
        "status": "processando"
    }
