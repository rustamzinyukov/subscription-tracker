import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://disciplined-cat-production.up.railway.app';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Define API client interface
interface ApiClient {
  getCurrentUser: () => Promise<any>;
  getSubscriptions: () => Promise<any>;
  getMonthlyAnalytics: () => Promise<any>;
  getYearlyAnalytics: () => Promise<any>;
  createSubscription: (data: any) => Promise<any>;
  updateSubscription: (id: number, data: any) => Promise<any>;
  deleteSubscription: (id: number) => Promise<any>;
  login: (data: any) => Promise<any>;
  register: (data: any) => Promise<any>;
}

// Add request interceptor to include auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API methods
export const getCurrentUser = () => api.get('/api/v1/auth/me');
export const getSubscriptions = () => api.get('/api/v1/subscriptions');
export const getMonthlyAnalytics = () => api.get('/api/v1/analytics/monthly');
export const getYearlyAnalytics = () => api.get('/api/v1/analytics/yearly');
export const createSubscription = (data: any) => api.post('/api/v1/subscriptions', data);
export const updateSubscription = (id: number, data: any) => api.put(`/api/v1/subscriptions/${id}`, data);
export const deleteSubscription = (id: number) => api.delete(`/api/v1/subscriptions/${id}`);
export const login = (data: any) => api.post('/api/v1/auth/login', data);
export const register = (data: any) => api.post('/api/v1/auth/register', data);

// Create apiClient object with methods
export const apiClient = {
  ...api,
  getCurrentUser,
  getSubscriptions,
  getMonthlyAnalytics,
  getYearlyAnalytics,
  createSubscription,
  updateSubscription,
  deleteSubscription,
  login,
  register,
} as ApiClient;
export default api;