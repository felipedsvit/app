// Arquivo de integração do módulo Kanban no backend
// Este arquivo configura a integração do módulo Kanban com o restante do sistema

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List

from app.db.session import get_db
from app.models.licitacao import Licitacao, StatusLicitacao
from app.models.user import User, UserRole
from app.core.security import get_current_active_user, check_user_role

# Definição das colunas do Kanban
KANBAN_COLUMNS = [
    {"id": "rascunho", "title": "Rascunho", "color": "#e0e0e0"},
    {"id": "publicada", "title": "Publicada", "color": "#a5d6a7"},
    {"id": "em_analise", "title": "Em Análise", "color": "#90caf9"},
    {"id": "adjudicada", "title": "Adjudicada", "color": "#9fa8da"},
    {"id": "homologada", "title": "Homologada", "color": "#ce93d8"},
    {"id": "concluida", "title": "Concluída", "color": "#81c784"},
    {"id": "cancelada", "title": "Cancelada", "color": "#ef9a9a"},
    {"id": "suspensa", "title": "Suspensa", "color": "#ffcc80"}
]

# Mapeamento de transições válidas
VALID_TRANSITIONS = {
    'rascunho': ['publicada', 'cancelada'],
    'publicada': ['em_analise', 'cancelada', 'suspensa'],
    'em_analise': ['adjudicada', 'cancelada', 'suspensa'],
    'adjudicada': ['homologada', 'cancelada', 'suspensa'],
    'homologada': ['concluida', 'cancelada', 'suspensa'],
    'suspensa': ['publicada', 'em_analise', 'adjudicada', 'homologada', 'cancelada'],
    'concluida': [],
    'cancelada': []
}

def configurar_rotas_kanban(router: APIRouter):
    """
    Configura as rotas para o módulo Kanban.
    
    Args:
        router: Router da API
    """
    
    @router.get("/kanban", response_model=Dict[str, Any])
    def get_kanban_data(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
    ) -> Dict[str, Any]:
        """
        Obtém os dados organizados para o painel Kanban.
        
        Args:
            db: Sessão do banco de dados
            current_user: Usuário autenticado
            
        Returns:
            Dict[str, Any]: Dados organizados por colunas do Kanban
        """
        # Busca todas as licitações
        query = db.query(Licitacao)
        
        # Filtra por usuário se não for admin ou gestor
        if current_user.role not in [UserRole.ADMIN, UserRole.GESTOR, UserRole.ANALISTA]:
            query = query.filter(Licitacao.created_by_id == current_user.id)
        
        licitacoes = query.all()
        
        # Organiza as licitações por status (coluna)
        columns = {}
        for column in KANBAN_COLUMNS:
            column_id = column["id"]
            columns[column_id] = {
                "id": column_id,
                "title": column["title"],
                "color": column["color"],
                "items": []
            }
        
        # Distribui as licitações nas colunas apropriadas
        for licitacao in licitacoes:
            if licitacao.status in columns:
                # Converte para dicionário e adiciona à coluna correspondente
                licitacao_dict = {
                    "id": licitacao.id,
                    "numero": licitacao.numero,
                    "titulo": licitacao.titulo,
                    "status": licitacao.status,
                    "data_abertura": licitacao.data_abertura,
                    "orgao_responsavel": licitacao.orgao_responsavel,
                    "valor_estimado": licitacao.valor_estimado
                }
                columns[licitacao.status]["items"].append(licitacao_dict)
        
        return {
            "columns": columns,
            "valid_transitions": VALID_TRANSITIONS
        }
    
    @router.put("/licitacoes/{licitacao_id}/move", response_model=Dict[str, Any])
    def move_licitacao(
        licitacao_id: str,
        novo_status: StatusLicitacao,
        db: Session = Depends(get_db),
        current_user: User = Depends(check_user_role([UserRole.ADMIN, UserRole.GESTOR]))
    ) -> Dict[str, Any]:
        """
        Move uma licitação para um novo status no Kanban.
        
        Args:
            licitacao_id: ID da licitação
            novo_status: Novo status da licitação
            db: Sessão do banco de dados
            current_user: Usuário autenticado com permissão de administrador ou gestor
            
        Returns:
            Dict[str, Any]: Resultado da operação
            
        Raises:
            HTTPException: Se a licitação não for encontrada ou a transição for inválida
        """
        # Busca a licitação
        licitacao = db.query(Licitacao).filter(Licitacao.id == licitacao_id).first()
        if not licitacao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Licitação não encontrada"
            )
        
        # Verifica se a transição é válida
        if novo_status not in VALID_TRANSITIONS.get(licitacao.status, []):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Transição inválida: {licitacao.status} -> {novo_status}"
            )
        
        # Atualiza o status da licitação
        status_anterior = licitacao.status
        licitacao.status = novo_status
        
        # Se estiver publicando, define a data de publicação
        if novo_status == StatusLicitacao.PUBLICADA and not licitacao.data_publicacao:
            from datetime import datetime
            licitacao.data_publicacao = datetime.utcnow()
        
        # Se estiver concluindo, define a data de encerramento
        if novo_status == StatusLicitacao.CONCLUIDA and not licitacao.data_encerramento:
            from datetime import datetime
            licitacao.data_encerramento = datetime.utcnow()
        
        db.add(licitacao)
        db.commit()
        db.refresh(licitacao)
        
        return {
            "success": True,
            "licitacao_id": licitacao_id,
            "status_anterior": status_anterior,
            "novo_status": novo_status,
            "mensagem": f"Licitação movida com sucesso para {novo_status}"
        }
    
    return router
