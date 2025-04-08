<template>
  <div class="device-heartbeats">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>设备心跳记录</span>
          <div>
            <el-select v-model="filter.deviceId" placeholder="选择设备" filterable>
              <el-option
                v-for="item in deviceOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
            <el-button type="primary" @click="fetchHeartbeats" style="margin-left: 10px;">查询</el-button>
          </div>
        </div>
      </template>
      
      <el-table :data="heartbeats" style="width: 100%" v-loading="loading" border>
        <el-table-column prop="deviceName" label="设备名称" />
        <el-table-column prop="deviceCode" label="设备编码" />
        <el-table-column prop="heartbeatTime" label="心跳时间" />
        <el-table-column prop="deviceStatus" label="设备状态">
          <template #default="scope">
            <el-tag :type="scope.row.deviceStatus ? 'success' : 'danger'">
              {{ scope.row.deviceStatus ? '在线' : '离线' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="softwareVersion" label="软件版本" />
        <el-table-column prop="communityName" label="所属小区" />
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          background
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          :page-size="pageSize"
          :current-page="currentPage"
          :page-sizes="[10, 20, 50, 100]"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DeviceHeartbeats',
  data() {
    return {
      filter: {
        deviceId: ''
      },
      deviceOptions: [],
      heartbeats: [],
      loading: false,
      total: 0,
      currentPage: 1,
      pageSize: 10
    };
  },
  methods: {
    async fetchDevices() {
      try {
        const response = await axios.get('/api/equipment/list');
        this.deviceOptions = response.data.map(device => ({
          value: device.id,
          label: device.equipmentName
        }));
      } catch (error) {
        console.error('获取设备列表失败:', error);
        this.$message.error('获取设备列表失败');
      }
    },
    async fetchHeartbeats() {
      this.loading = true;
      try {
        const params = {
          page: this.currentPage,
          size: this.pageSize
        };
        
        if (this.filter.deviceId) {
          params.deviceId = this.filter.deviceId;
        }
        
        const response = await axios.get('/api/equipment/heartbeats', { params });
        this.heartbeats = response.data.records;
        this.total = response.data.total;
      } catch (error) {
        console.error('获取心跳记录失败:', error);
        this.$message.error('获取心跳记录失败');
      } finally {
        this.loading = false;
      }
    },
    handleSizeChange(size) {
      this.pageSize = size;
      this.currentPage = 1;
      this.fetchHeartbeats();
    },
    handleCurrentChange(page) {
      this.currentPage = page;
      this.fetchHeartbeats();
    }
  },
  mounted() {
    this.fetchDevices();
    this.fetchHeartbeats();
  }
};
</script>

<style scoped>
.device-heartbeats {
  padding: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style>
