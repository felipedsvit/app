import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  TextField,
  Button,
  Paper,
  Alert,
  CircularProgress,
  InputAdornment,
  IconButton,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import { Visibility, VisibilityOff } from '@mui/icons-material';

const StyledPaper = styled(Paper)(({ theme }) => ({
  marginTop: theme.spacing(8),
  padding: theme.spacing(4),
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  maxWidth: 400,
  width: '100%',
}));

const StyledForm = styled('form')(({ theme }) => ({
  width: '100%',
  marginTop: theme.spacing(1),
}));

const StyledButton = styled(Button)(({ theme }) => ({
  margin: theme.spacing(3, 0, 2),
}));

const SignUp = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    password: '',
    dateOfBirth: '',
    username: '',
    profilePicture: null,
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'image/jpeg') {
      setFormData(prev => ({
        ...prev,
        profilePicture: file
      }));
    } else {
      setError('Por favor, selecione apenas arquivos JPG.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      setSuccess(true);
      setTimeout(() => {
        navigate('/login');
      }, 3000);
    } catch (err) {
      setError('Erro ao criar conta. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          minHeight: '100vh',
        }}
      >
        <StyledPaper elevation={3}>
          <Typography component="h1" variant="h5" sx={{ mb: 3 }}>
            Criar Conta
          </Typography>
          
          {error && (
            <Alert severity="error" sx={{ width: '100%', mb: 2 }}>
              {error}
            </Alert>
          )}

          {success && (
            <Alert severity="success" sx={{ width: '100%', mb: 2 }}>
              Email de confirmação enviado com sucesso!
            </Alert>
          )}

          <StyledForm onSubmit={handleSubmit}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="fullName"
              label="Nome Completo"
              name="fullName"
              autoComplete="name"
              autoFocus
              value={formData.fullName}
              onChange={handleChange}
              disabled={loading || success}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email"
              name="email"
              autoComplete="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              disabled={loading || success}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Senha"
              type={showPassword ? 'text' : 'password'}
              id="password"
              autoComplete="new-password"
              value={formData.password}
              onChange={handleChange}
              disabled={loading || success}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      aria-label="toggle password visibility"
                      onClick={() => setShowPassword(!showPassword)}
                      edge="end"
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              id="dateOfBirth"
              label="Data de Nascimento"
              name="dateOfBirth"
              type="date"
              value={formData.dateOfBirth}
              onChange={handleChange}
              disabled={loading || success}
              InputLabelProps={{
                shrink: true,
              }}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="Usuário"
              name="username"
              autoComplete="username"
              value={formData.username}
              onChange={handleChange}
              disabled={loading || success}
            />
            <Button
              variant="outlined"
              component="label"
              fullWidth
              sx={{ mt: 2 }}
              disabled={loading || success}
            >
              Upload Foto de Perfil (JPG)
              <input
                type="file"
                hidden
                accept=".jpg,.jpeg"
                onChange={handleFileChange}
              />
            </Button>
            {formData.profilePicture && (
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                Arquivo selecionado: {formData.profilePicture.name}
              </Typography>
            )}
            
            <StyledButton
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              disabled={loading || success}
            >
              {loading ? <CircularProgress size={24} /> : 'Criar Conta'}
            </StyledButton>

            <Button
              fullWidth
              color="primary"
              onClick={() => navigate('/login')}
              disabled={loading}
            >
              Voltar para o Login
            </Button>
          </StyledForm>
        </StyledPaper>
      </Box>
    </Container>
  );
};

export default SignUp; 