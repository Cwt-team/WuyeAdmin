<template>
  <div class="device-detail">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>设备详情: {{ device.equipmentName }}</span>
          <el-button @click="$router.back()">返回</el-button>
        </div>
      </template>
      
      <!-- 设备基本信息 -->
      <el-descriptions title="基本信息" :column="2" border>
        <el-descriptions-item label="设备名称">{{ device.equipmentName }}</el-descriptions-item>
        <el-descriptions-item label="设备状态">
          <el-tag :type="device.status === 'online' ? 'success' : 'danger'">
            {{ device.status === 'online' ? '在线' : '离线' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="设备编码">{{ device.deviceCode }}</el-descriptions-item>
        <el-descriptions-item label="设备SN">{{ device.deviceSn }}</el-descriptions-item>
        <el-descriptions-item label="小区编码">{{ device.communityCode }}</el-descriptions-item>
        <el-descriptions-item label="所属小区">{{ device.communityName }}</el-descriptions-item>
        <el-descriptions-item label="IP地址">{{ device.ip }}</el-descriptions-item>
        <el-descriptions-item label="单元号">{{ device.unitId || '-' }}</el-descriptions-item>
        <el-descriptions-item label="版本号">{{ device.version }}</el-descriptions-item>
        <el-descriptions-item label="MAC地址">{{ device.macAddress || '-' }}</el-descriptions-item>
        <el-descriptions-item label="最后心跳时间">{{ device.lastHeartbeatTime }}</el-descriptions-item>
        <el-descriptions-item label="人脸下载时间">{{ device.faceDownloadTime }}</el-descriptions-item>
      </el-descriptions>
      
      <!-- 操作按钮 -->
      <div class="operation-buttons">
        <el-button type="primary" @click="sendHeartbeat">发送心跳包</el-button>
        <el-button type="success" @click="downloadFace">下载人脸数据</el-button>
        <el-button type="warning" @click="remoteUnlock">远程开锁</el-button>
        <el-button type="danger" @click="resetDevice">重置设备</el-button>
        <el-button type="info" @click="goToConfig">配置管理</el-button>
      </div>
      
      <!-- 心跳记录选项卡 -->
      <el-tabs type="border-card" style="margin-top: 20px;">
        <el-tab-pane label="心跳记录">
          <el-table :data="heartbeatRecords" style="width: 100%">
            <el-table-column prop="heartbeatTime" label="心跳时间" />
            <el-table-column prop="deviceStatus" label="设备状态">
              <template #default="scope">
                <el-tag :type="scope.row.deviceStatus ? 'success' : 'danger'">
                  {{ scope.row.deviceStatus ? '在线' : '离线' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="softwareVersion" label="软件版本" />
          </el-table>
        </el-tab-pane>
        
        <el-tab-pane label="开锁记录">
          <el-table :data="unlockRecords" style="width: 100%">
            <el-table-column prop="unlockingTime" label="开锁时间" />
            <el-table-column prop="unlockingTypeText" label="开锁类型" />
            <el-table-column prop="phone" label="手机号" />
            <el-table-column prop="roomNumber" label="房间号" />
            <el-table-column label="开锁照片">
              <template #default="scope">
                <el-image 
                  v-if="scope.row.photoUrl" 
                  :src="scope.row.photoUrl" 
                  :preview-src-list="[scope.row.photoUrl]"
                  style="width: 50px; height: 50px;"
                />
                <span v-else>无照片</span>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        
        <el-tab-pane label="设备日志">
          <el-table :data="deviceLogs" style="width: 100%">
            <el-table-column prop="createdAt" label="日志时间" />
            <el-table-column prop="logType" label="日志类型" />
            <el-table-column prop="logContent" label="日志内容" />
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>
    
    <!-- 远程开锁对话框 -->
    <el-dialog title="远程开锁" v-model="unlockDialogVisible" width="30%">
      <el-form :model="unlockForm" label-width="100px">
        <el-form-item label="单元号">
          <el-input v-model="unlockForm.unitId" placeholder="请输入4位单元号" />
        </el-form-item>
        <el-form-item label="房间号">
          <el-input v-model="unlockForm.roomNumber" placeholder="请输入4位房间号" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="unlockForm.phone" placeholder="可选，无则留空" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="unlockDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmUnlock">确认开锁</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DeviceDetail',
  data() {
    return {
      device: {
        id: null,
        equipmentName: '',
        deviceCode: '',
        deviceSn: '',
        communityCode: '',
        communityName: '',
        ip: '',
        unitId: '',
        status: '',
        version: '',
        macAddress: '',
        lastHeartbeatTime: '',
        faceDownloadTime: ''
      },
      heartbeatRecords: [],
      unlockRecords: [],
      deviceLogs: [],
      unlockDialogVisible: false,
      unlockForm: {
        unitId: '',
        roomNumber: '',
        phone: ''
      }
    };
  },
  methods: {
    async fetchDeviceDetail() {
      try {
        const response = await axios.get(`/api/equipment/${this.$route.params.id}`);
        this.device = response.data;
      } catch (error) {
        console.error('获取设备详情失败:', error);
        this.$message.error('获取设备详情失败');
      }
    },
    async fetchHeartbeatRecords() {
      try {
        const response = await axios.get(`/api/equipment/${this.$route.params.id}/heartbeats`);
        this.heartbeatRecords = response.data.records;
      } catch (error) {
        console.error('获取心跳记录失败:', error);
        this.$message.error('获取心跳记录失败');
      }
    },
    async fetchUnlockRecords() {
      try {
        const response = await axios.get(`/api/equipment/${this.$route.params.id}/unlock-records`);
        this.unlockRecords = response.data.records.map(item => {
          // 将开锁类型代码转换为可读文本
          const unlockTypeMap = {
            '0': '二维码',
            '1': '小程序远程开锁',
            '2': '门禁卡',
            '3': '一次性密码',
            '4': '人脸',
            '5': '分机开锁',
            '6': '物业中心开锁',
            '7': '指纹开锁',
            '8': '公共密码开锁',
            '14': '手机电话开锁'
          };
          return {
            ...item,
            unlockingTypeText: unlockTypeMap[item.unlockingType] || item.unlockingType
          };
        });
      } catch (error) {
        console.error('获取开锁记录失败:', error);
        this.$message.error('获取开锁记录失败');
      }
    },
    async fetchDeviceLogs() {
      try {
        const response = await axios.get(`/api/equipment/${this.$route.params.id}/logs`);
        this.deviceLogs = response.data.logs;
      } catch (error) {
        console.error('获取设备日志失败:', error);
        this.$message.error('获取设备日志失败');
      }
    },
    async sendHeartbeat() {
      try {
        await axios.post(`/api/equipment/${this.$route.params.id}/heartbeat`);
        this.$message.success('心跳包发送成功');
        // 刷新心跳记录
        setTimeout(() => {
          this.fetchHeartbeatRecords();
          this.fetchDeviceDetail();
        }, 3000);
      } catch (error) {
        console.error('发送心跳包失败:', error);
        this.$message.error('发送心跳包失败');
      }
    },
    async downloadFace() {
      try {
        await axios.post(`/api/equipment/${this.$route.params.id}/download-face`);
        this.$message.success('人脸数据下载命令已发送');
        // 刷新设备信息
        setTimeout(() => {
          this.fetchDeviceDetail();
        }, 2000);
      } catch (error) {
        console.error('下载人脸数据失败:', error);
        this.$message.error('下载人脸数据失败');
      }
    },
    remoteUnlock() {
      this.unlockDialogVisible = true;
    },
    async confirmUnlock() {
      try {
        await axios.post(`/api/equipment/${this.$route.params.id}/remote-unlock`, this.unlockForm);
        this.$message.success('开锁命令已发送');
        this.unlockDialogVisible = false;
        // 刷新开锁记录
        setTimeout(() => {
          this.fetchUnlockRecords();
        }, 2000);
      } catch (error) {
        console.error('远程开锁失败:', error);
        this.$message.error('远程开锁失败');
      }
    },
    async resetDevice() {
      try {
        await this.$confirm('确定要重置设备吗？这将恢复设备的默认设置。', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        });
        await axios.post(`/api/equipment/${this.$route.params.id}/reset`);
        this.$message.success('设备重置命令已发送');
      } catch (error) {
        if (error !== 'cancel') {
          console.error('重置设备失败:', error);
          this.$message.error('重置设备失败');
        }
      }
    },
    goToConfig() {
      this.$router.push({
        name: 'DeviceConfig',
        params: { id: this.$route.params.id }
      });
    }
  },
  mounted() {
    this.fetchDeviceDetail();
    this.fetchHeartbeatRecords();
    this.fetchUnlockRecords();
    this.fetchDeviceLogs();
  }
};
</script>

<style scoped>
.device-detail {
  padding: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.operation-buttons {
  margin: 20px 0;
  display: flex;
  gap: 10px;
}
</style>
