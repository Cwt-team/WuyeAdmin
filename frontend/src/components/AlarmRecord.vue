<template>
  <div class="alarm-record-list">
    <el-card>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>记录信息管理</el-breadcrumb-item>
        <el-breadcrumb-item>报警记录</el-breadcrumb-item>
      </el-breadcrumb>

      <el-row class="filter-row">
        <el-col :span="4">
          <el-select v-model="filter.community" placeholder="选择社区" class="filter-item">
            <el-option label="1545, 惠民科技" value="huimin"></el-option>
          </el-select>
        </el-col>
        <el-col :span="3">
          <el-select v-model="filter.district" placeholder="选择区" class="filter-item">
            <el-option label="1区" value="1"></el-option>
            <el-option label="2区" value="2"></el-option>
          </el-select>
        </el-col>
        <el-col :span="3">
          <el-select v-model="filter.building" placeholder="选择栋" class="filter-item">
            <el-option label="1栋" value="1"></el-option>
            <el-option label="2栋" value="2"></el-option>
          </el-select>
        </el-col>
        <el-col :span="3">
          <el-select v-model="filter.floor" placeholder="选择楼层" class="filter-item">
            <el-option label="1层" value="1"></el-option>
            <el-option label="2层" value="2"></el-option>
          </el-select>
        </el-col>
        <el-col :span="3">
          <el-select v-model="filter.room" placeholder="选择房号" class="filter-item">
            <el-option label="0101" value="0101"></el-option>
            <el-option label="0102" value="0102"></el-option>
          </el-select>
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="searchAlarmRecords">查询</el-button>
        </el-col>
      </el-row>

      <el-table :data="alarmRecordList" style="width: 100%" v-if="alarmRecordList.length > 0">
        <el-table-column prop="alarmRoom" label="报警房间"/>
        <el-table-column prop="alarmType" label="报警类型"/>
        <el-table-column prop="firstAlarmTime" label="首次报警时间"/>
        <el-table-column prop="latestAlarmTime" label="最新报警时间"/>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="text" size="small" @click="viewAlarmRecord(scope.row)">查看详情</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div v-else class="empty-data">暂无数据</div>

      <el-pagination
          background
          layout="prev, pager, next"
          :total="isMockData ? mockTotal : total"
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
        community: 'huimin',
        district: '',
        building: '',
        floor: '',
        room: '',
      },
      alarmRecordList: [],
      mockAlarmRecordList: [
        {
          alarmRoom: '栋-1单元-0101',
          alarmType: '烟雾报警',
          firstAlarmTime: '2024-09-01 15:00:00',
          latestAlarmTime: '2024-09-01 15:00:00'
        },
        {
          alarmRoom: '栋-2单元-0201',
          alarmType: '燃气泄漏',
          firstAlarmTime: '2024-09-01 15:05:00',
          latestAlarmTime: '2024-09-01 15:06:00'
        },
      ],
      total: 0,
      mockTotal: 2,
      currentPage: 1,
      pageSize: 10,
      isMockData: false,
    };
  },
  methods: {
    async fetchAlarmRecords() {
      this.isMockData = false;
      try {
        const response = await axios.get('/api/alarm-records', { // 替换为你的实际接口
          params: {
            community: this.filter.community,
            district: this.filter.district,
            building: this.filter.building,
            floor: this.filter.floor,
            room: this.filter.room,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        if (response.status === 200) {
          this.alarmRecordList = response.data.alarmRecords;
          this.total = response.data.total;
        } else {
          this.$message.error(`获取报警记录失败，状态码: ${response.status}`);
          this.showMockData();
        }
      } catch (error) {
        console.error('获取报警记录失败:', error);
        this.$message.error('获取报警记录失败，已显示示例数据。');
        this.showMockData();
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
    showMockData() {
      this.isMockData = true;
      this.alarmRecordList = this.mockAlarmRecordList;
      this.total = this.mockTotal;
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
  width: 100%;
}

.empty-data {
  text-align: center;
  color: #999;
  padding: 20px 0;
}
</style>
