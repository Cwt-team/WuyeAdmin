<template>
  <div class="access-card-list">
    <el-card>
      <el-row class="filter-row">
        <el-col :span="4">
          <el-input v-model="filter.cardNumber" placeholder="卡号" class="filter-item" />
        </el-col>
        <el-col :span="4">
          <el-input v-model="filter.ownerName" placeholder="业主姓名" class="filter-item" />
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="searchCards">查询</el-button>
        </el-col>
      </el-row>

      <el-table :data="cardList" style="width: 100%">
        <el-table-column prop="cardNumber" label="卡号" />
        <el-table-column prop="ownerName" label="业主姓名" />
        <el-table-column prop="status" label="状态" />
        <el-table-column prop="issueDate" label="发卡日期" />
        <el-table-column prop="expirationDate" label="到期日期" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="text" size="small" @click="editCard(scope.row)">编辑</el-button>
            <el-button type="text" size="small" @click="deleteCard(scope.row)">删除</el-button>
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
  name: 'AccessCardList',
  data() {
    return {
      filter: {
        cardNumber: '',
        ownerName: '',
      },
      cardList: [
        {
          cardNumber: '卡号12345',
          ownerName: '李四',
          status: '有效',
          issueDate: '2024-01-01',
          expirationDate: '2024-12-31',
        },
        {
          cardNumber: '卡号67890',
          ownerName: '王五',
          status: '无效',
          issueDate: '2023-01-01',
          expirationDate: '2023-12-31',
        },
      ],
      total: 2,
      currentPage: 1,
      pageSize: 10,
    };
  },
  methods: {
    async fetchCards() {
      try {
        const response = await axios.get('/api/access-cards', {
          params: {
            cardNumber: this.filter.cardNumber,
            ownerName: this.filter.ownerName,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        this.cardList = response.data.cards;
        this.total = response.data.total;
      } catch (error) {
        console.error('获取门禁卡信息失败:', error);
      }
    },
    searchCards() {
      this.currentPage = 1;
      this.fetchCards();
    },
    handlePageChange(page) {
      this.currentPage = page;
      this.fetchCards();
    },
    editCard(row) {
      console.log('编辑门禁卡:', row);
    },
    deleteCard(row) {
      console.log('删除门禁卡:', row);
    },
  },
  mounted() {
    this.fetchCards();
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
