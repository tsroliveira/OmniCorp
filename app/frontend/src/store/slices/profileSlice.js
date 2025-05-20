import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

export const fetchProfiles = createAsyncThunk(
  'profiles/fetchProfiles',
  async (_, { rejectWithValue }) => {
    try {
      const response = await axios.get(`${API_URL}/profiles`);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const createProfile = createAsyncThunk(
  'profiles/createProfile',
  async (profileData, { rejectWithValue }) => {
    try {
      const response = await axios.post(`${API_URL}/profiles`, profileData);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const updateProfile = createAsyncThunk(
  'profiles/updateProfile',
  async ({ id, profileData }, { rejectWithValue }) => {
    try {
      const response = await axios.put(`${API_URL}/profiles/${id}`, profileData);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const deleteProfile = createAsyncThunk(
  'profiles/deleteProfile',
  async (id, { rejectWithValue }) => {
    try {
      await axios.delete(`${API_URL}/profiles/${id}`);
      return id;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const addPermissionToProfile = createAsyncThunk(
  'profiles/addPermission',
  async ({ profileId, permissionId }, { rejectWithValue }) => {
    try {
      await axios.post(`${API_URL}/profiles/${profileId}/permissions/${permissionId}`);
      return { profileId, permissionId };
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const removePermissionFromProfile = createAsyncThunk(
  'profiles/removePermission',
  async ({ profileId, permissionId }, { rejectWithValue }) => {
    try {
      await axios.delete(`${API_URL}/profiles/${profileId}/permissions/${permissionId}`);
      return { profileId, permissionId };
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

const profileSlice = createSlice({
  name: 'profiles',
  initialState: {
    profiles: [],
    loading: false,
    error: null,
  },
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Profiles
      .addCase(fetchProfiles.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchProfiles.fulfilled, (state, action) => {
        state.loading = false;
        state.profiles = action.payload;
      })
      .addCase(fetchProfiles.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // Create Profile
      .addCase(createProfile.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createProfile.fulfilled, (state, action) => {
        state.loading = false;
        state.profiles.push(action.payload);
      })
      .addCase(createProfile.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // Update Profile
      .addCase(updateProfile.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateProfile.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.profiles.findIndex(p => p.id === action.payload.id);
        if (index !== -1) {
          state.profiles[index] = action.payload;
        }
      })
      .addCase(updateProfile.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // Delete Profile
      .addCase(deleteProfile.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteProfile.fulfilled, (state, action) => {
        state.loading = false;
        state.profiles = state.profiles.filter(p => p.id !== action.payload);
      })
      .addCase(deleteProfile.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { clearError } = profileSlice.actions;
export default profileSlice.reducer; 