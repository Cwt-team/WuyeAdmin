<template>
  <div class="unlock-record-list">
    <el-card>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>记录信息管理</el-breadcrumb-item>
        <el-breadcrumb-item>开锁记录</el-breadcrumb-item>
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
          <el-select v-model="filter.deviceType" placeholder="所有设备" class="filter-item">
            <el-option label="门口机" value="Entrance Machine" />
            <el-option label="围墙机" value="Fencing Machine" />
            <el-option label="其他" value="Other" />
          </el-select>
        </el-col>
        <el-col :span="8">
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
          <el-button type="primary" :loading="loading" @click="searchUnlockRecords">查询</el-button>
        </el-col>
      </el-row>

      <el-table :data="unlockRecordList" style="width: 100%" v-loading="loading">
        <el-table-column prop="doorInfo" label="门禁信息"/>
        <el-table-column prop="deviceType" label="设备类型">
          <template #default="scope">
            {{ getDeviceTypeText(scope.row.deviceType) }}
          </template>
        </el-table-column>
        <el-table-column prop="unlockingType" label="开锁类型">
          <template #default="scope">
            {{ getUnlockTypeText(scope.row.unlockingType) }}
          </template>
        </el-table-column>
        <el-table-column prop="unlocker" label="开锁人员"/>
        <el-table-column prop="unlockingTime" label="开锁时间"/>
        <el-table-column label="开锁照片">
          <template #default="scope">
            <el-image 
              v-if="scope.row.photoUrl" 
              :src="scope.row.photoUrl" 
              :preview-src-list="[scope.row.photoUrl]"
              style="width: 50px; height: 50px;"
            />
            <span v-else>无照片</span>
          </template>
        </el-table-column>
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
import axios from 'axios';

export default {
  name: 'UnlockRecord',
  data() {
    return {
      loading: false,
      filter: {
        communityId: '',
        district: '',
        building: '',
        unit: '',
        deviceType: '',
        dateRange: []
      },
      communityOptions: [],
      districtOptions: [],
      buildingOptions: [],
      unitOptions: [],
      unlockRecordList: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      mockData: [
        {
          doorInfo: '1区1栋1单元门口机',
          deviceType: 'Entrance Machine',
          unlockingType: '密码开锁',
          unlocker: '业主本人',
          unlockingTime: '2024-08-08 15:30:00'
        },
        {
          doorInfo: '小区南门围墙机',
          deviceType: 'Fencing Machine',
          unlockingType: '刷卡开锁',
          unlocker: '快递员',
          unlockingTime: '2024-08-08 16:45:10'
        }
      ]
    }
  },
  methods: {
    getDeviceTypeText(type) {
      const types = {
        'Entrance Machine': '门口机',
        'Fencing Machine': '围墙机',
        'Other': '其他'
      }
      return types[type] || type
    },
    getUnlockTypeText(type) {
      const typeMap = {
        '0': '二维码开锁',
        '1': '小程序远程开锁',
        '2': '门禁卡开锁',
        '3': '一次性密码开锁',
        '4': '人脸识别开锁',
        '5': '分机开锁',
        '6': '物业中心开锁',
        '7': '指纹开锁',
        '8': '公共密码开锁',
        '14': '手机电话开锁'
      };
      return typeMap[type] || type;
    },
    async fetchUnlockRecords() {
      this.loading = true
      try {
        const response = await axios.get('/api/unlock-records', {
          params: {
            communityId: this.filter.communityId,
            district: this.filter.district,
            building: this.filter.building,
            unit: this.filter.unit,
            deviceType: this.filter.deviceType,
            startDate: this.filter.dateRange?.[0],
            endDate: this.filter.dateRange?.[1],
            page: this.currentPage,
            size: this.pageSize
          }
        })
        this.unlockRecordList = response.data.records
        this.total = response.data.total
        this.$message.success('获取数据成功')
      } catch (error) {
        console.error('获取开锁记录失败:', error)
        this.$message.warning('获取数据库失败，已展示示例数据')
        this.unlockRecordList = this.mockData
        this.total = this.mockData.length
      } finally {
        this.loading = false
      }
    },
    searchUnlockRecords() {
      this.currentPage = 1;
      this.fetchUnlockRecords();
    },
    handlePageChange(page) {
      this.currentPage = page;
      this.fetchUnlockRecords();
    },
    // handleCommunityChange(value) {
    //   // Implementation of handleCommunityChange method
    // },
    // handleDistrictChange(value) {
    //   // Implementation of handleDistrictChange method
    // },
    // handleBuildingChange(value) {
    //   // Implementation of handleBuildingChange method
    // },
    // handleSizeChange(size) {
    //   // Implementation of handleSizeChange method
    // },
  },
  mounted() {
    this.fetchUnlockRecords();
  },
};
</script>

<style scoped>
.unlock-record-list {
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
