// Arquivo de configuração inicial do React para o Sistema de Gestão de Licitações Governamentais
// Este arquivo configura as rotas e o contexto de autenticação para a aplicação

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';

// Contextos
import { AuthProvider, useAuth } from './context/AuthContext';

// Layouts
import DashboardLayout from './components/layouts/DashboardLayout';

// Páginas
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Licitacoes from './pages/Licitacoes';
import DetalhesLicitacao from './pages/DetalhesLicitacao';
import Fornecedores from './pages/Fornecedores';
import DetalhesFornecedor from './pages/DetalhesFornecedor';
import Propostas from './pages/Propostas';
import Usuarios from './pages/Usuarios';
import Perfil from './pages/Perfil';
import KanbanBoard from './pages/KanbanBoard';
import NotFound from './pages/NotFound';

// Cliente para React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutos
    },
  },
});

// Componente para rotas protegidas
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  // Mostra um indicador de carregamento enquanto verifica a autenticação
  if (loading) {
    return <div>Carregando...</div>;
  }

  // Redireciona para o login se não estiver autenticado
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  // Renderiza o conteúdo protegido
  return children;
};

// Componente principal da aplicação
function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Router>
          <Routes>
            {/* Rota pública */}
            <Route path="/login" element={<Login />} />
            
            {/* Rotas protegidas */}
            <Route 
              path="/" 
              element={
                <ProtectedRoute>
                  <DashboardLayout />
                </ProtectedRoute>
              }
            >
              <Route index element={<Dashboard />} />
              <Route path="licitacoes" element={<Licitacoes />} />
              <Route path="licitacoes/:id" element={<DetalhesLicitacao />} />
              <Route path="fornecedores" element={<Fornecedores />} />
              <Route path="fornecedores/:id" element={<DetalhesFornecedor />} />
              <Route path="propostas" element={<Propostas />} />
              <Route path="usuarios" element={<Usuarios />} />
              <Route path="perfil" element={<Perfil />} />
              <Route path="kanban" element={<KanbanBoard />} />
            </Route>
            
            {/* Rota para página não encontrada */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Router>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;
