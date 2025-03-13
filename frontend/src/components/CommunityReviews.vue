<template>
  <div>
    <el-table :data="reviews" style="width: 100%">
      <el-table-column prop="id" label="ID" width="100" />
      <el-table-column prop="rating" label="评分" />
      <el-table-column prop="comment" label="评论" />
      <el-table-column label="操作">
        <template #default="scope">
          <el-button type="primary" size="small" @click="handleReply(scope.row)">回复</el-button>
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
      reviews: []
    }
  },
  async created() {
    await this.fetchReviews()
  },
  methods: {
    async fetchReviews() {
      try {
        const response = await axios.get('/api/community-reviews')
        this.reviews = response.data.items
      } catch (error) {
        console.error('获取社区评价列表失败:', error)
        this.$message.error('获取社区评价列表失败')
      }
    },
    handleReply(row) {
      console.log('回复评价:', row)
      this.$message.success('回复成功')
    }
  }
}
</script> 