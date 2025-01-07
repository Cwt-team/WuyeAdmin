<template>
  <div class="alarm-record-list">
    <el-card>
      <el-row class="filter-row">
        <el-col :span="4">
          <el-input v-model="filter.room" placeholder="房间号" class="filter-item" />
        </el-col>
        <el-col :span="4">
          <el-input v-model="filter.type" placeholder="报警类型" class="filter-item" />
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="searchAlarmRecords">查询</el-button>
        </el-col>
      </el-row>

      <el-table :data="alarmRecordList" style="width: 100%">
        <el-table-column prop="room" label="房间号" />
        <el-table-column prop="type" label="报警类型" />
        <el-table-column prop="deviceName" label="设备名称" />
        <el-table-column prop="alarmTime" label="报警时间" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="text" size="small" @click="viewAlarmRecord(scope.row)">查看详情</el-button>
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
  name: 'AlarmRecord',
  data() {
    return {
      filter: {
        room: '',
        type: '',
      },
      alarmRecordList: [
        {
          room: '栋-1单元-0101',
          type: '火警',
          deviceName: '报警器1',
          alarmTime: '2024-09-01 14:32:44',
        },
        {
          room: '栋-1单元-0102',
          type: '入侵',
          deviceName: '报警器2',
          alarmTime: '2024-09-01 14:35:22',
        },
      ],
      total: 2,
      currentPage: 1,
      pageSize: 10,
    };
  },
  methods: {
    async fetchAlarmRecords() {
      try {
        const response = await axios.get('/api/alarm-records', {
          params: {
            room: this.filter.room,
            type: this.filter.type,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        this.alarmRecordList = response.data.alarmRecords;
        this.total = response.data.total;
      } catch (error) {
        console.error('获取报警记录失败:', error);
      }
    },
    searchAlarmRecords() {
      this.currentPage = 1;
      this.fetchAlarmRecords();
    },
    handlePageChange(page) {
      this.currentPage = page;
      this.fetchAlarmRecords();
    },
    viewAlarmRecord(row) {
      console.log('查看报警记录详情:', row);
    },
  },
  mounted() {
    this.fetchAlarmRecords();
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
