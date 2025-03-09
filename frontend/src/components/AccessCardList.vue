<template>
  <div class="access-card-list">
    <el-card>
      <el-row class="filter-row" :gutter="10">
        <el-col :span="4">
          <el-select v-model="filter.region" placeholder="区域" style="width: 100%">
            <el-option label="全部" value=""></el-option>
            <el-option label="1545 墨轩科技" value="1545 墨轩科技"></el-option>
            <!-- 实际项目中从接口获取 -->
          </el-select>
        </el-col>
        <el-col :span="3">
          <el-select v-model="filter.building" placeholder="栋" style="width: 100%">
            <el-option label="全部" value=""></el-option>
            <el-option label="1栋" value="1"></el-option>
            <!-- 实际项目中根据区域联动获取 -->
          </el-select>
        </el-col>
        <el-col :span="3">
          <el-select v-model="filter.unit" placeholder="单元" style="width: 100%">
            <el-option label="全部" value=""></el-option>
            <el-option label="1单元" value="1"></el-option>
            <!-- 实际项目中根据栋联动获取 -->
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-input v-model="filter.room" placeholder="房间号" clearable class="filter-item" />
        </el-col>
        <el-col :span="4">
          <el-input v-model="filter.cardNumber" placeholder="卡号" clearable class="filter-item" />
        </el-col>
        <el-col :span="4">
          <el-input v-model="filter.ownerName" placeholder="业主姓名" clearable class="filter-item" />
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="searchCards">查询</el-button>
        </el-col>
      </el-row>

      <el-row class="action-row" style="margin-bottom: 15px;">
        <el-col>
          <el-button type="success" @click="addNewCard">发放新卡</el-button>
          <el-button type="warning" @click="voidCard" :disabled="multipleSelection.length === 0">作废卡</el-button>
          <el-button type="danger" @click="batchDeleteCards" :disabled="multipleSelection.length === 0">批量删除</el-button>
          <el-button @click="importCards">导入</el-button>
        </el-col>
      </el-row>

      <el-table
        ref="multipleTable"
        :data="cardList"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="cardNumber" label="卡号" />
        <el-table-column prop="ownerName" label="持有者" />
        <el-table-column prop="roomInfo" label="房间信息" >
          <template #default="scope">{{ getRoomInfo(scope.row) }}</template>
        </el-table-column>
        <el-table-column prop="cardType" label="类型" />
        <el-table-column prop="status" label="状态" />
        <el-table-column prop="validityStart" label="有效日期" >
          <template #default="scope">{{ formatDate(scope.row.validityStart) }}</template>
        </el-table-column>
        <el-table-column prop="validityEnd" label="到期日期" >
          <template #default="scope">{{ formatDate(scope.row.validityEnd) }}</template>
        </el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="text" size="small" @click="editCard(scope.row)">编辑</el-button>
            <el-button type="text" size="small" @click="deleteCard(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          background
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          @current-change="handleCurrentChange"
          @size-change="handleSizeChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';
import { formatDate } from '@/utils/date'; // 假设你有一个日期格式化工具

export default {
  name: 'AccessCardList',
  components: {},
  data() {
    return {
      filter: {
        region: '',
        building: '',
        unit: '',
        room: '',
        cardNumber: '',
        ownerName: '',
      },

      cardList: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      multipleSelection: [],
      loading: false,
      // 示例数据，当接口错误时展示
      exampleCardList: [
        {
          id: 'example1',
          cardNumber: 'E-12345',
          ownerName: '示例业主A',
          region: '示例区域',
          building: '1栋',
          unit: '1单元',
          room: '101',
          cardType: '住户卡',
          status: '有效',
          validityStart: '2024-08-01T00:00:00',
          validityEnd: '2025-07-31T23:59:59',
        },
        {
          id: 'example2',
          cardNumber: 'E-67890',
          ownerName: '示例业主B',
          region: '示例区域',
          building: '2栋',
          unit: '2单元',
          room: '205',
          cardType: '访客卡',
          status: '无效',
          validityStart: '2023-07-01T00:00:00',
          validityEnd: '2023-07-31T23:59:59',
        },
      ],
    };
  },

  computed: {},
  watch: {},
  created() {
    this.fetchCards();
  },

  mounted() {},
  methods: {
    formatDate,
    getRoomInfo(row) {
      return `${row.region || ''} ${row.building || ''}栋 ${row.unit || ''}单元 ${row.room || ''}`;
    },

    handleSelectionChange(val) {
      this.multipleSelection = val;
    },

    handleCurrentChange(newPage) {
      this.currentPage = newPage;
      this.fetchCards();
    },

    handleSizeChange(newSize) {
      this.pageSize = newSize;
      this.currentPage = 1;
      this.fetchCards();
    },

    async fetchCards() {
      this.loading = true;
      try {
        const response = await axios.get('/api/access-cards', { // 替换为你的实际接口地址
          params: {
            region: this.filter.region,
            building: this.filter.building,
            unit: this.filter.unit,
            room: this.filter.room,
            cardNumber: this.filter.cardNumber,
            ownerName: this.filter.ownerName,
            page: this.currentPage,
            size: this.pageSize,
          },
        });

        if (response.status === 200) {
          this.cardList = response.data.items; // 根据你的后端返回数据结构调整
          this.total = response.data.total;   // 根据你的后端返回数据结构调整
        } else {
          this.$message.error('获取门禁卡信息失败');
          this.cardList = this.exampleCardList;
          this.total = this.exampleCardList.length;
        }
      } catch (error) {
        console.error('获取门禁卡信息出错:', error);
        this.$message.error('获取门禁卡信息出错，已展示示例数据');
        this.cardList = this.exampleCardList;
        this.total = this.exampleCardList.length;
      } finally {
        this.loading = false;
      }
    },

    searchCards() {
      this.currentPage = 1;
      this.fetchCards();
    },

    addNewCard() {
      console.log('发放新卡');
      // TODO: 实现发放新卡逻辑，可以打开一个弹窗或跳转到新页面
    },

    voidCard() {
      if (this.multipleSelection.length > 0) {
        const cardIds = this.multipleSelection.map(item => item.id); // 假设你的数据中有 id 字段
        console.log('作废卡:', cardIds);
        // TODO: 调用后端接口作废选中的卡
      }
    },

    batchDeleteCards() {
      if (this.multipleSelection.length > 0) {
        const cardIds = this.multipleSelection.map(item => item.id); // 假设你的数据中有 id 字段
        console.log('批量删除卡:', cardIds);
        // TODO: 调用后端接口删除选中的卡
      }
    },

    importCards() {
      console.log('导入卡');
      // TODO: 实现导入卡逻辑，可以打开一个文件选择器
    },

    editCard(row) {
      console.log('编辑门禁卡:', row);
      // TODO: 实现编辑门禁卡逻辑，可以打开一个弹窗或跳转到编辑页面
    },

    deleteCard(row) {
      console.log('删除门禁卡:', row);
      // TODO: 调用后端接口删除该卡

    },
  },
};
</script>

<style scoped>
.filter-row {
  margin-bottom: 15px;
}

.filter-item {
  margin-right: 10px;
}

.action-row {
  margin-bottom: 15px;
}

.pagination-container {
  margin-top: 15px;
  text-align: right;
}
</style>
