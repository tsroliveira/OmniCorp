import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate, useParams } from 'react-router-dom';
import {
  TextField,
  Button,
  Typography,
  Paper,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  CircularProgress,
} from '@mui/material';
import {
  createProfile,
  updateProfile,
  fetchProfiles,
} from '../store/slices/profileSlice';
import { fetchPermissions } from '../store/slices/permissionSlice';

const ProfileForm = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { id } = useParams();
  const isEdit = Boolean(id);

  const { profiles, loading: profilesLoading } = useSelector((state) => state.profiles);
  const { permissions, loading: permissionsLoading } = useSelector((state) => state.permissions);

  const [formData, setFormData] = useState({
    name: '',
    description: '',
    permissions: [],
  });

  const [selectedPermissions, setSelectedPermissions] = useState([]);

  useEffect(() => {
    dispatch(fetchPermissions());
    if (isEdit) {
      dispatch(fetchProfiles());
    }
  }, [dispatch, isEdit]);

  useEffect(() => {
    if (isEdit && profiles.length > 0) {
      const profile = profiles.find((p) => p.id === parseInt(id));
      if (profile) {
        setFormData({
          name: profile.name,
          description: profile.description || '',
        });
        setSelectedPermissions(profile.permissions.map((p) => p.id));
      }
    }
  }, [isEdit, id, profiles]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const profileData = {
      ...formData,
      permissions: selectedPermissions,
    };

    try {
      if (isEdit) {
        await dispatch(updateProfile({ id, profileData })).unwrap();
      } else {
        await dispatch(createProfile(profileData)).unwrap();
      }
      navigate('/profiles');
    } catch (error) {
      console.error('Erro ao salvar perfil:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handlePermissionChange = (event) => {
    setSelectedPermissions(event.target.value);
  };

  if (profilesLoading || permissionsLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        {isEdit ? 'Editar Perfil' : 'Novo Perfil'}
      </Typography>

      <form onSubmit={handleSubmit}>
        <Box mb={2}>
          <TextField
            fullWidth
            label="Nome"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </Box>

        <Box mb={2}>
          <TextField
            fullWidth
            label="Descrição"
            name="description"
            value={formData.description}
            onChange={handleChange}
            multiline
            rows={3}
          />
        </Box>

        <Box mb={2}>
          <FormControl fullWidth>
            <InputLabel>Permissões</InputLabel>
            <Select
              multiple
              value={selectedPermissions}
              onChange={handlePermissionChange}
              renderValue={(selected) => (
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                  {selected.map((value) => {
                    const permission = permissions.find((p) => p.id === value);
                    return (
                      <Chip
                        key={value}
                        label={permission ? permission.name : ''}
                      />
                    );
                  })}
                </Box>
              )}
            >
              {permissions.map((permission) => (
                <MenuItem key={permission.id} value={permission.id}>
                  {permission.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>

        <Box display="flex" justifyContent="flex-end" gap={1}>
          <Button
            variant="outlined"
            onClick={() => navigate('/profiles')}
          >
            Cancelar
          </Button>
          <Button
            type="submit"
            variant="contained"
            color="primary"
          >
            {isEdit ? 'Atualizar' : 'Criar'}
          </Button>
        </Box>
      </form>
    </Paper>
  );
};

export default ProfileForm; 