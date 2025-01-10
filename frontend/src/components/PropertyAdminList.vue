<template>
  <div class="property-admin-list">
    <el-card>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-input v-model="search.name" placeholder="搜索管理员姓名" class="filter-item" />
        </el-col>
        <el-col :span="8">
          <el-input v-model="search.phone" placeholder="搜索手机号" class="filter-item" />
        </el-col>
        <el-col :span="8">
          <el-button type="primary" @click="searchAdmins">搜索</el-button>
          <el-button type="success" @click="showAddDialog = true">添加管理员</el-button>
        </el-col>
      </el-row>

      <el-table 
        :data="adminList" 
        style="width: 100%" 
        class="admin-table"
        v-loading="loading"
      >
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="phone" label="手机号" />
        <el-table-column prop="role" label="角色" />
        <el-table-column prop="status" label="状态" :formatter="formatStatus" />
        <el-table-column label="操作">
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

    <property-admin-form
      :visible="showAddDialog"
      @update:visible="showAddDialog = $event"
      @submit="handleAddAdmin"
    />
  </div>
</template>

<script>
import axios from 'axios';
import PropertyAdminForm from './PropertyAdminForm.vue';

export default {
  name: 'PropertyAdminList',
  components: {
    PropertyAdminForm
  },
  data() {
    return {
      loading: false,
      search: {
        name: '',
        phone: ''
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
      this.loading = true;
      try {
        const response = await axios.get('/api/property-admins', {
          params: {
            name: this.search.name,
            phone: this.search.phone,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        this.adminList = response.data.admins;
        this.total = response.data.total;
        this.$message.success('数据加载成功');
      } catch (error) {
        console.error('获取物业管理员信息失败:', error);
        this.$message.error('获取物业管理员信息失败');
        // 添加模拟数据
        this.adminList = [
          {
            id: 1,
            name: '张三',
            phone: '13800138000',
            role: '物业管理员',
            status: 'active',
            remark: '负责A区管理'
          },
          {
            id: 2,
            name: '李四',
            phone: '13800138001',
            role: '超级管理员',
            status: 'inactive',
            remark: '系统管理员'
          },
          {
            id: 3,
            name: '王五',
            phone: '13800138002',
            role: '物业管理员',
            status: 'active',
            remark: '负责B区管理'
          }
        ];
        this.total = this.adminList.length;
        this.$message.success('已加载模拟数据');
      } finally {
        this.loading = false;
      }
    },
    searchAdmins() {
      this.currentPage = 1;
      this.fetchAdmins();
    },
    handleSizeChange(size) {
      this.pageSize = size;
      this.fetchAdmins();
    },
    handlePageChange(page) {
      this.currentPage = page;
      this.fetchAdmins();
    },
    formatStatus(row, column, cellValue) {
      return cellValue === 'active' ? '活跃' : '非活跃';
    },
    editAdmin(row) {
      console.log('编辑:', row);
      // 可以添加编辑逻辑
    },
    deleteAdmin(row) {
      this.$confirm('确定要删除该管理员吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        console.log('删除:', row);
        // 可以添加删除逻辑
      }).catch(() => {});
    },
    handleAddAdmin(formData) {
      console.log('添加管理员:', formData);
      this.fetchAdmins();
    }
  },
  mounted() {
    this.fetchAdmins();
  }
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
