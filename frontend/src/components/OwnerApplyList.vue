<template>
  <div class="owner-apply-list">
    <el-card>
      <el-row class="filter-row">
        <el-col :span="4">
          <el-select v-model="filter.area" placeholder="区域" class="filter-item">
            <el-option
              v-for="item in areaOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filter.building" placeholder="楼栋" class="filter-item">
            <el-option
              v-for="item in buildingOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-input v-model="filter.name" placeholder="姓名或手机号" class="filter-item" />
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="searchApplications">查询</el-button>
        </el-col>
        <el-col :span="4">
          <el-button type="success" @click="downloadQRCodes">下载二维码</el-button>
        </el-col>
      </el-row>

      <el-table :data="applicationList" style="width: 100%">
        <el-table-column prop="room" label="房间信息" />
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="gender" label="性别" />
        <el-table-column prop="idCard" label="身份证号" />
        <el-table-column prop="phone" label="手机号" />
        <el-table-column prop="status" label="状态" />
        <el-table-column prop="ownerType" label="业主类型" />
        <el-table-column prop="applyTime" label="申请时间" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="text" size="small" @click="viewApplication(scope.row)">查看详情</el-button>
          </template>
        </el-table-column>
        <template #empty>
          暂无数据
        </template>
      </el-table>

      <el-pagination
        background
        layout="prev, pager, next"
        :total="total"
        :current-page="currentPage"
        :page-size="pageSize"
        @current-change="handlePageChange"
      />
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';
import QRCode from 'qrcode'; // 引入 qrcode.js 库

export default {
  name: 'OwnerApplyList',
  data() {
    return {
      filter: {
        area: '',
        building: '',
        name: '',
      },
      areaOptions: [],
      buildingOptions: [],
      applicationList: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
    };
  },
  methods: {
    async fetchAreaOptions() {
      try {
        const response = await axios.get('/api/areas');
        this.areaOptions = response.data;
      } catch (error) {
        console.error('获取区域信息失败:', error);
        this.$message.error('获取区域信息失败');
      }
    },
    async fetchBuildingOptions() {
      try {
        const response = await axios.get('/api/buildings');
        this.buildingOptions = response.data;
      } catch (error) {
        console.error('获取楼栋信息失败:', error);
        this.$message.error('获取楼栋信息失败');
      }
    },
    async fetchApplications() {
      try {
        const response = await axios.get('/api/owner-applications', {
          params: {
            area: this.filter.area,
            building: this.filter.building,
            name: this.filter.name,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        this.applicationList = response.data.applications;
        this.total = response.data.total;
        if (this.applicationList.length === 0) {
          this.applicationList = this.generateMockData();
        }
      } catch (error) {
        console.error('获取业主申请信息失败:', error);
        this.applicationList = this.generateMockData();
        this.$message.error('获取业主申请信息失败，已显示模拟数据');
      }
    },
    generateMockData() {
      console.warn('从后端获取数据失败，正在生成模拟数据。');
      return [
        {
          room: 'A区-1栋-0101',
          name: '模拟数据1',
          gender: '男',
          idCard: '...',
          phone: '...',
          status: '待审核',
          ownerType: '业主',
          applyTime: '...',
        },
        {
          room: 'B区-2栋-0202',
          name: '模拟数据2',
          gender: '女',
          idCard: '...',
          phone: '...',
          status: '已通过',
          ownerType: '家属',
          applyTime: '...',
        },
      ];
    },
    searchApplications() {
      this.currentPage = 1;
      this.fetchApplications();
    },
    handlePageChange(page) {
      this.currentPage = page;
      this.fetchApplications();
    },
    viewApplication(row) {
      console.log('查看申请详情:', row);
    },
    downloadQRCodes() {
      this.applicationList.forEach(application => {
        const qrCodeData = `业主申请信息：\n房间: ${application.room}\n姓名: ${application.name}\n手机号: ${application.phone}`;
        QRCode.toCanvas(document.createElement('canvas'), qrCodeData, { errorCorrectionLevel: 'H' }, (error, canvas) => {
          if (error) {
            console.error('生成二维码失败', error);
            this.$message.error(`为 ${application.name} 生成二维码失败`);
            return;
          }
          const link = document.createElement('a');
          link.href = canvas.toDataURL('image/png');
          link.download = `业主申请二维码-${application.name}.png`;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        });
      });
      if (this.applicationList.length === 0) {
        this.$message.warning('当前没有业主申请数据，无法下载二维码');
      }
    },
  },
  mounted() {
    this.fetchAreaOptions();
    this.fetchBuildingOptions();
    this.fetchApplications();
  },
};
</script>

<style scoped>
.filter-row {
  margin-bottom: 20px;
}
.filter-item {
  margin-right: 10px;
}
</style>
