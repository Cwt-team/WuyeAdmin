<template>
  <div class="dashboard-container">
    <el-container style="height: 100vh;">
      <!-- 侧边栏 -->
      <el-aside width="220px" class="sidebar" :class="{ collapsed: sidebarCollapsed }">
        <div class="logo-container">
          <h3>物业管理系统</h3>
        </div>
        <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          :router="true"
          :collapse="sidebarCollapsed"
          background-color="#1A237E"
          text-color="#E8EAF6"
          active-text-color="#FFFFFF">
          
          <el-menu-item index="/dashboard/home">
            <el-icon><icon-menu /></el-icon>
            <span>首页</span>
          </el-menu-item>
          
          <el-sub-menu index="1">
            <template #title>
              <el-icon><location /></el-icon>
              <span>小区管理</span>
            </template>
            <el-menu-item index="/dashboard/community">小区信息</el-menu-item>
            <el-menu-item index="/dashboard/houses">房屋信息</el-menu-item>
            <el-menu-item index="/dashboard/owners">业主信息</el-menu-item>
          </el-sub-menu>
          
          <el-sub-menu index="2">
            <template #title>
              <el-icon><setting /></el-icon>
              <span>设备管理</span>
            </template>
            <el-menu-item index="/dashboard/doorAccess">门禁信息</el-menu-item>
          </el-sub-menu>
          
          <el-sub-menu index="3">
            <template #title>
              <el-icon><user /></el-icon>
              <span>个人中心</span>
            </template>
            <el-menu-item index="/dashboard/profile">个人资料设置</el-menu-item>
          </el-sub-menu>
        </el-menu>
      </el-aside>
      
      <!-- 主内容区 -->
      <el-container>
        <!-- 顶部导航 -->
        <el-header height="60px" class="header">
          <div class="left">
            <el-icon class="collapse-btn" @click="toggleSidebar">
              <fold v-if="!sidebarCollapsed" />
              <expand v-else />
            </el-icon>
            <breadcrumb />
          </div>
          <div class="right">
            <el-dropdown trigger="click">
              <span class="user-info">
                {{ userInfo.username }}
                <el-icon class="el-icon--right"><arrow-down /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="goToProfile">个人中心</el-dropdown-item>
                  <el-dropdown-item divided @click="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        
        <!-- 页面内容 -->
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Menu as IconMenu, Location, Setting, Fold, Expand, ArrowDown, User } from '@element-plus/icons-vue'
import Breadcrumb from '../components/layout/Breadcrumb.vue'

export default {
  name: 'DashboardView',
  components: {
    IconMenu,
    Location,
    Setting,
    Fold,
    Expand,
    ArrowDown,
    User,
    Breadcrumb
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    
    // 用户信息
    const userInfo = reactive({
      username: '管理员',
      // 其他用户信息
    })
    
    // 获取用户信息
    onMounted(() => {
      const storedUserInfo = localStorage.getItem('userInfo')
      if (storedUserInfo) {
        try {
          const parsedInfo = JSON.parse(storedUserInfo)
          userInfo.username = parsedInfo.username || '管理员'
          // 设置其他用户信息
        } catch (error) {
          console.error('解析用户信息失败:', error)
        }
      }
    })
    
    // 当前激活的菜单
    const activeMenu = computed(() => {
      return route.path
    })
    
    // 侧边栏折叠状态
    const sidebarCollapsed = ref(false)
    
    // 切换侧边栏
    const toggleSidebar = () => {
      sidebarCollapsed.value = !sidebarCollapsed.value
    }
    
    // 转到个人中心
    const goToProfile = () => {
      router.push('/dashboard/profile')
    }
    
    // 退出登录
    const logout = () => {
      ElMessageBox.confirm('确定要退出登录吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        localStorage.removeItem('token')
        localStorage.removeItem('userInfo')
        router.push('/login')
        ElMessage.success('退出登录成功')
      }).catch(() => {
        // 取消退出
      })
    }
    
    return {
      userInfo,
      activeMenu,
      sidebarCollapsed,
      toggleSidebar,
      goToProfile,
      logout
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  height: 100%;
  background-color: var(--bg-color);
}

.sidebar {
  background: linear-gradient(135deg, #1A237E, #3949AB);
  transition: all 0.3s;
  overflow-x: hidden;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.2);
  z-index: 10;
  position: relative;
  width: 220px;
}

.sidebar.collapsed {
  width: 64px;
}

.sidebar-menu {
  border-right: none;
}

.logo-container {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.15);
  position: relative;
  overflow: hidden;
}

.logo-container::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #2196F3, #1976D2);
}

.logo-container h3 {
  color: #fff;
  margin: 0;
  font-size: 18px;
  letter-spacing: 1px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.header {
  background-color: #fff;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  position: relative;
  z-index: 9;
}

.collapse-btn {
  font-size: 20px;
  cursor: pointer;
  margin-right: 20px;
  transition: transform 0.3s;
  color: #1A237E;
}

.collapse-btn:hover {
  transform: scale(1.2);
  color: #3949AB;
}

.user-info {
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 0 12px;
  height: 42px;
  border-radius: 21px;
  transition: all 0.3s;
  color: var(--text-regular);
  background-color: #F5F7FA;
}

.user-info:hover {
  background-color: #E8EAF6;
  color: #1A237E;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.left, .right {
  display: flex;
  align-items: center;
}

/* 美化菜单项 */
:deep(.el-menu) {
  background-color: transparent !important;
}

:deep(.el-sub-menu__title),
:deep(.el-menu-item) {
  height: 50px;
  line-height: 50px;
  transition: all 0.3s;
}

:deep(.el-menu-item.is-active) {
  background: rgba(255, 255, 255, 0.15) !important;
  position: relative;
  overflow: hidden;
}

:deep(.el-menu-item.is-active)::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  width: 4px;
  background: #64B5F6;
  box-shadow: 0 0 10px rgba(100, 181, 246, 0.8);
}

:deep(.el-menu-item):hover,
:deep(.el-sub-menu__title):hover {
  background: rgba(255, 255, 255, 0.1) !important;
}

:deep(.el-sub-menu__title) {
  padding-left: 20px !important;
}

:deep(.el-menu-item) {
  padding-left: 20px !important;
}

:deep(.el-menu--collapse) .logo-container h3 {
  display: none;
}

:deep(.el-menu--collapse) .el-sub-menu__title span {
  display: none;
}

:deep(.el-menu--collapse) .el-sub-menu__title .el-sub-menu__icon-arrow {
  display: none;
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    height: 100%;
    transform: translateX(-100%);
  }
  
  .sidebar.collapsed {
    transform: translateX(0);
  }
}
</style> 