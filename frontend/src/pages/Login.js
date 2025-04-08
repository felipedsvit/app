// Página de login para o Sistema de Gestão de Licitações Governamentais
// Este componente implementa o formulário de login e autenticação

import React, { useState } from 'react';
import { useNavigate, Navigate } from 'react-router-dom';
import { 
  Container, 
  Box, 
  Typography, 
  TextField, 
  Button, 
  Paper, 
  Alert, 
  CircularProgress 
} from '@mui/material';
import { LockOutlined } from '@mui/icons-material';
import { useAuth } from '../context/AuthContext';

const Login = () => {
  const { signIn, isAuthenticated, loading, error } = useAuth();
  const navigate = useNavigate();
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [formError, setFormError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Redireciona se já estiver autenticado
  if (isAuthenticated && !loading) {
    return <Navigate to="/" />;
  }

  // Manipulador do envio do formulário
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validação básica do formulário
    if (!email.trim()) {
      setFormError('O email é obrigatório');
      return;
    }
    
    if (!password) {
      setFormError('A senha é obrigatória');
      return;
    }
    
    setFormError('');
    setIsSubmitting(true);
    
    try {
      const result = await signIn(email, password);
      
      if (result.success) {
        navigate('/');
      } else {
        setFormError(result.error || 'Falha na autenticação');
      }
    } catch (err) {
      setFormError('Ocorreu um erro durante o login. Tente novamente.');
      console.error('Erro de login:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Paper 
          elevation={3} 
          sx={{ 
            p: 4, 
            display: 'flex', 
            flexDirection: 'column', 
            alignItems: 'center',
            width: '100%'
          }}
        >
          <Box
            sx={{
              backgroundColor: 'primary.main',
              color: 'white',
              borderRadius: '50%',
              p: 1,
              mb: 2
            }}
          >
            <LockOutlined />
          </Box>
          
          <Typography component="h1" variant="h5" gutterBottom>
            Sistema de Gestão de Licitações
          </Typography>
          
          <Typography variant="body2" color="text.secondary" align="center" sx={{ mb: 3 }}>
            Acesse sua conta para gerenciar licitações, fornecedores e propostas
          </Typography>
          
          {(error || formError) && (
            <Alert severity="error" sx={{ width: '100%', mb: 2 }}>
              {formError || error}
            </Alert>
          )}
          
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1, width: '100%' }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email"
              name="email"
              autoComplete="email"
              autoFocus
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={isSubmitting}
            />
            
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Senha"
              type="password"
              id="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={isSubmitting}
            />
            
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              disabled={isSubmitting}
            >
              {isSubmitting ? <CircularProgress size={24} /> : 'Entrar'}
            </Button>
          </Box>
        </Paper>
      </Box>
      
      <Box sx={{ mt: 8, textAlign: 'center' }}>
        <Typography variant="body2" color="text.secondary">
          © {new Date().getFullYear()} Sistema de Gestão de Licitações Governamentais
        </Typography>
      </Box>
    </Container>
  );
};

export default Login;
