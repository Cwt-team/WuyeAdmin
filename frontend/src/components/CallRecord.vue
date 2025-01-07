<template>
  <div class="call-record-list">
    <el-card>
      <el-row class="filter-row">
        <el-col :span="4">
          <el-input v-model="filter.room" placeholder="房间号" class="filter-item" />
        </el-col>
        <el-col :span="4">
          <el-input v-model="filter.type" placeholder="呼叫类型" class="filter-item" />
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="searchCallRecords">查询</el-button>
        </el-col>
      </el-row>

      <el-table :data="callRecordList" style="width: 100%">
        <el-table-column prop="room" label="房间号" />
        <el-table-column prop="type" label="呼叫类型" />
        <el-table-column prop="deviceName" label="设备名称" />
        <el-table-column prop="callTime" label="呼叫时间" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="text" size="small" @click="viewCallRecord(scope.row)">查看详情</el-button>
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
  name: 'CallRecord',
  data() {
    return {
      filter: {
        room: '',
        type: '',
      },
      callRecordList: [
        {
          room: '栋-1单元-0101',
          type: 'App门禁',
          deviceName: '设备1',
          callTime: '2024-09-01 14:32:44',
        },
        {
          room: '栋-1单元-0102',
          type: 'App门禁',
          deviceName: '设备2',
          callTime: '2024-09-01 14:35:22',
        },
      ],
      total: 2,
      currentPage: 1,
      pageSize: 10,
    };
  },
  methods: {
    async fetchCallRecords() {
      try {
        const response = await axios.get('/api/call-records', {
          params: {
            room: this.filter.room,
            type: this.filter.type,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        this.callRecordList = response.data.callRecords;
        this.total = response.data.total;
      } catch (error) {
        console.error('获取呼叫记录失败:', error);
      }
    },
    searchCallRecords() {
      this.currentPage = 1;
      this.fetchCallRecords();
    },
    handlePageChange(page) {
      this.currentPage = page;
      this.fetchCallRecords();
    },
    viewCallRecord(row) {
      console.log('查看呼叫记录详情:', row);
    },
  },
  mounted() {
    this.fetchCallRecords();
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
