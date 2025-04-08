// Serviço de API para o Sistema de Gestão de Licitações Governamentais
// Este arquivo configura o cliente Axios para comunicação com o backend

import axios from 'axios';

// Criação da instância do Axios com configurações base
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token de autenticação a todas as requisições
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('@LicitaGov:token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para tratamento de erros nas respostas
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Tratamento de erro de autenticação (token expirado)
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('@LicitaGov:token');
      localStorage.removeItem('@LicitaGov:user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
