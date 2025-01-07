<template>
  <div class="owner-apply-list">
    <el-card>
      <el-row class="filter-row">
        <el-col :span="4">
          <el-input v-model="filter.room" placeholder="房号" class="filter-item" />
        </el-col>
        <el-col :span="4">
          <el-input v-model="filter.name" placeholder="姓名或手机号" class="filter-item" />
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="searchApplications">查询</el-button>
        </el-col>
      </el-row>

      <el-table :data="applicationList" style="width: 100%">
        <el-table-column prop="room" label="房间信息" />
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="gender" label="性别" />
        <el-table-column prop="idCard" label="身份证号" />
        <el-table-column prop="phone" label="手机号" />
        <el-table-column prop="status" label="状态" />
        <el-table-column prop="ownerType" label="业主类型" />
        <el-table-column prop="applyTime" label="申请时间" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="text" size="small" @click="viewApplication(scope.row)">查看详情</el-button>
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
  name: 'OwnerApplyList',
  data() {
    return {
      filter: {
        room: '',
        name: '',
      },
      applicationList: [
        {
          room: '栋-1单元-0101',
          name: '王五',
          gender: '女',
          idCard: '112233445566778899',
          phone: '13711223344',
          status: '待审核',
          ownerType: '业主',
          applyTime: '2024-09-01 09:30:45',
        },
      ],
      total: 1,
      currentPage: 1,
      pageSize: 10,
    };
  },
  methods: {
    async fetchApplications() {
      try {
        const response = await axios.get('/api/owner-applications', {
          params: {
            room: this.filter.room,
            name: this.filter.name,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        this.applicationList = response.data.applications;
        this.total = response.data.total;
      } catch (error) {
        console.error('获取业主申请信息失败:', error);
      }
    },
    searchApplications() {
      this.currentPage = 1;
      this.fetchApplications();
    },
    handlePageChange(page) {
      this.currentPage = page;
      this.fetchApplications();
    },
    viewApplication(row) {
      console.log('查看申请详情:', row);
    },
  },
  mounted() {
    this.fetchApplications();
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
