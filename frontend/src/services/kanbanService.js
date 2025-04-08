// Arquivo de integração do painel Kanban com o sistema principal
// Este arquivo configura a integração entre o frontend e o backend para o módulo Kanban

import api from './api';

/**
 * Serviço para integração com o módulo de Kanban
 */
const kanbanService = {
  /**
   * Obtém dados de licitações organizados para o painel Kanban
   * 
   * @returns {Promise} - Promise com os dados das licitações organizados por status
   */
  obterDadosKanban: async () => {
    try {
      const response = await api.get('/api/v1/licitacoes');
      
      // Organiza as licitações por status (coluna)
      const colunas = {
        rascunho: {
          id: 'rascunho',
          title: 'Rascunho',
          items: []
        },
        publicada: {
          id: 'publicada',
          title: 'Publicada',
          items: []
        },
        em_analise: {
          id: 'em_analise',
          title: 'Em Análise',
          items: []
        },
        adjudicada: {
          id: 'adjudicada',
          title: 'Adjudicada',
          items: []
        },
        homologada: {
          id: 'homologada',
          title: 'Homologada',
          items: []
        },
        concluida: {
          id: 'concluida',
          title: 'Concluída',
          items: []
        },
        cancelada: {
          id: 'cancelada',
          title: 'Cancelada',
          items: []
        }
      };
      
      // Distribui as licitações nas colunas apropriadas
      response.data.forEach(licitacao => {
        if (colunas[licitacao.status]) {
          colunas[licitacao.status].items.push(licitacao);
        }
      });
      
      return colunas;
    } catch (error) {
      console.error('Erro ao obter dados do Kanban:', error);
      throw error;
    }
  },

  /**
   * Atualiza o status de uma licitação (move entre colunas do Kanban)
   * 
   * @param {string} licitacaoId - ID da licitação
   * @param {string} novoStatus - Novo status da licitação
   * @returns {Promise} - Promise com os dados atualizados da licitação
   */
  atualizarStatusLicitacao: async (licitacaoId, novoStatus) => {
    try {
      const response = await api.put(`/api/v1/licitacoes/${licitacaoId}/status`, {
        status: novoStatus
      });
      return response.data;
    } catch (error) {
      console.error('Erro ao atualizar status da licitação:', error);
      throw error;
    }
  },

  /**
   * Verifica se a transição de status é válida
   * 
   * @param {string} statusAtual - Status atual da licitação
   * @param {string} novoStatus - Novo status da licitação
   * @returns {boolean} - True se a transição for válida, False caso contrário
   */
  verificarTransicaoValida: (statusAtual, novoStatus) => {
    // Mapeamento de transições válidas
    const transicoesValidas = {
      'rascunho': ['publicada', 'cancelada'],
      'publicada': ['em_analise', 'cancelada', 'suspensa'],
      'em_analise': ['adjudicada', 'cancelada', 'suspensa'],
      'adjudicada': ['homologada', 'cancelada', 'suspensa'],
      'homologada': ['concluida', 'cancelada', 'suspensa'],
      'suspensa': ['publicada', 'em_analise', 'adjudicada', 'homologada', 'cancelada'],
      'concluida': [],
      'cancelada': []
    };
    
    return transicoesValidas[statusAtual]?.includes(novoStatus) || false;
  }
};

export default kanbanService;
