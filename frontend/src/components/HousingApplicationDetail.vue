<template>
  <div class="housing-application-detail" v-loading="loading">
    <div class="header">
      <h2>房屋绑定申请详情</h2>
      <div class="actions">
        <el-button @click="goBack">返回</el-button>
        <el-button 
          type="success" 
          v-if="application && application.status === '待审核'"
          @click="approveApplication">通过申请</el-button>
        <el-button 
          type="danger" 
          v-if="application && application.status === '待审核'"
          @click="rejectApplication">拒绝申请</el-button>
      </div>
    </div>
    
    <el-card v-if="application" class="application-card">
      <el-descriptions title="申请基本信息" :column="2" border>
        <el-descriptions-item label="申请ID">{{ application.id }}</el-descriptions-item>
        <el-descriptions-item label="申请状态">
          <el-tag :type="getStatusType(application.status)">{{ application.status }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="申请人">{{ application.name }}</el-descriptions-item>
        <el-descriptions-item label="手机号码">{{ application.phoneNumber }}</el-descriptions-item>
        <el-descriptions-item label="身份证号">{{ application.idCard }}</el-descriptions-item>
        <el-descriptions-item label="申请时间">{{ application.applicationTime }}</el-descriptions-item>
        <el-descriptions-item label="业主类型">{{ application.ownerType }}</el-descriptions-item>
        <el-descriptions-item label="审核反馈" :span="2">
          {{ application.callbackMessage || '暂无' }}
        </el-descriptions-item>
      </el-descriptions>
      
      <div class="divider"></div>
      
      <el-descriptions title="房屋信息" :column="2" border>
        <el-descriptions-item label="小区名称">{{ application.communityName }}</el-descriptions-item>
        <el-descriptions-item label="楼栋名称">{{ application.buildingName }}</el-descriptions-item>
        <el-descriptions-item label="单元名称">{{ application.unitName }}</el-descriptions-item>
        <el-descriptions-item label="房间号">{{ application.houseNumber }}</el-descriptions-item>
      </el-descriptions>
      
      <div class="divider"></div>
      
      <div v-if="application.informationPhoto" class="photo-section">
        <h3>申请证明材料</h3>
        <el-image 
          :src="application.informationPhoto" 
          :preview-src-list="[application.informationPhoto]"
          fit="contain"
          style="width: 100%; max-height: 300px;">
        </el-image>
      </div>
    </el-card>
    <el-empty v-else description="未找到申请信息"></el-empty>
    
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
  name: 'HousingApplicationDetail',
  data() {
    return {
      applicationId: null,
      application: null,
      loading: false,
      submitting: false,
      rejectDialogVisible: false,
      rejectForm: {
        callbackMessage: ''
      }
    };
  },
  created() {
    this.applicationId = this.$route.params.id;
    this.fetchApplicationDetail();
  },
  methods: {
    fetchApplicationDetail() {
      this.loading = true;
      axios.get(`/api/housing-applications/${this.applicationId}`)
        .then(response => {
          this.application = response.data;
        })
        .catch(error => {
          ElMessage.error('获取申请详情失败');
          console.error(error);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    getStatusType(status) {
      switch(status) {
        case '待审核': return 'warning';
        case '已审核': return 'success';
        case '已拒绝': return 'danger';
        default: return 'info';
      }
    },
    goBack() {
      this.$router.push('/housing-applications');
    },
    approveApplication() {
      ElMessageBox.confirm('确认通过该房屋绑定申请?', '确认', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.submitting = true;
        axios.post(`/api/housing-applications/${this.applicationId}/approve`)
          .then(() => {
            ElMessage.success('审核通过成功');
            // 重新获取申请详情
            this.fetchApplicationDetail();
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
    rejectApplication() {
      this.rejectForm.callbackMessage = '';
      this.rejectDialogVisible = true;
    },
    confirmReject() {
      if (!this.rejectForm.callbackMessage) {
        ElMessage.warning('请填写拒绝原因');
        return;
      }
      
      this.submitting = true;
      axios.post(`/api/housing-applications/${this.applicationId}/reject`, {
        callbackMessage: this.rejectForm.callbackMessage
      }).then(() => {
        ElMessage.success('已拒绝该申请');
        this.rejectDialogVisible = false;
        // 重新获取申请详情
        this.fetchApplicationDetail();
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
.housing-application-detail {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.application-card {
  margin-bottom: 20px;
}

.divider {
  height: 1px;
  background-color: #EBEEF5;
  margin: 24px 0;
}

.photo-section {
  margin-top: 20px;
}

.photo-section h3 {
  margin-bottom: 16px;
  font-weight: 500;
}
</style> 