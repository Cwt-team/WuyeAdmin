<template>
  <div class="community-review-container">
    <div class="page-header">
      <div class="breadcrumb">
        <span>首页</span> / <span>区域维护管理</span> / <span>社区评价</span>
      </div>
      <h1>社区评价</h1>
    </div>
    
    <el-card class="filter-card">
      <div class="filter-row">
        <el-form :inline="true" :model="filters" class="filter-form">
          <el-form-item label="社区名称">
            <el-select v-model="filters.community" placeholder="选择社区" clearable style="width: 200px">
              <el-option 
                v-for="item in communities" 
                :key="item.id" 
                :label="item.name" 
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="评分">
            <el-select v-model="filters.rating" placeholder="选择评分" clearable style="width: 150px">
              <el-option label="1星" value="1"></el-option>
              <el-option label="2星" value="2"></el-option>
              <el-option label="3星" value="3"></el-option>
              <el-option label="4星" value="4"></el-option>
              <el-option label="5星" value="5"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="日期范围">
            <el-date-picker v-model="filters.dateRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期">
            </el-date-picker>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="resetFilters">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>

    <el-card class="data-card">
      <el-table :data="reviews" style="width: 100%" border v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        <el-table-column prop="community_name" label="社区名称" min-width="120"></el-table-column>
        <el-table-column prop="user_name" label="用户名" min-width="120"></el-table-column>
        <el-table-column label="评分" width="150" align="center">
          <template #default="scope">
            <el-rate v-model="scope.row.rating" disabled show-score text-color="#ff9900"></el-rate>
          </template>
        </el-table-column>
        <el-table-column prop="comment" label="评价内容" min-width="200" show-overflow-tooltip></el-table-column>
        <el-table-column prop="created_at" label="评价时间" width="160" align="center"></el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.replied ? 'success' : 'info'">
              {{ scope.row.replied ? '已回复' : '未回复' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" align="center">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleReply(scope.row)">
              {{ scope.row.replied ? '查看回复' : '回复' }}
            </el-button>
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
    </el-card>

    <el-dialog
      v-model="replyDialogVisible"
      :title="currentReview && currentReview.replied ? '查看回复' : '回复评价'"
      width="500px"
      :before-close="handleClose"
    >
      <el-form label-position="top">
        <el-form-item v-if="currentReview" label="评价内容">
          <div class="review-content">
            <p><strong>用户名：</strong>{{ currentReview.user_name }}</p>
            <p><strong>评分：</strong>
              <el-rate v-model="currentReview.rating" disabled></el-rate>
            </p>
            <p><strong>内容：</strong>{{ currentReview.comment }}</p>
            <p><strong>时间：</strong>{{ currentReview.created_at }}</p>
          </div>
        </el-form-item>
        <el-form-item label="回复内容">
          <el-input
            type="textarea"
            v-model="replyContent"
            :rows="4"
            placeholder="请输入回复内容"
            :disabled="currentReview && currentReview.replied && !editingReply"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="handleClose">{{ currentReview && currentReview.replied ? '关闭' : '取消' }}</el-button>
        <el-button v-if="currentReview && currentReview.replied" type="primary" @click="toggleEdit">
          {{ editingReply ? '取消编辑' : '编辑回复' }}
        </el-button>
        <el-button v-if="!currentReview || !currentReview.replied || editingReply" type="primary" @click="submitReply">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CommunityReviewPage',
  data() {
    return {
      reviews: [],
      communities: [],
      filters: {
        community: '',
        rating: '',
        dateRange: []
      },
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      replyDialogVisible: false,
      currentReview: null,
      replyContent: '',
      loading: false,
      editingReply: false
    };
  },
  methods: {
    handleReply(row) {
      this.currentReview = row;
      this.replyContent = row.reply || '';
      this.replyDialogVisible = true;
      this.editingReply = false;
    },
    async submitReply() {
      if (!this.replyContent.trim()) {
        this.$message.warning('回复内容不能为空');
        return;
      }
      
      this.loading = true;
      try {
        await axios.post(`/api/community-reviews/${this.currentReview.id}/reply`, {
          reply: this.replyContent
        });
        this.$message.success('回复成功');
        this.replyDialogVisible = false;
        this.editingReply = false;
        await this.fetchData();
      } catch (error) {
        console.error('回复失败:', error);
        this.$message.error('回复失败: ' + (error.response?.data?.message || '未知错误'));
      } finally {
        this.loading = false;
      }
    },
    toggleEdit() {
      this.editingReply = !this.editingReply;
      if (!this.editingReply) {
        this.replyContent = this.currentReview.reply || '';
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
    async fetchCommunities() {
      try {
        this.loading = true;
        const response = await axios.get('/api/reviews/communities');
        
        if (Array.isArray(response.data)) {
          this.communities = response.data.map(item => ({
            id: item.id,
            name: item.community_name || '未命名社区'
          }));
          
          if (this.communities.length === 0) {
            this.$message.warning('暂无社区数据');
          }
        } else {
          this.$message.error('获取社区数据格式错误');
          this.communities = [];
        }
        
        console.log('社区列表:', this.communities);
      } catch (error) {
        console.error('获取社区列表失败:', error);
        this.$message.error(error.response?.data?.message || '获取社区列表失败');
      } finally {
        this.loading = false;
      }
    },
    async fetchData() {
      try {
        this.loading = true;
        const params = {
          page: this.pagination.currentPage,
          pageSize: this.pagination.pageSize
        };
        
        if (this.filters.community) {
          params.community = this.filters.community;
        }
        if (this.filters.rating) {
          params.rating = this.filters.rating;
        }
        if (this.filters.dateRange && this.filters.dateRange.length === 2) {
          params.startDate = this.formatDate(this.filters.dateRange[0]);
          params.endDate = this.formatDate(this.filters.dateRange[1]);
        }
        
        console.log('请求参数:', params);
        const response = await axios.get('/api/community-reviews', { params });
        this.reviews = response.data.items;
        this.pagination.total = response.data.total;
        console.log('获取到的评价数据:', this.reviews);
      } catch (error) {
        console.error('获取评价数据失败:', error);
        this.$message.error('获取评价数据失败: ' + (error.response?.data?.message || error.message || '未知错误'));
      } finally {
        this.loading = false;
      }
    },
    formatDate(date) {
      const d = new Date(date);
      const year = d.getFullYear();
      const month = String(d.getMonth() + 1).padStart(2, '0');
      const day = String(d.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },
    handleSearch() {
      this.pagination.currentPage = 1;
      this.fetchData();
    },
    resetFilters() {
      this.filters = {
        community: '',
        rating: '',
        dateRange: []
      };
      this.pagination.currentPage = 1;
      this.fetchData();
    },
    handleClose() {
      this.replyDialogVisible = false;
      this.replyContent = '';
      this.editingReply = false;
    }
  },
  mounted() {
    this.fetchCommunities();
    this.fetchData();
  }
};
</script>

<style scoped>
.community-review-container {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.breadcrumb {
  margin-bottom: 10px;
  font-size: 14px;
  color: #606266;
}

h1 {
  font-size: 22px;
  margin: 0;
  color: #303133;
}

.filter-card {
  margin-bottom: 20px;
}

.filter-form {
  display: flex;
  flex-wrap: wrap;
}

.data-card {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.review-content {
  background-color: #f8f8f8;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 10px;
}

.review-content p {
  margin: 8px 0;
}
</style> 