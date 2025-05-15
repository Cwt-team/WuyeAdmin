<template>
  <el-breadcrumb separator="/">
    <el-breadcrumb-item v-for="(item, index) in breadcrumbs" :key="index" :to="item.path">
      {{ item.title }}
    </el-breadcrumb-item>
  </el-breadcrumb>
</template>

<script>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

export default {
  name: 'AppBreadcrumb',
  setup() {
    const route = useRoute()
    const breadcrumbs = ref([])

    // 生成面包屑数据
    const getBreadcrumbs = () => {
      // 始终有仪表盘作为第一项
      breadcrumbs.value = [
        {
          path: '/dashboard',
          title: '首页'
        }
      ]

      // 当前路由匹配信息
      const matched = route.matched.filter(item => item.meta && item.meta.title)
      
      if (matched.length > 0) {
        matched.forEach(item => {
          breadcrumbs.value.push({
            path: item.path,
            title: item.meta.title
          })
        })
      }
    }

    // 初始化
    getBreadcrumbs()

    // 监听路由变化
    watch(() => route.path, () => {
      getBreadcrumbs()
    })

    return {
      breadcrumbs
    }
  }
}
</script>

<style scoped>
.el-breadcrumb {
  font-size: 14px;
  line-height: 60px;
}
</style>