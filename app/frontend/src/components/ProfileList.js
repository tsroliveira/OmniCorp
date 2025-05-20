import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  Typography,
  CircularProgress,
  Box,
} from '@mui/material';
import { fetchProfiles, deleteProfile } from '../store/slices/profileSlice';
import { Link } from 'react-router-dom';

const ProfileList = () => {
  const dispatch = useDispatch();
  const { profiles, loading, error } = useSelector((state) => state.profiles);

  useEffect(() => {
    dispatch(fetchProfiles());
  }, [dispatch]);

  const handleDelete = (id) => {
    if (window.confirm('Tem certeza que deseja excluir este perfil?')) {
      dispatch(deleteProfile(id));
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Typography color="error" align="center">
        Erro ao carregar perfis: {error.message}
      </Typography>
    );
  }

  return (
    <div>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h5">Perfis</Typography>
        <Button
          component={Link}
          to="/profiles/create"
          variant="contained"
          color="primary"
        >
          Novo Perfil
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Nome</TableCell>
              <TableCell>Descrição</TableCell>
              <TableCell>Permissões</TableCell>
              <TableCell>Ações</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {profiles.map((profile) => (
              <TableRow key={profile.id}>
                <TableCell>{profile.name}</TableCell>
                <TableCell>{profile.description}</TableCell>
                <TableCell>
                  {profile.permissions.map((p) => p.name).join(', ')}
                </TableCell>
                <TableCell>
                  <Button
                    component={Link}
                    to={`/profiles/${profile.id}`}
                    variant="outlined"
                    size="small"
                    sx={{ mr: 1 }}
                  >
                    Editar
                  </Button>
                  <Button
                    variant="outlined"
                    color="error"
                    size="small"
                    onClick={() => handleDelete(profile.id)}
                  >
                    Excluir
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default ProfileList; 