import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

export const fetchRoles = createAsyncThunk('roles/fetchRoles', async () => {
    const response = await axios.get('/api/roles');
    return response.data;
});

export const createRole = createAsyncThunk('roles/createRole', async (role) => {
    const response = await axios.post('/api/roles', role);
    return response.data;
});

export const updateRole = createAsyncThunk('roles/updateRole', async (role) => {
    const response = await axios.put(`/api/roles/${role.id}`, role);
    return response.data;
});

export const deleteRole = createAsyncThunk('roles/deleteRole', async (roleId) => {
    await axios.delete(`/api/roles/${roleId}`);
    return roleId;
});

const roleSlice = createSlice({
    name: 'roles',
    initialState: {
        items: [],
        status: 'idle',
        error: null,
    },
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(fetchRoles.pending, (state) => {
                state.status = 'loading';
            })
            .addCase(fetchRoles.fulfilled, (state, action) => {
                state.status = 'succeeded';
                state.items = action.payload;
            })
            .addCase(fetchRoles.rejected, (state, action) => {
                state.status = 'failed';
                state.error = action.error.message;
            })
            .addCase(createRole.fulfilled, (state, action) => {
                state.items.push(action.payload);
            })
            .addCase(updateRole.fulfilled, (state, action) => {
                const index = state.items.findIndex(role => role.id === action.payload.id);
                state.items[index] = action.payload;
            })
            .addCase(deleteRole.fulfilled, (state, action) => {
                state.items = state.items.filter(role => role.id !== action.payload);
            });
    },
});

export default roleSlice.reducer; 