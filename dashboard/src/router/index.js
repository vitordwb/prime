import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '@/views/HomeView.vue'

const routes = [
  {
    meta: {
      title: 'Home'
    },
    path: '/',
    component: Home
  },
  {
    meta: {
      title: 'Dashboard'
    },
    path: '/',
    name: 'dashboard',
    component: Home
  },
  {
    meta: {
      title: 'Qr Code'
    },
    path: '/qrcode',
    name: 'qrcode',
    component: () => import('@/views/QrcodeView.vue')
  },
  {
    meta: {
      title: 'Perfil'
    },
    path: '/perfil',
    name: 'perfil',
    component: () => import('@/views/ProfileView.vue')
  },
  {
    meta: {
      title: 'Charts'
    },
    path: '/charts',
    name: 'charts',
    component: () => import('@/views/ChartsView.vue')
  },
  {
    meta: {
      title: 'Login'
    },
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue')
  },
  {
    meta: {
      title: 'Error'
    },
    path: '/error',
    name: 'error',
    component: () => import('@/views/ErrorView.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 }
  }
})

export default router
