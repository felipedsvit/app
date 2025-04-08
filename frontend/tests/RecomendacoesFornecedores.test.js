import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from '../src/context/AuthContext';
import RecomendacoesFornecedores from '../src/pages/RecomendacoesFornecedores';

// Mock do serviço de API e recomendacoesService
jest.mock('../src/services/api', () => ({
  get: jest.fn(),
  post: jest.fn(),
  defaults: {
    headers: {
      common: {}
    }
  }
}));

jest.mock('../src/services/recomendacoesService', () => ({
  obterRecomendacoes: jest.fn(),
  treinarModelo: jest.fn(),
  calcularPontuacoes: jest.fn(),
  convidarFornecedor: jest.fn()
}));

// Mock do useParams e useNavigate
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useParams: () => ({ licitacaoId: '123' }),
  useNavigate: () => mockNavigate
}));

// Mock do contexto de autenticação
jest.mock('../src/context/AuthContext', () => ({
  ...jest.requireActual('../src/context/AuthContext'),
  useAuth: () => ({
    hasPermission: (roles) => roles.includes('admin') || roles.includes('gestor')
  })
}));

// Dados de exemplo para os testes
const mockLicitacao = {
  id: '123',
  numero: '2025/001',
  titulo: 'Aquisição de Equipamentos de TI',
  descricao: 'Aquisição de computadores, servidores e equipamentos de rede para modernização do parque tecnológico.',
  objeto: 'Computadores desktop, notebooks, servidores e switches de rede',
  status: 'publicada',
  data_abertura: '2025-05-15T10:00:00',
  orgao_responsavel: 'Ministério da Educação',
  valor_estimado: 1500000.0,
  palavras_chave: 'computadores, servidores, TI, tecnologia, informática'
};

const mockRecomendacoes = {
  licitacao_id: '123',
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
    }
  ]
};

// Componente de teste com providers necessários
const TestComponent = () => (
  <BrowserRouter>
    <AuthProvider>
      <RecomendacoesFornecedores />
    </AuthProvider>
  </BrowserRouter>
);

