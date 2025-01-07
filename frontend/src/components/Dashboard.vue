<template>
  <div class="dashboard">
    <header>
      <h1>智慧社区管理平台</h1>
      <div class="user-info">
        <span>{{ username }}</span>
        <el-button type="text" @click="logout">退出</el-button>
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
      <p>&copy; 2019 智慧社区管理平台 粤ICP备16012265号-1</p>
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
  },
  mounted() {
    this.fetchUserInfo();
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
}

.user-info {
  display: flex;
  align-items: center;
}

.content-wrapper {
  display: flex;
  flex: 1;
}

.sidebar {
  width: 200px; /* 调整侧边栏宽度 */
  background: #001529; /* 深蓝色背景 */
  color: #ffffff; /* 侧边栏文字颜色 */
  height: 100vh;
  overflow: auto;
}

.el-menu-vertical-demo {
  border-right: none;
}

.el-menu-item, .el-sub-menu__title {
  color: #ffffff !important; /* 确保侧边栏菜单项文字为白色 */
}

.el-menu-item:focus,
.el-menu-item:active,
.el-menu-item.is-active {
  background-color: #409EFF !important; /* 活动项背景颜色 */
}

.el-sub-menu__title:hover {
  background-color: #2d3a4b !important; /* 悬停时背景颜色 */
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

