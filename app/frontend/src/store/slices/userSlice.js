import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

// Estado inicial
const initialState = {
  users: [],
  roles: [],
  currentUser: null,
  isLoading: false,
  error: null,
};

// Configuração do cabeçalho com token
const getAuthHeader = (getState) => {
  const { auth } = getState();
  return {
    headers: {
      Authorization: `Bearer ${auth.token}`,
    },
  };
};

// Buscar todos os usuários
export const fetchUsers = createAsyncThunk(
  'users/fetchAll',
  async (_, { getState, rejectWithValue }) => {
    try {
      const response = await axios.get('/api/users/', getAuthHeader(getState));
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Erro ao buscar usuários');
    }
  }
);

// Buscar perfis
export const fetchRoles = createAsyncThunk(
  'users/fetchRoles',
  async (_, { getState, rejectWithValue }) => {
    try {
      const response = await axios.get('/api/users/roles/', getAuthHeader(getState));
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Erro ao buscar perfis');
    }
  }
);

// Criar usuário
export const createUser = createAsyncThunk(
  'users/create',
  async (userData, { getState, rejectWithValue }) => {
    try {
      const response = await axios.post('/api/users/', userData, getAuthHeader(getState));
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Erro ao criar usuário');
    }
  }
);

// Atualizar usuário
export const updateUser = createAsyncThunk(
  'users/update',
  async ({ id, userData }, { getState, rejectWithValue }) => {
    try {
      const response = await axios.put(`/api/users/${id}`, userData, getAuthHeader(getState));
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Erro ao atualizar usuário');
    }
  }
);

// Remover usuário
export const deleteUser = createAsyncThunk(
  'users/delete',
  async (id, { getState, rejectWithValue }) => {
    try {
      await axios.delete(`/api/users/${id}`, getAuthHeader(getState));
      return id;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Erro ao remover usuário');
    }
  }
);

// Slice
const userSlice = createSlice({
  name: 'users',
  initialState,
  reducers: {
    clearUserError: (state) => {
      state.error = null;
    },
    setCurrentUser: (state, action) => {
      state.currentUser = action.payload;
    },
    clearCurrentUser: (state) => {
      state.currentUser = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch users
      .addCase(fetchUsers.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchUsers.fulfilled, (state, action) => {
        state.isLoading = false;
        state.users = action.payload;
        state.error = null;
      })
      .addCase(fetchUsers.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      
      // Fetch roles
      .addCase(fetchRoles.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchRoles.fulfilled, (state, action) => {
        state.isLoading = false;
        state.roles = action.payload;
        state.error = null;
      })
      .addCase(fetchRoles.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      
      // Create user
      .addCase(createUser.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(createUser.fulfilled, (state, action) => {
        state.isLoading = false;
        state.users.push(action.payload);
        state.error = null;
      })
      .addCase(createUser.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      
      // Update user
      .addCase(updateUser.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(updateUser.fulfilled, (state, action) => {
        state.isLoading = false;
        const index = state.users.findIndex((user) => user.id === action.payload.id);
        if (index !== -1) {
          state.users[index] = action.payload;
        }
        state.error = null;
      })
      .addCase(updateUser.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      
      // Delete user
      .addCase(deleteUser.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(deleteUser.fulfilled, (state, action) => {
        state.isLoading = false;
        state.users = state.users.filter((user) => user.id !== action.payload);
        state.error = null;
      })
      .addCase(deleteUser.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });
  },
});

export const { clearUserError, setCurrentUser, clearCurrentUser } = userSlice.actions;

export default userSlice.reducer; 