import React from 'react';
import { useSelector } from 'react-redux';
import { 
  Grid, 
  Card, 
  CardContent, 
  Typography, 
  Box,
  Paper,
  Container
} from '@mui/material';
import PeopleIcon from '@mui/icons-material/People';
import ExtensionIcon from '@mui/icons-material/Extension';
import ArticleIcon from '@mui/icons-material/Article';
import ChecklistIcon from '@mui/icons-material/Checklist';

const Dashboard = () => {
  const { user } = useSelector((state) => state.auth);
  
  // Cards de estatística
  const statCards = [
    {
      title: 'Usuários',
      count: 15,
      icon: <PeopleIcon fontSize="large" sx={{ color: '#1976d2' }} />,
    },
    {
      title: 'Módulos',
      count: 8,
      icon: <ExtensionIcon fontSize="large" sx={{ color: '#2e7d32' }} />,
    },
    {
      title: 'Artigos Wiki',
      count: 24,
      icon: <ArticleIcon fontSize="large" sx={{ color: '#ed6c02' }} />,
    },
    {
      title: 'Tarefas',
      count: 12,
      icon: <ChecklistIcon fontSize="large" sx={{ color: '#9c27b0' }} />,
    },
  ];
  
  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Dashboard
        </Typography>
        <Typography variant="body1" color="text.secondary" gutterBottom>
          Bem-vindo, {user?.full_name || user?.username}!
        </Typography>
        
        {/* Cards de estatísticas */}
        <Grid container spacing={3} sx={{ mt: 2 }}>
          {statCards.map((card, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Card 
                sx={{ 
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'center',
                  alignItems: 'center',
                  py: 2
                }}
              >
                <CardContent 
                  sx={{ 
                    textAlign: 'center',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center'
                  }}
                >
                  {card.icon}
                  <Typography variant="h3" sx={{ mt: 2, fontWeight: 'bold' }}>
                    {card.count}
                  </Typography>
                  <Typography variant="subtitle1" color="text.secondary">
                    {card.title}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
        
        {/* Conteúdo informativo */}
        <Grid container spacing={3} sx={{ mt: 2 }}>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                Atividades Recentes
              </Typography>
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" paragraph>
                  • João Silva atualizou o artigo "Configuração do Ambiente" na Wiki
                </Typography>
                <Typography variant="body2" paragraph>
                  • Maria Oliveira completou 3 tarefas do checklist diário
                </Typography>
                <Typography variant="body2" paragraph>
                  • Pedro Santos adicionou um novo cliente
                </Typography>
                <Typography variant="body2" paragraph>
                  • Ana Souza foi designada para o plantão do fim de semana
                </Typography>
              </Box>
            </Paper>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                Próximos Eventos
              </Typography>
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" paragraph>
                  • Manutenção programada: 15/04/2025 às 22:00
                </Typography>
                <Typography variant="body2" paragraph>
                  • Reunião de equipe: 10/04/2025 às 14:00
                </Typography>
                <Typography variant="body2" paragraph>
                  • Treinamento de segurança: 12/04/2025 às 09:00
                </Typography>
                <Typography variant="body2" paragraph>
                  • Visita ao cliente XYZ: 18/04/2025 às 10:30
                </Typography>
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default Dashboard; 