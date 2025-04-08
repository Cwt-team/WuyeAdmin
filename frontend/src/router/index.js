import { createRouter, createWebHistory } from 'vue-router'
import UserLogin from '../components/UserLogin.vue'
import DashboardView from '../components/Dashboard.vue'
import HomeView from '../views/HomeView.vue'
import AreaMaintenance from '../views/AreaMaintenance.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'UserLogin', component: UserLogin },
  { path: '/dashboard', name: 'DashboardView', component: DashboardView, meta: { requiresAuth: true } },
  {
    path: '/property-admins',
    name: 'PropertyAdminList',
    component: () => import('../components/PropertyAdminList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/AboutView.vue')
  },
  {
    path: '/area-maintenance',
    name: 'AreaMaintenance',
    component: AreaMaintenance
  },
  {
    path: '/device-detail/:id',
    name: 'DeviceDetail',
    component: () => import('../components/DeviceDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/device-config/:id',
    name: 'DeviceConfig',
    component: () => import('../components/DeviceConfig.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/device-heartbeats',
    name: 'DeviceHeartbeats',
    component: () => import('../components/DeviceHeartbeats.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth) && !isLoggedIn()) {
    next({ path: '/login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

function isLoggedIn() {
  return localStorage.getItem('isLoggedIn') === 'true'
}

export default router
