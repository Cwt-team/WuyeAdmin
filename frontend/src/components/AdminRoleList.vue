<template>
  <div class="admin-role-list">
    <el-card>
      <el-row>
        <el-col :span="24">
          <el-input v-model="search" placeholder="搜索管理员角色" class="filter-item" />
          <el-button type="primary" @click="searchRole">搜索</el-button>
        </el-col>
      </el-row>
      <el-table :data="roleList" style="width: 100%" class="role-table">
        <el-table-column prop="roleName" label="角色名称" />
        <el-table-column prop="description" label="描述" />
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
  name: 'AdminRoleList',
  data() {
    return {
      search: '',
      roleList: [
        {
          roleName: '管理员',
          description: '系统管理员',
        },
        {
          roleName: '编辑',
          description: '内容编辑',
        },
      ],
      total: 2,
      currentPage: 1,
      pageSize: 10,
    };
  },
  methods: {
    async fetchRoles() {
      try {
        const response = await axios.get('/api/roles', {
          params: {
            search: this.search,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        this.roleList = response.data.roles;
        this.total = response.data.total;
      } catch (error) {
        console.error('获取角色信息失败:', error);
      }
    },
    searchRole() {
      this.currentPage = 1;
      this.fetchRoles();
    },
    async handlePageChange(page) {
      this.currentPage = page;
      this.fetchRoles();
    },
    viewDetails(row) {
      console.log('查看详情:', row);
      // 可以添加查看详情的逻辑
    },
  },
  mounted() {
    this.fetchRoles();
  },
};
</script>

<style scoped>
.filter-item {
  margin-right: 20px;
}

.role-table {
  margin-top: 20px;
}

.el-card {
  padding: 20px;
}
</style>
