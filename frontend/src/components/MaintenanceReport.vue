<template>
  <div class="maintenance-report-container">
    <div class="breadcrumb">
      <span>首页</span> / <span>区域维护管理</span> / <span>报事报修</span>
    </div>
    <h1>报事报修</h1>
    <div class="filter-row">
      <el-select v-model="filters.community" placeholder="选择社区" clearable>
        <el-option v-for="item in communities" :key="item.id" :label="item.name" :value="item.id"></el-option>
      </el-select>
      <el-select v-model="filters.building" placeholder="选择楼" clearable>
        <el-option v-for="item in buildings" :key="item.id" :label="item.name" :value="item.id"></el-option>
      </el-select>
      <el-select v-model="filters.status" placeholder="选择状态" clearable>
        <el-option label="待处理" value="pending"></el-option>
        <el-option label="处理中" value="processing"></el-option>
        <el-option label="已完成" value="completed"></el-option>
      </el-select>
      <el-date-picker v-model="filters.dateRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期">
      </el-date-picker>
      <el-button type="primary">查询</el-button>
    </div>

    <el-table :data="requests" style="width: 100%" border>
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="communityName" label="社区名称"></el-table-column>
      <el-table-column prop="buildingInfo" label="楼栋信息"></el-table-column>
      <el-table-column prop="description" label="问题描述"></el-table-column>
      <el-table-column prop="reportTime" label="报修时间"></el-table-column>
      <el-table-column prop="status" label="状态">
        <template #default="scope">
          <el-tag :type="getStatusType(scope.row.status)">{{ getStatusText(scope.row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button type="primary" size="small" @click="handleEdit(scope.row)">处理</el-button>
          <el-button type="info" size="small" @click="handleDetail(scope.row)">详情</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination">
      <el-pagination
        :current-page="pagination.currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pagination.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="pagination.total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MaintenanceReport',
  data() {
    return {
      requests: [
        { id: 1, communityName: '阳光花园', buildingInfo: '1区1栋', description: '水管漏水', reportTime: '2024-08-13 14:30:00', status: 'pending' },
        { id: 2, communityName: '阳光花园', buildingInfo: '2区3栋', description: '电梯故障', reportTime: '2024-08-12 09:15:00', status: 'processing' },
        { id: 3, communityName: '阳光花园', buildingInfo: '5区12栋', description: '门锁损坏', reportTime: '2024-08-11 16:45:00', status: 'completed' }
      ],
      communities: [
        { id: 1, name: '阳光花园' },
        { id: 2, name: '翠竹新城' }
      ],
      buildings: [
        { id: 1, name: '1区1栋' },
        { id: 2, name: '2区3栋' },
        { id: 3, name: '5区12栋' }
      ],
      filters: {
        community: '',
        building: '',
        status: '',
        dateRange: []
      },
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 3
      }
    };
  },
  methods: {
    getStatusType(status) {
      switch(status) {
        case 'pending': return 'warning';
        case 'processing': return 'primary';
        case 'completed': return 'success';
        default: return 'info';
      }
    },
    getStatusText(status) {
      switch(status) {
        case 'pending': return '待处理';
        case 'processing': return '处理中';
        case 'completed': return '已完成';
        default: return '未知';
      }
    },
    handleEdit(row) {
      console.log('处理请求:', row);
      this.$message.success('开始处理请求');
    },
    handleDetail(row) {
      console.log('查看详情:', row);
      this.$message.info('查看请求详情');
    },
    handleSizeChange(size) {
      this.pagination.pageSize = size;
      this.fetchData();
    },
    handleCurrentChange(page) {
      this.pagination.currentPage = page;
      this.fetchData();
    },
    async fetchData() {
      try {
        // 这里应当调用实际的API获取数据
        console.log('获取报修数据，页码:', this.pagination.currentPage, '每页数量:', this.pagination.pageSize);
      } catch (error) {
        console.error('获取报修数据失败:', error);
        this.$message.error('获取报修数据失败');
      }
    }
  },
  mounted() {
    this.fetchData();
  }
};
</script>

<style scoped>
.maintenance-report-container {
  padding: 20px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.breadcrumb {
  margin-bottom: 15px;
  font-size: 14px;
  color: #606266;
}

h1 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #303133;
}

.filter-row {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>