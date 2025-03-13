<template>
  <div class="community-review-container">
    <div class="breadcrumb">
      <span>首页</span> / <span>区域维护管理</span> / <span>社区评价</span>
    </div>
    <h1>社区评价</h1>
    <div class="filter-row">
      <el-select v-model="filters.community" placeholder="选择社区" clearable>
        <el-option v-for="item in communities" :key="item.id" :label="item.name" :value="item.id"></el-option>
      </el-select>
      <el-select v-model="filters.rating" placeholder="选择评分" clearable>
        <el-option label="1星" value="1"></el-option>
        <el-option label="2星" value="2"></el-option>
        <el-option label="3星" value="3"></el-option>
        <el-option label="4星" value="4"></el-option>
        <el-option label="5星" value="5"></el-option>
      </el-select>
      <el-date-picker v-model="filters.dateRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期">
      </el-date-picker>
      <el-button type="primary">查询</el-button>
    </div>

    <el-table :data="reviews" style="width: 100%" border>
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="communityName" label="社区名称"></el-table-column>
      <el-table-column prop="userName" label="用户名"></el-table-column>
      <el-table-column prop="rating" label="评分">
        <template #default="scope">
          <el-rate v-model="scope.row.rating" disabled show-score text-color="#ff9900"></el-rate>
        </template>
      </el-table-column>
      <el-table-column prop="comment" label="评价内容"></el-table-column>
      <el-table-column prop="createTime" label="评价时间"></el-table-column>
      <el-table-column prop="replied" label="是否回复">
        <template #default="scope">
          <el-tag :type="scope.row.replied ? 'success' : 'info'">
            {{ scope.row.replied ? '已回复' : '未回复' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100">
        <template #default="scope">
          <el-button type="primary" size="small" @click="handleReply(scope.row)">{{ scope.row.replied ? '查看回复' : '回复' }}</el-button>
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
  name: 'CommunityReviewPage',
  data() {
    return {
      reviews: [
        { id: 1, communityName: '阳光花园', userName: '张三', rating: 4, comment: '物业服务很好，环境整洁', createTime: '2024-08-13 10:15:00', replied: true },
        { id: 2, communityName: '阳光花园', userName: '李四', rating: 2, comment: '垃圾分类不到位，希望加强管理', createTime: '2024-08-12 14:30:00', replied: false },
        { id: 3, communityName: '阳光花园', userName: '王五', rating: 5, comment: '小区绿化很棒，住着很舒服', createTime: '2024-08-11 09:45:00', replied: true }
      ],
      communities: [
        { id: 1, name: '阳光花园' },
        { id: 2, name: '翠竹新城' }
      ],
      filters: {
        community: '',
        rating: '',
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
    handleReply(row) {
      console.log('回复评价:', row);
      if (row.replied) {
        this.$message.info('查看回复内容');
      } else {
        this.$message.success('回复成功');
        row.replied = true;
      }
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
        console.log('获取评价数据，页码:', this.pagination.currentPage, '每页数量:', this.pagination.pageSize);
      } catch (error) {
        console.error('获取评价数据失败:', error);
        this.$message.error('获取评价数据失败');
      }
    }
  },
  mounted() {
    this.fetchData();
  }
};
</script>

<style scoped>
.community-review-container {
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