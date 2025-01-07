<template>
  <div class="equipment-list">
    <el-card>
      <el-row class="filter-row">
        <el-col :span="4">
          <el-input v-model="filter.equipment" placeholder="设备名称" class="filter-item" />
        </el-col>
        <el-col :span="4">
          <el-input v-model="filter.uid" placeholder="UID" class="filter-item" />
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="searchEquipment">查询</el-button>
        </el-col>
      </el-row>

      <el-table :data="equipmentList" style="width: 100%">
        <el-table-column prop="equipment" label="设备名称" />
        <el-table-column prop="uid" label="UID" />
        <el-table-column prop="ip" label="IP地址" />
        <el-table-column prop="location" label="安装位置" />
        <el-table-column prop="status" label="状态" />
        <el-table-column prop="updateTime" label="更新时间" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="text" size="small" @click="editEquipment(scope.row)">编辑</el-button>
            <el-button type="text" size="small" @click="deleteEquipment(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        background
        layout="prev, pager, next"
        :total="total"
        :current-page="currentPage"
        :page-size="pageSize"
        @current-change="handlePageChange"
      />
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'EquipmentList',
  data() {
    return {
      filter: {
        equipment: '',
        uid: '',
      },
      equipmentList: [
        {
          equipment: '设备1',
          uid: 'UID12345',
          ip: '192.168.0.1',
          location: '大门口',
          status: '在线',
          updateTime: '2024-08-16 14:02:36',
        },
        {
          equipment: '设备2',
          uid: 'UID54321',
          ip: '192.168.0.2',
          location: '后门',
          status: '离线',
          updateTime: '2024-08-18 10:15:20',
        },
      ],
      total: 2,
      currentPage: 1,
      pageSize: 10,
    };
  },
  methods: {
    async fetchEquipment() {
      try {
        const response = await axios.get('/api/equipment', {
          params: {
            equipment: this.filter.equipment,
            uid: this.filter.uid,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        this.equipmentList = response.data.equipment;
        this.total = response.data.total;
      } catch (error) {
        console.error('获取设备信息失败:', error);
      }
    },
    searchEquipment() {
      this.currentPage = 1;
      this.fetchEquipment();
    },
    handlePageChange(page) {
      this.currentPage = page;
      this.fetchEquipment();
    },
    editEquipment(row) {
      console.log('编辑设备:', row);
    },
    deleteEquipment(row) {
      console.log('删除设备:', row);
    },
  },
  mounted() {
    this.fetchEquipment();
  },
};
</script>

<style scoped>
.filter-row {
  margin-bottom: 20px;
}
.filter-item {
  margin-right: 10px;
}
</style>
