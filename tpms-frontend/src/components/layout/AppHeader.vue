<template>
  <header class="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <div class="flex items-center space-x-4">
          <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
            <el-icon class="text-white text-xl">
              <Promotion />
            </el-icon>
          </div>
          <h1 class="text-xl font-bold gradient-text">TPMS</h1>
        </div>
        
        <nav class="hidden md:flex items-center space-x-8">
          <router-link 
            to="/" 
            class="text-gray-700 hover:text-blue-600 transition-colors font-medium"
            :class="{ 'text-blue-600': $route.path === '/' }"
          >
            Панель
          </router-link>
          <router-link 
            to="/posts" 
            class="text-gray-700 hover:text-blue-600 transition-colors font-medium"
            :class="{ 'text-blue-600': $route.path === '/posts' }"
          >
            Публикации
          </router-link>
          <router-link 
            to="/channels" 
            class="text-gray-700 hover:text-blue-600 transition-colors font-medium"
            :class="{ 'text-blue-600': $route.path === '/channels' }"
          >
            Каналы
          </router-link>
          <router-link 
            to="/calendar" 
            class="text-gray-700 hover:text-blue-600 transition-colors font-medium"
            :class="{ 'text-blue-600': $route.path === '/calendar' }"
          >
            Календарь
          </router-link>
        </nav>
        
        <div class="flex items-center space-x-4">
          <el-button 
            text 
            class="p-2 rounded-lg hover:bg-gray-100 transition-colors"
            @click="toggleNotifications"
          >
            <el-icon class="text-gray-600">
              <Bell />
            </el-icon>
          </el-button>
          
          <el-dropdown trigger="click">
            <div class="flex items-center space-x-2 cursor-pointer">
              <div class="w-8 h-8 bg-gradient-to-br from-green-400 to-blue-500 rounded-full"></div>
              <span class="text-sm font-medium text-gray-700">{{ currentUser?.username || 'User' }}</span>
              <el-icon class="text-gray-500">
                <ArrowDown />
              </el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="$router.push('/profile')">
                  <el-icon><User /></el-icon>
                  Профиль
                </el-dropdown-item>
                <el-dropdown-item @click="$router.push('/settings')">
                  <el-icon><Setting /></el-icon>
                  Настройки
                </el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">
                  <el-icon><SwitchButton /></el-icon>
                  Выйти
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { 
  Promotion, 
  Bell, 
  ArrowDown, 
  User, 
  Setting, 
  SwitchButton 
} from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()

const currentUser = computed(() => authStore.user)

const toggleNotifications = () => {
  // TODO: Implement notifications panel
  console.log('Toggle notifications')
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>