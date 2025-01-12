<template>
  <div class="call-record-list">
    <el-card>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>记录信息管理</el-breadcrumb-item>
        <el-breadcrumb-item>呼叫记录</el-breadcrumb-item>
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
          <el-select v-model="filter.unit" placeholder="选择单元" class="filter-item">
            <el-option label="1单元" value="1"></el-option>
            <el-option label="2单元" value="2"></el-option>
          </el-select>
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="searchCallRecords">查询</el-button>
        </el-col>
      </el-row>

      <el-table :data="callRecordList" style="width: 100%" v-if="callRecordList.length > 0">
        <el-table-column prop="deviceInfo" label="门禁信息"/>
        <el-table-column prop="callTime" label="呼叫时间"/>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="text" size="small" @click="viewCallRecord(scope.row)">查看详情</el-button>
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
  name: 'CallRecord',
  data() {
    return {
      filter: {
        community: 'huimin', // 默认值
        district: '',
        building: '',
        unit: '',
      },
      callRecordList: [],
      mockCallRecordList: [
        {deviceInfo: '门禁设备-1', callTime: '2024-09-01 15:00:00'},
        {deviceInfo: '门禁设备-2', callTime: '2024-09-01 15:05:00'},
      ],
      total: 0,
      mockTotal: 2,
      currentPage: 1,
      pageSize: 10,
      isMockData: false, // 标识当前是否为模拟数据
    };
  },
  methods: {
    async fetchCallRecords() {
      this.isMockData = false; // 重置为非模拟数据
      try {
        const response = await axios.get('/api/call-records', { // 替换为你的实际接口
          params: {
            community: this.filter.community,
            district: this.filter.district,
            building: this.filter.building,
            unit: this.filter.unit,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        if (response.status === 200) {
          this.callRecordList = response.data.callRecords;
          this.total = response.data.total;
        } else {
          this.$message.error(`获取呼叫记录失败，状态码: ${response.status}`);
          this.showMockData();
        }
      } catch (error) {
        console.error('获取呼叫记录失败:', error);
        this.$message.error('获取呼叫记录失败，已显示示例数据。');
        this.showMockData();
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
    showMockData() {
      this.isMockData = true;
      this.callRecordList = this.mockCallRecordList;
      this.total = this.mockTotal;
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
  width: 100%; /* 让筛选框宽度撑满 */
}

.empty-data {
  text-align: center;
  color: #999;
  padding: 20px 0;
}
</style>
