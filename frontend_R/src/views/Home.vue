<template>
  <div class="home-container">
    <!-- 顶部统计卡片 -->
    <div class="stat-cards">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-title">居民总数</div>
            <div class="stat-value">{{ stats.residents }}</div>
            <div class="stat-icon resident-icon">
              <el-icon><user /></el-icon>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-title">房间总数</div>
            <div class="stat-value">{{ stats.rooms }}</div>
            <div class="stat-icon room-icon">
              <el-icon><house /></el-icon>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-title">本月收入</div>
            <div class="stat-value">¥{{ stats.monthlyIncome }}</div>
            <div class="stat-icon income-icon">
              <el-icon><money /></el-icon>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-title">待办事项</div>
            <div class="stat-value">{{ stats.todoCount }}</div>
            <div class="stat-icon todo-icon">
              <el-icon><warning /></el-icon>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <!-- 图表区域 -->
    <div class="charts-container">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card shadow="hover" class="chart-card">
            <template #header>
              <div class="card-header">
                <span>收入趋势</span>
              </div>
            </template>
            <div class="chart-placeholder">
              <!-- 实际应用中这里会放置收入趋势图表 -->
              <div class="empty-chart">图表将在此处显示</div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="12">
          <el-card shadow="hover" class="chart-card">
            <template #header>
              <div class="card-header">
                <span>费用类型分布</span>
              </div>
            </template>
            <div class="chart-placeholder">
              <!-- 实际应用中这里会放置费用类型分布图表 -->
              <div class="empty-chart">图表将在此处显示</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <!-- 最近活动 -->
    <el-card shadow="hover" class="activity-card">
      <template #header>
        <div class="card-header">
          <span>最近活动</span>
        </div>
      </template>
      <el-table :data="activities" style="width: 100%" :show-header="false">
        <el-table-column width="50">
          <template #default="scope">
            <el-avatar :size="30" :icon="getActivityIcon(scope.row.type)"></el-avatar>
          </template>
        </el-table-column>
        <el-table-column prop="content"></el-table-column>
        <el-table-column prop="time" align="right" width="180"></el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { User, House, Money, Warning } from '@element-plus/icons-vue'

export default {
  name: 'HomeView',
  components: {
    User,
    House,
    Money,
    Warning
  },
  setup() {
    // 统计数据
    const stats = reactive({
      residents: 320,
      rooms: 450,
      monthlyIncome: '45,600',
      todoCount: 12
    })
    
    // 活动列表
    const activities = ref([
      { type: 'payment', content: '张三完成物业费缴纳', time: '今天 14:35' },
      { type: 'repair', content: '新增报修工单: 水管漏水', time: '今天 13:12' },
      { type: 'user', content: '新增居民: 李四', time: '今天 10:45' },
      { type: 'system', content: '系统数据备份完成', time: '今天 03:00' },
      { type: 'payment', content: '王五完成水费缴纳', time: '昨天 16:23' }
    ])
    
    // 根据活动类型获取图标
    const getActivityIcon = (type) => {
      switch (type) {
        case 'payment':
          return Money
        case 'repair':
          return Warning
        case 'user':
          return User
        case 'system':
          return 'Setting'
        default:
          return 'Info'
      }
    }
    
    // 模拟获取数据
    onMounted(() => {
      // 实际应用中，这里会从API获取数据
      console.log('Home组件已加载，可以从API获取数据')
    })
    
    return {
      stats,
      activities,
      getActivityIcon
    }
  }
}
</script>

<style scoped>
.home-container {
  padding: 20px;
}

.stat-cards, .charts-container {
  margin-bottom: 20px;
}

.stat-card {
  height: 120px;
  position: relative;
  overflow: hidden;
}

.stat-title {
  font-size: 16px;
  color: #666;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  margin-top: 10px;
}

.stat-icon {
  position: absolute;
  right: 20px;
  bottom: 20px;
  font-size: 36px;
  opacity: 0.3;
}

.resident-icon {
  color: #409EFF;
}

.room-icon {
  color: #67C23A;
}

.income-icon {
  color: #E6A23C;
}

.todo-icon {
  color: #F56C6C;
}

.chart-card, .activity-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-placeholder {
  height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.empty-chart {
  color: #999;
  font-size: 14px;
}

.el-table {
  margin-top: 10px;
}
</style>