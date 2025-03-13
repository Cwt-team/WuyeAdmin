<template>
  <div>
    <el-table :data="requests" style="width: 100%">
      <el-table-column prop="id" label="ID" width="100" />
      <el-table-column prop="description" label="问题描述" />
      <el-table-column prop="status" label="状态" />
      <el-table-column label="操作">
        <template #default="scope">
          <el-button type="primary" size="small" @click="handleEdit(scope.row)">处理</el-button>
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
    }
  }
}
</script> 