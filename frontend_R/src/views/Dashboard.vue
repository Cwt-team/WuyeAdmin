<template>
  <div class="dashboard-container">
    <el-container style="height: 100vh;">
      <!-- 侧边栏 -->
      <el-aside width="220px" class="sidebar">
        <div class="logo-container">
          <h3>物业管理系统</h3>
        </div>
        <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          :router="true"
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF">
          
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
              <fold />
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
import { Menu as IconMenu, Location, Setting, Fold, ArrowDown, User } from '@element-plus/icons-vue'
import Breadcrumb from '../components/layout/Breadcrumb.vue'

export default {
  name: 'DashboardView',
  components: {
    IconMenu,
    Location,
    Setting,
    Fold,
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
  background-color: #f5f7fa;
}

.sidebar {
  background: linear-gradient(to bottom, #304156, #1f2d3d);
  transition: all 0.3s;
  overflow-x: hidden;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
}

.sidebar-menu {
  border-right: none;
}

.logo-container {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(43, 54, 73, 0.8);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.12);
}

.logo-container h3 {
  color: #fff;
  margin: 0;
  font-size: 18px;
  letter-spacing: 1px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.header {
  background-color: #fff;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.collapse-btn {
  font-size: 20px;
  cursor: pointer;
  margin-right: 20px;
  transition: transform 0.3s;
}

.collapse-btn:hover {
  transform: rotate(90deg);
  color: #409EFF;
}

.user-info {
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 0 10px;
  height: 40px;
  border-radius: 20px;
  transition: all 0.3s;
  color: #606266;
}

.user-info:hover {
  background-color: #f5f7fa;
  color: #409EFF;
}

.left, .right {
  display: flex;
  align-items: center;
}

/* 添加全局转场动画 */
.el-main {
  padding: 20px;
}

.el-main > div {
  animation: fade-in 0.3s ease-in-out;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style> 