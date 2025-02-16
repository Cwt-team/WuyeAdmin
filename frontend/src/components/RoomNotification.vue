<template>
  <div class="room-notification-list">
    <el-card>
      <el-alert
        v-if="!selectedHouse"
        title="请先选择房号，再发送通知！"
        type="warning"
        show-icon
        :closable="false"
      />
      
      <el-row class="filter-row" :gutter="10">
        <el-col :span="4">
          <el-select 
            v-model="filter.community" 
            placeholder="选择社区" 
            class="filter-item"
            @change="handleCommunityChange"
          >
            <el-option 
              v-for="item in communityOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col :span="3">
          <el-select 
            v-model="filter.district" 
            placeholder="选择区" 
            class="filter-item"
            @change="handleDistrictChange"
          >
            <el-option 
              v-for="item in districtOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col :span="3">
          <el-select 
            v-model="filter.building" 
            placeholder="选择栋" 
            class="filter-item"
            @change="handleBuildingChange"
          >
            <el-option 
              v-for="item in buildingOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col :span="3">
          <el-select 
            v-model="filter.unit" 
            placeholder="选择单元" 
            class="filter-item"
          >
            <el-option 
              v-for="item in unitOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
      </el-row>

      <el-row class="filter-row" :gutter="10">
        <el-col :span="4">
          <el-input v-model="filter.title" placeholder="标题" clearable class="filter-item" />
        </el-col>
        <el-col :span="6">
          <el-date-picker
            v-model="filter.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
            class="filter-item"
          />
        </el-col>
        <el-col :span="2">
          <el-button type="primary" :loading="loading" @click="searchNotifications">查询</el-button>
        </el-col>
        <el-col :span="2">
          <el-button 
            type="primary" 
            @click="addNotification"
            :disabled="!selectedHouse"
          >
            房间通知
          </el-button>
        </el-col>
      </el-row>

      <el-table :data="notificationList" style="width: 100%" v-loading="loading">
        <el-table-column prop="title" label="标题"/>
        <el-table-column prop="content" label="内容"/>
        <el-table-column prop="displayStartTime" label="展示开始时间" width="180"/>
        <el-table-column prop="displayEndTime" label="展示结束时间" width="180"/>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" link @click="editNotification(scope.row)">编辑</el-button>
            <el-button type="danger" link @click="deleteNotification(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          background
          layout="total, prev, pager, next, sizes"
          :total="total"
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          @current-change="handlePageChange"
          @size-change="handleSizeChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'RoomNotification',
  data() {
    return {
      loading: false,
      filter: {
        community: '',
        district: '',
        building: '',
        unit: '',
        title: '',
        dateRange: null
      },
      selectedHouse: null,
      communityOptions: [],
      districtOptions: [],
      buildingOptions: [],
      unitOptions: [],
      notificationList: [],
      total: 0,
      currentPage: 1,
      pageSize: 10
    }
  },
  methods: {
    async fetchCommunities() {
      try {
        const response = await axios.get('/api/communities')
        this.communityOptions = response.data.map(item => ({
          value: item.id,
          label: item.communityName
        }))
      } catch (error) {
        console.error('获取社区列表失败:', error)
        this.$message.error('获取社区列表失败')
      }
    },

    async handleCommunityChange() {
      this.filter.district = ''
      this.filter.building = ''
      this.filter.unit = ''
      this.selectedHouse = null
      await this.fetchDistricts()
    },

    async handleDistrictChange() {
      this.filter.building = ''
      this.filter.unit = ''
      this.selectedHouse = null
      await this.fetchBuildings()
    },

    async handleBuildingChange() {
      this.filter.unit = ''
      this.selectedHouse = null
      await this.fetchUnits()
    },

    async fetchDistricts() {
      if (!this.filter.community) return
      try {
        const response = await axios.get(`/api/districts`, {
          params: { communityId: this.filter.community }
        })
        this.districtOptions = response.data
      } catch (error) {
        console.error('获取区域列表失败:', error)
        this.$message.error('获取区域列表失败')
      }
    },

    async fetchBuildings() {
      if (!this.filter.district) return
      try {
        const response = await axios.get(`/api/buildings`, {
          params: { 
            communityId: this.filter.community,
            districtId: this.filter.district
          }
        })
        this.buildingOptions = response.data
      } catch (error) {
        console.error('获取楼栋列表失败:', error)
        this.$message.error('获取楼栋列表失败')
      }
    },

    async fetchUnits() {
      if (!this.filter.building) return
      try {
        const response = await axios.get(`/api/units`, {
          params: {
            communityId: this.filter.community,
            districtId: this.filter.district,
            buildingId: this.filter.building
          }
        })
        this.unitOptions = response.data
      } catch (error) {
        console.error('获取单元列表失败:', error)
        this.$message.error('获取单元列表失败')
      }
    },

    async fetchNotifications() {
      this.loading = true
      try {
        const params = {
          communityId: this.filter.community,
          districtId: this.filter.district,
          buildingId: this.filter.building,
          unitId: this.filter.unit,
          title: this.filter.title,
          page: this.currentPage,
          size: this.pageSize
        }
        if (this.filter.dateRange) {
          params.startDate = this.filter.dateRange[0]
          params.endDate = this.filter.dateRange[1]
        }
        const response = await axios.get('/api/room-notifications', { params })
        this.notificationList = response.data.records
        this.total = response.data.total
      } catch (error) {
        console.error('获取通知列表失败:', error)
        this.$message.error('获取通知列表失败')
      } finally {
        this.loading = false
      }
    },

    searchNotifications() {
      this.currentPage = 1
      this.fetchNotifications()
    },

    handlePageChange(page) {
      this.currentPage = page
      this.fetchNotifications()
    },

    handleSizeChange(size) {
      this.pageSize = size
      this.currentPage = 1
      this.fetchNotifications()
    },

    addNotification() {
      if (!this.selectedHouse) {
        this.$message.warning('请先选择房号')
        return
      }
      this.$router.push('/room-notifications/add')
    },

    editNotification(row) {
      this.$router.push(`/room-notifications/edit/${row.id}`)
    },

    async deleteNotification(row) {
      try {
        await this.$confirm('确认删除该通知?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        await axios.delete(`/api/room-notifications/${row.id}`)
        this.$message.success('删除成功')
        this.fetchNotifications()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除通知失败:', error)
          this.$message.error('删除通知失败')
        }
      }
    }
  },
  mounted() {
    this.fetchCommunities()
  }
}
</script>

<style scoped>
.room-notification-list {
  padding: 20px;
}

.filter-row {
  margin-bottom: 20px;
}

.filter-item {
  width: 100%;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style>
