import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

// Estado inicial
const initialState = {
  user: null,
  token: localStorage.getItem('token') || null,
  isAuthenticated: !!localStorage.getItem('token'),
  isLoading: false,
  error: null,
};

// Ação para login
export const login = createAsyncThunk(
  'auth/login',
  async ({ username, password }, { rejectWithValue }) => {
    try {
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      const response = await axios.post('/api/auth/token', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      const { access_token } = response.data;
      
      // Salva o token no localStorage
      localStorage.setItem('token', access_token);
      
      // Obtém informações do usuário
      const userResponse = await axios.get('/api/auth/me', {
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      });
      
      return {
        token: access_token,
        user: userResponse.data,
      };
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Erro ao fazer login');
    }
  }
);

// Ação para logout
export const logout = createAsyncThunk(
  'auth/logout',
  async () => {
    localStorage.removeItem('token');
    return null;
  }
);

// Ação para verificar usuário atual
export const checkCurrentUser = createAsyncThunk(
  'auth/checkCurrentUser',
  async (_, { getState, rejectWithValue }) => {
    try {
      const { auth } = getState();
      if (!auth.token) return null;
      
      const response = await axios.get('/api/auth/me', {
        headers: {
          Authorization: `Bearer ${auth.token}`,
        },
      });
      
      return response.data;
    } catch (error) {
      // Se o token estiver inválido, remove do localStorage
      if (error.response?.status === 401) {
        localStorage.removeItem('token');
      }
      return rejectWithValue(error.response?.data?.detail || 'Erro ao obter usuário atual');
    }
  }
);

// Slice
const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Login
      .addCase(login.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isAuthenticated = true;
        state.token = action.payload.token;
        state.user = action.payload.user;
        state.error = null;
      })
      .addCase(login.rejected, (state, action) => {
        state.isLoading = false;
        state.isAuthenticated = false;
        state.token = null;
        state.user = null;
        state.error = action.payload;
      })
      
      // Logout
      .addCase(logout.fulfilled, (state) => {
        state.isAuthenticated = false;
        state.token = null;
        state.user = null;
      })
      
      // Check current user
      .addCase(checkCurrentUser.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(checkCurrentUser.fulfilled, (state, action) => {
        state.isLoading = false;
        if (action.payload) {
          state.user = action.payload;
          state.isAuthenticated = true;
        } else {
          state.isAuthenticated = false;
          state.token = null;
        }
      })
      .addCase(checkCurrentUser.rejected, (state) => {
        state.isLoading = false;
        state.isAuthenticated = false;
        state.token = null;
        state.user = null;
      });
  },
});

export const { clearError } = authSlice.actions;

export default authSlice.reducer; 