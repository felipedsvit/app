// Arquivo de integração principal do sistema
// Este arquivo configura a integração entre todos os componentes do sistema

import api from './api';
import recomendacoesService from './recomendacoesService';
import kanbanService from './kanbanService';

/**
 * Serviço de integração principal do sistema
 * Coordena a comunicação entre os diferentes módulos
 */
const integracaoService = {
  /**
   * Inicializa o sistema, carregando dados necessários e verificando conexões
   * 
   * @returns {Promise} - Promise com o status da inicialização
   */
  inicializarSistema: async () => {
    try {
      // Verifica conexão com o backend
      const statusResponse = await api.get('/api/v1/status');
      
      // Verifica se o modelo de IA está treinado
      let modeloTreinado = false;
      try {
        // Tenta obter recomendações para verificar se o modelo está treinado
        await recomendacoesService.obterRecomendacoes('test', 1);
        modeloTreinado = true;
      } catch (error) {
        console.log('Modelo de IA não está treinado ou ocorreu um erro:', error);
      }
      
      return {
        status: 'online',
        backendConectado: true,
        modeloIATreinado: modeloTreinado,
        versao: statusResponse.data.versao
      };
    } catch (error) {
      console.error('Erro ao inicializar sistema:', error);
      return {
        status: 'offline',
        backendConectado: false,
        modeloIATreinado: false,
        erro: error.message
      };
    }
  },

  /**
   * Processa uma licitação completa, incluindo recomendações de fornecedores
   * 
   * @param {string} licitacaoId - ID da licitação
   * @returns {Promise} - Promise com os dados processados
   */
  processarLicitacaoCompleta: async (licitacaoId) => {
    try {
      // Obtém dados da licitação
      const licitacaoResponse = await api.get(`/api/v1/licitacoes/${licitacaoId}`);
      const licitacao = licitacaoResponse.data;
      
      // Obtém recomendações de fornecedores
      let recomendacoes = [];
      try {
        const recomendacoesData = await recomendacoesService.obterRecomendacoes(licitacaoId, 5);
        recomendacoes = recomendacoesData.recomendacoes || [];
      } catch (error) {
        console.warn('Não foi possível obter recomendações:', error);
      }
      
      // Obtém propostas existentes
      const propostasResponse = await api.get(`/api/v1/propostas?licitacao_id=${licitacaoId}`);
      const propostas = propostasResponse.data;
      
      // Retorna dados consolidados
      return {
        licitacao,
        recomendacoes,
        propostas,
        processadoEm: new Date().toISOString()
      };
    } catch (error) {
      console.error('Erro ao processar licitação completa:', error);
      throw error;
    }
  },

  /**
   * Atualiza o status de uma licitação e recalcula recomendações
   * 
   * @param {string} licitacaoId - ID da licitação
   * @param {string} novoStatus - Novo status da licitação
   * @returns {Promise} - Promise com o resultado da operação
   */
  atualizarLicitacaoERecalcular: async (licitacaoId, novoStatus) => {
    try {
      // Verifica se a transição de status é válida
      const licitacaoResponse = await api.get(`/api/v1/licitacoes/${licitacaoId}`);
      const statusAtual = licitacaoResponse.data.status;
      
      if (!kanbanService.verificarTransicaoValida(statusAtual, novoStatus)) {
        throw new Error(`Transição de status inválida: ${statusAtual} -> ${novoStatus}`);
      }
      
      // Atualiza o status da licitação
      const atualizacaoResponse = await kanbanService.atualizarStatusLicitacao(licitacaoId, novoStatus);
      
      // Se o status for alterado para "em_analise", calcula pontuações para propostas
      if (novoStatus === 'em_analise') {
        await recomendacoesService.calcularPontuacoes(licitacaoId);
      }
      
      return {
        success: true,
        licitacao: atualizacaoResponse,
        mensagem: `Status da licitação atualizado para ${novoStatus}`
      };
    } catch (error) {
      console.error('Erro ao atualizar licitação e recalcular:', error);
      throw error;
    }
  },

  /**
   * Sincroniza dados entre o frontend e o backend
   * 
   * @returns {Promise} - Promise com o status da sincronização
   */
  sincronizarDados: async () => {
    try {
      // Obtém dados do Kanban
      const dadosKanban = await kanbanService.obterDadosKanban();
      
      // Obtém lista de fornecedores
      const fornecedoresResponse = await api.get('/api/v1/fornecedores');
      const fornecedores = fornecedoresResponse.data;
      
      // Obtém lista de usuários (apenas para administradores)
      let usuarios = [];
      try {
        const usuariosResponse = await api.get('/api/v1/users');
        usuarios = usuariosResponse.data;
      } catch (error) {
        console.warn('Não foi possível obter lista de usuários:', error);
      }
      
      return {
        success: true,
        dadosKanban,
        fornecedores,
        usuarios,
        sincronizadoEm: new Date().toISOString()
      };
    } catch (error) {
      console.error('Erro ao sincronizar dados:', error);
      throw error;
    }
  }
};

export default integracaoService;
