<template>
  <div class="owner-info-list">
    <el-card>
      <el-row class="filter-row">
        <el-col :span="4">
          <el-input v-model="filter.room" placeholder="房号" class="filter-item" />
        </el-col>
        <el-col :span="4">
          <el-input v-model="filter.name" placeholder="姓名或手机号" class="filter-item" />
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="searchOwners">查询</el-button>
        </el-col>
        <el-col :span="4">
          <el-button type="success" @click="exportTemplate">导出模版</el-button>
        </el-col>
        <el-col :span="4">
          <el-button type="warning" @click="exportOwners">导出业主</el-button>
        </el-col>
        <el-col :span="4">
          <el-upload
            action="/api/owners/import"
            :show-file-list="false"
            :before-upload="beforeUpload"
            :on-success="handleImportSuccess"
            :on-error="handleImportError"
          >
            <el-button type="info">导入业主</el-button>
          </el-upload>
        </el-col>
      </el-row>

      <el-table :data="ownerList" style="width: 100%">
        <el-table-column prop="room" label="房间信息" />
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="gender" label="性别" />
        <el-table-column prop="idCard" label="身份证号" />
        <el-table-column prop="phone" label="手机号" />
        <el-table-column prop="remark" label="备注" />
        <el-table-column prop="ownerType" label="业主类型" />
        <el-table-column prop="updateTime" label="更新时间" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="text" size="small" @click="editOwner(scope.row)">编辑</el-button>
            <el-button type="text" size="small" @click="deleteOwner(scope.row)">删除</el-button>
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
  name: 'OwnerInfoList',
  data() {
    return {
      filter: {
        room: '',
        name: '',
      },
      ownerList: [
        {
          room: '栋-1单元-0101',
          name: '张三',
          gender: '男',
          idCard: '123456789012345678',
          phone: '13712345678',
          remark: '',
          ownerType: '业主',
          updateTime: '2024-07-30 10:24:58',
        },
        {
          room: '栋-1单元-0201',
          name: '李四',
          gender: '男',
          idCard: '987654321098765432',
          phone: '13787654321',
          remark: '',
          ownerType: '业主',
          updateTime: '2024-08-03 12:45:30',
        },
      ],
      total: 2,
      currentPage: 1,
      pageSize: 10,
    };
  },
  methods: {
    async fetchOwners() {
      try {
        const response = await axios.get('/api/owners', {
          params: {
            room: this.filter.room,
            name: this.filter.name,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        this.ownerList = response.data.owners;
        this.total = response.data.total;
      } catch (error) {
        console.error('获取业主信息失败:', error);
      }
    },
    searchOwners() {
      this.currentPage = 1;
      this.fetchOwners();
    },
    handlePageChange(page) {
      this.currentPage = page;
      this.fetchOwners();
    },
    editOwner(row) {
      console.log('编辑业主:', row);
    },
    deleteOwner(row) {
      console.log('删除业主:', row);
    },
    exportTemplate() {
      window.location.href = '/api/owners/export-template';
    },
    exportOwners() {
      const params = new URLSearchParams({
        room: this.filter.room,
        name: this.filter.name
      });
      window.location.href = `/api/owners/export?${params.toString()}`;
    },
    beforeUpload(file) {
      const isCSV = file.type === 'text/csv';
      if (!isCSV) {
        this.$message.error('只能上传CSV文件');
      }
      return isCSV;
    },
    handleImportSuccess(response) {
      if (response.success) {
        this.$message.success('导入成功');
        this.fetchOwners();
      } else {
        this.$message.error(response.message || '导入失败');
      }
    },
    handleImportError(error) {
      this.$message.error(error.message || '导入失败');
    },
  },
  mounted() {
    this.fetchOwners();
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
