import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import { createI18n } from 'vue-i18n'

import App from './App.vue'
import { routes } from './router'
import { useAuthStore } from './store/auth'
import './assets/styles/main.scss'

// Create app
const app = createApp(App)

// Create store
const pinia = createPinia()
app.use(pinia)

// Initialize auth store after pinia is installed
const authStore = useAuthStore()
authStore.init()

// Create router
const router = createRouter({
  history: createWebHistory(),
  routes
})

// Router guards
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Check if route requires authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

app.use(router)

// Element Plus
app.use(ElementPlus)

// Register icons
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// i18n
const i18n = createI18n({
  legacy: false,
  locale: 'ru',
  fallbackLocale: 'en',
  messages: {
    ru: {
      // Russian translations
    },
    en: {
      // English translations
    }
  }
})
app.use(i18n)

// Mount app
app.mount('#app')