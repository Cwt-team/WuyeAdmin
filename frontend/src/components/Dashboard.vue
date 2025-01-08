<template>
  <div class="dashboard">
    <header>
      <div class="header-left">
        <h1>智慧社区管理平台</h1>
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item v-for="(item, index) in breadcrumb" :key="index">
            {{ item }}
          </el-breadcrumb-item>
        </el-breadcrumb>
      </div>
      <div class="header-right">
        <el-dropdown>
          <div class="user-info">
            <el-avatar :size="36" :src="userAvatar" />
            <span class="username">{{ username }}</span>
            <el-icon><arrow-down /></el-icon>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="goToSettings">
                <el-icon><setting /></el-icon>
                个人设置
              </el-dropdown-item>
              <el-dropdown-item divided @click="logout">
                <el-icon><switch-button /></el-icon>
                退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </header>
    <div class="content-wrapper">
      <nav class="sidebar">
        <el-menu :default-active="activeMenu" class="el-menu-vertical-demo" @select="selectMenuItem">
          <el-sub-menu v-for="item in menuItemsWithChildren" :key="item.id" :index="item.id.toString()">
            <template #title>
              <i :class="item.icon"></i>
              <span>{{ item.name }}</span>
            </template>
            <el-menu-item v-for="child in item.children" :key="child.id" :index="`${item.id}-${child.id}`">
              {{ child.name }}
            </el-menu-item>
          </el-sub-menu>
          <el-menu-item v-for="item in menuItemsWithoutChildren" :key="item.id" :index="item.id.toString()">
            <i :class="item.icon"></i>
            <span>{{ item.name }}</span>
          </el-menu-item>
        </el-menu>
      </nav>
      <main>
        <component v-if="currentComponent" :is="currentComponent"></component>
      </main>
    </div>
    <footer>
      <p>&copy; 2023 智慧社区管理平台 粤ICP备16012265号-1</p>
    </footer>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMenu, ElSubMenu, ElMenuItem, ElButton } from 'element-plus';

