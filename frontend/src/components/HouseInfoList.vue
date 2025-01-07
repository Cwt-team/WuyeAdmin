<template>
  <div class="house-info-list">
    <el-card>
      <el-row>
        <el-col :span="24">
          <el-input v-model="search" placeholder="搜索房屋信息" class="filter-item" />
          <el-button type="primary" @click="searchHouse">搜索</el-button>
        </el-col>
      </el-row>
      <el-table :data="houseList" style="width: 100%" class="house-table">
        <el-table-column prop="houseNumber" label="房屋编号" />
        <el-table-column prop="owner" label="业主" />
        <el-table-column prop="area" label="面积" />
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
  name: 'HouseInfoList',
  data() {
    return {
      search: '',
      houseList: [
        {
          houseNumber: 'A-101',
          owner: '张三',
          area: '120㎡',
          status: 'occupied',
        },
        {
          houseNumber: 'B-202',
          owner: '李四',
          area: '150㎡',
          status: 'unoccupied',
        },
      ],
      total: 2,
      currentPage: 1,
      pageSize: 10,
    };
  },
  methods: {
    async fetchHouses() {
      try {
        const response = await axios.get('/api/houses', {
          params: {
            search: this.search,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        this.houseList = response.data.houses;
        this.total = response.data.total;
      } catch (error) {
        console.error('获取房屋信息失败:', error);
      }
    },
    searchHouse() {
      this.currentPage = 1;
      this.fetchHouses();
    },
    async handlePageChange(page) {
      this.currentPage = page;
      this.fetchHouses();
    },
    formatStatus(row, column, cellValue) {
      return cellValue === 'occupied' ? '已入住' : '未入住';
    },
    viewDetails(row) {
      console.log('查看详情:', row);
      // 可以添加查看详情的逻辑
    },
  },
  mounted() {
    this.fetchHouses();
  },
};
</script>

<style scoped>
.filter-item {
  margin-right: 20px;
}

.house-table {
  margin-top: 20px;
}

.el-card {
  padding: 20px;
}
</style>
