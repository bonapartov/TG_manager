<template>
  <div id="app" class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
    <AppHeader v-if="isAuthenticated" />
    <main :class="{ 'pt-16': isAuthenticated }">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from './store/auth'
import AppHeader from './components/layout/AppHeader.vue'

const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)
</script>

<style>
#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Global styles */
.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.glass-effect {
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.1);
}

.hover-lift {
  transition: all 0.3s ease;
}

.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.slide-in {
  animation: slideIn 0.6s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.pulse-dot {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
</style>