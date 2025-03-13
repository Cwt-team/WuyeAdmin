<template>
  <el-menu>
    <!-- 其他菜单项 -->
    <el-menu-item index="area-maintenance" @click="$router.push('/area-maintenance')">
      <i class="el-icon-s-management"></i>
      <span>区域维护管理</span>
    </el-menu-item>
  </el-menu>
</template>

<script>
export default {
  name: 'AppSidebar'
}
</script>

<style scoped>
/* 样式部分 */
</style> 