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
          <el-select v-model="filter.unit" placeholder="单元" class="filter-item">
            <el-option
              v-for="item in unitOptions"
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
        <el-table-column prop="gender" label="性别">
          <template #default="scope">
            {{ scope.row.gender === 'M' ? '男' : '女' }}
          </template>
        </el-table-column>
        <el-table-column prop="idCard" label="身份证号" />
        <el-table-column prop="phone" label="手机号" />
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="ownerType" label="业主类型" />
        <el-table-column prop="applyTime" label="申请时间" />
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button-group>
              <el-button type="primary" size="small" @click="viewApplication(scope.row)">查看详情</el-button>
              <el-button type="danger" size="small" @click="deleteApplication(scope.row)">删除</el-button>
            </el-button-group>
          </template>
        </el-table-column>
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

    <!-- 申请详情对话框 -->
    <el-dialog
      v-model="detailDialog.visible"
      title="申请详情"
      width="600px"
    >
      <el-form label-width="120px">
        <el-form-item label="房间信息">
          {{ detailDialog.form.room }}
        </el-form-item>
        <el-form-item label="姓名">
          {{ detailDialog.form.name }}
        </el-form-item>
        <el-form-item label="性别">
          {{ detailDialog.form.gender === 'M' ? '男' : '女' }}
        </el-form-item>
        <el-form-item label="身份证号">
          {{ detailDialog.form.idCard }}
        </el-form-item>
        <el-form-item label="手机号">
          {{ detailDialog.form.phone }}
        </el-form-item>
        <el-form-item label="业主类型">
          {{ detailDialog.form.ownerType }}
        </el-form-item>
        <el-form-item label="申请时间">
          {{ detailDialog.form.applyTime }}
        </el-form-item>
        <el-form-item label="状态">
          <el-tag :type="getStatusType(detailDialog.form.status)">
            {{ getStatusText(detailDialog.form.status) }}
          </el-tag>
        </el-form-item>
        <el-form-item label="打回信息" v-if="detailDialog.form.status === 'Returned'">
          {{ detailDialog.form.callbackMessage }}
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="detailDialog.visible = false">关闭</el-button>
        <el-button type="success" @click="handleApprove" v-if="detailDialog.form.status === 'Pending'">通过</el-button>
        <el-button type="warning" @click="handleReturn" v-if="detailDialog.form.status === 'Pending'">打回</el-button>
      </template>
    </el-dialog>

    <!-- 打回原因对话框 -->
    <el-dialog
      v-model="returnDialog.visible"
      title="打回原因"
      width="500px"
    >
      <el-form>
        <el-form-item>
          <el-input
            v-model="returnDialog.reason"
            type="textarea"
            rows="3"
            placeholder="请输入打回原因"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="returnDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="confirmReturn">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';
import QRCode from 'qrcode';

export default {
  name: 'OwnerApplyList',
  data() {
    return {
      filter: {
        area: '',
        building: '',
        unit: '',
        name: '',
      },
      areaOptions: [],
      buildingOptions: [],
      unitOptions: [],
      applicationList: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      detailDialog: {
        visible: false,
        form: {},
      },
      returnDialog: {
        visible: false,
        reason: '',
        currentApplication: null
      },
      // 模拟数据
      mockData: [
        {
          id: 1,
          room: '5区42栋12单元',
          name: 'lil',
          gender: 'M',
          idCard: null,
          phone: '13542406097',
          status: 'Returned',
          ownerType: '业主',
          applyTime: '2025-02-11 11:20:29',
          callbackMessage: '不合格'
        },
        {
          id: 2,
          room: '5区42栋12单元',
          name: '张三',
          gender: 'F',
          idCard: '440307199001010011',
          phone: '13912345678',
          status: 'Pending',
          ownerType: '业主',
          applyTime: '2025-03-15 14:30:00',
          callbackMessage: null
        }
      ]
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
    async fetchUnitOptions() {
      try {
        const response = await axios.get('/api/units');
        this.unitOptions = response.data;
      } catch (error) {
        console.error('获取单元信息失败:', error);
        this.$message.error('获取单元信息失败');
      }
    },
    async fetchApplications() {
      try {
        const response = await axios.get('/api/owner-applications', {
          params: {
            area: this.filter.area,
            building: this.filter.building,
            unit: this.filter.unit,
            name: this.filter.name,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        this.applicationList = response.data.applications;
        this.total = response.data.total;
      } catch (error) {
        console.error('获取业主申请列表失败:', error);
        this.$message.warning('获取数据失败，显示模拟数据');
        this.applicationList = this.mockData;
        this.total = this.mockData.length;
      }
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
      this.detailDialog.form = { ...row };
      this.detailDialog.visible = true;
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
    getStatusType(status) {
      const statusMap = {
        'Pending': 'warning',
        'Approved': 'success',
        'Returned': 'danger',
        'Rejected': 'info'
      };
      return statusMap[status] || 'info';
    },
    getStatusText(status) {
      const statusMap = {
        'Pending': '待审核',
        'Approved': '已通过',
        'Returned': '已打回',
        'Rejected': '已拒绝'
      };
      return statusMap[status] || status;
    },
    handleApprove() {
      this.handleApprove();
    },
    handleReturn() {
      this.returnDialog.currentApplication = this.detailDialog.form;
      this.returnDialog.reason = '';
      this.returnDialog.visible = true;
    },
    confirmReturn() {
      if (!this.returnDialog.reason.trim()) {
        this.$message.warning('请输入打回原因');
        return;
      }
      
      this.confirmReturn();
    },
    deleteApplication() {
      // 实现删除逻辑
    },
  },
  created() {
    this.fetchAreaOptions();
    this.fetchBuildingOptions();
    this.fetchUnitOptions();
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
