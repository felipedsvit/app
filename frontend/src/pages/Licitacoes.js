// Página de Licitações para o Sistema de Gestão de Licitações Governamentais
// Este componente implementa a listagem e filtros de licitações

import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow,
  TablePagination,
  Button,
  Chip,
  TextField,
  MenuItem,
  Grid,
  IconButton,
  Tooltip,
  CircularProgress,
  Alert
} from '@mui/material';
import { 
  Add as AddIcon,
  Search as SearchIcon,
  Visibility as VisibilityIcon,
  Edit as EditIcon
} from '@mui/icons-material';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';

// Componente principal de Licitações
const Licitacoes = () => {
  const { user, hasPermission } = useAuth();
  const navigate = useNavigate();
  
  // Estados
  const [licitacoes, setLicitacoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  
  // Filtros
  const [filtros, setFiltros] = useState({
    numero: '',
    titulo: '',
    status: '',
    orgao: ''
  });

  // Opções de status para filtro
  const statusOptions = [
    { value: '', label: 'Todos' },
    { value: 'rascunho', label: 'Rascunho' },
    { value: 'publicada', label: 'Publicada' },
    { value: 'em_analise', label: 'Em Análise' },
    { value: 'adjudicada', label: 'Adjudicada' },
    { value: 'homologada', label: 'Homologada' },
    { value: 'concluida', label: 'Concluída' },
    { value: 'cancelada', label: 'Cancelada' },
    { value: 'suspensa', label: 'Suspensa' }
  ];

  // Busca licitações da API
  useEffect(() => {
    const fetchLicitacoes = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Em um sistema real, esta seria uma chamada à API com filtros
        // const response = await api.get('/api/v1/licitacoes', { params: filtros });
        
        // Simulação de resposta da API
        const response = {
          data: [
            { 
              id: '1', 
              numero: '2025/001', 
              titulo: 'Aquisição de Equipamentos de TI', 
              status: 'publicada',
              data_abertura: '2025-05-15T10:00:00',
              orgao_responsavel: 'Ministério da Educação',
              valor_estimado: 1500000.0
            },
            { 
              id: '2', 
              numero: '2025/002', 
              titulo: 'Contratação de Serviços de Limpeza', 
              status: 'em_analise',
              data_abertura: '2025-05-20T14:00:00',
              orgao_responsavel: 'Ministério da Saúde',
              valor_estimado: 800000.0
            },
            { 
              id: '3', 
              numero: '2025/003', 
              titulo: 'Fornecimento de Material de Escritório', 
              status: 'rascunho',
              data_abertura: '2025-06-01T09:00:00',
              orgao_responsavel: 'Ministério da Fazenda',
              valor_estimado: 250000.0
            },
            { 
              id: '4', 
              numero: '2025/004', 
              titulo: 'Manutenção de Ar Condicionado', 
              status: 'publicada',
              data_abertura: '2025-05-25T11:00:00',
              orgao_responsavel: 'Ministério da Educação',
              valor_estimado: 350000.0
            },
            { 
              id: '5', 
              numero: '2025/005', 
              titulo: 'Serviços de Segurança', 
              status: 'adjudicada',
              data_abertura: '2025-04-10T10:00:00',
              orgao_responsavel: 'Ministério da Justiça',
              valor_estimado: 1200000.0
            },
            { 
              id: '6', 
              numero: '2025/006', 
              titulo: 'Desenvolvimento de Software', 
              status: 'homologada',
              data_abertura: '2025-03-15T09:00:00',
              orgao_responsavel: 'Ministério da Ciência e Tecnologia',
              valor_estimado: 2500000.0
            },
            { 
              id: '7', 
              numero: '2025/007', 
              titulo: 'Aquisição de Mobiliário', 
              status: 'concluida',
              data_abertura: '2025-02-20T14:00:00',
              orgao_responsavel: 'Ministério da Educação',
              valor_estimado: 750000.0
            },
            { 
              id: '8', 
              numero: '2025/008', 
              titulo: 'Serviços de Consultoria', 
              status: 'cancelada',
              data_abertura: '2025-01-10T10:00:00',
              orgao_responsavel: 'Ministério da Economia',
              valor_estimado: 900000.0
            },
          ]
        };
        
        // Filtra os resultados simulados
        let filteredData = response.data;
        
        if (filtros.numero) {
          filteredData = filteredData.filter(item => 
            item.numero.toLowerCase().includes(filtros.numero.toLowerCase())
          );
        }
        
        if (filtros.titulo) {
          filteredData = filteredData.filter(item => 
            item.titulo.toLowerCase().includes(filtros.titulo.toLowerCase())
          );
        }
        
        if (filtros.status) {
          filteredData = filteredData.filter(item => 
            item.status === filtros.status
          );
        }
        
        if (filtros.orgao) {
          filteredData = filteredData.filter(item => 
            item.orgao_responsavel.toLowerCase().includes(filtros.orgao.toLowerCase())
          );
        }
        
        setLicitacoes(filteredData);
        
      } catch (err) {
        console.error('Erro ao buscar licitações:', err);
        setError('Não foi possível carregar as licitações. Tente novamente mais tarde.');
      } finally {
        setLoading(false);
      }
    };

    fetchLicitacoes();
  }, [filtros]);

  // Manipuladores de eventos
  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleFiltroChange = (e) => {
    const { name, value } = e.target;
    setFiltros(prev => ({ ...prev, [name]: value }));
    setPage(0);
  };

  const handleLimparFiltros = () => {
    setFiltros({
      numero: '',
      titulo: '',
      status: '',
      orgao: ''
    });
    setPage(0);
  };

  // Formata a data para exibição
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };

  // Formata o valor monetário
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  // Traduz o status da licitação
  const getStatusLabel = (status) => {
    const statusMap = {
      rascunho: 'Rascunho',
      publicada: 'Publicada',
      em_analise: 'Em Análise',
      adjudicada: 'Adjudicada',
      homologada: 'Homologada',
      concluida: 'Concluída',
      cancelada: 'Cancelada',
      suspensa: 'Suspensa'
    };
    return statusMap[status] || status;
  };

  // Obtém a cor do status
  const getStatusColor = (status) => {
    const colorMap = {
      rascunho: 'default',
      publicada: 'success',
      em_analise: 'info',
      adjudicada: 'primary',
      homologada: 'secondary',
      concluida: 'success',
      cancelada: 'error',
      suspensa: 'warning'
    };
    return colorMap[status] || 'default';
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">
          Licitações
        </Typography>
        
        {/* Botão de Nova Licitação (apenas para admin e gestor) */}
        {hasPermission(['admin', 'gestor']) && (
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => navigate('/licitacoes/nova')}
          >
            Nova Licitação
          </Button>
        )}
      </Box>
      
      {/* Filtros */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Filtros
        </Typography>
        
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6} md={3}>
            <TextField
              fullWidth
              label="Número"
              name="numero"
              value={filtros.numero}
              onChange={handleFiltroChange}
              variant="outlined"
              size="small"
            />
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <TextField
              fullWidth
              label="Título"
              name="titulo"
              value={filtros.titulo}
              onChange={handleFiltroChange}
              variant="outlined"
              size="small"
            />
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <TextField
              fullWidth
              select
              label="Status"
              name="status"
              value={filtros.status}
              onChange={handleFiltroChange}
              variant="outlined"
              size="small"
            >
              {statusOptions.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <TextField
              fullWidth
              label="Órgão Responsável"
              name="orgao"
              value={filtros.orgao}
              onChange={handleFiltroChange}
              variant="outlined"
              size="small"
            />
          </Grid>
        </Grid>
        
        <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
          <Button onClick={handleLimparFiltros}>
            Limpar Filtros
          </Button>
        </Box>
      </Paper>
      
      {/* Mensagem de erro */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}
      
      {/* Tabela de licitações */}
      <Paper>
        <TableContainer>
          {loading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
              <CircularProgress />
            </Box>
          ) : licitacoes.length === 0 ? (
            <Box sx={{ p: 3, textAlign: 'center' }}>
              <Typography variant="body1">
                Nenhuma licitação encontrada.
              </Typography>
            </Box>
          ) : (
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Número</TableCell>
                  <TableCell>Título</TableCell>
                  <TableCell>Órgão</TableCell>
                  <TableCell>Data de Abertura</TableCell>
                  <TableCell>Valor Estimado</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell align="center">Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {licitacoes
                  .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                  .map((licitacao) => (
                    <TableRow key={licitacao.id}>
                      <TableCell>{licitacao.numero}</TableCell>
                      <TableCell>{licitacao.titulo}</TableCell>
                      <TableCell>{licitacao.orgao_responsavel}</TableCell>
                      <TableCell>{formatDate(licitacao.data_abertura)}</TableCell>
                      <TableCell>{formatCurrency(licitacao.valor_estimado)}</TableCell>
                      <TableCell>
                        <Chip 
                          label={getStatusLabel(licitacao.status)} 
                          color={getStatusColor(licitacao.status)}
                          size="small"
                        />
                      </TableCell>
                      <TableCell align="center">
                        <Tooltip title="Visualizar">
                          <IconButton 
                            component={Link} 
                            to={`/licitacoes/${licitacao.id}`}
                            size="small"
                          >
                            <VisibilityIcon fontSize="small" />
                          </IconButton>
                        </Tooltip>
                        
                        {hasPermission(['admin', 'gestor']) && (
                          <Tooltip title="Editar">
                            <IconButton 
                              component={Link} 
                              to={`/licitacoes/${licitacao.id}/editar`}
                              size="small"
                            >
                              <EditIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
              </TableBody>
            </Table>
          )}
        </TableContainer>
        
        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={licitacoes.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
          labelRowsPerPage="Linhas por página:"
          labelDisplayedRows={({ from, to, count }) => `${from}-${to} de ${count}`}
        />
      </Paper>
    </Box>
  );
};

export default Licitacoes;
