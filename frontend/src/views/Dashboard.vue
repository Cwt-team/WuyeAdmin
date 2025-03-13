<template>
  <div>
    <!-- 保持模板内容不变 -->
  </div>
</template>

<script>
export default {
  name: 'DashboardView',
  data() {
    return {
      activeMenu: ''
    }
  },
  mounted() {
    // 保持原有逻辑
  },
  methods: {
    handleMenuSelect(index) {
      // 简化菜单选择逻辑以避免错误
      console.log('选择菜单项:', index)
      if (index === 'area-maintenance') {
        this.$router.push({ name: 'AreaMaintenance' })
      }
    }
  }
}
</script>

<style>
/* 保持样式不变 */
</style> 