import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getTraces = async (category) => {
  const params = category ? { category } : {};
  const response = await apiClient.get('/traces', { params });
  return response.data;
};

export const getAnalytics = async () => {
  const response = await apiClient.get('/analytics');
  return response.data;
};

export const searchTraces = async (query) => {
  const response = await apiClient.get('/traces/search', {
    params: { q: query },
  });
  return response.data;
};

export default apiClient;
