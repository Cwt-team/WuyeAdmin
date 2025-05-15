<template>
  <div class="profile-container">
    <el-row :gutter="20">
      <!-- 左侧用户信息卡片 -->
      <el-col :span="8">
        <el-card class="profile-card">
          <div class="user-info">
            <div class="avatar-container">
              <el-avatar :size="100" :src="userInfo.avatar || defaultAvatar"></el-avatar>
              <div class="avatar-upload">
                <el-upload
                  class="avatar-uploader"
                  action="#"
                  :show-file-list="false"
                  :http-request="uploadAvatar"
                >
                  <el-button size="small" type="primary" plain>更换头像</el-button>
                </el-upload>
              </div>
            </div>
            <h2 class="user-name">{{ userInfo.name }}</h2>
            <p class="user-role">{{ userInfo.role === 'admin' ? '管理员' : '普通用户' }}</p>
            <div class="user-stats">
              <div class="stat-item">
                <div class="stat-value">{{ userInfo.loginCount }}</div>
                <div class="stat-label">登录次数</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ userInfo.lastLoginDays }}</div>
                <div class="stat-label">上次登录</div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <!-- 右侧信息编辑表单 -->
      <el-col :span="16">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>个人资料设置</span>
            </div>
          </template>
          
          <el-tabs v-model="activeTab">
            <!-- 基本信息设置 -->
            <el-tab-pane label="基本信息" name="basic">
              <el-form 
                :model="basicForm" 
                :rules="basicRules" 
                ref="basicFormRef" 
                label-width="100px"
                class="profile-form"
              >
                <el-form-item label="姓名" prop="name">
                  <el-input v-model="basicForm.name" placeholder="请输入姓名"></el-input>
                </el-form-item>
                <el-form-item label="手机号码" prop="phone">
                  <el-input v-model="basicForm.phone" placeholder="请输入手机号码"></el-input>
                </el-form-item>
                <el-form-item label="邮箱" prop="email">
                  <el-input v-model="basicForm.email" placeholder="请输入邮箱"></el-input>
                </el-form-item>
                <el-form-item label="角色">
                  <el-input v-model="userInfo.roleName" disabled></el-input>
                </el-form-item>
                <el-form-item label="部门">
                  <el-input v-model="basicForm.department" placeholder="请输入部门"></el-input>
                </el-form-item>
                <el-form-item label="个人简介" prop="introduction">
                  <el-input 
                    v-model="basicForm.introduction" 
                    type="textarea" 
                    placeholder="请输入个人简介"
                    :rows="4"
                  ></el-input>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="saveBasicInfo" :loading="basicLoading">保存信息</el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
            
            <!-- 修改密码 -->
            <el-tab-pane label="修改密码" name="password">
              <el-form 
                :model="passwordForm" 
                :rules="passwordRules" 
                ref="passwordFormRef" 
                label-width="100px"
                class="profile-form"
              >
                <el-form-item label="当前密码" prop="oldPassword">
                  <el-input 
                    v-model="passwordForm.oldPassword" 
                    type="password" 
                    placeholder="请输入当前密码"
                    show-password
                  ></el-input>
                </el-form-item>
                <el-form-item label="新密码" prop="newPassword">
                  <el-input 
                    v-model="passwordForm.newPassword" 
                    type="password" 
                    placeholder="请输入新密码"
                    show-password
                  ></el-input>
                </el-form-item>
                <el-form-item label="确认新密码" prop="confirmPassword">
                  <el-input 
                    v-model="passwordForm.confirmPassword" 
                    type="password" 
                    placeholder="请再次输入新密码"
                    show-password
                  ></el-input>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="changePassword" :loading="passwordLoading">修改密码</el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
            
            <!-- 消息通知设置 -->
            <el-tab-pane label="消息通知" name="notification">
              <el-form 
                :model="notificationForm" 
                ref="notificationFormRef" 
                label-width="100px"
                class="profile-form"
              >
                <el-form-item label="系统消息">
                  <el-switch v-model="notificationForm.system"></el-switch>
                </el-form-item>
                <el-form-item label="报修通知">
                  <el-switch v-model="notificationForm.maintenance"></el-switch>
                </el-form-item>
                <el-form-item label="住户通知">
                  <el-switch v-model="notificationForm.resident"></el-switch>
                </el-form-item>
                <el-form-item label="邮件提醒">
                  <el-switch v-model="notificationForm.email"></el-switch>
                </el-form-item>
                <el-form-item label="短信提醒">
                  <el-switch v-model="notificationForm.sms"></el-switch>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="saveNotificationSettings" :loading="notificationLoading">保存设置</el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
