import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from '../src/context/AuthContext';
import KanbanBoard from '../src/pages/KanbanBoard';

// Mock do serviço de API e kanbanService
jest.mock('../src/services/api', () => ({
  get: jest.fn(),
  put: jest.fn(),
  defaults: {
    headers: {
      common: {}
    }
  }
}));

jest.mock('../src/services/kanbanService', () => ({
  obterDadosKanban: jest.fn(),
  atualizarStatusLicitacao: jest.fn(),
  verificarTransicaoValida: jest.fn()
}));

// Mock do react-beautiful-dnd
jest.mock('react-beautiful-dnd', () => ({
  DragDropContext: ({ children }) => children,
  Droppable: ({ children }) => children({
    droppableProps: {},
    innerRef: jest.fn()
  }),
  Draggable: ({ children }) => children({
    draggableProps: {},
    dragHandleProps: {},
    innerRef: jest.fn()
  })
}));

// Dados de exemplo para os testes
const mockKanbanData = {
  columns: {
    rascunho: {
      id: 'rascunho',
      title: 'Rascunho',
      color: '#e0e0e0',
      items: [
        {
          id: '1',
          numero: '2025/001',
          titulo: 'Aquisição de Equipamentos de TI',
          status: 'rascunho',
          data_abertura: '2025-05-15T10:00:00',
          orgao_responsavel: 'Ministério da Educação',
          valor_estimado: 1500000.0
        }
      ]
    },
    publicada: {
      id: 'publicada',
      title: 'Publicada',
      color: '#a5d6a7',
      items: [
        {
          id: '2',
          numero: '2025/002',
          titulo: 'Contratação de Serviços de Limpeza',
          status: 'publicada',
          data_abertura: '2025-06-10T10:00:00',
          orgao_responsavel: 'Ministério da Saúde',
          valor_estimado: 800000.0
        }
      ]
    },
    em_analise: {
      id: 'em_analise',
      title: 'Em Análise',
      color: '#90caf9',
      items: []
    },
    adjudicada: {
      id: 'adjudicada',
      title: 'Adjudicada',
      color: '#9fa8da',
      items: []
    },
    homologada: {
      id: 'homologada',
      title: 'Homologada',
      color: '#ce93d8',
      items: []
    },
    concluida: {
      id: 'concluida',
      title: 'Concluída',
      color: '#81c784',
      items: []
    },
    cancelada: {
      id: 'cancelada',
      title: 'Cancelada',
      color: '#ef9a9a',
      items: []
    }
  },
  valid_transitions: {
    'rascunho': ['publicada', 'cancelada'],
    'publicada': ['em_analise', 'cancelada', 'suspensa']
  }
};

// Mock do useNavigate
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate
}));

// Componente de teste com providers necessários
const TestComponent = () => (
  <BrowserRouter>
    <AuthProvider>
      <KanbanBoard />
    </AuthProvider>
  </BrowserRouter>
);

