<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-left">
        <div class="login-bg"></div>
      </div>
      <div class="login-right">
        <el-card class="login-card" shadow="never">
          <div class="login-header">
            <img :src="logo" alt="Logo" class="logo">
            <h1>智慧社区管理平台</h1>
          </div>
          <div class="login-form">
            <h2>账户密码登录</h2>
            <el-form :model="loginForm" @submit.prevent="login">
              <el-form-item>
                <el-input
                  v-model="loginForm.username"
                  placeholder="请输入用户名"
                  :prefix-icon="User"
                />
              </el-form-item>
              <el-form-item>
                <el-input
                  v-model="loginForm.password"
                  type="password"
                  placeholder="请输入密码"
                  :prefix-icon="Lock"
                  show-password
                />
              </el-form-item>
              <el-form-item class="remember-me">
                <el-checkbox v-model="loginForm.rememberMe">自动登录</el-checkbox>
                <a href="#" class="forget-password">忘记密码?</a>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="login" class="login-button">登录</el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-card>
      </div>
    </div>
    <div class="copyright">
      Copyright © 2024 智慧社区管理平台
    </div>
  </div>
</template>

<script>
import { User, Lock } from '@element-plus/icons-vue'
import axios from 'axios'

export default {
  name: 'LoginForm',
  data() {
    return {
      loginForm: {
        username: '',
        password: '',
        rememberMe: false
      },
      logo: '/logo.png' // 确保public目录下有logo.png
    }
  },
  setup() {
    return {
      User,
      Lock
    }
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('/api/login', {
          username: this.loginForm.username,
          password: this.loginForm.password
        })
        if (response.data.success) {
          localStorage.setItem('isLoggedIn', 'true')
          this.$router.push('/dashboard')
        } else {
          this.$message.error(response.data.message)
        }
      } catch (error) {
        console.error('登录失败:', error)
        this.$message.error('登录失败，请稍后重试')
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  width: 100vw;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7eb 100%);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
}

.login-box {
  display: flex;
  width: 900px;
  height: 500px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.login-left {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.login-bg {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #1890ff 0%, #36cfc9 100%);
  opacity: 0.9;
}

.login-right {
  width: 400px;
  padding: 20px;
}

.login-card {
  border: none;
  box-shadow: none !important;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.logo {
  width: 80px;
  height: auto;
  margin-bottom: 15px;
}

.login-header h1 {
  font-size: 24px;
  color: #333;
  margin: 0;
}

.login-form h2 {
  font-size: 18px;
  color: #666;
  text-align: center;
  margin-bottom: 25px;
}

:deep(.el-input__wrapper) {
  padding: 1px 11px;
}

:deep(.el-input__inner) {
  height: 40px;
}

.remember-me {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 0 0 20px 0;
}

.forget-password {
  color: #409EFF;
  text-decoration: none;
  font-size: 14px;
}

.forget-password:hover {
  color: #66b1ff;
}

.login-button {
  width: 100%;
  height: 40px;
  font-size: 16px;
}

.copyright {
  position: absolute;
  bottom: 20px;
  color: #666;
  font-size: 12px;
}

/* 响应式设计 */
@media screen and (max-width: 992px) {
  .login-box {
    width: 90%;
    height: auto;
    flex-direction: column;
  }

  .login-left {
    display: none;
  }

  .login-right {
    width: 100%;
    padding: 30px;
  }
}
</style>