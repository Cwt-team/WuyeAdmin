<template>
  <div class="community-admin-list">
    <el-card>
      <el-row>
        <el-col :span="24">
          <el-input v-model="search" placeholder="搜索小区管理员" class="filter-item" />
          <el-button type="primary" @click="searchAdmin">搜索</el-button>
        </el-col>
      </el-row>
      <el-table :data="adminList" style="width: 100%" class="admin-table">
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="realName" label="真实姓名" />
        <el-table-column prop="role" label="角色" />
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
  name: 'CommunityAdminList',
  data() {
    return {
      search: '',
      adminList: [
        {
          username: 'admin1',
          realName: '张三',
          role: '管理员',
        },
        {
          username: 'admin2',
          realName: '李四',
          role: '编辑',
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
