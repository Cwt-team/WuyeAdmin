<template>
  <div class="community-notice-list">
    <el-card>
      <el-row class="filter-row" :gutter="20">
        <el-col :span="6">
          <el-input v-model="filter.title" placeholder="标题" clearable class="filter-item" />
        </el-col>
        <el-col :span="6">
          <el-date-picker
            v-model="filter.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
            class="filter-item"
          />
        </el-col>
        <el-col :span="2">
          <el-button type="primary" :loading="loading" @click="searchNotices">查询</el-button>
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="addNotice">小区通知</el-button>
        </el-col>
      </el-row>

      <el-table :data="noticeList" style="width: 100%" v-loading="loading">
        <el-table-column prop="title" label="标题"/>
        <el-table-column prop="content" label="内容"/>
        <el-table-column prop="displayStartTime" label="展示开始时间" width="180"/>
        <el-table-column prop="displayEndTime" label="展示结束时间" width="180"/>
        <el-table-column prop="createdAt" label="发送时间" width="180"/>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" link @click="editNotice(scope.row)">编辑</el-button>
            <el-button type="danger" link @click="deleteNotice(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          background
          layout="total, prev, pager, next, sizes"
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
import axios from 'axios'

export default {
  name: 'CommunityNotice',
  data() {
    return {
      loading: false,
      filter: {
        title: '',
        dateRange: null
      },
      noticeList: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      // 示例数据
      mockData: [
        {
          id: 1,
          title: '杀虫',
          content: '请住户关好门窗',
          displayStartTime: '2024-08-05',
          displayEndTime: '2024-08-06',
          createdAt: '2024-08-03 04:38:51'
        },
        {
          id: 2,
          title: '暴雨预警',
          content: '天气预报',
          displayStartTime: '2024-07-30',
          displayEndTime: '2024-07-31',
          createdAt: '2024-07-30 11:36:07'
        }
      ]
    }
  },
  methods: {
    async fetchNotices() {
      this.loading = true
      try {
        const params = {
          title: this.filter.title,
          page: this.currentPage,
          size: this.pageSize
        }
        if (this.filter.dateRange) {
          params.startDate = this.filter.dateRange[0]
          params.endDate = this.filter.dateRange[1]
        }
        const response = await axios.get('/api/community-notices', { params })
        this.noticeList = response.data.records
        this.total = response.data.total
        this.$message.success('获取数据成功')
      } catch (error) {
        console.error('获取小区通知失败:', error)
        this.$message.warning('获取数据库失败，已展示示例数据')
        this.noticeList = this.mockData
        this.total = this.mockData.length
      } finally {
        this.loading = false
      }
    },

    searchNotices() {
      this.currentPage = 1
      this.fetchNotices()
    },

    handlePageChange(page) {
      this.currentPage = page
      this.fetchNotices()
    },

    handleSizeChange(size) {
      this.pageSize = size
      this.currentPage = 1
      this.fetchNotices()
    },

    addNotice() {
      this.$router.push('/community-notices/add')
    },

    editNotice(row) {
      this.$router.push(`/community-notices/edit/${row.id}`)
    },

    async deleteNotice(row) {
      try {
        await this.$confirm('确认删除该通知?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        await axios.delete(`/api/community-notices/${row.id}`)
        this.$message.success('删除成功')
        this.fetchNotices()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除通知失败:', error)
          this.$message.error('删除失败')
        }
      }
    }
  },
  mounted() {
    this.fetchNotices()
  }
}
</script>

<style scoped>
.community-notice-list {
  padding: 20px;
}

.filter-row {
  margin-bottom: 20px;
}

.filter-item {
  width: 100%;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style>
