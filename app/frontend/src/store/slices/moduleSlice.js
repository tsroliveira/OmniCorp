import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

// Estado inicial
const initialState = {
  modules: [],
  currentModule: null,
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

// Buscar todos os módulos
export const fetchModules = createAsyncThunk(
  'modules/fetchAll',
  async (_, { getState, rejectWithValue }) => {
    try {
      const response = await axios.get('/api/modules/', getAuthHeader(getState));
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Erro ao buscar módulos');
    }
  }
);

// Criar módulo
export const createModule = createAsyncThunk(
  'modules/create',
  async (moduleData, { getState, rejectWithValue }) => {
    try {
      const response = await axios.post('/api/modules/', moduleData, getAuthHeader(getState));
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Erro ao criar módulo');
    }
  }
);

// Atualizar módulo
export const updateModule = createAsyncThunk(
  'modules/update',
  async ({ id, moduleData }, { getState, rejectWithValue }) => {
    try {
      const response = await axios.put(`/api/modules/${id}`, moduleData, getAuthHeader(getState));
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Erro ao atualizar módulo');
    }
  }
);

// Remover módulo
export const deleteModule = createAsyncThunk(
  'modules/delete',
  async (id, { getState, rejectWithValue }) => {
    try {
      await axios.delete(`/api/modules/${id}`, getAuthHeader(getState));
      return id;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Erro ao remover módulo');
    }
  }
);

// Slice
const moduleSlice = createSlice({
  name: 'modules',
  initialState,
  reducers: {
    clearModuleError: (state) => {
      state.error = null;
    },
    setCurrentModule: (state, action) => {
      state.currentModule = action.payload;
    },
    clearCurrentModule: (state) => {
      state.currentModule = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch modules
      .addCase(fetchModules.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchModules.fulfilled, (state, action) => {
        state.isLoading = false;
        state.modules = action.payload;
        state.error = null;
      })
      .addCase(fetchModules.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      
      // Create module
      .addCase(createModule.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(createModule.fulfilled, (state, action) => {
        state.isLoading = false;
        state.modules.push(action.payload);
        state.error = null;
      })
      .addCase(createModule.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      
      // Update module
      .addCase(updateModule.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(updateModule.fulfilled, (state, action) => {
        state.isLoading = false;
        const index = state.modules.findIndex((module) => module.id === action.payload.id);
        if (index !== -1) {
          state.modules[index] = action.payload;
        }
        state.error = null;
      })
      .addCase(updateModule.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      
      // Delete module
      .addCase(deleteModule.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(deleteModule.fulfilled, (state, action) => {
        state.isLoading = false;
        state.modules = state.modules.filter((module) => module.id !== action.payload);
        state.error = null;
      })
      .addCase(deleteModule.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });
  },
});

export const { clearModuleError, setCurrentModule, clearCurrentModule } = moduleSlice.actions;

export default moduleSlice.reducer; 