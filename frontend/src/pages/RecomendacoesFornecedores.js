// Componente de Recomendações de Fornecedores para o Sistema de Gestão de Licitações Governamentais
// Este componente implementa a interface para visualização e gerenciamento de recomendações de fornecedores

import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Grid, 
  Card, 
  CardContent, 
  Button, 
  Chip, 
  Rating, 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow,
  IconButton, 
  Tooltip, 
  CircularProgress, 
  Alert,
  Divider
} from '@mui/material';
import { 
  Visibility as VisibilityIcon,
  Check as CheckIcon,
  Refresh as RefreshIcon,
  Add as AddIcon
} from '@mui/icons-material';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';

// Componente principal de Recomendações
const RecomendacoesFornecedores = () => {
  const { licitacaoId } = useParams();
  const { hasPermission } = useAuth();
  const navigate = useNavigate();
  
  // Estados
  const [licitacao, setLicitacao] = useState(null);
  const [recomendacoes, setRecomendacoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadingRecomendacoes, setLoadingRecomendacoes] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  // Busca dados da licitação
  useEffect(() => {
    const fetchLicitacao = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Em um sistema real, esta seria uma chamada à API
        // const response = await api.get(`/api/v1/licitacoes/${licitacaoId}`);
        
        // Simulação de resposta da API
        const response = {
          data: {
            id: licitacaoId,
            numero: '2025/001',
            titulo: 'Aquisição de Equipamentos de TI',
            descricao: 'Aquisição de computadores, servidores e equipamentos de rede para modernização do parque tecnológico.',
            objeto: 'Computadores desktop, notebooks, servidores e switches de rede',
            status: 'publicada',
            data_abertura: '2025-05-15T10:00:00',
            orgao_responsavel: 'Ministério da Educação',
            valor_estimado: 1500000.0,
            palavras_chave: 'computadores, servidores, TI, tecnologia, informática'
          }
        };
        
        setLicitacao(response.data);
        
        // Busca recomendações
        await fetchRecomendacoes();
        
      } catch (err) {
        console.error('Erro ao buscar dados da licitação:', err);
        setError('Não foi possível carregar os dados da licitação. Tente novamente mais tarde.');
      } finally {
        setLoading(false);
      }
    };

    if (licitacaoId) {
      fetchLicitacao();
    }
  }, [licitacaoId]);

  // Busca recomendações de fornecedores
  const fetchRecomendacoes = async () => {
    try {
      setLoadingRecomendacoes(true);
      setError(null);
      
      // Em um sistema real, esta seria uma chamada à API
      // const response = await api.get(`/api/v1/recomendacoes/recomendar/${licitacaoId}?top_n=10`);
      
      // Simulação de resposta da API
      const response = {
        data: {
          licitacao_id: licitacaoId,
          licitacao_titulo: 'Aquisição de Equipamentos de TI',
          recomendacoes: [
            {
              fornecedor_id: '1',
              razao_social: 'TechSolutions Informática Ltda',
              cnpj: '12.345.678/0001-90',
              area_atuacao: 'Tecnologia da Informação',
              avaliacao_media: 4.8,
              pontuacao_ia: 92.5,
              ranking: 1
            },
            {
              fornecedor_id: '6',
              razao_social: 'DevPro Desenvolvimento de Software',
              cnpj: '98.765.432/0001-10',
              area_atuacao: 'Desenvolvimento de Software',
              avaliacao_media: 4.2,
              pontuacao_ia: 78.3,
              ranking: 2
            },
            {
              fornecedor_id: '3',
              razao_social: 'PapelTudo Materiais de Escritório',
              cnpj: '45.678.901/0001-23',
              area_atuacao: 'Material de Escritório',
              avaliacao_media: 3.9,
              pontuacao_ia: 65.7,
              ranking: 3
            },
            {
              fornecedor_id: '7',
              razao_social: 'MobiOffice Mobiliário Corporativo',
              cnpj: '56.789.012/0001-34',
              area_atuacao: 'Mobiliário',
              avaliacao_media: 4.1,
              pontuacao_ia: 52.4,
              ranking: 4
            },
            {
              fornecedor_id: '4',
              razao_social: 'FrioCool Ar Condicionado e Refrigeração',
              cnpj: '67.890.123/0001-45',
              area_atuacao: 'Refrigeração e Climatização',
              avaliacao_media: 3.7,
              pontuacao_ia: 38.9,
              ranking: 5
            }
          ]
        }
      };
      
      setRecomendacoes(response.data.recomendacoes);
      
    } catch (err) {
      console.error('Erro ao buscar recomendações:', err);
      setError('Não foi possível carregar as recomendações. Tente novamente mais tarde.');
    } finally {
      setLoadingRecomendacoes(false);
    }
  };

  // Treina o modelo de recomendação
  const handleTreinarModelo = async () => {
    try {
      setLoadingRecomendacoes(true);
      setError(null);
      setSuccess(null);
      
      // Em um sistema real, esta seria uma chamada à API
      // await api.post('/api/v1/recomendacoes/treinar');
      
      // Simulação de chamada à API
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      setSuccess('Treinamento do modelo iniciado com sucesso. Este processo pode levar alguns minutos.');
      
      // Atualiza as recomendações após um tempo
      setTimeout(() => {
        fetchRecomendacoes();
      }, 2000);
      
    } catch (err) {
      console.error('Erro ao treinar modelo:', err);
      setError('Não foi possível iniciar o treinamento do modelo. Tente novamente mais tarde.');
    } finally {
      setLoadingRecomendacoes(false);
    }
  };

  // Calcula pontuações para propostas
  const handleCalcularPontuacoes = async () => {
    try {
      setLoadingRecomendacoes(true);
      setError(null);
      setSuccess(null);
      
      // Em um sistema real, esta seria uma chamada à API
      // await api.post(`/api/v1/recomendacoes/calcular-pontuacoes/${licitacaoId}`);
      
      // Simulação de chamada à API
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setSuccess('Cálculo de pontuações iniciado com sucesso. Este processo pode levar alguns minutos.');
      
    } catch (err) {
      console.error('Erro ao calcular pontuações:', err);
      setError('Não foi possível iniciar o cálculo de pontuações. Tente novamente mais tarde.');
    } finally {
      setLoadingRecomendacoes(false);
    }
  };

  // Convida fornecedor para participar da licitação
  const handleConvidarFornecedor = async (fornecedorId) => {
    try {
      setError(null);
      setSuccess(null);
      
      // Em um sistema real, esta seria uma chamada à API
      // await api.post(`/api/v1/licitacoes/${licitacaoId}/convidar-fornecedor`, {
      //   fornecedor_id: fornecedorId
      // });
      
      // Simulação de chamada à API
      await new Promise(resolve => setTimeout(resolve, 800));
      
      setSuccess(`Convite enviado com sucesso para o fornecedor.`);
      
    } catch (err) {
      console.error('Erro ao enviar convite:', err);
      setError('Não foi possível enviar o convite. Tente novamente mais tarde.');
    }
  };

  // Formata o valor monetário
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!licitacao) {
    return (
      <Alert severity="error">
        Licitação não encontrada.
      </Alert>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">
          Recomendações de Fornecedores
        </Typography>
        
        <Box>
          <Button
            variant="outlined"
            onClick={() => navigate(`/licitacoes/${licitacaoId}`)}
            sx={{ mr: 1 }}
          >
            Voltar para Licitação
          </Button>
          
          {hasPermission(['admin', 'gestor']) && (
            <Button
              variant="contained"
              startIcon={<RefreshIcon />}
              onClick={handleTreinarModelo}
              disabled={loadingRecomendacoes}
            >
              Treinar Modelo
            </Button>
          )}
        </Box>
      </Box>
      
      {/* Informações da licitação */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h5" gutterBottom>
          {licitacao.titulo}
        </Typography>
        
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="body2" color="text.secondary">
              Número:
            </Typography>
            <Typography variant="body1">
              {licitacao.numero}
            </Typography>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="body2" color="text.secondary">
              Órgão Responsável:
            </Typography>
            <Typography variant="body1">
              {licitacao.orgao_responsavel}
            </Typography>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="body2" color="text.secondary">
              Valor Estimado:
            </Typography>
            <Typography variant="body1">
              {formatCurrency(licitacao.valor_estimado)}
            </Typography>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="body2" color="text.secondary">
              Status:
            </Typography>
            <Chip 
              label={licitacao.status.charAt(0).toUpperCase() + licitacao.status.slice(1).replace('_', ' ')} 
              color={licitacao.status === 'publicada' ? 'success' : 'primary'}
              size="small"
            />
          </Grid>
        </Grid>
        
        <Typography variant="body2" color="text.secondary">
          Descrição:
        </Typography>
        <Typography variant="body1" paragraph>
          {licitacao.descricao}
        </Typography>
        
        <Typography variant="body2" color="text.secondary">
          Objeto:
        </Typography>
        <Typography variant="body1" paragraph>
          {licitacao.objeto}
        </Typography>
        
        <Typography variant="body2" color="text.secondary">
          Palavras-chave:
        </Typography>
        <Box sx={{ mt: 1 }}>
          {licitacao.palavras_chave.split(',').map((palavra, index) => (
            <Chip 
              key={index} 
              label={palavra.trim()} 
              size="small" 
              sx={{ mr: 1, mb: 1 }} 
            />
          ))}
        </Box>
      </Paper>
      
      {/* Mensagens de erro e sucesso */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}
      
      {success && (
        <Alert severity="success" sx={{ mb: 3 }}>
          {success}
        </Alert>
      )}
      
      {/* Ações para recomendações */}
      {hasPermission(['admin', 'gestor', 'analista']) && (
        <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h5">
            Fornecedores Recomendados pela IA
          </Typography>
          
          {hasPermission(['admin', 'gestor']) && (
            <Button
              variant="outlined"
              startIcon={<RefreshIcon />}
              onClick={fetchRecomendacoes}
              disabled={loadingRecomendacoes}
            >
              Atualizar Recomendações
            </Button>
          )}
        </Box>
      )}
      
      {/* Tabela de recomendações */}
      {hasPermission(['admin', 'gestor', 'analista']) && (
        <Paper>
          <TableContainer>
            {loadingRecomendacoes ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
                <CircularProgress />
              </Box>
            ) : recomendacoes.length === 0 ? (
              <Box sx={{ p: 3, textAlign: 'center' }}>
                <Typography variant="body1">
                  Nenhuma recomendação encontrada.
                </Typography>
                <Button
                  variant="contained"
                  onClick={handleTreinarModelo}
                  sx={{ mt: 2 }}
                  disabled={loadingRecomendacoes}
                >
                  Treinar Modelo de IA
                </Button>
              </Box>
            ) : (
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Ranking</TableCell>
                    <TableCell>Fornecedor</TableCell>
                    <TableCell>CNPJ</TableCell>
                    <TableCell>Área de Atuação</TableCell>
                    <TableCell>Avaliação</TableCell>
                    <TableCell>Pontuação IA</TableCell>
                    <TableCell align="center">Ações</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {recomendacoes.map((recomendacao) => (
                    <TableRow key={recomendacao.fornecedor_id}>
                      <TableCell>
                        <Chip 
                          label={`#${recomendacao.ranking}`} 
                          color={
                            recomendacao.ranking === 1 ? 'success' :
                            recomendacao.ranking === 2 ? 'primary' :
                            recomendacao.ranking === 3 ? 'secondary' : 'default'
                          }
                          size="small"
                        />
                      </TableCell>
                      <TableCell>{recomendacao.razao_social}</TableCell>
                      <TableCell>{recomendacao.cnpj}</TableCell>
                      <TableCell>{recomendacao.area_atuacao}</TableCell>
                      <TableCell>
                        <Rating 
                          value={recomendacao.avaliacao_media} 
                          precision={0.1} 
                          readOnly 
                          size="small" 
                        />
                      </TableCell>
                      <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <Box
                            sx={{
                              width: 60,
                              mr: 1,
                              backgroundColor: '#f0f0f0',
                              borderRadius: 1,
                              position: 'relative',
                              height: 8
                            }}
                          >
                            <Box
                              sx={{
                                position: 'absolute',
                                left: 0,
                                top: 0,
                                bottom: 0,
                                backgroundColor: 
                                  recomendacao.pontuacao_ia > 80 ? 'success.main' :
                                  recomendacao.pontuacao_ia > 60 ? 'primary.main' :
                                  recomendacao.pontuacao_ia > 40 ? 'warning.main' : 'error.main
(Content truncated due to size limit. Use line ranges to read in chunks)