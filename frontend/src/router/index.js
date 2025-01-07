import { createRouter, createWebHistory } from 'vue-router';
import UserLogin from '@/components/UserLogin.vue';
import DashboardView from '@/components/Dashboard.vue'; // 确保名称一致

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'UserLogin', component: UserLogin },
  { path: '/dashboard', name: 'DashboardView', component: DashboardView, meta: { requiresAuth: true } }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth) && !isLoggedIn()) {
    next({ path: '/login', query: { redirect: to.fullPath } });
  } else {
    next();
  }
});

function isLoggedIn() {
  return localStorage.getItem('isLoggedIn') === 'true';
}

export default router;
