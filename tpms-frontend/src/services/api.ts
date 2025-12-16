import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    // Add auth token if available
    const token = localStorage.getItem('token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config

    // Handle 401 Unauthorized
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        // Try to refresh token
        const refreshToken = localStorage.getItem('refresh_token')
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
            refresh_token: refreshToken
          })

          const { access_token, refresh_token } = response.data
          localStorage.setItem('token', access_token)
          localStorage.setItem('refresh_token', refresh_token)

          // Retry original request with new token
          originalRequest.headers.Authorization = `Bearer ${access_token}`
          return axios(originalRequest)
        }
      } catch (refreshError) {
        // Refresh failed, redirect to login
        localStorage.clear()
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

// Auth API
export const authApi = {
  login: (credentials: any) => api.post('/auth/login', credentials),
  loginTelegram: (hash: string) => api.post('/auth/login/telegram', { telegram_hash: hash }),
  logout: () => api.post('/auth/logout'),
  refreshToken: (refreshToken: string) => api.post('/auth/refresh', { refresh_token: refreshToken }),
  getMe: () => api.get('/auth/me'),
  setAuthToken: (token: string | null) => setAuthToken(token),
}

// Posts API
export const postsApi = {
  getPosts: (params?: any) => api.get('/posts', { params }),
  getPost: (id: number) => api.get(`/posts/${id}`),
  createPost: (data: any) => api.post('/posts', data),
  updatePost: (id: number, data: any) => api.put(`/posts/${id}`, data),
  deletePost: (id: number) => api.delete(`/posts/${id}`),
  publishPost: (id: number) => api.post(`/posts/${id}/publish_now`),
  cancelPost: (id: number) => api.post(`/posts/${id}/cancel`),
  retryPost: (id: number) => api.post(`/posts/${id}/retry`),
  uploadMedia: (id: number, file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post(`/posts/${id}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
  getDashboardStats: () => api.get('/posts/stats/dashboard'),
  getPublicationStats: (days: number) => api.get('/posts/stats/publications', { params: { days } }),
}

// Channels API
export const channelsApi = {
  getChannels: (params?: any) => api.get('/channels', { params }),
  getChannel: (id: number) => api.get(`/channels/${id}`),
  createChannel: (data: any) => api.post('/channels', data),
  updateChannel: (id: number, data: any) => api.put(`/channels/${id}`, data),
  deleteChannel: (id: number) => api.delete(`/channels/${id}`),
  checkChannelAccess: (id: number) => api.post(`/channels/${id}/check_access`),
  getChannelPosts: (id: number, params?: any) => api.get(`/channels/${id}/posts`, { params }),
  getChannelStats: (id: number) => api.get(`/channels/${id}/stats`),
}

// Users API
export const usersApi = {
  getUsers: (params?: any) => api.get('/users', { params }),
  getUser: (id: number) => api.get(`/users/${id}`),
  createUser: (data: any) => api.post('/users', data),
  updateUser: (id: number, data: any) => api.put(`/users/${id}`, data),
  deleteUser: (id: number) => api.delete(`/users/${id}`),
}

// Audit API
export const auditApi = {
  getAuditLogs: (params?: any) => api.get('/audit', { params }),
}

// Metrics API
export const metricsApi = {
  getMetrics: () => api.get('/metrics'),
}

// File upload API
export const uploadApi = {
  uploadFile: (file: File, folder?: string) => {
    const formData = new FormData()
    formData.append('file', file)
    if (folder) {
      formData.append('folder', folder)
    }
    return api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
}

// Set auth token
export const setAuthToken = (token: string | null) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
  } else {
    delete api.defaults.headers.common['Authorization']
  }
}

export default api