describe('Testes do componente RecomendacoesFornecedores', () => {
  beforeEach(() => {
    // Limpa os mocks antes de cada teste
    jest.clearAllMocks();
    
    // Configura os mocks para retornar dados de exemplo
    require('../src/services/api').get.mockImplementation((url) => {
      if (url.includes('/api/v1/licitacoes/123')) {
        return Promise.resolve({ data: mockLicitacao });
      }
      return Promise.reject(new Error('URL não suportada nos testes'));
    });
    
    require('../src/services/recomendacoesService').obterRecomendacoes.mockResolvedValue(mockRecomendacoes);
  });

  test('Renderiza a página de recomendações corretamente', async () => {
    render(<TestComponent />);
    
    // Verifica se o título da página está presente
    expect(screen.getByText(/Recomendações de Fornecedores/i)).toBeInTheDocument();
    
    // Aguarda o carregamento dos dados da licitação
    await waitFor(() => {
      expect(screen.getByText(/Aquisição de Equipamentos de TI/i)).toBeInTheDocument();
    });
    
    // Verifica se os detalhes da licitação são exibidos
    expect(screen.getByText(/Ministério da Educação/i)).toBeInTheDocument();
    expect(screen.getByText(/Computadores desktop, notebooks, servidores e switches de rede/i)).toBeInTheDocument();
    
    // Verifica se as recomendações são exibidas
    expect(screen.getByText(/TechSolutions Informática Ltda/i)).toBeInTheDocument();
    expect(screen.getByText(/DevPro Desenvolvimento de Software/i)).toBeInTheDocument();
    
    // Verifica se os botões de ação estão presentes
    expect(screen.getByRole('button', { name: /Treinar Modelo/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Calcular Pontuações/i })).toBeInTheDocument();
  });

  test('Exibe mensagem de carregamento enquanto busca dados', async () => {
    // Configura o mock para atrasar a resposta
    require('../src/services/api').get.mockImplementation(
      () => new Promise(resolve => setTimeout(() => resolve({ data: mockLicitacao }), 100))
    );
    
    render(<TestComponent />);
    
    // Verifica se a mensagem de carregamento é exibida
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
    
    // Aguarda o carregamento dos dados
    await waitFor(() => {
      expect(screen.getByText(/Aquisição de Equipamentos de TI/i)).toBeInTheDocument();
    });
  });

  test('Treina o modelo ao clicar no botão correspondente', async () => {
    // Configura o mock para simular um treinamento bem-sucedido
    require('../src/services/recomendacoesService').treinarModelo.mockResolvedValue({
      message: 'Treinamento do modelo de recomendação iniciado em background',
      status: 'processando'
    });
    
    render(<TestComponent />);
    
    // Aguarda o carregamento dos dados
    await waitFor(() => {
      expect(screen.getByText(/Aquisição de Equipamentos de TI/i)).toBeInTheDocument();
    });
    
    // Clica no botão de treinar modelo
    fireEvent.click(screen.getByRole('button', { name: /Treinar Modelo/i }));
    
    // Verifica se o serviço foi chamado
    await waitFor(() => {
      expect(require('../src/services/recomendacoesService').treinarModelo).toHaveBeenCalled();
    });
    
    // Verifica se a mensagem de sucesso é exibida
    await waitFor(() => {
      expect(screen.getByText(/Treinamento do modelo iniciado com sucesso/i)).toBeInTheDocument();
    });
  });

  test('Calcula pontuações ao clicar no botão correspondente', async () => {
    // Configura o mock para simular um cálculo bem-sucedido
    require('../src/services/recomendacoesService').calcularPontuacoes.mockResolvedValue({
      message: 'Cálculo de pontuações iniciado para a licitação 123',
      status: 'processando'
    });
    
    render(<TestComponent />);
    
    // Aguarda o carregamento dos dados
    await waitFor(() => {
      expect(screen.getByText(/Aquisição de Equipamentos de TI/i)).toBeInTheDocument();
    });
    
    // Clica no botão de calcular pontuações
    fireEvent.click(screen.getByRole('button', { name: /Calcular Pontuações/i }));
    
    // Verifica se o serviço foi chamado
    await waitFor(() => {
      expect(require('../src/services/recomendacoesService').calcularPontuacoes).toHaveBeenCalledWith('123');
    });
    
    // Verifica se a mensagem de sucesso é exibida
    await waitFor(() => {
      expect(screen.getByText(/Cálculo de pontuações iniciado com sucesso/i)).toBeInTheDocument();
    });
  });

  test('Convida fornecedor ao clicar no botão correspondente', async () => {
    // Configura o mock para simular um convite bem-sucedido
    require('../src/services/recomendacoesService').convidarFornecedor.mockResolvedValue({
      message: 'Convite enviado com sucesso',
      status: 'success'
    });
    
    render(<TestComponent />);
    
    // Aguarda o carregamento dos dados
    await waitFor(() => {
      expect(screen.getByText(/TechSolutions Informática Ltda/i)).toBeInTheDocument();
    });
    
    // Clica no botão de convidar fornecedor
    const botaoConvidar = screen.getAllByRole('button', { name: /Convidar/i })[0];
    fireEvent.click(botaoConvidar);
    
    // Verifica se o serviço foi chamado
    await waitFor(() => {
      expect(require('../src/services/recomendacoesService').convidarFornecedor).toHaveBeenCalledWith('123', '1');
    });
    
    // Verifica se a mensagem de sucesso é exibida
    await waitFor(() => {
      expect(screen.getByText(/Convite enviado com sucesso/i)).toBeInTheDocument();
    });
  });

  test('Navega de volta para a licitação ao clicar no botão voltar', async () => {
    render(<TestComponent />);
    
    // Aguarda o carregamento dos dados
    await waitFor(() => {
      expect(screen.getByText(/Aquisição de Equipamentos de TI/i)).toBeInTheDocument();
    });
    
    // Clica no botão de voltar
    fireEvent.click(screen.getByRole('button', { name: /Voltar para Licitação/i }));
    
    // Verifica se o usuário é redirecionado para a página da licitação
    expect(mockNavigate).toHaveBeenCalledWith('/licitacoes/123');
  });
});
