<template>
  <div class="personal-info">
    <el-card>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>个人信息中心</el-breadcrumb-item>
        <el-breadcrumb-item>个人资料</el-breadcrumb-item>
      </el-breadcrumb>

      <div class="info-header">
        <el-avatar size="large" :src="avatarUrl">
          <img v-if="!avatarUrl" src="https://cube.elemecdn.com/e/fd/0fc7d20532fdaf7695ce8d3101915png.png" />
        </el-avatar>
        <el-button type="text" @click="changeAvatar">更换头像</el-button>
      </div>

      <el-descriptions class="margin-top" :column="3" border>
        <el-descriptions-item label="ID">{{ personalInfo.id }}</el-descriptions-item>
        <el-descriptions-item label="账号">{{ personalInfo.account }}</el-descriptions-item>
        <el-descriptions-item label="组织名称">{{ personalInfo.organization }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ personalInfo.email }}</el-descriptions-item>
      </el-descriptions>

      <el-card class="edit-card" shadow="never">
        <el-form :model="editableInfo" label-width="120px">
          <el-form-item label="姓名">
            <el-input v-model="editableInfo.name" placeholder="请输入姓名" />
          </el-form-item>
          <el-form-item label="联系电话">
            <el-input v-model="editableInfo.contact" placeholder="请输入联系电话" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="savePersonalInfo">保存</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'PersonalInfo',
  data() {
    return {
      personalInfo: {
        id: '',
        account: '',
        name: '',
        contact: '',
        organization: '',
        email: '',
      },
      editableInfo: {
        name: '',
        contact: '',
      },
      avatarUrl: '', // 假设头像地址
    };
  },
  methods: {
    async fetchPersonalInfo() {
      try {
        const response = await axios.get('/api/personal-info');
        if (response.status === 200) {
          this.personalInfo = response.data;
          // 初始化可编辑信息
          this.editableInfo.name = response.data.name;
          this.editableInfo.contact = response.data.contact;
        } else {
          this.$message.error('获取个人资料失败');
        }
      } catch (error) {
        console.error('获取个人资料失败:', error);
        this.$message.error('获取个人资料失败');
      }
    },
    async savePersonalInfo() {
      try {
        await axios.post('/api/personal-info', this.editableInfo); // 只保存可编辑的信息
        this.$message.success('个人资料保存成功');
        // 重新获取最新的个人信息以保持数据同步
        this.fetchPersonalInfo();
      } catch (error) {
        console.error('保存个人资料失败:', error);
        this.$message.error('个人资料保存失败');
      }
    },
    changeAvatar() {
      console.log('更换头像');
      // TODO: 实现更换头像的逻辑，例如打开上传图片的对话框
    },
  },
  mounted() {
    this.fetchPersonalInfo();
  },
};
</script>

<style scoped>
.personal-info {
  padding: 20px;
}
.info-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}
.info-header .el-avatar {
  margin-right: 10px;
}
.edit-card {
  margin-top: 20px;
}
</style>
