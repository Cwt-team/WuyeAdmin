<template>
  <div class="complaint-suggestion-container">
    <div class="breadcrumb">
      <span>首页</span> / <span>区域维护管理</span> / <span>投诉建议</span>
    </div>
    <h1>投诉建议</h1>
    <div class="filter-row">
      <el-form :inline="true" :model="filters" class="search-form">
        <el-form-item>
          <el-select 
            v-model="filters.community" 
            placeholder="选择社区" 
            clearable
            filterable
          >
            <el-option 
              v-for="item in communities" 
              :key="item.id" 
              :label="item.name"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-select v-model="filters.type" placeholder="选择类型" clearable>
            <el-option label="投诉" value="complaint"></el-option>
            <el-option label="建议" value="suggestion"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-select v-model="filters.status" placeholder="选择状态" clearable>
            <el-option label="待处理" value="pending"></el-option>
            <el-option label="处理中" value="processing"></el-option>
            <el-option label="已完成" value="completed"></el-option>
            <el-option label="已驳回" value="rejected"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-date-picker
            v-model="filters.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
          ></el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-table :data="items" style="width: 100%" border>
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="communityName" label="社区名称">
        <template #default="scope">
          {{ scope.row.communityName || '未知社区' }}
        </template>
      </el-table-column>
      <el-table-column prop="userName" label="用户名">
        <template #default="scope">
          {{ scope.row.userName || '未知用户' }}
        </template>
      </el-table-column>
      <el-table-column prop="type" label="类型">
        <template #default="scope">
          <el-tag :type="scope.row.type === 'complaint' ? 'danger' : 'primary'">
            {{ scope.row.type === 'complaint' ? '投诉' : '建议' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="content" label="内容" show-overflow-tooltip></el-table-column>
      <el-table-column prop="createdAt" label="提交时间"></el-table-column>
      <el-table-column prop="status" label="状态">
        <template #default="scope">
          <el-tag :type="getStatusType(scope.row.status)">
            {{ getStatusText(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button type="primary" size="small" @click="handleProcess(scope.row)">处理</el-button>
          <el-button type="info" size="small" @click="handleDetail(scope.row)">详情</el-button>
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
  </div>
</template>

<script>
export default {
  name: 'ComplaintSuggestionPage',
  data() {
    return {
      items: [],
      communities: [],
      filters: {
        community: '',
        type: '',
        status: '',
        dateRange: [],
        startDate: '',
        endDate: ''
      },
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      }
    };
  },
  methods: {
    getStatusType(status) {
      const typeMap = {
        'pending': 'warning',
        'processing': 'primary',
        'completed': 'success',
        'rejected': 'danger'
      };
      return typeMap[status] || 'info';
    },
    
    getStatusText(status) {
      const statusMap = {
        'pending': '待处理',
        'processing': '处理中',
        'completed': '已完成',
        'rejected': '已驳回'
      };
      return statusMap[status] || status;
    },

    handleDetail(row) {
      console.log('查看详情:', row);
      this.$message.info('查看详情');
    },
    handleSizeChange(size) {
      this.pagination.pageSize = size;
      this.fetchData();
    },
    handleCurrentChange(page) {
      this.pagination.currentPage = page;
      this.fetchData();
    },
    handleSearch() {
      this.pagination.currentPage = 1;
      this.fetchData();
    },
    resetFilters() {
      this.filters = {
        community: '',
        type: '',
        status: '',
        dateRange: [],
        startDate: '',
        endDate: ''
      };
      this.handleSearch();
    },
    async fetchData() {
      try {
        // 处理日期范围
        if (this.filters.dateRange && this.filters.dateRange.length === 2) {
          [this.filters.startDate, this.filters.endDate] = this.filters.dateRange;
        }

        const params = {
          communityId: this.filters.community,
          type: this.filters.type,
          status: this.filters.status,
          startDate: this.filters.startDate,
          endDate: this.filters.endDate,
          page: this.pagination.currentPage,
          size: this.pagination.pageSize
        };

        const response = await this.$axios.get('/api/complaints', { params });
        
        if (response.data.code === 200) {
          this.items = response.data.items;
          this.pagination.total = response.data.total;
        } else {
          this.$message.error(response.data.message || '获取数据失败');
        }
      } catch (error) {
        console.error('获取投诉建议数据失败:', error);
        this.$message.error('获取投诉建议数据失败');
      }
    },
    async handleProcess(row) {
      try {
        if (row.status === 'completed' || row.status === 'rejected') {
          this.$message.info('此项已处理完成');
          return;
        }

        // 打开处理对话框
        const { value: formData } = await this.$prompt('请输入处理回复', '处理投诉建议', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputType: 'textarea',
          inputPlaceholder: '请输入处理回复内容'
        });

        if (formData) {
          // 更新状态为已完成并提交回复
          await this.$axios.put(`/api/complaints/${row.id}/status`, {
            status: 'completed'
          });

          await this.$axios.post(`/api/complaints/${row.id}/reply`, {
            reply: formData
          });

          this.$message.success('处理成功');
          await this.fetchData(); // 刷新数据
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('处理失败:', error);
          this.$message.error('处理失败');
        }
      }
    },
    async fetchCommunities() {
      try {
        const response = await this.$axios.get('/api/complaints/communities');
        if (response.data.code === 200) {
          this.communities = response.data.items;
        } else {
          this.$message.error(response.data.message || '获取社区列表失败');
        }
      } catch (error) {
        console.error('获取社区列表失败:', error);
        this.$message.error('获取社区列表失败');
      }
    }
  },
  async mounted() {
    await this.fetchCommunities();
    await this.fetchData();
  }
};
</script>

<style scoped>
.complaint-suggestion-container {
  padding: 20px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.breadcrumb {
  margin-bottom: 15px;
  font-size: 14px;
  color: #606266;
}

h1 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #303133;
}

.filter-row {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.search-form {
  width: 100%;
}

.filter-row .el-form-item {
  margin-bottom: 15px;
  margin-right: 15px;
}

.filter-row .el-select {
  width: 160px;
}

.filter-row .el-date-picker {
  width: 320px;
}
</style> 