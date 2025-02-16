<template>
  <div class="call-record-list">
    <el-card>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>记录信息管理</el-breadcrumb-item>
        <el-breadcrumb-item>呼叫记录</el-breadcrumb-item>
      </el-breadcrumb>

      <el-row class="filter-row" :gutter="20">
        <el-col :span="6">
          <el-select v-model="filter.communityId" placeholder="选择社区" class="filter-item" @change="handleCommunityChange">
            <el-option 
              v-for="item in communityOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filter.district" placeholder="选择区" class="filter-item" @change="handleDistrictChange">
            <el-option 
              v-for="item in districtOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filter.building" placeholder="选择栋" class="filter-item" @change="handleBuildingChange">
            <el-option 
              v-for="item in buildingOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filter.unit" placeholder="选择单元" class="filter-item">
            <el-option 
              v-for="item in unitOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-date-picker
            v-model="filter.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            class="filter-item"
          />
        </el-col>
        <el-col :span="2">
          <el-button type="primary" :loading="loading" @click="searchCallRecords">查询</el-button>
        </el-col>
      </el-row>

      <el-table :data="callRecordList" style="width: 100%" v-loading="loading">
        <el-table-column prop="doorAccessInfo" label="门禁信息"/>
        <el-table-column prop="callStartTime" label="呼叫时间"/>
        <el-table-column prop="callDuration" label="呼叫时长(秒)"/>
        <el-table-column prop="houseName" label="房屋信息"/>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          background
          layout="total, prev, pager, next, sizes"
          :total="total"
          :current-page="currentPage"
          :page-size="pageSize"
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
  name: 'CallRecord',
  data() {
    return {
      loading: false,
      filter: {
        communityId: '',
        district: '',
        building: '',
        unit: '',
        dateRange: []
      },
      communityOptions: [],
      districtOptions: [],
      buildingOptions: [],
      unitOptions: [],
      callRecordList: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      mockData: [
        {
          id: 1,
          doorAccessInfo: '1区1栋1单元门口机',
          callStartTime: '2024-08-08 10:15:30',
          callDuration: 35,
          houseName: '1区1栋1单元101'
        },
        {
          id: 2,
          doorAccessInfo: '2区1栋1单元门口机',
          callStartTime: '2024-08-08 14:20:00',
          callDuration: 58,
          houseName: '2区1栋1单元102'
        }
      ]
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
      }
    },
    async fetchCallRecords() {
      this.loading = true
      try {
        const response = await axios.get('/api/call-records', {
          params: {
            communityId: this.filter.communityId,
            district: this.filter.district,
            building: this.filter.building,
            unit: this.filter.unit,
            startDate: this.filter.dateRange?.[0],
            endDate: this.filter.dateRange?.[1],
            page: this.currentPage,
            size: this.pageSize
          }
        })
        this.callRecordList = response.data.records
        this.total = response.data.total
        this.$message.success('获取数据成功')
      } catch (error) {
        console.error('获取呼叫记录失败:', error)
        this.$message.warning('获取数据库失败，已展示示例数据')
        this.callRecordList = this.mockData
        this.total = this.mockData.length
      } finally {
        this.loading = false
      }
    },
    handleCommunityChange() {
      this.filter.district = ''
      this.filter.building = ''
      this.filter.unit = ''
      // 获取区列表
    },
    handleDistrictChange() {
      this.filter.building = ''
      this.filter.unit = ''
      // 获取楼栋列表
    },
    handleBuildingChange() {
      this.filter.unit = ''
      // 获取单元列表
    },
    searchCallRecords() {
      this.currentPage = 1
      this.fetchCallRecords()
    },
    handlePageChange(page) {
      this.currentPage = page
      this.fetchCallRecords()
    },
    handleSizeChange(size) {
      this.pageSize = size
      this.currentPage = 1
      this.fetchCallRecords()
    }
  },
  mounted() {
    this.fetchCommunities()
    this.fetchCallRecords()
  }
}
</script>

<style scoped>
.call-record-list {
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
