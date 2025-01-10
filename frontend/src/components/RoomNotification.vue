<template>
  <div class="room-notification-list">
    <el-card>
      <el-row class="filter-row" :gutter="10">
        <el-col :span="4">
          <el-input v-model="filter.title" placeholder="标题" clearable class="filter-item" />
        </el-col>
        <el-col :span="4">
          <el-input v-model="filter.region" placeholder="区域" clearable class="filter-item" />
        </el-col>
        <el-col :span="4">
          <el-input v-model="filter.building" placeholder="楼栋" clearable class="filter-item" />
        </el-col>
        <el-col :span="4">
          <el-input v-model="filter.unit" placeholder="单元" clearable class="filter-item" />
        </el-col>
      </el-row>
      <el-row class="filter-row" :gutter="10">
        <el-col :span="4">
          <el-input v-model="filter.floor" placeholder="楼层" clearable class="filter-item" />
        </el-col>
        <el-col :span="4">
          <el-input v-model="filter.roomNumber" placeholder="房号" clearable class="filter-item" />
        </el-col>
        <el-col :span="6">
          <el-date-picker
            v-model="filter.publishDateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="发布开始日期"
            end-placeholder="发布结束日期"
            value-format="yyyy-MM-dd"
            class="filter-item"
          />
        </el-col>
        <el-col :span="2">
          <el-button type="primary" :loading="searchLoading" @click="searchNotifications">查询</el-button>
        </el-col>
        <el-col :span="2" style="text-align: right;">
          <el-button type="primary" @click="addNotification">添加房间通知</el-button>
        </el-col>
      </el-row>

      <el-table :data="notificationList" style="width: 100%" v-loading="loading">
        <el-table-column prop="title" label="标题"/>
        <el-table-column prop="content" label="内容"/>
        <el-table-column prop="publishDate" label="发布时间" width="150">
          <template #default="scope">
            {{ formatDate(scope.row.publishDate) }}
          </template>
        </el-table-column>
        <el-table-column prop="validUntil" label="有效期至" width="150">
          <template #default="scope">
            {{ formatDate(scope.row.validUntil) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" link size="small" @click="editNotification(scope.row)">编辑</el-button>
            <el-button type="danger" link size="small" @click="deleteNotification(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
            background
            layout="total, prev, pager, next, sizes, jumper"
            :total="total"
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            @current-change="handlePageChange"
            @size-change="handleSizeChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';
import {ElMessage} from 'element-plus';
import {useRouter} from 'vue-router'; // 引入 useRouter

export default {
  name: 'RoomNotificationList',
  setup() {
    const router = useRouter(); // 获取 router 实例
    return {
      router,
    };
  },
  data() {
    return {
      loading: false,
      searchLoading: false, // 控制查询按钮的 loading 状态
      filter: {
        title: '',
        region: '',
        building: '',
        unit: '',
        floor: '',
        roomNumber: '',
        publishDateRange: null,
      },
      notificationList: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      exampleNotifications: [
        {
          title: '示例通知1',
          content: '这是一个示例通知的内容，用于在数据加载失败时展示。',
          publishDate: '2024-11-01',
          validUntil: '2024-12-01',
        },
        {
          title: '示例通知2',
          content: '这是另一个示例通知的内容，用于在数据加载失败时展示。',
          publishDate: '2024-11-05',
          validUntil: '2024-12-05',
        },
      ],
    };
  },
  watch: {
    // eslint-disable-next-line no-unused-vars
    'filter.publishDateRange'(newVal) {
      // 可以根据需要处理日期范围
    },
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    },
    addNotification() {
      // 使用 vue-router 进行页面跳转
      this.router.push('/room-notifications/add');
      // 或者使用弹窗
      // console.log('打开添加房间通知弹窗');
    },
    async fetchNotifications() {
      this.loading = true;
      try {
        const params = {
          page: this.currentPage,
          size: this.pageSize,
          title: this.filter.title,
          region: this.filter.region,
          building: this.filter.building,
          unit: this.filter.unit,
          floor: this.filter.floor,
          roomNumber: this.filter.roomNumber,
        };
        if (this.filter.publishDateRange) {
          params.startDate = this.filter.publishDateRange[0];
          params.endDate = this.filter.publishDateRange[1];
        }
        const response = await axios.get('/api/room-notifications', {params});
        this.notificationList = response.data.records;
        this.total = response.data.total;
      } catch (error) {
        console.error('获取房间通知失败:', error);
        this.notificationList = [...this.exampleNotifications];
        this.total = this.exampleNotifications.length;
        ElMessage.error('获取房间通知数据失败，已展示示例数据。');
      } finally {
        this.loading = false;
      }
    },
    searchNotifications() {
      this.currentPage = 1;
      this.fetchNotifications();
    },
    handlePageChange(newPage) {
      this.currentPage = newPage;
      this.fetchNotifications();
    },
    handleSizeChange(newSize) {
      this.pageSize = newSize;
      this.currentPage = 1;
      this.fetchNotifications();
    },
    editNotification(row) {
      console.log('编辑通知:', row);
      // 跳转到编辑页面，传递通知 ID
      this.router.push(`/room-notifications/edit/${row.id}`);
    },
    async deleteNotification(row) {
      try {
        await axios.delete(`/api/room-notifications/${row.id}`);
        ElMessage.success('删除通知成功');
        this.fetchNotifications(); // 刷新列表
      } catch (error) {
        console.error('删除通知失败:', error);
        ElMessage.error('删除通知失败');
      }
    },
  },
  mounted() {
    this.fetchNotifications();
  },
};
</script>

<style scoped>
.filter-row {
  margin-bottom: 15px;
}

.filter-item {
  width: 100%;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style>
