import { createRouter, createWebHistory } from 'vue-router'
import UserLogin from '../components/UserLogin.vue'
import DashboardView from '../components/Dashboard.vue'
import HouseDetail from '../components/HouseDetail.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'UserLogin', component: UserLogin },
  { path: '/dashboard', name: 'DashboardView', component: DashboardView, meta: { requiresAuth: true } },
  { path: '/houses/:id', name: 'HouseDetail', component: HouseDetail, meta: { requiresAuth: true } },
  { 
    path: '/property-admins', 
    name: 'PropertyAdminList', 
    component: () => import('../components/PropertyAdminList.vue'),
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
