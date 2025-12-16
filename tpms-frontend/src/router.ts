import { RouteRecordRaw } from 'vue-router'

export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/posts',
    name: 'Posts',
    component: () => import('@/views/Posts.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/channels',
    name: 'Channels',
    component: () => import('@/views/Channels.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/calendar',
    name: 'Calendar',
    component: () => import('@/views/Calendar.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue')
  }
]



