<template>
  <div class="device-config">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>设备配置: {{ deviceName }}</span>
          <el-button @click="$router.back()">返回</el-button>
        </div>
      </template>
      
      <el-form :model="configForm" label-width="150px" v-loading="loading">
        <el-form-item label="设备编码">
          <el-input v-model="configForm.deviceCode" />
        </el-form-item>
        <el-form-item label="小区编码">
          <el-input v-model="configForm.communityCode" />
        </el-form-item>
        <el-form-item label="设备密码">
          <el-input v-model="configForm.devicePassword" show-password />
        </el-form-item>
        <el-form-item label="心跳包间隔(秒)">
          <el-input-number v-model="configForm.heartbeatInterval" :min="10" :max="300" />
        </el-form-item>
        <el-form-item label="门禁响应时间(秒)">
          <el-input-number v-model="configForm.doorResponseTime" :min="1" :max="30" />
        </el-form-item>
        <el-form-item label="开门延时(秒)">
          <el-input-number v-model="configForm.unlockDelay" :min="1" :max="60" />
        </el-form-item>
        <el-form-item label="通话超时(秒)">
          <el-input-number v-model="configForm.callTimeout" :min="30" :max="300" />
        </el-form-item>
        
        <el-divider content-position="left">高级配置</el-divider>
        
        <el-form-item label="允许远程开锁">
          <el-switch v-model="configForm.allowRemoteUnlock" />
        </el-form-item>
        <el-form-item label="允许人脸识别">
          <el-switch v-model="configForm.allowFaceRecognition" />
        </el-form-item>
        <el-form-item label="允许密码开锁">
          <el-switch v-model="configForm.allowPasswordUnlock" />
        </el-form-item>
        <el-form-item label="允许门禁卡开锁">
          <el-switch v-model="configForm.allowCardUnlock" />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="saveConfig">保存配置</el-button>
          <el-button type="warning" @click="resetConfig">恢复默认</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DeviceConfig',
  data() {
    return {
      loading: false,
      deviceId: null,
      deviceName: '',
      configForm: {
        deviceCode: '',
        communityCode: '',
        devicePassword: '',
        heartbeatInterval: 50,
        doorResponseTime: 5,
        unlockDelay: 5,
        callTimeout: 60,
        allowRemoteUnlock: true,
        allowFaceRecognition: true,
        allowPasswordUnlock: true,
        allowCardUnlock: true
      }
    };
  },
  methods: {
    async fetchDeviceConfig() {
      this.loading = true;
      try {
        const response = await axios.get(`/api/equipment/${this.deviceId}/config`);
        this.deviceName = response.data.equipmentName;
        this.configForm = { ...this.configForm, ...response.data.config };
      } catch (error) {
        console.error('获取设备配置失败:', error);
        this.$message.error('获取设备配置失败');
      } finally {
        this.loading = false;
      }
    },
    async saveConfig() {
      this.loading = true;
      try {
        await axios.put(`/api/equipment/${this.deviceId}/config`, this.configForm);
        this.$message.success('设备配置保存成功');
      } catch (error) {
        console.error('保存设备配置失败:', error);
        this.$message.error('保存设备配置失败');
      } finally {
        this.loading = false;
      }
    },
    async resetConfig() {
      try {
        await this.$confirm('确定要恢复默认配置吗？', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        });
        
        this.loading = true;
        await axios.post(`/api/equipment/${this.deviceId}/reset-config`);
        this.$message.success('设备配置已重置为默认值');
        this.fetchDeviceConfig();
      } catch (error) {
        if (error !== 'cancel') {
          console.error('重置设备配置失败:', error);
          this.$message.error('重置设备配置失败');
        }
      } finally {
        this.loading = false;
      }
    }
  },
  created() {
    this.deviceId = this.$route.params.id;
    this.fetchDeviceConfig();
  }
};
</script>

<style scoped>
.device-config {
  padding: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
