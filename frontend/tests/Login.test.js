import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from '../src/context/AuthContext';
import Login from '../src/pages/Login';

// Mock do serviço de API
jest.mock('../src/services/api', () => ({
  post: jest.fn().mockImplementation((url, data) => {
    // Simula autenticação bem-sucedida
    if (url === '/api/v1/auth/login' && data.username === 'admin@example.com' && data.password === 'password') {
      return Promise.resolve({ 
        data: { 
          access_token: 'fake-token' 
        } 
      });
    }
    
    // Simula erro de autenticação
    return Promise.reject({ 
      response: { 
        data: { 
          detail: 'Credenciais inválidas' 
        } 
      } 
    });
  }),
  get: jest.fn().mockImplementation((url) => {
    // Simula resposta para obter dados do usuário
    if (url === '/api/v1/users/me') {
      return Promise.resolve({ 
        data: { 
          id: '1', 
          email: 'admin@example.com', 
          nome: 'Administrador', 
          role: 'admin' 
        } 
      });
    }
    return Promise.reject(new Error('URL não suportada nos testes'));
  }),
  defaults: {
    headers: {
      common: {}
    }
  }
}));

// Mock do localStorage
const localStorageMock = (function() {
  let store = {};
  return {
    getItem: jest.fn(key => store[key] || null),
    setItem: jest.fn((key, value) => {
      store[key] = value.toString();
    }),
    removeItem: jest.fn(key => {
      delete store[key];
    }),
    clear: jest.fn(() => {
      store = {};
    })
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock
});

// Mock do useNavigate
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
  Navigate: ({ to }) => {
    mockNavigate(to);
    return null;
  }
}));

// Componente de teste com providers necessários
const TestComponent = () => (
  <BrowserRouter>
    <AuthProvider>
      <Login />
    </AuthProvider>
  </BrowserRouter>
);

describe('Testes do componente Login', () => {
  beforeEach(() => {
    // Limpa os mocks antes de cada teste
    jest.clearAllMocks();
    localStorageMock.clear();
  });

  test('Renderiza o formulário de login corretamente', () => {
    render(<TestComponent />);
    
    // Verifica se os elementos do formulário estão presentes
    expect(screen.getByLabelText(/Email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Senha/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Entrar/i })).toBeInTheDocument();
    expect(screen.getByText(/Sistema de Gestão de Licitações/i)).toBeInTheDocument();
  });

  test('Exibe erro quando campos obrigatórios estão vazios', async () => {
    render(<TestComponent />);
    
    // Clica no botão de login sem preencher os campos
    fireEvent.click(screen.getByRole('button', { name: /Entrar/i }));
    
    // Verifica se a mensagem de erro é exibida
    await waitFor(() => {
      expect(screen.getByText(/O email é obrigatório/i)).toBeInTheDocument();
    });
    
    // Preenche apenas o email
    fireEvent.change(screen.getByLabelText(/Email/i), {
      target: { value: 'admin@example.com' }
    });
    
    // Clica no botão de login novamente
    fireEvent.click(screen.getByRole('button', { name: /Entrar/i }));
    
    // Verifica se a mensagem de erro sobre a senha é exibida
    await waitFor(() => {
      expect(screen.getByText(/A senha é obrigatória/i)).toBeInTheDocument();
    });
  });

  test('Realiza login com sucesso e redireciona', async () => {
    render(<TestComponent />);
    
    // Preenche os campos do formulário
    fireEvent.change(screen.getByLabelText(/Email/i), {
      target: { value: 'admin@example.com' }
    });
    
    fireEvent.change(screen.getByLabelText(/Senha/i), {
      target: { value: 'password' }
    });
    
    // Clica no botão de login
    fireEvent.click(screen.getByRole('button', { name: /Entrar/i }));
    
    // Verifica se a API foi chamada com os dados corretos
    await waitFor(() => {
      expect(require('../src/services/api').post).toHaveBeenCalledWith(
        '/api/v1/auth/login',
        {
          username: 'admin@example.com',
          password: 'password'
        }
      );
    });
    
    // Verifica se o token foi armazenado no localStorage
    await waitFor(() => {
      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        '@LicitaGov:token',
        'fake-token'
      );
    });
    
    // Verifica se o usuário foi redirecionado para a página inicial
    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/');
    });
  });

  test('Exibe erro quando as credenciais são inválidas', async () => {
    render(<TestComponent />);
    
    // Preenche os campos do formulário com credenciais inválidas
    fireEvent.change(screen.getByLabelText(/Email/i), {
      target: { value: 'usuario@example.com' }
    });
    
    fireEvent.change(screen.getByLabelText(/Senha/i), {
      target: { value: 'senha-incorreta' }
    });
    
    // Clica no botão de login
    fireEvent.click(screen.getByRole('button', { name: /Entrar/i }));
    
    // Verifica se a mensagem de erro é exibida
    await waitFor(() => {
      expect(screen.getByText(/Credenciais inválidas/i)).toBeInTheDocument();
    });
    
    // Verifica se o usuário não foi redirecionado
    expect(mockNavigate).not.toHaveBeenCalled();
  });
});
