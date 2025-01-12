<template>
  <div class="unlock-record-list">
    <el-card>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>记录信息管理</el-breadcrumb-item>
        <el-breadcrumb-item>开锁记录</el-breadcrumb-item>
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
          <el-select v-model="filter.building" placeholder="选择楼栋" class="filter-item">
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
        <el-col :span="4">
          <el-select v-model="filter.device" placeholder="所有设备" class="filter-item">
            <el-option label="门锁1" value="lock1"></el-option>
            <el-option label="门锁2" value="lock2"></el-option>
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-date-picker
              v-model="filter.startDate"
              type="date"
              placeholder="开始日期"
              class="filter-item"
              value-format="yyyy-MM-dd"
              format="yyyy-MM-dd"
          />
        </el-col>
        <el-col :span="4">
          <el-date-picker
              v-model="filter.endDate"
              type="date"
              placeholder="结束日期"
              class="filter-item"
              value-format="yyyy-MM-dd"
              format="yyyy-MM-dd"
          />
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="searchUnlockRecords">查询</el-button>
        </el-col>
      </el-row>

      <el-table :data="unlockRecordList" style="width: 100%" v-if="unlockRecordList.length > 0">
        <el-table-column prop="doorLockInfo" label="门锁信息"/>
        <el-table-column prop="unlockType" label="开锁类型"/>
        <el-table-column prop="unlocker" label="开锁人员"/>
        <el-table-column prop="unlockTime" label="开锁时间"/>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="text" size="small" @click="viewUnlockRecord(scope.row)">查看详情</el-button>
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
  name: 'UnlockRecord',
  data() {
    return {
      filter: {
        community: 'huimin',
        district: '',
        building: '',
        unit: '',
        floor: '',
        room: '',
        device: '',
        startDate: '',
        endDate: '',
      },
      unlockRecordList: [],
      mockUnlockRecordList: [
        {doorLockInfo: '门锁设备-A', unlockType: '密码开锁', unlocker: '张三', unlockTime: '2024-09-01 15:00:00'},
        {doorLockInfo: '门锁设备-B', unlockType: '指纹开锁', unlocker: '李四', unlockTime: '2024-09-01 15:05:00'},
      ],
      total: 0,
      mockTotal: 2,
      currentPage: 1,
      pageSize: 10,
      isMockData: false,
    };
  },
  methods: {
    async fetchUnlockRecords() {
      this.isMockData = false;
      try {
        const response = await axios.get('/api/unlock-records', { // 替换为你的实际接口
          params: {
            community: this.filter.community,
            district: this.filter.district,
            building: this.filter.building,
            unit: this.filter.unit,
            floor: this.filter.floor,
            room: this.filter.room,
            device: this.filter.device,
            startDate: this.filter.startDate,
            endDate: this.filter.endDate,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        if (response.status === 200) {
          this.unlockRecordList = response.data.unlockRecords;
          this.total = response.data.total;
        } else {
          this.$message.error(`获取开锁记录失败，状态码: ${response.status}`);
          this.showMockData();
        }
      } catch (error) {
        console.error('获取开锁记录失败:', error);
        this.$message.error('获取开锁记录失败，已显示示例数据。');
        this.showMockData();
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
    showMockData() {
      this.isMockData = true;
      this.unlockRecordList = this.mockUnlockRecordList;
      this.total = this.mockTotal;
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
  width: 100%;
}

.empty-data {
  text-align: center;
  color: #999;
  padding: 20px 0;
}
</style>
