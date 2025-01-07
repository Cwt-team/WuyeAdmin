<template>
  <div class="property-admin-list">
    <el-card>
      <el-row>
        <el-col :span="24">
          <el-input v-model="search" placeholder="搜索物业管理员" class="filter-item" />
          <el-button type="primary" @click="searchAdmin">搜索</el-button>
        </el-col>
      </el-row>
      <el-table :data="adminList" style="width: 100%" class="admin-table">
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="phone" label="手机号" />
        <el-table-column prop="role" label="角色" />
        <el-table-column prop="date" label="创建时间" />
        <el-table-column prop="status" label="状态" :formatter="formatStatus" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="text" size="small" @click="viewDetails(scope.row)">查看详情</el-button>
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
  name: 'PropertyAdminList',
  data() {
    return {
      search: '',
      adminList: [
        {
          name: '张三',
          phone: '13712345678',
          role: '物业管理员',
          date: '2023-08-16 14:02:36',
          status: 'active',
        },
        {
          name: '李四',
          phone: '13787654321',
          role: '物业管理员',
          date: '2023-09-01 10:15:20',
          status: 'inactive',
        },
      ],
      total: 2,
      currentPage: 1,
      pageSize: 10,
    };
  },
  methods: {
    async fetchAdmins() {
      try {
        const response = await axios.get('/api/admins', {
          params: {
            search: this.search,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        this.adminList = response.data.admins;
        this.total = response.data.total;
      } catch (error) {
        console.error('获取管理员信息失败:', error);
      }
    },
    searchAdmin() {
      this.currentPage = 1;
      this.fetchAdmins();
    },
    async handlePageChange(page) {
      this.currentPage = page;
      this.fetchAdmins();
    },
    formatStatus(row, column, cellValue) {
      return cellValue === 'active' ? '活跃' : '非活跃';
    },
    viewDetails(row) {
      console.log('查看详情:', row);
      // 可以添加查看详情的逻辑
    },
  },
  mounted() {
    this.fetchAdmins();
  },
};
</script>

<style scoped>
.filter-item {
  margin-right: 20px;
}

.admin-table {
  margin-top: 20px;
}

.el-card {
  padding: 20px;
}
</style>
