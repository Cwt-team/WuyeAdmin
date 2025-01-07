<template>
  <div class="personal-info">
    <el-card>
      <el-form :model="personalInfo" label-width="120px">
        <el-form-item label="姓名">
          <el-input v-model="personalInfo.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="联系方式">
          <el-input v-model="personalInfo.contact" placeholder="请输入联系方式" />
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="personalInfo.address" placeholder="请输入地址" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="savePersonalInfo">保存</el-button>
        </el-form-item>
      </el-form>
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
        name: '',
        contact: '',
        address: '',
      },
    };
  },
  methods: {
    async fetchPersonalInfo() {
      try {
        const response = await axios.get('/api/personal-info');
        this.personalInfo = response.data;
      } catch (error) {
        console.error('获取个人资料失败:', error);
      }
    },
    async savePersonalInfo() {
      try {
        await axios.post('/api/personal-info', this.personalInfo);
        this.$message.success('个人资料保存成功');
      } catch (error) {
        console.error('保存个人资料失败:', error);
        this.$message.error('保存个人资料失败');
      }
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
</style>
