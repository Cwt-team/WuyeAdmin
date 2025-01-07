<template>
  <div class="account-settings">
    <el-card>
      <el-form :model="accountForm" label-width="120px">
        <el-form-item label="用户名">
          <el-input v-model="accountForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="accountForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="accountForm.password" placeholder="请输入密码" type="password" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="saveAccountSettings">保存</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AccountSettings',
  data() {
    return {
      accountForm: {
        username: '',
        email: '',
        password: '',
      },
    };
  },
  methods: {
    async fetchAccountSettings() {
      try {
        const response = await axios.get('/api/account-settings');
        this.accountForm = response.data;
      } catch (error) {
        console.error('获取账号设置信息失败:', error);
      }
    },
    async saveAccountSettings() {
      try {
        await axios.post('/api/account-settings', this.accountForm);
        this.$message.success('账号设置信息保存成功');
      } catch (error) {
        console.error('保存账号设置信息失败:', error);
        this.$message.error('保存账号设置信息失败');
      }
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
