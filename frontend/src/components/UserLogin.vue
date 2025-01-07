<template>
  <div class="login-container">
    <el-card class="login-card">
      <div class="login-header">
        <!-- 使用导入的图片 -->
        <img :src="logo" alt="Logo" class="logo">
        <h1>智慧社区管理平台</h1>
      </div>
      <div class="login-form">
        <h2>账户密码登录</h2>
        <!-- 登录表单 -->
        <el-form :model="loginForm" @submit.prevent="login">
          <el-form-item>
            <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
            >
              <template #prefix>
                <UserIcon />
              </template>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
            >
              <template #prefix>
                <LockIcon />
              </template>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-checkbox v-model="loginForm.rememberMe">自动登录</el-checkbox>
            <a href="#" class="forget-password">忘记密码</a>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="login">登录</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
    <div class="copyright">
      Copyright © 2019 智慧社区管理平台 粤ICP备16012265号-1
    </div>
  </div>
</template>

<script>
import axios from 'axios'; // 引入 Axios 库，用于发送 HTTP 请求
import logoImage from '@/assets/logo.png'; // 使用 ES 模块导入图片
import { User, Lock } from '@element-plus/icons-vue'; // 导入所需的图标组件

export default {
  name: 'LoginForm',
  components: {
    UserIcon: User,
    LockIcon: Lock,
  },
  data() {
    return {
      loginForm: {
        username: '',
        password: '',
        rememberMe: false,
      },
      logo: logoImage, // 将导入的图片赋值给 data
    };
  },
  mounted() {
    console.log('UserLogin component mounted');
  },
  methods: {
    async login() {
      console.log('Login method triggered');
      try {
        const response = await axios.post('/api/login', {
          username: this.loginForm.username,
          password: this.loginForm.password,
        });
        if (response.data.success) {
          console.log('登录成功:', response.data.message);
          localStorage.setItem('isLoggedIn', 'true');
          this.$router.push('/dashboard');
        } else {
          console.log('登录失败:', response.data.message);
          alert(response.data.message);
        }
      } catch (error) {
        console.error('登录请求失败:', error);
        alert('登录请求失败，请稍后再试');
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: #f0f2f5;
  position: relative; /* 新增 */
}

.login-card {
  width: 400px;
  padding: 20px;
}

.login-header {
  text-align: center;
  margin-bottom: 20px;
}

.logo {
  width: 100px;
  height: auto;
}

.login-form h2 {
  text-align: center;
  margin-bottom: 20px;
}

.forget-password {
  float: right;
  font-size: 12px;
}

.copyright {
  position: absolute; /* 新增 */
  bottom: 10px; /* 调整到页面底部，并增加一些空隙 */
  width: 100%; /* 确保它占满整个宽度 */
  text-align: center; /* 居中对齐文本 */
  font-size: 12px; /* 字体大小可以根据需要调整 */
  color: #999; /* 灰色文本 */
}
</style>