// Arquivo de integração do módulo de IA com o sistema principal
// Este arquivo configura a integração entre o frontend e o backend para o módulo de recomendações

import api from './api';

/**
 * Serviço para integração com o módulo de IA de recomendações
 */
const recomendacoesService = {
  /**
   * Obtém recomendações de fornecedores para uma licitação específica
   * 
   * @param {string} licitacaoId - ID da licitação
   * @param {number} topN - Número de recomendações a retornar
   * @returns {Promise} - Promise com os dados das recomendações
   */
  obterRecomendacoes: async (licitacaoId, topN = 5) => {
    try {
      const response = await api.get(`/api/v1/recomendacoes/recomendar/${licitacaoId}?top_n=${topN}`);
      return response.data;
    } catch (error) {
      console.error('Erro ao obter recomendações:', error);
      throw error;
    }
  },

  /**
   * Inicia o treinamento do modelo de recomendação
   * 
   * @returns {Promise} - Promise com o status do treinamento
   */
  treinarModelo: async () => {
    try {
      const response = await api.post('/api/v1/recomendacoes/treinar');
      return response.data;
    } catch (error) {
      console.error('Erro ao treinar modelo:', error);
      throw error;
    }
  },

  /**
   * Calcula pontuações de IA para propostas de uma licitação
   * 
   * @param {string} licitacaoId - ID da licitação
   * @returns {Promise} - Promise com o status do cálculo
   */
  calcularPontuacoes: async (licitacaoId) => {
    try {
      const response = await api.post(`/api/v1/recomendacoes/calcular-pontuacoes/${licitacaoId}`);
      return response.data;
    } catch (error) {
      console.error('Erro ao calcular pontuações:', error);
      throw error;
    }
  },

  /**
   * Envia convite para um fornecedor participar de uma licitação
   * 
   * @param {string} licitacaoId - ID da licitação
   * @param {string} fornecedorId - ID do fornecedor
   * @returns {Promise} - Promise com o status do convite
   */
  convidarFornecedor: async (licitacaoId, fornecedorId) => {
    try {
      const response = await api.post(`/api/v1/licitacoes/${licitacaoId}/convidar-fornecedor`, {
        fornecedor_id: fornecedorId
      });
      return response.data;
    } catch (error) {
      console.error('Erro ao convidar fornecedor:', error);
      throw error;
    }
  }
};

export default recomendacoesService;
