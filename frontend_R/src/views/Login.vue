<template>
  <div class="login-container">
    <div class="login-box">
      <h2>物业管理系统</h2>
      <el-form :model="loginForm" :rules="loginRules" ref="loginFormRef">
        <el-form-item prop="username">
          <el-input v-model="loginForm.username" placeholder="用户名" prefix-icon="el-icon-user"></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="loginForm.password" placeholder="密码" type="password" prefix-icon="el-icon-lock"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleLogin" style="width: 100%">登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const loginFormRef = ref(null)
    const loading = ref(false)

    const loginForm = reactive({
      username: '',
      password: ''
    })

    const loginRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' }
      ]
    }

    const handleLogin = () => {
      if (loginFormRef.value) {
        loginFormRef.value.validate(async (valid) => {
          if (valid) {
            loading.value = true
            try {
              // 实际应用中，这里应该调用后端接口进行身份验证
              const response = await axios.post('/api/login', {
                username: loginForm.username,
                password: loginForm.password
              })
              
              if (response.data.success === true) {
                // 存储用户信息，如果后端没返回这些字段，创建一些基本信息
                localStorage.setItem('token', response.data.token || 'demo-token')
                localStorage.setItem('userInfo', JSON.stringify({
                  username: loginForm.username,
                  ...response.data.user
                }))
                ElMessage.success(response.data.message || '登录成功')
                router.push('/dashboard')
              } else {
                ElMessage.error(response.data.message || '登录失败')
              }
            } catch (error) {
              console.error('登录出错：', error)
              ElMessage.error('登录失败，请检查网络连接或联系管理员')
            } finally {
              loading.value = false
            }
          }
        })
      }
    }

    return {
      loginFormRef,
      loginForm,
      loginRules,
      loading,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f7fa;
}

.login-box {
  width: 400px;
  padding: 30px;
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #409EFF;
}
</style> 