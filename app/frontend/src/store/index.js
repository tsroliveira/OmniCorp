import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import userReducer from './slices/userSlice';
import profileReducer from './slices/profileSlice';
import permissionReducer from './slices/permissionSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    users: userReducer,
    profiles: profileReducer,
    permissions: permissionReducer,
  },
}); 