<template>
  <div class="complaint-suggestion-container">
    <div class="breadcrumb">
      <span>首页</span> / <span>区域维护管理</span> / <span>投诉建议</span>
    </div>
    <h1>投诉建议</h1>
    <div class="filter-row">
      <el-select v-model="filters.community" placeholder="选择社区" clearable>
        <el-option v-for="item in communities" :key="item.id" :label="item.name" :value="item.id"></el-option>
      </el-select>
      <el-select v-model="filters.type" placeholder="选择类型" clearable>
        <el-option label="投诉" value="complaint"></el-option>
        <el-option label="建议" value="suggestion"></el-option>
      </el-select>
      <el-select v-model="filters.status" placeholder="选择状态" clearable>
        <el-option label="待处理" value="pending"></el-option>
        <el-option label="已处理" value="processed"></el-option>
      </el-select>
      <el-date-picker v-model="filters.dateRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期">
      </el-date-picker>
      <el-button type="primary">查询</el-button>
    </div>

    <el-table :data="items" style="width: 100%" border>
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="communityName" label="社区名称"></el-table-column>
      <el-table-column prop="userName" label="用户名"></el-table-column>
      <el-table-column prop="type" label="类型">
        <template #default="scope">
          <el-tag :type="scope.row.type === 'complaint' ? 'danger' : 'primary'">
            {{ scope.row.type === 'complaint' ? '投诉' : '建议' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="content" label="内容"></el-table-column>
      <el-table-column prop="createTime" label="提交时间"></el-table-column>
      <el-table-column prop="status" label="状态">
        <template #default="scope">
          <el-tag :type="scope.row.status === 'pending' ? 'warning' : 'success'">
            {{ scope.row.status === 'pending' ? '待处理' : '已处理' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button type="primary" size="small" @click="handleProcess(scope.row)">处理</el-button>
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
  name: 'ComplaintSuggestionPage',
  data() {
    return {
      items: [
        { id: 1, communityName: '阳光花园', userName: '张三', type: 'complaint', content: '楼下施工噪音太大', createTime: '2024-08-13 11:20:00', status: 'pending' },
        { id: 2, communityName: '阳光花园', userName: '李四', type: 'suggestion', content: '建议增加小区健身设施', createTime: '2024-08-12 15:40:00', status: 'processed' },
        { id: 3, communityName: '阳光花园', userName: '王五', type: 'complaint', content: '车位被占用', createTime: '2024-08-11 08:30:00', status: 'pending' }
      ],
      communities: [
        { id: 1, name: '阳光花园' },
        { id: 2, name: '翠竹新城' }
      ],
      filters: {
        community: '',
        type: '',
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
    handleProcess(row) {
      console.log('处理投诉/建议:', row);
      if (row.status === 'pending') {
        this.$message.success('处理成功');
        row.status = 'processed';
      } else {
        this.$message.info('此项已处理');
      }
    },
    handleDetail(row) {
      console.log('查看详情:', row);
      this.$message.info('查看详情');
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
        console.log('获取投诉建议数据，页码:', this.pagination.currentPage, '每页数量:', this.pagination.pageSize);
      } catch (error) {
        console.error('获取投诉建议数据失败:', error);
        this.$message.error('获取投诉建议数据失败');
      }
    }
  },
  mounted() {
    this.fetchData();
  }
};
</script>

<style scoped>
.complaint-suggestion-container {
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