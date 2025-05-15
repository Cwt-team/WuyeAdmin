import { createRouter, createWebHashHistory } from 'vue-router'

// 路由定义
const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/dashboard/home'
      },
      {
        path: 'home',
        name: 'Home',
        component: () => import('../views/Home.vue'),
        meta: { title: '首页' }
      },
      // 小区管理
      {
        path: 'community',
        name: 'Community',
        component: () => import('../views/community/CommunityInfo.vue'),
        meta: { title: '小区信息' }
      },
      {
        path: 'houses',
        name: 'Houses',
        component: () => import('../views/community/HouseInfo.vue'),
        meta: { title: '房屋信息' }
      },
      {
        path: 'owners',
        name: 'Owners',
        component: () => import('../views/community/OwnerInfo.vue'),
        meta: { title: '业主信息' }
      },
      // 设备管理
      {
        path: 'doorAccess',
        name: 'DoorAccess',
        component: () => import('../views/device/DoorAccess.vue'),
        meta: { title: '门禁信息' }
      },
      // 个人中心
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('../views/profile/UserProfile.vue'),
        meta: { title: '个人资料' }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// 导航守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!token) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router 