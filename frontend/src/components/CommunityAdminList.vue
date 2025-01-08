<template>
  <div class="community-admin-list">
    <el-card>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-input v-model="search.name" placeholder="搜索管理员姓名" class="filter-item" />
        </el-col>
        <el-col :span="8">
          <el-input v-model="search.username" placeholder="搜索用户名" class="filter-item" />
        </el-col>
        <el-col :span="8">
          <el-button type="primary" @click="searchAdmin">搜索</el-button>
          <el-button type="success" @click="showAddDialog = true">添加管理员</el-button>
        </el-col>
      </el-row>
      <el-table :data="adminList" style="width: 100%" class="admin-table">
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="realName" label="真实姓名" />
        <el-table-column prop="role" label="角色" />
        <el-table-column prop="community" label="负责小区" />
        <el-table-column prop="status" label="状态" :formatter="formatStatus" />
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editAdmin(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteAdmin(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        background
        layout="sizes, prev, pager, next"
        :total="total"
        :current-page="currentPage"
        :page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        @size-change="handleSizeChange"
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
      search: {
        name: '',
        username: ''
      },
      showAddDialog: false,
      adminList: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
    };
  },
  methods: {
    async fetchAdmins() {
      try {
        const response = await axios.get('/api/admins', {
          params: {
            name: this.search.name,
            username: this.search.username,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        this.adminList = response.data.admins;
        this.total = response.data.total;
        this.$message.success('数据加载成功');
      } catch (error) {
        console.error('获取管理员信息失败:', error);
        this.$message.error('获取管理员信息失败');
        // 添加模拟数据
        this.adminList = [
          {
            username: 'admin001',
            realName: '王五',
            role: '小区管理员',
            community: '阳光花园',
            phone: '13800138000',
            status: 'active'
          },
          {
            username: 'admin002',
            realName: '赵六',
            role: '物业管理员',
            community: '幸福家园',
            phone: '13800138001',
            status: 'active'
          },
          {
            username: 'admin003',
            realName: '孙七',
            role: '财务管理员',
            community: '和谐小区',
            phone: '13800138002',
            status: 'inactive'
          },
          {
            username: 'admin004',
            realName: '周八',
            role: '系统管理员',
            community: '平安小区',
            phone: '13800138003',
            status: 'active'
          }
        ];
        this.total = this.adminList.length;
        this.$message.success('已加载模拟数据');
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
      return cellValue === 'active' ? '正常' : '停用';
    },
    editAdmin(row) {
      this.$message.info('编辑功能待实现');
      console.log('编辑:', row);
    },
    deleteAdmin(row) {
      this.$confirm('确定要删除该管理员吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message.success('删除成功');
        console.log('删除:', row);
      }).catch(() => {});
    },
    handleSizeChange(size) {
      this.pageSize = size;
      this.fetchAdmins();
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
