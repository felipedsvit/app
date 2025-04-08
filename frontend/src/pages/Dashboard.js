// Página de Dashboard para o Sistema de Gestão de Licitações Governamentais
// Este componente implementa a visão geral do sistema com estatísticas e gráficos

import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Grid, 
  Paper, 
  Typography, 
  Card, 
  CardContent, 
  CardHeader,
  Divider,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
  Alert
} from '@mui/material';
import { 
  Description as DescriptionIcon,
  Business as BusinessIcon,
  Assignment as AssignmentIcon,
  CheckCircle as CheckCircleIcon
} from '@mui/icons-material';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';

// Componente de card de estatística
const StatCard = ({ title, value, icon, color }) => (
  <Card sx={{ height: '100%' }}>
    <CardContent>
      <Grid container spacing={2} alignItems="center">
        <Grid item>
          <Box
            sx={{
              backgroundColor: `${color}.light`,
              borderRadius: '50%',
              p: 1,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            {icon}
          </Box>
        </Grid>
        <Grid item xs>
          <Typography variant="h6" component="div">
            {value}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {title}
          </Typography>
        </Grid>
      </Grid>
    </CardContent>
  </Card>
);

// Componente principal do Dashboard
const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    totalLicitacoes: 0,
    licitacoesAbertas: 0,
    totalFornecedores: 0,
    totalPropostas: 0
  });
  const [recentLicitacoes, setRecentLicitacoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Busca dados do dashboard
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Em um sistema real, estas seriam chamadas separadas à API
        // Aqui estamos simulando para simplificar
        
        // Simulação de resposta da API
        const statsResponse = {
          data: {
            totalLicitacoes: 24,
            licitacoesAbertas: 8,
            totalFornecedores: 45,
            totalPropostas: 67
          }
        };
        
        const licitacoesResponse = {
          data: [
            { 
              id: '1', 
              numero: '2025/001', 
              titulo: 'Aquisição de Equipamentos de TI', 
              status: 'publicada',
              data_abertura: '2025-05-15T10:00:00'
            },
            { 
              id: '2', 
              numero: '2025/002', 
              titulo: 'Contratação de Serviços de Limpeza', 
              status: 'em_analise',
              data_abertura: '2025-05-20T14:00:00'
            },
            { 
              id: '3', 
              numero: '2025/003', 
              titulo: 'Fornecimento de Material de Escritório', 
              status: 'rascunho',
              data_abertura: '2025-06-01T09:00:00'
            },
            { 
              id: '4', 
              numero: '2025/004', 
              titulo: 'Manutenção de Ar Condicionado', 
              status: 'publicada',
              data_abertura: '2025-05-25T11:00:00'
            },
          ]
        };
        
        // Em um sistema real, estas seriam as chamadas à API:
        // const statsResponse = await api.get('/api/v1/dashboard/stats');
        // const licitacoesResponse = await api.get('/api/v1/dashboard/recent-licitacoes');
        
        setStats(statsResponse.data);
        setRecentLicitacoes(licitacoesResponse.data);
        
      } catch (err) {
        console.error('Erro ao buscar dados do dashboard:', err);
        setError('Não foi possível carregar os dados do dashboard. Tente novamente mais tarde.');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

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
      rascunho: 'text.secondary',
      publicada: 'success.main',
      em_analise: 'info.main',
      adjudicada: 'primary.main',
      homologada: 'secondary.main',
      concluida: 'success.dark',
      cancelada: 'error.main',
      suspensa: 'warning.main'
    };
    return colorMap[status] || 'text.primary';
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      
      <Typography variant="body1" paragraph>
        Bem-vindo(a), {user?.nome}! Aqui está uma visão geral do sistema.
      </Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}
      
      {/* Cards de estatísticas */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard 
            title="Total de Licitações" 
            value={stats.totalLicitacoes} 
            icon={<DescriptionIcon sx={{ color: 'primary.main' }} />}
            color="primary"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard 
            title="Licitações Abertas" 
            value={stats.licitacoesAbertas} 
            icon={<DescriptionIcon sx={{ color: 'success.main' }} />}
            color="success"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard 
            title="Fornecedores" 
            value={stats.totalFornecedores} 
            icon={<BusinessIcon sx={{ color: 'info.main' }} />}
            color="info"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard 
            title="Propostas Recebidas" 
            value={stats.totalPropostas} 
            icon={<AssignmentIcon sx={{ color: 'warning.main' }} />}
            color="warning"
          />
        </Grid>
      </Grid>
      
      {/* Licitações recentes */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Licitações Recentes
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            {recentLicitacoes.length === 0 ? (
              <Typography variant="body2" color="text.secondary">
                Nenhuma licitação encontrada.
              </Typography>
            ) : (
              <List>
                {recentLicitacoes.map((licitacao) => (
                  <React.Fragment key={licitacao.id}>
                    <ListItem alignItems="flex-start">
                      <ListItemText
                        primary={
                          <Typography variant="subtitle1">
                            {licitacao.titulo}
                          </Typography>
                        }
                        secondary={
                          <React.Fragment>
                            <Typography variant="body2" component="span" display="block">
                              Número: {licitacao.numero}
                            </Typography>
                            <Typography variant="body2" component="span" display="block">
                              Data de Abertura: {formatDate(licitacao.data_abertura)}
                            </Typography>
                            <Typography 
                              variant="body2" 
                              component="span" 
                              sx={{ color: getStatusColor(licitacao.status) }}
                            >
                              Status: {getStatusLabel(licitacao.status)}
                            </Typography>
                          </React.Fragment>
                        }
                      />
                    </ListItem>
                    <Divider variant="inset" component="li" />
                  </React.Fragment>
                ))}
              </List>
            )}
          </Paper>
        </Grid>
        
        {/* Atividades recentes */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Atividades Recentes
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            <List>
              <ListItem alignItems="flex-start">
                <ListItemText
                  primary="Nova proposta recebida"
                  secondary={
                    <React.Fragment>
                      <Typography variant="body2" component="span" display="block">
                        Fornecedor: Empresa ABC Ltda.
                      </Typography>
                      <Typography variant="body2" component="span" display="block">
                        Licitação: Aquisição de Equipamentos de TI
                      </Typography>
                      <Typography variant="body2" component="span" display="block">
                        Data: {formatDate(new Date().toISOString())}
                      </Typography>
                    </React.Fragment>
                  }
                />
              </ListItem>
              <Divider variant="inset" component="li" />
              
              <ListItem alignItems="flex-start">
                <ListItemText
                  primary="Licitação publicada"
                  secondary={
                    <React.Fragment>
                      <Typography variant="body2" component="span" display="block">
                        Número: 2025/004
                      </Typography>
                      <Typography variant="body2" component="span" display="block">
                        Título: Manutenção de Ar Condicionado
                      </Typography>
                      <Typography variant="body2" component="span" display="block">
                        Data: {formatDate(new Date(Date.now() - 86400000).toISOString())}
                      </Typography>
                    </React.Fragment>
                  }
                />
              </ListItem>
              <Divider variant="inset" component="li" />
              
              <ListItem alignItems="flex-start">
                <ListItemText
                  primary="Fornecedor cadastrado"
                  secondary={
                    <React.Fragment>
                      <Typography variant="body2" component="span" display="block">
                        Razão Social: XYZ Serviços Ltda.
                      </Typography>
                      <Typography variant="body2" component="span" display="block">
                        CNPJ: 12.345.678/0001-90
                      </Typography>
                      <Typography variant="body2" component="span" display="block">
                        Data: {formatDate(new Date(Date.now() - 172800000).toISOString())}
                      </Typography>
                    </React.Fragment>
                  }
                />
              </ListItem>
            </List>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
