<template>
  <div class="alarm-record-list">
    <el-card>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>记录信息管理</el-breadcrumb-item>
        <el-breadcrumb-item>报警记录</el-breadcrumb-item>
      </el-breadcrumb>

      <el-row class="filter-row" :gutter="20">
        <el-col :span="6">
          <el-select v-model="filter.communityId" placeholder="选择社区" class="filter-item" @change="handleCommunityChange">
            <el-option 
              v-for="item in communityOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filter.district" placeholder="选择区" class="filter-item" @change="handleDistrictChange">
            <el-option 
              v-for="item in districtOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filter.building" placeholder="选择栋" class="filter-item" @change="handleBuildingChange">
            <el-option 
              v-for="item in buildingOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filter.unit" placeholder="选择单元" class="filter-item">
            <el-option 
              v-for="item in unitOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-date-picker
            v-model="filter.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            class="filter-item"
          />
        </el-col>
        <el-col :span="2">
          <el-button type="primary" :loading="loading" @click="searchAlarmRecords">查询</el-button>
        </el-col>
      </el-row>

      <el-table :data="alarmRecordList" style="width: 100%" v-loading="loading">
        <el-table-column prop="houseName" label="报警房间"/>
        <el-table-column prop="alarmType" label="报警类型"/>
        <el-table-column prop="firstAlarmTime" label="首次报警时间"/>
        <el-table-column prop="latestAlarmTime" label="最新报警时间"/>
        <el-table-column prop="alarmStatus" label="报警状态">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.alarmStatus)">
              {{ getStatusText(scope.row.alarmStatus) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button type="text" size="small" @click="viewAlarmRecord(scope.row)">查看详情</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          background
          layout="total, prev, pager, next, sizes"
          :total="total"
          :current-page="currentPage"
          :page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          @current-change="handlePageChange"
          @size-change="handleSizeChange"
        />
      </div>
    </el-card>

    <!-- 报警详情对话框 -->
    <el-dialog
      title="报警详情"
      v-model="dialogVisible"
      width="50%"
    >
      <el-descriptions :column="2" border>
        <el-descriptions-item label="报警房间">{{ currentRecord.houseName }}</el-descriptions-item>
        <el-descriptions-item label="报警类型">{{ currentRecord.alarmType }}</el-descriptions-item>
        <el-descriptions-item label="首次报警时间">{{ currentRecord.firstAlarmTime }}</el-descriptions-item>
        <el-descriptions-item label="最新报警时间">{{ currentRecord.latestAlarmTime }}</el-descriptions-item>
        <el-descriptions-item label="报警状态">
          <el-tag :type="getStatusType(currentRecord.alarmStatus)">
            {{ getStatusText(currentRecord.alarmStatus) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="报警描述">{{ currentRecord.alarmDescription }}</el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>


export default {
  name: 'AlarmRecord',
  data() {
    return {
      loading: false,
      filter: {
        communityId: '',
        district: '',
        building: '',
        unit: '',
        dateRange: []
      },
      communityOptions: [],
      districtOptions: [],
      buildingOptions: [],
      unitOptions: [],
      alarmRecordList: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      dialogVisible: false,
      currentRecord: {},
      mockData: [
        {
          id: 1,
          houseName: '1区-1栋-1单元-101',
          alarmType: '火警',
          firstAlarmTime: '2024-08-08 08:30:00',
          latestAlarmTime: '2024-08-08 08:30:00',
          alarmStatus: 'Pending',
          alarmDescription: '厨房烟雾感应器触发'
        },
        {
          id: 2,
          houseName: '2区-1栋-1单元-201',
          alarmType: '盗警',
          firstAlarmTime: '2024-08-08 14:45:10',
          latestAlarmTime: '2024-08-08 14:50:00',
          alarmStatus: 'Processing',
          alarmDescription: '门磁报警，疑似非法入侵'
        }
      ]
    };
  },
  methods: {
    getStatusType(status) {
      const types = {
        'Pending': 'warning',
        'Processing': 'primary',
        'Resolved': 'success'
      }
      return types[status] || 'info'
    },
    getStatusText(status) {
      const texts = {
        'Pending': '待处理',
        'Processing': '处理中',
        'Resolved': '已解决'
      }
      return texts[status] || status
    },
    async fetchAlarmRecords() {
      this.loading = true
      try {
        const response = await this.$axios.get('/api/alarm-records', {
          params: {
            ...this.filter,
            page: this.currentPage,
            size: this.pageSize
          }
        })
        this.alarmRecordList = response.data.records
        this.total = response.data.total
        this.$message.success('获取数据成功')
      } catch (error) {
        console.error('获取报警记录失败:', error)
        this.$message.warning('获取数据库失败，已展示示例数据')
        this.alarmRecordList = this.mockData
        this.total = this.mockData.length
      } finally {
        this.loading = false
      }
    },
    viewAlarmRecord(record) {
      this.currentRecord = record
      this.dialogVisible = true
    },
    searchAlarmRecords() {
      this.currentPage = 1;
      this.fetchAlarmRecords();
    },
    handlePageChange(page) {
      this.currentPage = page;
      this.fetchAlarmRecords();
    },
    handleSizeChange(size) {
      this.pageSize = size;
      this.fetchAlarmRecords();
    },
    handleCommunityChange(value) {
      this.filter.communityId = value;
      this.fetchAlarmRecords();
    },
    handleDistrictChange(value) {
      this.filter.district = value;
      this.fetchAlarmRecords();
    },
    handleBuildingChange(value) {
      this.filter.building = value;
      this.fetchAlarmRecords();
    },
  },
  mounted() {
    this.fetchAlarmRecords();
  },
};
</script>

<style scoped>
.alarm-record-list {
  padding: 20px;
}

.filter-row {
  margin-bottom: 20px;
}

.filter-item {
  width: 100%;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}

.dialog-footer {
  text-align: right;
  margin-top: 20px;
}
</style>
