<template>
  <div>
    <el-table :data="requests" style="width: 100%">
      <el-table-column prop="request_number" label="报修单号" width="120" />
      <el-table-column prop="reporter_name" label="报修人" width="100" />
      <el-table-column prop="reporter_phone" label="联系电话" width="120" />
      <el-table-column prop="houseName" label="房屋位置" width="180" />
      <el-table-column prop="title" label="报修标题" />
      <el-table-column prop="description" label="问题描述" />
      <el-table-column prop="reportTime" label="报修时间" width="160" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="getStatusType(scope.row.status)">
            {{ getStatusText(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="scope">
          <el-button type="primary" size="small" @click="handleEdit(scope.row)">处理</el-button>
          <el-button type="info" size="small" @click="handleDetail(scope.row)">详情</el-button>
        </template>
      </el-table-column>
    </el-table>

  </div>
</template>

<script>
import axios from 'axios';  // 导入 axios

export default {
  data() {
    return {
      requests: []
    }
  },
  async created() {
    await this.fetchRequests()
  },
  methods: {
    async fetchRequests() {
      try {
        const response = await axios.get('/api/maintenance-requests')
        this.requests = response.data.items
      } catch (error) {
        console.error('获取报事报修列表失败:', error)
        this.$message.error('获取报事报修列表失败')
      }
    },
    handleEdit(row) {
      console.log('处理报修请求:', row)
      this.$message.success('处理成功')
    },
    getStatusText(status) {
      const statusMap = {
        'pending': '待处理',
        'processing': '处理中',
        'completed': '已完成',
        'cancelled': '已取消'
      }
      return statusMap[status] || status
    },
    getStatusType(status) {
      const typeMap = {
        'pending': 'warning',
        'processing': 'primary',
        'completed': 'success',
        'cancelled': 'info'
      }
      return typeMap[status] || ''
    },
    handleDetail(row) {
      // 显示详情对话框
      this.currentRequest = row
      this.detailDialogVisible = true
    }
  }
}
</script> 