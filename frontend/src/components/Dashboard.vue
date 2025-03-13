<template>
  <div class="dashboard">
    <header>
      <div class="header-left">
        <h1>智慧社区管理平台</h1>
      </div>
      <div class="header-right">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item v-for="(item, index) in breadcrumb" :key="index">
            {{ item }}
          </el-breadcrumb-item>
        </el-breadcrumb>
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
import { ArrowDown, Setting, SwitchButton } from '@element-plus/icons-vue';

export default {
  name: 'DashboardView',
  components: {
    ElMenu,
    ElSubMenu,
    ElMenuItem,
    ElButton,
    ArrowDown,
    Setting,
    SwitchButton,
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
          name: '区域维护管理',
          icon: 'el-icon-s-management',
          children: [
            { id: 1, name: '报事报修', component: 'AreaMaintenance', params: { tab: 'maintenance' } },
            { id: 2, name: '社区评价', component: 'AreaMaintenance', params: { tab: 'reviews' } },
            { id: 3, name: '投诉建议', component: 'AreaMaintenance', params: { tab: 'complaints' } }
          ]
        },
        {
          id: 9,
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
        const selectedChild = selectedItem.children.find(child => child.id === childId);
        if (selectedChild) {
          console.log('加载组件:', selectedChild.component);
          
          // 处理 AreaMaintenance 组件的特殊情况
          if (selectedChild.component === 'AreaMaintenance' && selectedChild.params) {
            // 动态导入组件
            const componentModule = await import(`@/views/${selectedChild.component}.vue`);
            const component = componentModule.default;
            
            // 创建带有参数的组件
            this.currentComponent = {
              render: h => h(component, { props: selectedChild.params })
            };
          } else {
            // 普通组件加载
            this.currentComponent = () => import(`@/components/${selectedChild.component}.vue`);
          }
          
          // 更新面包屑
          this.breadcrumb = [
            { name: selectedItem.name, path: '#' },
            { name: selectedChild.name, path: '#' }
          ];
        }
      } else if (selectedItem) {
        console.log('加载父级组件:', selectedItem.component);
        this.currentComponent = () => import(`@/components/${selectedItem.component}.vue`);
        
        // 更新面包屑
        this.breadcrumb = [
          { name: selectedItem.name, path: '#' }
        ];
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
  justify-content: space-between; /* 将左右两部分分开 */
  align-items: center;
  /* background: #1890ff;  */ /* 移除纯色背景 */
  background: linear-gradient(135deg, #86d0ff 0%, #33a3dc 100%); /* 柔和的渐变 */
  color: white;
  padding: 10px 20px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px; /* 调整元素之间的间距 */
}

.header-left h1 {
  font-size: 20px;
  font-weight: bold;
  margin-right: 20px; /* 调整标题与面包屑的间距 */
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
  background-color: #f0f5ff; /* 浅蓝色背景 */
  color: #003a8c; /* 深蓝色文字，作为默认颜色 */
  height: 100vh;
  overflow: auto;
}

.el-menu-vertical-demo {
  border-right: none;
  background: transparent; /* 让菜单背景透明，显示 sidebar 的背景色 */
}

.el-menu-item, .el-sub-menu__title {
  color: #003a8c !important; /* 深蓝色文字 */
  transition: all 0.3s ease;
}

.el-menu-item {
  border-bottom: 1px solid rgba(0, 58, 140, 0.1); /* 深蓝色的分割线，稍微透明 */
}

.el-menu-item i {
  margin-right: 12px;
}

.el-menu-item:focus,
.el-menu-item:active,
.el-menu-item.is-active {
  background-color: #bae7ff !important; /* 更浅的蓝色作为选中背景 */
  color: #003a8c !important; /* 选中时保持深蓝色文字 */
}

.el-menu-item:hover {
  background-color: #e6f7ff !important; /* 更浅的蓝色作为悬停背景 */
}

.el-sub-menu__title:hover {
  background-color: #e6f7ff !important; /* 子菜单标题悬停背景 */
}

.el-sub-menu .el-menu-item {
  padding-left: 50px !important;
  background-color: transparent; /* 子菜单背景透明 */
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
  background: linear-gradient(135deg, #86d0ff 0%, #33a3dc 100%); /* 与 header 相同的渐变 */
  color: white;
  position: relative; /* 保证在页脚固定底部 */
}
</style>
