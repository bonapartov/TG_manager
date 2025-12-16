import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '@/services/api'
import type { User, LoginForm, TokenResponse } from '@/types/auth'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  
  // State
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const refreshToken = ref<string | null>(localStorage.getItem('refresh_token'))
  
  // Getters
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin' || user.value?.role === 'superadmin')
  const isEditor = computed(() => user.value?.role === 'editor' || isAdmin.value)
  
  // Actions
  const setAuth = (authData: TokenResponse, userData: User) => {
    token.value = authData.access_token
    refreshToken.value = authData.refresh_token
    user.value = userData
    
    // Save to localStorage
    localStorage.setItem('token', authData.access_token)
    localStorage.setItem('refresh_token', authData.refresh_token)
    localStorage.setItem('user', JSON.stringify(userData))
    
    // Set default auth header
    authApi.setAuthToken(authData.access_token)
  }
  
  const clearAuth = () => {
    token.value = null
    refreshToken.value = null
    user.value = null
    
    // Clear localStorage
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    
    // Clear auth header
    authApi.setAuthToken(null)
  }
  
  const login = async (credentials: LoginForm) => {
    try {
      const response = await authApi.login(credentials)
      const { data } = response
      
      // Get user info
      const userResponse = await authApi.getMe()
      
      setAuth(data, userResponse.data)
      
      // Redirect to dashboard
      await router.push('/')
      
      return { success: true }
    } catch (error: any) {
      clearAuth()
      return {
        success: false,
        error: error.response?.data?.detail || 'Login failed'
      }
    }
  }
  
  const logout = async () => {
    try {
      if (token.value) {
        await authApi.logout()
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      clearAuth()
      await router.push('/login')
    }
  }
  
  const refreshAccessToken = async () => {
    if (!refreshToken.value) {
      clearAuth()
      return false
    }
    
    try {
      const response = await authApi.refreshToken(refreshToken.value)
      const { data } = response
      
      token.value = data.access_token
      refreshToken.value = data.refresh_token
      
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)
      
      authApi.setAuthToken(data.access_token)
      
      return true
    } catch (error) {
      clearAuth()
      await router.push('/login')
      return false
    }
  }
  
  const loadUserFromStorage = () => {
    const storedUser = localStorage.getItem('user')
    const storedToken = localStorage.getItem('token')
    const storedRefreshToken = localStorage.getItem('refresh_token')
    
    if (storedUser && storedToken) {
      try {
        user.value = JSON.parse(storedUser)
        token.value = storedToken
        refreshToken.value = storedRefreshToken
        authApi.setAuthToken(storedToken)
        return true
      } catch (error) {
        clearAuth()
        return false
      }
    }
    
    return false
  }
  
  const checkAuth = async () => {
    if (!token.value) {
      clearAuth()
      return false
    }
    
    try {
      const response = await authApi.getMe()
      user.value = response.data
      return true
    } catch (error) {
      // Try to refresh token
      return await refreshAccessToken()
    }
  }
  
  const hasPermission = (requiredRole: string) => {
    const roles = ['guest', 'editor', 'admin', 'superadmin']
    const userRoleIndex = roles.indexOf(user.value?.role || 'guest')
    const requiredRoleIndex = roles.indexOf(requiredRole)
    
    return userRoleIndex >= requiredRoleIndex
  }
  
  // Initialize store
  const init = () => {
    loadUserFromStorage()
  }
  
  return {
    // State
    user,
    token,
    refreshToken,
    
    // Getters
    isAuthenticated,
    isAdmin,
    isEditor,
    
    // Actions
    login,
    logout,
    refreshAccessToken,
    loadUserFromStorage,
    checkAuth,
    hasPermission,
    init
  }
})