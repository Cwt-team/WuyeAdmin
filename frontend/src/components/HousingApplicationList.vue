<template>
  <div class="housing-application-container">
    <div class="header">
      <h2>房屋绑定申请管理</h2>
      <div class="filter-options">
        <el-select v-model="statusFilter" placeholder="申请状态筛选">
          <el-option label="全部" value=""></el-option>
          <el-option label="待审核" value="待审核"></el-option>
          <el-option label="已审核" value="已审核"></el-option>
          <el-option label="已拒绝" value="已拒绝"></el-option>
        </el-select>
        <el-button type="primary" @click="fetchApplications">查询</el-button>
      </div>
    </div>
    
    <el-table :data="applications" border stripe v-loading="loading">
      <el-table-column prop="id" label="申请ID" width="80"></el-table-column>
      <el-table-column prop="name" label="申请人" width="100"></el-table-column>
      <el-table-column prop="phoneNumber" label="手机号码" width="120"></el-table-column>
      <el-table-column label="申请房屋" min-width="200">
        <template #default="scope">
          {{ scope.row.communityName || '未指定' }} - 
          {{ scope.row.buildingName || '未指定' }} - 
          {{ scope.row.unitName || '未指定' }} - 
          {{ scope.row.houseNumber || '未指定' }}
        </template>
      </el-table-column>
      <el-table-column prop="applicationTime" label="申请时间" width="160"></el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="getStatusType(scope.row.status)">{{ scope.row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="scope">
          <el-button size="small" @click="viewDetail(scope.row.id)">查看</el-button>
          <el-button 
            size="small" 
            type="success" 
            v-if="scope.row.status === '待审核'"
            @click="approveApplication(scope.row.id)">通过</el-button>
          <el-button 
            size="small" 
            type="danger" 
            v-if="scope.row.status === '待审核'"
            @click="rejectApplication(scope.row.id)">拒绝</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        @current-change="handlePageChange"
        :current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next">
      </el-pagination>
    </div>
    
    <!-- 拒绝申请对话框 -->
    <el-dialog title="拒绝申请" v-model="rejectDialogVisible" width="500px">
      <el-form :model="rejectForm">
        <el-form-item label="拒绝原因" prop="callbackMessage">
          <el-input type="textarea" v-model="rejectForm.callbackMessage" rows="4" placeholder="请填写拒绝原因，该信息将反馈给申请人"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="rejectDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmReject" :loading="submitting">确认拒绝</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus';

export default {
  name: 'HousingApplicationList',
  data() {
    return {
      applications: [],
      statusFilter: '',
      currentPage: 1,
      pageSize: 10,
      total: 0,
      loading: false,
      submitting: false,
      rejectDialogVisible: false,
      rejectForm: {
        applicationId: null,
        callbackMessage: ''
      }
    };
  },
  created() {
    this.fetchApplications();
  },
  methods: {
    fetchApplications() {
      this.loading = true;
      const params = {
        page: this.currentPage,
        size: this.pageSize
      };
      
      if (this.statusFilter) {
        params.status = this.statusFilter;
      }
      
      axios.get('/api/housing-applications', { params })
        .then(response => {
          this.applications = response.data.applications;
          this.total = response.data.total;
        })
        .catch(error => {
          ElMessage.error('获取申请列表失败');
          console.error(error);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    handlePageChange(page) {
      this.currentPage = page;
      this.fetchApplications();
    },
    getStatusType(status) {
      switch(status) {
        case '待审核': return 'warning';
        case '已审核': return 'success';
        case '已拒绝': return 'danger';
        default: return 'info';
      }
    },
    viewDetail(id) {
      this.$router.push(`/housing-applications/${id}`);
    },
    approveApplication(id) {
      ElMessageBox.confirm('确认通过该房屋绑定申请?', '确认', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.submitting = true;
        axios.post(`/api/housing-applications/${id}/approve`)
          .then(() => {
            ElMessage.success('审核通过成功');
            this.fetchApplications();
          })
          .catch(error => {
            ElMessage.error('操作失败');
            console.error(error);
          })
          .finally(() => {
            this.submitting = false;
          });
      }).catch(() => {});
    },
    rejectApplication(id) {
      this.rejectForm.applicationId = id;
      this.rejectForm.callbackMessage = '';
      this.rejectDialogVisible = true;
    },
    confirmReject() {
      if (!this.rejectForm.callbackMessage) {
        ElMessage.warning('请填写拒绝原因');
        return;
      }
      
      this.submitting = true;
      axios.post(`/api/housing-applications/${this.rejectForm.applicationId}/reject`, {
        callbackMessage: this.rejectForm.callbackMessage
      }).then(() => {
        ElMessage.success('已拒绝该申请');
        this.rejectDialogVisible = false;
        this.fetchApplications();
      }).catch(error => {
        ElMessage.error('操作失败');
        console.error(error);
      }).finally(() => {
        this.submitting = false;
      });
    }
  }
}
</script>

<style scoped>
.housing-application-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filter-options {
  display: flex;
  gap: 10px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 