export default {
  name: 'DashboardView',
  components: {
    ElMenu,
    ElSubMenu,
    ElMenuItem,
    ElButton,
  },
  data() {
    return {
      username: 'admin', // 示例用户名
      userAvatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
      breadcrumb: [],
      menuItems: [
        {
          id: 1,
          name: '小区信息管理',
          icon: 'el-icon-s-home',
          children: [
            { id: 1, name: '小区信息列表', component: 'CommunityInfoList' },
            { id: 2, name: '房屋信息列表', component: 'HouseInfoList' },
            { id: 3, name: '管理员角色列表', component: 'AdminRoleList' },
            { id: 4, name: '小区管理员列表', component: 'CommunityAdminList' },
          ],
        },
        {
          id: 2,
          name: '物业人员管理',
          icon: 'el-icon-user-solid',
          children: [
            { id: 1, name: '物业管理员列表', component: 'PropertyAdminList' },
          ],
        },
        {
          id: 3,
          name: '业主信息管理',
          icon: 'el-icon-user',
          children: [
            { id: 1, name: '业主信息列表', component: 'OwnerInfoList' },
            { id: 2, name: '业主申请列表', component: 'OwnerApplyList' },
          ],
        },
        {
          id: 4,
          name: '门禁信息管理',
          icon: 'el-icon-lock',
          children: [
            { id: 1, name: '设备列表', component: 'EquipmentList' },
            { id: 2, name: '门禁卡列表', component: 'AccessCardList' },
          ],
        },
        {
          id: 5,
          name: '公告信息管理',
          icon: 'el-icon-bell',
          children: [
            { id: 1, name: '房间通知', component: 'RoomNotification' },
            { id: 2, name: '小区通知', component: 'CommunityNotice' },
          ],
        },
        {
          id: 6,
          name: '内容信息管理',
          icon: 'el-icon-document',
          children: [
            { id: 1, name: '图片广告', component: 'PictureAdvertisement' },
          ],
        },
        {
          id: 7,
          name: '记录信息管理',
          icon: 'el-icon-document-copy',
          children: [
            { id: 1, name: '呼叫记录', component: 'CallRecord' },
            { id: 2, name: '报警记录', component: 'AlarmRecord' },
            { id: 3, name: '开锁记录', component: 'UnlockRecord' }
          ]
        },
        {
          id: 8,
          name: '个人信息中心',
          icon: 'el-icon-user',
          children: [
            { id: 1, name: '账号设置', component: 'AccountSettings' },
            { id: 2, name: '个人资料', component: 'PersonalInfo' },
          ],
        },
      ],
      currentComponent: null,
      activeMenu: '1-1',
    };
  },
  computed: {
    menuItemsWithChildren() {
      return this.menuItems.filter(item => item.children && item.children.length);
    },
    menuItemsWithoutChildren() {
      return this.menuItems.filter(item => !item.children || !item.children.length);
    },
  },
  methods: {
    async selectMenuItem(index) {
      console.log('选中菜单项:', index);

      const [parentId, childId] = index.split('-').map(Number);
      const selectedItem = this.menuItems.find(item => item.id === parentId);

      if (selectedItem && selectedItem.children) {
        const selectedSubItem = selectedItem.children.find(child => child.id === childId);
        if (selectedSubItem) {
          try {
            const module = await import(`@/components/${selectedSubItem.component}.vue`);
            this.currentComponent = module.default;
          } catch (error) {
            console.error('加载组件失败:', error);
            this.currentComponent = null;
          }
        }
      } else if (selectedItem) {
        // 如果没有子菜单，只加载父菜单的组件
        try {
          const module = await import(`@/components/${selectedItem.component}.vue`);
          this.currentComponent = module.default;
        } catch (error) {
          console.error('加载组件失败:', error);
          this.currentComponent = null;
        }
      }
    },
    async fetchUserInfo() {
      try {
        const response = await axios.get('/api/user-info');
        if (response.data.username) {
          this.username = response.data.username;
        } else {
          this.$router.push('/login');
        }
      } catch (error) {
        console.error('获取用户信息失败:', error);
        this.$router.push('/login');
      }
    },
    async logout() {
      try {
        await axios.post('/api/logout');
        localStorage.removeItem('isLoggedIn');
        this.$router.push('/login');
      } catch (error) {
        console.error('退出登录失败:', error);
      }
    },
    goToSettings() {
      this.$router.push('/settings');
    },
    updateBreadcrumb() {
      const matched = this.$route.matched;
      this.breadcrumb = matched.map(item => item.meta?.title || item.name);
    },
  },
  mounted() {
    this.fetchUserInfo();
    this.updateBreadcrumb();
    this.$watch(
      () => this.$route,
      () => {
        this.updateBreadcrumb();
      }
    );
  },
};
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #409EFF; /* 顶部背景颜色 */
  color: white;
  padding: 10px 20px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.username {
  font-weight: 500;
}

.el-breadcrumb {
  font-size: 14px;
}

.el-breadcrumb__item:last-child {
  color: #ffffff;
}

.el-breadcrumb__item:not(:last-child) {
  color: rgba(255, 255, 255, 0.7);
}

.el-breadcrumb__item:not(:last-child):hover {
  color: #ffffff;
  text-decoration: underline;
}

.content-wrapper {
  display: flex;
  flex: 1;
}

.sidebar {
  width: 200px;
  background: #001529;
  color: #ffffff;
  height: 100vh;
  overflow: auto;
}

.el-menu-vertical-demo {
  border-right: none;
}

.el-menu-item, .el-sub-menu__title {
  color: #000000 !important;
  transition: all 0.3s ease;
}

.el-menu-item {
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.el-menu-item i {
  margin-right: 12px;
}

.el-menu-item:focus,
.el-menu-item:active,
.el-menu-item.is-active {
  background-color: #1677ff !important;
  color: #fff !important;
}

.el-menu-item:hover {
  background-color: rgba(255, 255, 255, 0.05) !important;
}

.el-sub-menu__title:hover {
  background-color: rgba(255, 255, 255, 0.05) !important;
}

.el-sub-menu .el-menu-item {
  padding-left: 50px !important;
}

main {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background: #f0f2f5; /* 主内容区域背景色 */
}

footer {
  text-align: center;
  padding: 10px;
  background: #409EFF; /* 页脚背景颜色 */
  color: white;
  position: relative; /* 保证在页脚固定底部 */
}
</style>
