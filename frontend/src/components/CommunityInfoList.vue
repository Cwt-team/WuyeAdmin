<template>
  <div class="community-info-list">
    <el-card>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-input v-model="search.name" placeholder="搜索小区名称" class="filter-item" />
        </el-col>
        <el-col :span="8">
          <el-input v-model="search.code" placeholder="搜索小区编号" class="filter-item" />
        </el-col>
        <el-col :span="8">
          <el-button type="primary" @click="searchCommunity">搜索</el-button>
          <el-button type="success" @click="showAddDialog = true">添加小区</el-button>
        </el-col>
      </el-row>
      <el-table :data="communityList" style="width: 100%" class="community-table">
        <el-table-column prop="name" label="小区名称" />
        <el-table-column prop="location" label="小区位置" />
        <el-table-column prop="totalUnits" label="总户数" />
        <el-table-column prop="status" label="状态" :formatter="formatStatus" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editCommunity(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteCommunity(scope.row)">删除</el-button>
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
  name: 'CommunityInfoList',
  data() {
    return {
      loading: false,
      batchLoading: false,
      emptyText: '暂无数据',
      search: {
        name: '',
        code: ''
      },
      showAddDialog: false,
      communityList: [],
      selectedCommunities: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
    };
  },
  methods: {
    async fetchCommunities() {
      this.loading = true;
      try {
        const response = await axios.get('/api/communities', {
          params: {
            name: this.search.name,
            code: this.search.code,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        this.communityList = response.data.communities;
        this.total = response.data.total;
        this.$message.success('数据加载成功');
      } catch (error) {
        console.error('获取小区信息失败:', error);
        this.$message.error('获取小区信息失败');
        // 添加模拟数据
        this.communityList = [
          {
            id: 1,
            name: '阳光花园',
            code: 'YG001',
            location: '北京市朝阳区',
            totalUnits: 500,
            status: 'active',
            createTime: '2023-01-01 10:00:00'
          },
          {
            id: 2,
            name: '幸福家园',
            code: 'XF002',
            location: '上海市浦东新区',
            totalUnits: 800,
            status: 'inactive',
            createTime: '2023-02-15 14:30:00'
          },
          {
            id: 3,
            name: '和谐小区',
            code: 'HX003',
            location: '广州市天河区',
            totalUnits: 300,
            status: 'active',
            createTime: '2023-03-20 09:15:00'
          }
        ];
        this.total = this.communityList.length;
        this.$message.success('已加载模拟数据');
      } finally {
        this.loading = false;
      }
    },
    searchCommunity() {
      this.currentPage = 1;
      this.fetchCommunities();
    },
    async handlePageChange(page) {
      this.currentPage = page;
      this.fetchCommunities();
    },
    formatStatus(row, column, cellValue) {
      return cellValue === 'active' ? '活跃' : '非活跃';
    },
    editCommunity(row) {
      console.log('编辑:', row);
      // 可以添加编辑逻辑
    },
    deleteCommunity(row) {
      this.$confirm('确定要删除该小区吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        console.log('删除:', row);
        // 可以添加删除逻辑
      }).catch(() => {});
    },
    handleSizeChange(size) {
      this.pageSize = size;
      this.fetchCommunities();
    },
  },
  mounted() {
    this.fetchCommunities();
  },
};
</script>

<style scoped>
.filter-item {
  margin-right: 20px;
}

.community-table {
  margin-top: 20px;
}

.el-card {
  padding: 20px;
}
</style>
