<template>
  <div class="unlock-record-list">
    <el-card>
      <el-row class="filter-row">
        <el-col :span="4">
          <el-input v-model="filter.room" placeholder="房间号" class="filter-item" />
        </el-col>
        <el-col :span="4">
          <el-input v-model="filter.method" placeholder="开锁方式" class="filter-item" />
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="searchUnlockRecords">查询</el-button>
        </el-col>
      </el-row>

      <el-table :data="unlockRecordList" style="width: 100%">
        <el-table-column prop="room" label="房间号" />
        <el-table-column prop="method" label="开锁方式" />
        <el-table-column prop="deviceName" label="设备名称" />
        <el-table-column prop="unlockTime" label="开锁时间" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="text" size="small" @click="viewUnlockRecord(scope.row)">查看详情</el-button>
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
  name: 'UnlockRecord',
  data() {
    return {
      filter: {
        room: '',
        method: '',
      },
      unlockRecordList: [
        {
          room: '栋-1单元-0101',
          method: '密码开锁',
          deviceName: '门锁1',
          unlockTime: '2024-09-01 14:32:44',
        },
        {
          room: '栋-1单元-0102',
          method: '刷卡开锁',
          deviceName: '门锁2',
          unlockTime: '2024-09-01 14:35:22',
        },
      ],
      total: 2,
      currentPage: 1,
      pageSize: 10,
    };
  },
  methods: {
    async fetchUnlockRecords() {
      try {
        const response = await axios.get('/api/unlock-records', {
          params: {
            room: this.filter.room,
            method: this.filter.method,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        this.unlockRecordList = response.data.unlockRecords;
        this.total = response.data.total;
      } catch (error) {
        console.error('获取开锁记录失败:', error);
      }
    },
    searchUnlockRecords() {
      this.currentPage = 1;
      this.fetchUnlockRecords();
    },
    handlePageChange(page) {
      this.currentPage = page;
      this.fetchUnlockRecords();
    },
    viewUnlockRecord(row) {
      console.log('查看开锁记录详情:', row);
    },
  },
  mounted() {
    this.fetchUnlockRecords();
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
