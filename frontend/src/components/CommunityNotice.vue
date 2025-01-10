<template>
  <div class="community-notice-list">
    <el-card>
      <!-- 筛选区域 -->
      <el-row class="filter-row">
        <el-col :span="4">
          <el-input v-model="filter.title" placeholder="标题" class="filter-item" />
        </el-col>
        <el-col :span="4">
          <el-input v-model="filter.publishDate" placeholder="发布时间" class="filter-item" />
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="searchNotices">查询</el-button>
        </el-col>
      </el-row>

      <!-- 表格区域 -->
      <el-table :data="noticeList" style="width: 100%">
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="content" label="内容" />
        <el-table-column prop="publishDate" label="发布时间" />
        <el-table-column prop="displayDate" label="展示时间" />
        <el-table-column prop="validUntil" label="有效期至" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="text" size="small" @click="editNotice(scope.row)">编辑</el-button>
            <el-button type="text" size="small" @click="deleteNotice(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页区域 -->
      <el-pagination
        background
        layout="total, prev, pager, next"
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
  name: 'CommunityNotice',
  data() {
    return {
      filter: {
        title: '',
        publishDate: '',
      },
      // 初始空的通知列表
      noticeList: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
    };
  },
  methods: {
    async fetchNotices() {
      try {
        const response = await axios.get('/api/community-notices', {
          params: {
            title: this.filter.title,
            publishDate: this.filter.publishDate,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        this.noticeList = response.data.notices.map(notice => ({
          ...notice,
          displayDate: `${notice.publishDate} 至 ${notice.validUntil}`, // 新增展示时间字段
        }));
        this.total = response.data.total;
      } catch (error) {
        console.error('获取小区通知失败:', error);
        // 后端请求失败时，提供模拟数据
        this.noticeList = [
          {
            title: '模拟通知1',
            content: '这是一条模拟数据的内容1',
            publishDate: '2024-10-22',
            displayDate: '2024-10-22 至 2024-11-22',
            validUntil: '2024-11-22',
          },
          {
            title: '模拟通知2',
            content: '这是一条模拟数据的内容2',
            publishDate: '2024-10-23',
            displayDate: '2024-10-23 至 2024-11-23',
            validUntil: '2024-11-23',
          },
        ];
        this.total = this.noticeList.length; // 模拟数据条数
      }
    },
    // 搜索功能
    searchNotices() {
      this.currentPage = 1; // 重置到第一页
      this.fetchNotices();
    },
    // 分页切换
    handlePageChange(page) {
      this.currentPage = page;
      this.fetchNotices();
    },
    // 编辑通知
    editNotice(row) {
      console.log('编辑通知:', row);
    },
    // 删除通知
    deleteNotice(row) {
      console.log('删除通知:', row);
    },
  },
  mounted() {
    this.fetchNotices(); // 初始化请求
  },
};
</script>

<style scoped>
/* 筛选区域样式 */
.filter-row {
  margin-bottom: 20px;
}

.filter-item {
  margin-right: 10px;
}

/* 分页器调整 */
.el-pagination {
  margin-top: 20px;
  text-align: right;
}
</style>
