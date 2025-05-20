import axios from 'axios';

// Determina a URL base dependendo do ambiente
const API_URL = process.env.REACT_APP_API_URL || '';

// Criando uma instância do axios com configurações base
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token de autenticação a todas as requisições
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para tratar erros de resposta
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Tratamento de erro de autenticação (token expirado)
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      // Redirecionar para login se necessário
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api; 