<template>
  <div class="house-detail">
    <div v-if="loading" class="loading-spinner">
      <i class="el-icon-loading"></i>
    </div>

    <div v-else>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/dashboard' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>房产详情</el-breadcrumb-item>
      </el-breadcrumb>

      <el-card class="detail-card">
        <div class="detail-header">
          <h2>{{ houseInfo.name }}</h2>
          <el-tag type="success">{{ houseInfo.status }}</el-tag>
        </div>

        <el-row :gutter="20" class="detail-content">
          <el-col :span="8">
            <div class="detail-item">
              <label>房产层级：</label>
              <span>{{ houseInfo.level }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="detail-item">
              <label>户型：</label>
              <span>{{ houseInfo.layout }}</span>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="detail-item">
              <label>创建时间：</label>
              <span>{{ houseInfo.createTime }}</span>
            </div>
          </el-col>
        </el-row>

        <el-divider></el-divider>

        <div class="action-buttons">
          <el-button type="primary" @click="handleEdit">编辑</el-button>
          <el-button type="danger" @click="handleDelete">删除</el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loading: true,
      houseInfo: {
        id: '',
        name: '',
        level: '',
        layout: '',
        createTime: '',
        status: ''
      }
    }
  },
  async created() {
    await this.fetchHouseDetail()
  },
  methods: {
    async fetchHouseDetail() {
      try {
        const houseId = this.$route.params.id
        // 这里调用API获取房产详情
        // const response = await this.$http.get(`/houses/${houseId}`)
        // this.houseInfo = response.data
        
        // 模拟数据
        this.houseInfo = {
          id: houseId,
          name: '阳光小区 1栋 101',
          level: '1栋/1单元/101',
          layout: '三室一厅',
          createTime: '2023-01-15',
          status: '已出租'
        }
        
        this.loading = false
      } catch (error) {
        this.$message.error('获取房产详情失败')
        console.error(error)
      }
    },
    handleEdit() {
      // 编辑逻辑
    },
    handleDelete() {
      // 删除逻辑
    }
  }
}
</script>

<style scoped>
.house-detail {
  padding: 20px;
}

.loading-spinner {
  text-align: center;
  padding: 50px;
}

.detail-card {
  margin-top: 20px;
}

.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.detail-content {
  margin-top: 20px;
}

.detail-item {
  margin-bottom: 15px;
}

.detail-item label {
  font-weight: bold;
  margin-right: 10px;
}

.action-buttons {
  text-align: right;
  margin-top: 20px;
}
</style>
