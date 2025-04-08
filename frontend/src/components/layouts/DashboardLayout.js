// Layout principal do dashboard para o Sistema de Gestão de Licitações Governamentais
// Este componente implementa o layout base para todas as páginas autenticadas

import React, { useState } from 'react';
import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { 
  AppBar, 
  Box, 
  CssBaseline, 
  Divider, 
  Drawer, 
  IconButton, 
  List, 
  ListItem, 
  ListItemButton, 
  ListItemIcon, 
  ListItemText, 
  Toolbar, 
  Typography, 
  Avatar, 
  Menu, 
  MenuItem, 
  Tooltip 
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  Description as DescriptionIcon,
  Business as BusinessIcon,
  Assignment as AssignmentIcon,
  People as PeopleIcon,
  ViewKanban as ViewKanbanIcon,
  Person as PersonIcon,
  Logout as LogoutIcon
} from '@mui/icons-material';

import { useAuth } from '../../context/AuthContext';

const drawerWidth = 240;

const DashboardLayout = () => {
  const { user, signOut, hasPermission } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);

  // Manipuladores de eventos
  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleProfileMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleProfileMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    signOut();
    navigate('/login');
  };

  // Itens do menu lateral
  const menuItems = [
    { 
      text: 'Dashboard', 
      icon: <DashboardIcon />, 
      path: '/',
      roles: ['admin', 'gestor', 'analista', 'fornecedor', 'usuario']
    },
    { 
      text: 'Licitações', 
      icon: <DescriptionIcon />, 
      path: '/licitacoes',
      roles: ['admin', 'gestor', 'analista', 'fornecedor', 'usuario']
    },
    { 
      text: 'Fornecedores', 
      icon: <BusinessIcon />, 
      path: '/fornecedores',
      roles: ['admin', 'gestor', 'analista', 'usuario']
    },
    { 
      text: 'Propostas', 
      icon: <AssignmentIcon />, 
      path: '/propostas',
      roles: ['admin', 'gestor', 'analista', 'fornecedor']
    },
    { 
      text: 'Kanban', 
      icon: <ViewKanbanIcon />, 
      path: '/kanban',
      roles: ['admin', 'gestor', 'analista']
    },
    { 
      text: 'Usuários', 
      icon: <PeopleIcon />, 
      path: '/usuarios',
      roles: ['admin', 'gestor']
    }
  ];

  // Conteúdo do drawer
  const drawer = (
    <div>
      <Toolbar>
        <Typography variant="h6" noWrap component="div">
          LicitaGov
        </Typography>
      </Toolbar>
      <Divider />
      <List>
        {menuItems.map((item) => (
          // Renderiza o item apenas se o usuário tiver permissão
          hasPermission(item.roles) && (
            <ListItem key={item.text} disablePadding>
              <ListItemButton 
                component={Link} 
                to={item.path}
                selected={location.pathname === item.path}
              >
                <ListItemIcon>
                  {item.icon}
                </ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItemButton>
            </ListItem>
          )
        ))}
      </List>
    </div>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      
      {/* Barra superior */}
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="abrir menu"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            Sistema de Gestão de Licitações Governamentais
          </Typography>
          
          {/* Perfil do usuário */}
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Typography variant="body2" sx={{ mr: 2 }}>
              {user?.nome}
            </Typography>
            
            <Tooltip title="Configurações de perfil">
              <IconButton onClick={handleProfileMenuOpen} sx={{ p: 0 }}>
                <Avatar alt={user?.nome} src="/static/images/avatar/1.jpg" />
              </IconButton>
            </Tooltip>
            
            <Menu
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={handleProfileMenuClose}
            >
              <MenuItem onClick={() => { navigate('/perfil'); handleProfileMenuClose(); }}>
                <ListItemIcon>
                  <PersonIcon fontSize="small" />
                </ListItemIcon>
                Meu Perfil
              </MenuItem>
              
              <MenuItem onClick={handleLogout}>
                <ListItemIcon>
                  <LogoutIcon fontSize="small" />
                </ListItemIcon>
                Sair
              </MenuItem>
            </Menu>
          </Box>
        </Toolbar>
      </AppBar>
      
      {/* Menu lateral */}
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
      >
        {/* Versão móvel */}
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true, // Melhor desempenho em dispositivos móveis
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
        
        {/* Versão desktop */}
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
      
      {/* Conteúdo principal */}
      <Box
        component="main"
        sx={{ 
          flexGrow: 1, 
          p: 3, 
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          minHeight: '100vh'
        }}
      >
        <Toolbar /> {/* Espaçamento para a AppBar */}
        <Outlet /> {/* Renderiza as rotas filhas */}
      </Box>
    </Box>
  );
};

export default DashboardLayout;
