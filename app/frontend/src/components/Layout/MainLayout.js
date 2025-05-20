import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { Box, Toolbar } from '@mui/material';
import Header from './Header';
import Sidebar from './Sidebar';
import { checkCurrentUser } from '../../store/slices/authSlice';

const MainLayout = ({ children }) => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { isAuthenticated, isLoading } = useSelector((state) => state.auth);
  
  useEffect(() => {
    // Verifica o usuário atual ao montar o componente
    dispatch(checkCurrentUser());
  }, [dispatch]);
  
  useEffect(() => {
    // Redireciona para login se não estiver autenticado
    if (!isLoading && !isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, isLoading, navigate]);
  
  // Se estiver carregando, não renderiza nada
  if (isLoading) {
    return null;
  }
  
  // Se não estiver autenticado, não renderiza o layout
  if (!isAuthenticated) {
    return null;
  }
  
  return (
    <Box sx={{ display: 'flex' }}>
      <Header />
      <Sidebar />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          marginLeft: '240px',
          marginTop: '64px',
          minHeight: 'calc(100vh - 64px)',
          backgroundColor: '#f5f5f5',
        }}
      >
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
};

export default MainLayout; 