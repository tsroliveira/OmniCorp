import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Box,
  Typography,
} from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';
import PeopleIcon from '@mui/icons-material/People';
import ExtensionIcon from '@mui/icons-material/Extension';
import SettingsIcon from '@mui/icons-material/Settings';
import ArticleIcon from '@mui/icons-material/Article';
import CalendarMonthIcon from '@mui/icons-material/CalendarMonth';
import ChecklistIcon from '@mui/icons-material/Checklist';
import { Link } from 'react-router-dom';
import { fetchModules } from '../../store/slices/moduleSlice';

// Largura da barra lateral
const drawerWidth = 240;

const Sidebar = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();
  const { modules } = useSelector((state) => state.modules);
  const { user } = useSelector((state) => state.auth);
  
  // Busca os módulos disponíveis quando o componente é montado
  useEffect(() => {
    dispatch(fetchModules());
  }, [dispatch]);
  
  // Módulos fixos que sempre aparecem (dashboard)
  const fixedModules = [
    {
      id: 'dashboard',
      name: 'Dashboard',
      url: '/dashboard',
      icon: <DashboardIcon />,
    },
  ];
  
  // Módulos de administração
  const adminModules = [
    {
      id: 'users',
      name: 'Usuários',
      url: '/admin/users',
      icon: <PeopleIcon />,
    },
    {
      id: 'modules',
      name: 'Módulos',
      url: '/admin/modules',
      icon: <ExtensionIcon />,
    },
  ];
  
  // Módulos de exemplo para exibição no menu
  const exampleModules = [
    {
      id: 'wiki',
      name: 'Wiki',
      url: '/wiki',
      icon: <ArticleIcon />,
    },
    {
      id: 'checklist',
      name: 'Checklist',
      url: '/checklist',
      icon: <ChecklistIcon />,
    },
    {
      id: 'calendar',
      name: 'Calendário',
      url: '/calendar',
      icon: <CalendarMonthIcon />,
    },
  ];
  
  // Verifica se o usuário é admin
  const isAdmin = user?.role?.name === 'admin' || user?.username === 'administrator';
  
  const menuItems = [
    {
      text: 'Dashboard',
      icon: <DashboardIcon />,
      path: '/',
    },
    {
      text: 'Usuários',
      icon: <PeopleIcon />,
      path: '/users',
      adminOnly: true,
    },
    {
      text: 'Perfis',
      icon: <SettingsIcon />,
      path: '/profiles',
      adminOnly: true,
    },
    {
      text: 'Configurações',
      icon: <SettingsIcon />,
      path: '/settings',
      adminOnly: true,
    },
  ];

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
          top: '64px',
          height: 'calc(100% - 64px)',
          borderRight: '1px solid rgba(0, 0, 0, 0.12)',
        },
      }}
    >
      <Box sx={{ overflow: 'auto' }}>
        <List>
          {menuItems
            .filter((item) => !item.adminOnly || isAdmin)
            .map((item) => (
              <ListItem
                button
                component={Link}
                to={item.path}
                key={item.text}
                selected={location.pathname === item.path}
              >
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItem>
            ))}
        </List>
        
        <Divider />
        
        {isAdmin && (
          <>
            <Box sx={{ px: 2, py: 1 }}>
              <Typography variant="subtitle2" color="text.secondary">
                Administração
              </Typography>
            </Box>
            <List>
              {adminModules.map((module) => (
                <ListItem
                  button
                  key={module.id}
                  onClick={() => navigate(module.url)}
                  selected={location.pathname === module.url}
                >
                  <ListItemIcon>{module.icon}</ListItemIcon>
                  <ListItemText primary={module.name} />
                </ListItem>
              ))}
            </List>
            <Divider />
          </>
        )}
        
        <Box sx={{ px: 2, py: 1 }}>
          <Typography variant="subtitle2" color="text.secondary">
            Módulos
          </Typography>
        </Box>
        
        <List>
          {/* Aqui seriam exibidos os módulos do banco, por enquanto vamos mostrar exemplos */}
          {exampleModules.map((module) => (
            <ListItem
              button
              key={module.id}
              onClick={() => navigate(module.url)}
              selected={location.pathname === module.url}
            >
              <ListItemIcon>{module.icon}</ListItemIcon>
              <ListItemText primary={module.name} />
            </ListItem>
          ))}
        </List>
      </Box>
    </Drawer>
  );
};

export default Sidebar; 