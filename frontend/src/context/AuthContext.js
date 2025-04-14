// Contexto de autenticação para o Sistema de Gestão de Licitações Governamentais
// Este arquivo implementa o contexto de autenticação usando React Context API

import React, { createContext, useState, useContext, useEffect } from 'react';
import api from '../services/api';

// Criação do contexto de autenticação
const AuthContext = createContext({});

// Provedor do contexto de autenticação
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Efeito para verificar se o usuário já está autenticado ao carregar a aplicação
  useEffect(() => {
    const loadStoredAuth = async () => {
      setLoading(true);
      const storedToken = localStorage.getItem('@LicitaGov:token');
      const storedUser = localStorage.getItem('@LicitaGov:user');
      
      if (storedToken && storedUser) {
        api.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`;
        setUser(JSON.parse(storedUser));
        setIsAuthenticated(true);
      }
      
      setLoading(false);
    };

    loadStoredAuth();
  }, []);

  // Função para realizar login
  const signIn = async (email, password) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await api.post('/api/v1/auth/login', {
        username: email,
        password,
      });

      const { access_token } = response.data;
      
      // Busca informações do usuário
      api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      const userResponse = await api.get('/api/v1/users/me');
      
      // Armazena dados no localStorage
      localStorage.setItem('@LicitaGov:token', access_token);
      localStorage.setItem('@LicitaGov:user', JSON.stringify(userResponse.data));
      
      setUser(userResponse.data);
      setIsAuthenticated(true);
      setLoading(false);
      
      return { success: true };
    } catch (err) {
      setLoading(false);
      setError(
        err.response?.data?.detail || 
        'Ocorreu um erro durante o login. Verifique suas credenciais.'
      );
      return { success: false, error: err.response?.data?.detail || 'Erro de autenticação' };
    }
  };

  // Função para realizar logout
  const signOut = () => {
    localStorage.removeItem('@LicitaGov:token');
    localStorage.removeItem('@LicitaGov:user');
    setUser(null);
    setIsAuthenticated(false);
    api.defaults.headers.common['Authorization'] = '';
  };

  // Função para atualizar dados do usuário
  const updateUser = (userData) => {
    setUser(userData);
    localStorage.setItem('@LicitaGov:user', JSON.stringify(userData));
  };

  // Verifica se o usuário tem uma determinada permissão
  const hasPermission = (requiredRoles) => {
    if (!user) return false;
    return requiredRoles.includes(user.role);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        error,
        isAuthenticated,
        signIn,
        signOut,
        updateUser,
        hasPermission,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// Hook personalizado para usar o contexto de autenticação
export const useAuth = () => {
  const context = useContext(AuthContext);
  
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }
  
  return context;
};
