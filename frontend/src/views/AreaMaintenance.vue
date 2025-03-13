<template>
  <div class="area-maintenance-container">
    <h1>区域维护管理</h1>
    <el-tabs v-model="activeTab" type="card">
      <el-tab-pane label="报事报修" name="maintenance">
        <MaintenanceRequests />
      </el-tab-pane>
      <el-tab-pane label="社区评价" name="reviews">
        <CommunityReviews />
      </el-tab-pane>
      <el-tab-pane label="投诉建议" name="complaints">
        <ComplaintSuggestions />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import MaintenanceRequests from '@/components/MaintenanceRequests.vue'
import CommunityReviews from '@/components/CommunityReviews.vue'
import ComplaintSuggestions from '@/components/ComplaintSuggestions.vue'

export default {
  components: {
    MaintenanceRequests,
    CommunityReviews,
    ComplaintSuggestions
  },
  data() {
    return {
      activeTab: 'maintenance'
    }
  }
}
</script>

<style scoped>
.area-maintenance-container {
  padding: 20px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #303133;
}
</style> 