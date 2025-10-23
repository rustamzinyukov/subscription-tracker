import axios from 'axios';

// Force HTTPS for all API requests
const BACKEND_API_URL = 'https://disciplined-cat-production.up.railway.app';

export const api = axios.create({
  baseURL: BACKEND_API_URL,
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
  const token = localStorage.getItem('access_token');
  console.log(`🔑 API Request to ${config.url} - Token:`, token ? `${token.substring(0, 20)}...` : 'not found');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
    console.log('✅ Authorization header set');
    console.log(`🔑 Full Authorization header: Bearer ${token.substring(0, 20)}...`);
  } else {
    console.log('❌ No token found, request will be unauthorized');
  }
  return config;
});

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response from ${response.config.url}: ${response.status}`);
    return response;
  },
  (error) => {
    console.log(`❌ API Error from ${error.config?.url}: ${error.message}`);
    console.log(`❌ Error details:`, error);
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
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