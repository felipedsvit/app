// Componente de Painel Kanban para o Sistema de Gestão de Licitações Governamentais
// Este componente implementa o painel Kanban para visualização e gerenciamento do fluxo de licitações

import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Grid, 
  Card, 
  CardContent, 
  CardHeader, 
  Chip, 
  IconButton, 
  Tooltip, 
  CircularProgress, 
  Alert,
  Divider
} from '@mui/material';
import { 
  Visibility as VisibilityIcon,
  Edit as EditIcon,
  ArrowForward as ArrowForwardIcon,
  ArrowBack as ArrowBackIcon
} from '@mui/icons-material';
import { Link } from 'react-router-dom';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';

// Componente principal do Kanban
const KanbanBoard = () => {
  const { hasPermission } = useAuth();
  
  // Estados
  const [columns, setColumns] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [movingItem, setMovingItem] = useState(null);

  // Definição das colunas do Kanban
  const columnDefinitions = [
    { id: 'rascunho', title: 'Rascunho', color: '#e0e0e0' },
    { id: 'publicada', title: 'Publicada', color: '#a5d6a7' },
    { id: 'em_analise', title: 'Em Análise', color: '#90caf9' },
    { id: 'adjudicada', title: 'Adjudicada', color: '#9fa8da' },
    { id: 'homologada', title: 'Homologada', color: '#ce93d8' },
    { id: 'concluida', title: 'Concluída', color: '#81c784' },
    { id: 'cancelada', title: 'Cancelada', color: '#ef9a9a' }
  ];

  // Busca licitações da API
  useEffect(() => {
    const fetchLicitacoes = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Em um sistema real, esta seria uma chamada à API
        // const response = await api.get('/api/v1/licitacoes');
        
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
        
        // Organiza as licitações por status (coluna)
        const columnsData = {};
        
        columnDefinitions.forEach(column => {
          columnsData[column.id] = {
            id: column.id,
            title: column.title,
            color: column.color,
            items: response.data.filter(item => item.status === column.id)
          };
        });
        
        setColumns(columnsData);
        
      } catch (err) {
        console.error('Erro ao buscar licitações:', err);
        setError('Não foi possível carregar as licitações. Tente novamente mais tarde.');
      } finally {
        setLoading(false);
      }
    };

    fetchLicitacoes();
  }, []);

  // Formata a data para exibição
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    }).format(date);
  };

  // Formata o valor monetário
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      maximumFractionDigits: 0
    }).format(value);
  };

  // Manipulador de arrastar e soltar
  const onDragEnd = async (result) => {
    const { source, destination, draggableId } = result;
    
    // Retorna se não houver destino válido
    if (!destination) return;
    
    // Retorna se a origem e o destino forem iguais
    if (
      source.droppableId === destination.droppableId &&
      source.index === destination.index
    ) return;
    
    // Obtém as colunas de origem e destino
    const sourceColumn = columns[source.droppableId];
    const destColumn = columns[destination.droppableId];
    
    // Obtém o item arrastado
    const item = sourceColumn.items.find(i => i.id === draggableId);
    
    // Verifica permissão para mover o item
    if (!hasPermission(['admin', 'gestor'])) {
      setError('Você não tem permissão para mover licitações.');
      return;
    }
    
    // Verifica se a transição de status é válida
    const validTransitions = {
      'rascunho': ['publicada', 'cancelada'],
      'publicada': ['em_analise', 'cancelada', 'suspensa'],
      'em_analise': ['adjudicada', 'cancelada', 'suspensa'],
      'adjudicada': ['homologada', 'cancelada', 'suspensa'],
      'homologada': ['concluida', 'cancelada', 'suspensa'],
      'suspensa': ['publicada', 'em_analise', 'adjudicada', 'homologada', 'cancelada'],
      'concluida': [],
      'cancelada': []
    };
    
    if (!validTransitions[source.droppableId].includes(destination.droppableId)) {
      setError(`Não é possível mover uma licitação de "${sourceColumn.title}" para "${destColumn.title}".`);
      return;
    }
    
    // Atualiza o estado localmente
    setMovingItem(item.id);
    
    // Cria cópias das listas de itens
    const sourceItems = [...sourceColumn.items];
    const destItems = [...destColumn.items];
    
    // Remove o item da coluna de origem
    sourceItems.splice(source.index, 1);
    
    // Adiciona o item à coluna de destino
    const updatedItem = { ...item, status: destination.droppableId };
    destItems.splice(destination.index, 0, updatedItem);
    
    // Atualiza o estado das colunas
    setColumns({
      ...columns,
      [source.droppableId]: {
        ...sourceColumn,
        items: sourceItems
      },
      [destination.droppableId]: {
        ...destColumn,
        items: destItems
      }
    });
    
    try {
      // Em um sistema real, esta seria uma chamada à API para atualizar o status
      // await api.put(`/api/v1/licitacoes/${item.id}/status`, {
      //   status: destination.droppableId
      // });
      
      // Simulação de chamada à API
      console.log(`Atualizando licitação ${item.id} para status ${destination.droppableId}`);
      
      // Aguarda um tempo para simular a chamada à API
      await new Promise(resolve => setTimeout(resolve, 500));
      
    } catch (err) {
      console.error('Erro ao atualizar status da licitação:', err);
      setError('Não foi possível atualizar o status da licitação. Tente novamente mais tarde.');
      
      // Reverte as alterações em caso de erro
      setColumns({
        ...columns,
        [source.droppableId]: {
          ...sourceColumn,
          items: [...sourceColumn.items]
        },
        [destination.droppableId]: {
          ...destColumn,
          items: [...destColumn.items]
        }
      });
    } finally {
      setMovingItem(null);
    }
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
        Painel Kanban de Licitações
      </Typography>
      
      <Typography variant="body1" paragraph>
        Arraste e solte os cartões para atualizar o status das licitações.
      </Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}
      
      {!hasPermission(['admin', 'gestor']) && (
        <Alert severity="info" sx={{ mb: 3 }}>
          Você está no modo de visualização. Apenas administradores e gestores podem mover licitações.
        </Alert>
      )}
      
      <DragDropContext onDragEnd={onDragEnd}>
        <Box sx={{ display: 'flex', overflowX: 'auto', pb: 2 }}>
          {columnDefinitions.map(columnDef => {
            const column = columns[columnDef.id];
            return (
              <Box 
                key={columnDef.id} 
                sx={{ 
                  minWidth: 280, 
                  mx: 1, 
                  flexShrink: 0 
                }}
              >
                <Paper 
                  sx={{ 
                    height: '100%',
                    backgroundColor: `${columnDef.color}20`, // Cor com transparência
                    borderTop: `4px solid ${columnDef.color}`
                  }}
                >
                  <Box sx={{ p: 2, borderBottom: '1px solid rgba(0, 0, 0, 0.12)' }}>
                    <Typography variant="h6">
                      {columnDef.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {column?.items.length || 0} licitações
                    </Typography>
                  </Box>
                  
                  <Droppable droppableId={columnDef.id}>
                    {(provided) => (
                      <Box
                        ref={provided.innerRef}
                        {...provided.droppableProps}
                        sx={{ 
                          p: 1, 
                          minHeight: 500,
                          height: '100%'
                        }}
                      >
                        {column?.items.map((item, index) => (
                          <Draggable 
                            key={item.id} 
                            draggableId={item.id} 
                            index={index}
                            isDragDisabled={!hasPermission(['admin', 'gestor'])}
                          >
                            {(provided, snapshot) => (
                              <Card
                                ref={provided.innerRef}
                                {...provided.draggableProps}
                                {...provided.dragHandleProps}
                                sx={{ 
                                  mb: 2, 
                                  opacity: movingItem === item.id ? 0.6 : 1,
                                  backgroundColor: snapshot.isDragging ? 'rgba(255, 255, 255, 0.9)' : 'white'
                                }}
                              >
                                <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                                  <Typography variant="subtitle1" gutterBottom>
                                    {item.titulo}
                                  </Typography>
                                  
                                  <Typography variant="body2" color="text.secondary" gutterBottom>
                                    Número: {item.numero}
                                  </Typography>
                                  
                                  <Typography variant="body2" color="text.secondary" gutterBottom>
                                    Órgão: {item.orgao_responsavel}
                                  </Typography>
                                  
                                  <Typography variant="body2" color="text.secondary" gutterBottom>
                                    Abertura: {formatDate(item.data_abertura)}
                                  </Typography>
                                  
                                  <Typography variant="body2" color="text.secondary" gutterBottom>
                                    Valor: {formatCurrency(item.valor_estimado)}
                                  </Typography>
                                  
                                  <Box sx={{ mt: 1, display: 'flex', justifyContent: 'flex-end' }}>
                                    <Tooltip title="Visualizar">
                                      <IconButton 
                                        component={Link} 
                                        to={`/licitacoes/${item.id}`}
                                        size="small"
                                      >
                                        <VisibilityIcon fontSize="small" />
                                      </IconButton>
                                    </Tooltip>
                                    
                                    {hasPermission(['admin', 'gestor']) && (
                                      <Tooltip title="Editar">
                                        <IconButton 
                                          component={Link} 
                                          to={`/licitacoes/${item.id}/editar`}
                                          size="small"
                                        >
                                          <EditIcon fontSize="small" />
                                        </IconButton>
                                      </Tooltip>
                                    )}
                                  </Box>
                                </CardContent>
                              </Card>
                            )}
                          </Draggable>
                        ))}
                        {provided.placeholder}
                      </Box>
                    )}
                  </Droppable>
                </Paper>
              </Box>
            );
          })}
        </Box>
      </DragDropContext>
    </Box>
  );
};

export default KanbanBoard;
