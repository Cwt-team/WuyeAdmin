<template>
  <div class="not-found">
    <div class="content">
      <h1>404</h1>
      <h3>页面不存在</h3>
      <p>抱歉，您访问的页面不存在或已被移除</p>
      <el-button type="primary" @click="goHome">返回首页</el-button>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'

export default {
  name: 'NotFoundView',
  setup() {
    const router = useRouter()
    
    const goHome = () => {
      router.push('/dashboard')
    }
    
    return {
      goHome
    }
  }
}
</script>

<style scoped>
.not-found {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  min-height: 500px;
}

.content {
  text-align: center;
}

h1 {
  font-size: 120px;
  margin: 0;
  color: #409EFF;
  line-height: 1.2;
}

h3 {
  font-size: 30px;
  margin: 20px 0;
  color: #606266;
}

p {
  color: #909399;
  margin-bottom: 30px;
}
</style> 