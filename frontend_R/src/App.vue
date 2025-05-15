<template>
  <router-view v-slot="{ Component }">
    <transition name="fade" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f7fa;
  color: #303133;
}

#app {
  height: 100%;
}

/* 按钮、卡片等元素的统一过渡效果 */
.el-button, .el-card, .el-menu-item, .el-select, .el-input, .el-pagination__sizes {
  transition: all 0.3s;
}

/* 设置卡片内容区域内边距 */
.el-card__body {
  padding: 20px;
}
</style> 