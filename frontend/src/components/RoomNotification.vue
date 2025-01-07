<template>
  <div class="room-notification-list">
    <el-card>
      <el-row class="filter-row">
        <el-col :span="4">
          <el-input v-model="filter.title" placeholder="标题" class="filter-item" />
        </el-col>
        <el-col :span="4">
          <el-input v-model="filter.publishDate" placeholder="发布时间" class="filter-item" />
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="searchNotifications">查询</el-button>
        </el-col>
      </el-row>

      <el-table :data="notificationList" style="width: 100%">
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="content" label="内容" />
        <el-table-column prop="publishDate" label="发布时间" />
        <el-table-column prop="validUntil" label="有效期至" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="text" size="small" @click="editNotification(scope.row)">编辑</el-button>
            <el-button type="text" size="small" @click="deleteNotification(scope.row)">删除</el-button>
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
  name: 'RoomNotificationList',
  data() {
    return {
      filter: {
        title: '',
        publishDate: '',
      },
      notificationList: [
        {
          title: '通知1',
          content: '这是通知1的内容',
          publishDate: '2024-10-22',
          validUntil: '2024-11-22',
        },
        {
          title: '通知2',
          content: '这是通知2的内容',
          publishDate: '2024-10-23',
          validUntil: '2024-11-23',
        },
      ],
      total: 2,
      currentPage: 1,
      pageSize: 10,
    };
  },
  methods: {
    async fetchNotifications() {
      try {
        const response = await axios.get('/api/room-notifications', {
          params: {
            title: this.filter.title,
            publishDate: this.filter.publishDate,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        this.notificationList = response.data.notifications;
        this.total = response.data.total;
      } catch (error) {
        console.error('获取房间通知失败:', error);
      }
    },
    searchNotifications() {
      this.currentPage = 1;
      this.fetchNotifications();
    },
    handlePageChange(page) {
      this.currentPage = page;
      this.fetchNotifications();
    },
    editNotification(row) {
      console.log('编辑通知:', row);
    },
    deleteNotification(row) {
      console.log('删除通知:', row);
    },
  },
  mounted() {
    this.fetchNotifications();
  },
};
</script>

<style scoped>
.filter-row {
  margin-bottom: 20px;
}
.filter-item {
  margin-right: 10px;
}
</style>
