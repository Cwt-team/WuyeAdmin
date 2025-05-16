<template>
  <router-view v-slot="{ Component }">
    <transition name="fade" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: 'Noto Sans SC', 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: var(--bg-color);
  background-image: 
    radial-gradient(#e0e8f5 1px, transparent 1px),
    radial-gradient(#e0e8f5 1px, transparent 1px);
  background-size: 40px 40px;
  background-position: 0 0, 20px 20px;
  color: var(--text-primary);
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

/* 添加全局按钮样式 */
.action-button {
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
}

.action-button-primary {
  background: var(--primary-gradient);
  color: white;
  border: none;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.25);
}

/* 添加全局标签式样 */
.tag-label {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

/* 添加页面内容容器样式 */
.page-container {
  padding: 20px;
  animation: fade-in 0.3s;
}

/* 添加图标色彩类 */
.icon-primary { color: var(--primary-color); }
.icon-success { color: #67c23a; }
.icon-warning { color: #e6a23c; }
.icon-danger { color: #f56c6c; }
.icon-info { color: #909399; }
</style> 