// import axios from 'axios'

export default {
  name: 'UserProfileView',
  setup() {
    // 默认头像
    const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
    
    // 用户信息
    const userInfo = reactive({
      id: '1',
      name: '张管理',
      avatar: '',
      role: 'admin',
      roleName: '系统管理员',
      loginCount: 128,
      lastLoginDays: 1
    })
    
    // 活动标签页
    const activeTab = ref('basic')
    
    // 基本信息表单
    const basicFormRef = ref(null)
    const basicLoading = ref(false)
    const basicForm = reactive({
      name: '张管理',
      phone: '13800138000',
      email: 'admin@example.com',
      department: '物业管理部',
      introduction: '物业管理系统的系统管理员，负责系统的日常维护和用户管理。'
    })
    
    const basicRules = {
      name: [
        { required: true, message: '请输入姓名', trigger: 'blur' },
        { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
      ],
      phone: [
        { required: true, message: '请输入手机号码', trigger: 'blur' },
        { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
      ]
    }
    
    // 密码表单
    const passwordFormRef = ref(null)
    const passwordLoading = ref(false)
    const passwordForm = reactive({
      oldPassword: '',
      newPassword: '',
      confirmPassword: ''
    })
    
    const validateConfirmPassword = (rule, value, callback) => {
      if (value !== passwordForm.newPassword) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }
    
    const passwordRules = {
      oldPassword: [
        { required: true, message: '请输入当前密码', trigger: 'blur' }
      ],
      newPassword: [
        { required: true, message: '请输入新密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
      ],
      confirmPassword: [
        { required: true, message: '请再次输入新密码', trigger: 'blur' },
        { validator: validateConfirmPassword, trigger: 'blur' }
      ]
    }
    
    // 消息通知表单
    const notificationFormRef = ref(null)
    const notificationLoading = ref(false)
    const notificationForm = reactive({
      system: true,
      maintenance: true,
      resident: true,
      email: false,
      sms: true
    })
    
    // 获取用户信息
    const fetchUserInfo = async () => {
      try {
        // 实际应用中应该调用API接口
        // const response = await axios.get('/api/user/profile')
        // Object.assign(userInfo, response.data)
        // Object.assign(basicForm, {
        //   name: response.data.name,
        //   phone: response.data.phone,
        //   email: response.data.email,
        //   department: response.data.department,
        //   introduction: response.data.introduction
        // })
        
        // 模拟数据，不需要实际获取
      } catch (error) {
        console.error('获取用户信息失败:', error)
        ElMessage.error('获取用户信息失败')
      }
    }
    
    // 上传头像
    const uploadAvatar = async (options) => {
      try {
        const file = options.file
        // 实际应用中应该调用API接口上传文件
        // const formData = new FormData()
        // formData.append('avatar', file)
        // const response = await axios.post('/api/user/avatar', formData)
        // userInfo.avatar = response.data.url
        
        // 模拟上传
        setTimeout(() => {
          // 使用 FileReader 读取文件，获取 base64 编码
          const reader = new FileReader()
          reader.readAsDataURL(file)
          reader.onload = () => {
            userInfo.avatar = reader.result
            ElMessage.success('头像上传成功')
          }
        }, 500)
      } catch (error) {
        console.error('上传头像失败:', error)
        ElMessage.error('上传头像失败')
      }
    }
    
    // 保存基本信息
    const saveBasicInfo = async () => {
      if (!basicFormRef.value) return
      
      basicFormRef.value.validate(async (valid) => {
        if (valid) {
          basicLoading.value = true
          try {
            // 实际应用中应该调用API接口
            // await axios.post('/api/user/updateProfile', basicForm)
            
            // 模拟保存
            setTimeout(() => {
              userInfo.name = basicForm.name
              ElMessage.success('个人信息保存成功')
              basicLoading.value = false
            }, 500)
          } catch (error) {
            console.error('保存个人信息失败:', error)
            ElMessage.error('保存个人信息失败')
            basicLoading.value = false
          }
        }
      })
    }
    
    // 修改密码
    const changePassword = async () => {
      if (!passwordFormRef.value) return
      
      passwordFormRef.value.validate(async (valid) => {
        if (valid) {
          passwordLoading.value = true
          try {
            // 实际应用中应该调用API接口
            // await axios.post('/api/user/changePassword', {
            //   oldPassword: passwordForm.oldPassword,
            //   newPassword: passwordForm.newPassword
            // })
            
            // 模拟修改
            setTimeout(() => {
              ElMessage.success('密码修改成功')
              passwordForm.oldPassword = ''
              passwordForm.newPassword = ''
              passwordForm.confirmPassword = ''
              passwordLoading.value = false
            }, 500)
          } catch (error) {
            console.error('修改密码失败:', error)
            ElMessage.error('修改密码失败')
            passwordLoading.value = false
          }
        }
      })
    }
    
    // 保存通知设置
    const saveNotificationSettings = async () => {
      notificationLoading.value = true
      try {
        // 实际应用中应该调用API接口
        // await axios.post('/api/user/updateNotificationSettings', notificationForm)
        
        // 模拟保存
        setTimeout(() => {
          ElMessage.success('通知设置保存成功')
          notificationLoading.value = false
        }, 500)
      } catch (error) {
        console.error('保存通知设置失败:', error)
        ElMessage.error('保存通知设置失败')
        notificationLoading.value = false
      }
    }
    
    // 初始化
    onMounted(() => {
      fetchUserInfo()
    })
    
    return {
      userInfo,
      defaultAvatar,
      activeTab,
      basicFormRef,
      basicForm,
      basicRules,
      basicLoading,
      passwordFormRef,
      passwordForm,
      passwordRules,
      passwordLoading,
      notificationFormRef,
      notificationForm,
      notificationLoading,
      uploadAvatar,
      saveBasicInfo,
      changePassword,
      saveNotificationSettings
    }
  }
}
</script>

<style scoped>
.profile-container {
  padding: 20px;
  animation: fade-in 0.3s;
}

.profile-card, .el-card {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
  height: 100%;
}

.profile-card:hover, .el-card:hover {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
  transform: translateY(-3px);
}

.card-header {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.card-header::before {
  content: '';
  display: inline-block;
  width: 4px;
  height: 18px;
  background: linear-gradient(to bottom, #409EFF, #53a8ff);
  margin-right: 8px;
  border-radius: 2px;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px 0;
  position: relative;
  overflow: hidden;
}

.user-info::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 100px;
  background: linear-gradient(135deg, #409EFF, #53a8ff);
  z-index: 0;
}

.avatar-container {
  position: relative;
  margin-bottom: 20px;
  z-index: 1;
}

.avatar-container .el-avatar {
  border: 4px solid #fff;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
}

.avatar-upload {
  margin-top: 15px;
  text-align: center;
  z-index: 1;
  position: relative;
}

.user-name {
  margin: 10px 0 5px;
  font-size: 20px;
  color: #303133;
  font-weight: 600;
  position: relative;
  z-index: 1;
}

.user-role {
  margin-top: 0;
  color: #606266;
  font-size: 14px;
  position: relative;
  z-index: 1;
}

.user-stats {
  display: flex;
  justify-content: space-around;
  width: 100%;
  margin-top: 20px;
  border-top: 1px solid #eee;
  padding-top: 20px;
  position: relative;
  z-index: 1;
}

.stat-item {
  text-align: center;
  padding: 0 15px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}

.stat-label {
  color: #606266;
  font-size: 14px;
  margin-top: 5px;
}

.profile-form {
  max-width: 500px;
  margin: 0 auto;
}

.el-form-item:last-child {
  margin-bottom: 0;
  margin-top: 30px;
  text-align: center;
}

/* 标签页样式优化 */
:deep(.el-tabs__item) {
  font-size: 15px;
  font-weight: 500;
  transition: all 0.3s;
  padding: 0 20px;
  height: 50px;
  line-height: 50px;
}

:deep(.el-tabs__item.is-active) {
  color: #409EFF;
  font-weight: 600;
}

:deep(.el-tabs__active-bar) {
  height: 3px;
  border-radius: 3px;
  background: linear-gradient(90deg, #409EFF, #53a8ff);
}

/* 表单样式优化 */
:deep(.el-input__inner), :deep(.el-textarea__inner) {
  border-radius: 4px;
  transition: all 0.3s;
}

:deep(.el-input__inner:focus), :deep(.el-textarea__inner:focus) {
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

:deep(.el-button) {
  border-radius: 4px;
  padding: 12px 20px;
  transition: all 0.3s;
}

:deep(.el-button:hover) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

:deep(.el-button--primary) {
  background: linear-gradient(90deg, #409EFF, #53a8ff);
  border: none;
}

:deep(.el-switch__core) {
  border-radius: 12px;
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