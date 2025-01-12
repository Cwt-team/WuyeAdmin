<template>
  <div class="account-settings">
    <el-card>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>个人信息中心</el-breadcrumb-item>
        <el-breadcrumb-item>账号设置</el-breadcrumb-item>
      </el-breadcrumb>

      <el-form :model="accountForm" label-width="120px">
        <el-form-item label="账号归属组织">
          <el-input v-model="accountForm.organization" disabled />
        </el-form-item>
        <el-form-item label="用户名">
          <el-input v-model="accountForm.username" disabled />
        </el-form-item>
        <el-form-item label="绑定安全手机">
          <el-input v-model="accountForm.phone" disabled>
            <template #append>
              <el-button @click="replacePhone">替换手机</el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="绑定安全邮箱">
          <el-input v-model="accountForm.email" disabled>
            <template #append>
              <el-button @click="replaceEmail">替换邮箱</el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-button @click="openChangePasswordDialog">修改密码</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-dialog title="修改密码" v-model="changePasswordDialogVisible" width="30%">
      <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="100px">
        <el-form-item label="新密码" prop="newPassword">
          <el-input type="password" v-model="passwordForm.newPassword" autocomplete="off"/>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input type="password" v-model="passwordForm.confirmPassword" autocomplete="off"/>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="changePasswordDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitChangePassword">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AccountSettings',
  data() {
    return {
      accountForm: {
        organization: '',
        username: '',
        phone: '',
        email: '',
      },
      changePasswordDialogVisible: false,
      passwordForm: {
        newPassword: '',
        confirmPassword: '',
      },
      passwordRules: {
        newPassword: [
          {required: true, message: '请输入新密码', trigger: 'blur'},
          {min: 6, message: '密码长度至少为 6 个字符', trigger: 'blur'},
        ],
        confirmPassword: [
          {required: true, message: '请确认密码', trigger: 'blur'},
          {
            validator: (rule, value, callback) => {
              if (value !== this.passwordForm.newPassword) {
                callback(new Error('两次输入的密码不一致'));
              } else {
                callback();
              }
            },
            trigger: 'blur',
          },
        ],
      },
      passwordFormRef: null,
    };
  },
  methods: {
    async fetchAccountSettings() {
      try {
        const response = await axios.get('/api/account-settings');
        if (response.status === 200) {
          this.accountForm = response.data;
        } else {
          this.$message.error('获取账号设置信息失败');
        }
      } catch (error) {
        console.error('获取账号设置信息失败:', error);
        this.$message.error('获取账号设置信息失败');
      }
    },
    openChangePasswordDialog() {
      this.changePasswordDialogVisible = true;
    },
    replacePhone() {
      console.log('替换手机');
      // TODO: 实现替换手机的逻辑
    },
    replaceEmail() {
      console.log('替换邮箱');
      // TODO: 实现替换邮箱的逻辑
    },
    submitChangePassword() {
      this.passwordFormRef.validate(async (valid) => {
        if (valid) {
          try {
            await axios.post('/api/change-password', {newPassword: this.passwordForm.newPassword});
            this.$message.success('密码修改成功，请重新登录');
            this.changePasswordDialogVisible = false;
            // TODO: 跳转到登录页面或执行其他登出操作
          } catch (error) {
            console.error('修改密码失败:', error);
            this.$message.error('修改密码失败');
          }
        } else {
          return false;
        }
      });
    },
  },
  mounted() {
    this.fetchAccountSettings();
  },
};
</script>

<style scoped>
.account-settings {
  padding: 20px;
}
</style>
