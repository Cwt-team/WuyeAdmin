<template>
  <div>
    <el-table :data="items" style="width: 100%">
      <el-table-column prop="id" label="ID" width="100" />
      <el-table-column prop="type" label="类型" />
      <el-table-column prop="content" label="内容" />
      <el-table-column label="操作">
        <template #default="scope">
          <el-button type="primary" size="small" @click="handleProcess(scope.row)">处理</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      items: []
    }
  },
  async created() {
    await this.fetchItems()
  },
  methods: {
    async fetchItems() {
      try {
        const response = await axios.get('/api/complaint-suggestions')
        this.items = response.data.items
      } catch (error) {
        console.error('获取投诉建议列表失败:', error)
        this.$message.error('获取投诉建议列表失败')
      }
    },
    handleProcess(row) {
      console.log('处理投诉建议:', row)
      this.$message.success('处理成功')
    }
  }
}
</script> 