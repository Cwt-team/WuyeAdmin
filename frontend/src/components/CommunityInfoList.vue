<template>
  <div class="community-info-list">
    <el-card>
      <el-row>
        <el-col :span="24">
          <el-input v-model="search" placeholder="搜索小区名称" class="filter-item" />
          <el-button type="primary" @click="searchCommunity">搜索</el-button>
        </el-col>
      </el-row>
      <el-table :data="communityList" style="width: 100%" class="community-table">
        <el-table-column prop="name" label="小区名称" />
        <el-table-column prop="location" label="小区位置" />
        <el-table-column prop="totalUnits" label="总户数" />
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
  name: 'CommunityInfoList',
  data() {
    return {
      search: '',
      communityList: [
        {
          name: '小区A',
          location: '位置A',
          totalUnits: 100,
          status: 'active',
        },
        {
          name: '小区B',
          location: '位置B',
          totalUnits: 150,
          status: 'inactive',
        },
      ],
      total: 2,
      currentPage: 1,
      pageSize: 10,
    };
  },
  methods: {
    async fetchCommunities() {
      try {
        const response = await axios.get('/api/communities', {
          params: {
            search: this.search,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        this.communityList = response.data.communities;
        this.total = response.data.total;
      } catch (error) {
        console.error('获取小区信息失败:', error);
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
    viewDetails(row) {
      console.log('查看详情:', row);
      // 可以添加查看详情的逻辑
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