describe('Testes do componente KanbanBoard', () => {
  beforeEach(() => {
    // Limpa os mocks antes de cada teste
    jest.clearAllMocks();
    
    // Configura o mock do kanbanService para retornar dados de exemplo
    require('../src/services/kanbanService').obterDadosKanban.mockResolvedValue(mockKanbanData);
    require('../src/services/kanbanService').verificarTransicaoValida.mockImplementation((atual, novo) => {
      return mockKanbanData.valid_transitions[atual]?.includes(novo) || false;
    });
  });

  test('Renderiza o painel Kanban corretamente', async () => {
    render(<TestComponent />);
    
    // Verifica se o título da página está presente
    expect(screen.getByText(/Painel Kanban de Licitações/i)).toBeInTheDocument();
    
    // Aguarda o carregamento dos dados
    await waitFor(() => {
      // Verifica se as colunas do Kanban são exibidas
      expect(screen.getByText(/Rascunho/i)).toBeInTheDocument();
      expect(screen.getByText(/Publicada/i)).toBeInTheDocument();
      expect(screen.getByText(/Em Análise/i)).toBeInTheDocument();
      
      // Verifica se os itens das colunas são exibidos
      expect(screen.getByText(/Aquisição de Equipamentos de TI/i)).toBeInTheDocument();
      expect(screen.getByText(/Contratação de Serviços de Limpeza/i)).toBeInTheDocument();
    });
    
    // Verifica se o serviço foi chamado para obter os dados
    expect(require('../src/services/kanbanService').obterDadosKanban).toHaveBeenCalled();
  });

  test('Exibe mensagem de carregamento enquanto busca dados', async () => {
    // Configura o mock para atrasar a resposta
    require('../src/services/kanbanService').obterDadosKanban.mockImplementation(
      () => new Promise(resolve => setTimeout(() => resolve(mockKanbanData), 100))
    );
    
    render(<TestComponent />);
    
    // Verifica se a mensagem de carregamento é exibida
    expect(screen.getByText(/Carregando.../i)).toBeInTheDocument();
    
    // Aguarda o carregamento dos dados
    await waitFor(() => {
      expect(screen.getByText(/Aquisição de Equipamentos de TI/i)).toBeInTheDocument();
    });
  });

  test('Exibe detalhes da licitação ao clicar em um card', async () => {
    render(<TestComponent />);
    
    // Aguarda o carregamento dos dados
    await waitFor(() => {
      expect(screen.getByText(/Aquisição de Equipamentos de TI/i)).toBeInTheDocument();
    });
    
    // Clica no card da licitação
    fireEvent.click(screen.getByText(/Aquisição de Equipamentos de TI/i));
    
    // Verifica se o usuário é redirecionado para a página de detalhes da licitação
    expect(mockNavigate).toHaveBeenCalledWith('/licitacoes/1');
  });

  test('Atualiza o status de uma licitação ao movê-la', async () => {
    // Configura o mock para simular uma atualização bem-sucedida
    require('../src/services/kanbanService').atualizarStatusLicitacao.mockResolvedValue({
      success: true,
      licitacao_id: '1',
      status_anterior: 'rascunho',
      novo_status: 'publicada',
      mensagem: 'Licitação movida com sucesso para publicada'
    });
    
    render(<TestComponent />);
    
    // Aguarda o carregamento dos dados
    await waitFor(() => {
      expect(screen.getByText(/Aquisição de Equipamentos de TI/i)).toBeInTheDocument();
    });
    
    // Simula o evento de arrastar e soltar
    // Como o react-beautiful-dnd está mockado, precisamos chamar diretamente a função que seria chamada
    // após o evento de arrastar e soltar
    const component = screen.getByTestId('kanban-board');
    const instance = component.__reactInternalInstance;
    
    // Chama a função onDragEnd diretamente (simulando o fim do arrasto)
    instance.onDragEnd({
      source: { droppableId: 'rascunho', index: 0 },
      destination: { droppableId: 'publicada', index: 0 },
      draggableId: '1'
    });
    
    // Verifica se o serviço foi chamado para atualizar o status
    await waitFor(() => {
      expect(require('../src/services/kanbanService').atualizarStatusLicitacao).toHaveBeenCalledWith('1', 'publicada');
    });
  });

  test('Exibe mensagem de erro quando a transição é inválida', async () => {
    // Configura o mock para simular uma transição inválida
    require('../src/services/kanbanService').atualizarStatusLicitacao.mockRejectedValue({
      response: {
        data: {
          detail: 'Transição inválida: rascunho -> adjudicada'
        }
      }
    });
    
    render(<TestComponent />);
    
    // Aguarda o carregamento dos dados
    await waitFor(() => {
      expect(screen.getByText(/Aquisição de Equipamentos de TI/i)).toBeInTheDocument();
    });
    
    // Simula o evento de arrastar e soltar para uma transição inválida
    const component = screen.getByTestId('kanban-board');
    const instance = component.__reactInternalInstance;
    
    instance.onDragEnd({
      source: { droppableId: 'rascunho', index: 0 },
      destination: { droppableId: 'adjudicada', index: 0 },
      draggableId: '1'
    });
    
    // Verifica se a mensagem de erro é exibida
    await waitFor(() => {
      expect(screen.getByText(/Transição inválida/i)).toBeInTheDocument();
    });
  });
});
