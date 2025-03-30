<template>
  <div class="personal-info">
    <el-card>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>个人信息中心</el-breadcrumb-item>
        <el-breadcrumb-item>个人资料</el-breadcrumb-item>
      </el-breadcrumb>

      <div class="info-header">
        <el-avatar size="large" :src="avatarUrl">
          <img v-if="!avatarUrl" src="https://cube.elemecdn.com/e/fd/0fc7d20532fdaf7695ce8d3101915png.png" />
        </el-avatar>
        <el-button type="text" @click="changeAvatar">更换头像</el-button>
        <input 
          ref="fileInput" 
          type="file" 
          accept="image/*" 
          style="display:none" 
          @change="onFileSelected" 
        />
      </div>

      <el-descriptions class="margin-top" :column="3" border>
        <el-descriptions-item label="ID">{{ personalInfo.id }}</el-descriptions-item>
        <el-descriptions-item label="用户名">{{ personalInfo.username }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ personalInfo.createdAt }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ personalInfo.updatedAt }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ personalInfo.email }}</el-descriptions-item>
        <el-descriptions-item label="电话">{{ personalInfo.phoneNumber }}</el-descriptions-item>
      </el-descriptions>

      <el-card class="edit-card" shadow="never">
        <el-form :model="editableInfo" label-width="120px" :rules="formRules" ref="infoFormRef">
          <el-form-item label="昵称" prop="nickname">
            <el-input v-model="editableInfo.nickname" placeholder="请输入昵称" />
          </el-form-item>
          <el-form-item label="联系电话" prop="phoneNumber">
            <el-input v-model="editableInfo.phoneNumber" placeholder="请输入联系电话" />
          </el-form-item>
          <el-form-item label="电子邮箱" prop="email">
            <el-input v-model="editableInfo.email" placeholder="请输入电子邮箱" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="savePersonalInfo">保存</el-button>
            <el-button @click="resetForm">重置</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </el-card>

    <!-- 添加上传头像的对话框 -->
    <el-dialog
      title="上传头像"
      v-model="uploadDialog.visible"
      width="400px"
    >
      <div class="avatar-uploader">
        <div v-if="uploadDialog.imageUrl" class="avatar-preview">
          <img :src="uploadDialog.imageUrl" alt="头像预览" />
        </div>
        <el-upload
          class="avatar-upload"
          action="#"
          :auto-upload="false"
          :show-file-list="false"
          :on-change="handleFileChange"
        >
          <el-button type="primary">选择图片</el-button>
          <div class="el-upload__tip">
            请上传JPG/PNG格式图片，文件大小不超过2MB
          </div>
        </el-upload>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="uploadDialog.visible = false">取消</el-button>
          <el-button type="primary" :loading="uploading" @click="uploadAvatar">确定上传</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'PersonalInfo',
  data() {
    return {
      personalInfo: {
        id: '',
        username: '',
        nickname: '',
        phoneNumber: '',
        email: '',
        profilePicturePath: '',
        createdAt: '',
        updatedAt: ''
      },
      editableInfo: {
        nickname: '',
        phoneNumber: '',
        email: '',
      },
      avatarUrl: '',
      formRules: {
        phoneNumber: [
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ],
        email: [
          { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
        ]
      },
      uploading: false,
      uploadDialog: {
        visible: false,
        imageUrl: '',
        file: null
      }
    };
  },
  methods: {
    async fetchPersonalInfo() {
      try {
        const response = await axios.get('/api/personal-info');
        if (response.status === 200) {
          this.personalInfo = response.data;
          this.avatarUrl = response.data.profilePicturePath || '';
          // 初始化可编辑信息
          this.editableInfo.nickname = response.data.nickname || '';
          this.editableInfo.phoneNumber = response.data.phoneNumber || '';
          this.editableInfo.email = response.data.email || '';
        } else {
          this.$message.error('获取个人资料失败');
        }
      } catch (error) {
        console.error('获取个人资料失败:', error);
        this.$message.error('获取个人资料失败');
      }
    },
    async savePersonalInfo() {
      try {
        this.$refs.infoFormRef.validate(async (valid) => {
          if (valid) {
            const response = await axios.put('/api/personal-info', this.editableInfo);
            if (response.data && response.data.message) {
              this.$message.success(response.data.message);
              // 更新本地数据
              if (response.data.data) {
                this.personalInfo = response.data.data;
              } else {
                // 重新获取最新的个人信息以保持数据同步
                this.fetchPersonalInfo();
              }
            }
          } else {
            return false;
          }
        });
      } catch (error) {
        console.error('保存个人资料失败:', error);
        this.$message.error(error.response?.data?.error || '个人资料保存失败');
      }
    },
    resetForm() {
      // 重置表单为当前个人信息
      this.editableInfo.nickname = this.personalInfo.nickname || '';
      this.editableInfo.phoneNumber = this.personalInfo.phoneNumber || '';
      this.editableInfo.email = this.personalInfo.email || '';
      this.$refs.infoFormRef.clearValidate();
    },
    changeAvatar() {
      // 打开上传对话框
      this.uploadDialog.visible = true;
      this.uploadDialog.imageUrl = '';
      this.uploadDialog.file = null;
    },
    handleFileChange(file) {
      // 处理文件选择变化
      const isImage = file.raw.type.indexOf('image/') !== -1;
      const isLt2M = file.size / 1024 / 1024 < 2;
      
      if (!isImage) {
        this.$message.error('请上传图片格式文件!');
        return false;
      }
      
      if (!isLt2M) {
        this.$message.error('图片大小不能超过2MB!');
        return false;
      }
      
      // 创建本地预览URL
      this.uploadDialog.imageUrl = URL.createObjectURL(file.raw);
      this.uploadDialog.file = file.raw;
    },
    async uploadAvatar() {
      if (!this.uploadDialog.file) {
        this.$message.error('请先选择图片');
        return;
      }
      
      try {
        this.uploading = true;
        
        // 创建FormData对象
        const formData = new FormData();
        formData.append('avatar', this.uploadDialog.file);
        
        // 发送上传请求
        const response = await axios.post('/api/upload-avatar', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        
        if (response.data && response.data.url) {
          // 更新头像URL
          this.avatarUrl = response.data.url;
          this.$message.success('头像上传成功');
          this.uploadDialog.visible = false;
          
          // 刷新个人信息
          this.fetchPersonalInfo();
        } else {
          throw new Error('上传失败');
        }
      } catch (error) {
        console.error('头像上传失败:', error);
        this.$message.error(error.response?.data?.error || '头像上传失败');
      } finally {
        this.uploading = false;
      }
    }
  },
  mounted() {
    this.fetchPersonalInfo();
  },
};
</script>

<style scoped>
.personal-info {
  padding: 20px;
}
.info-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}
.info-header .el-avatar {
  margin-right: 10px;
}
.edit-card {
  margin-top: 20px;
}
.avatar-uploader {
  text-align: center;
  padding: 20px 0;
}
.avatar-preview {
  width: 200px;
  height: 200px;
  margin: 0 auto 20px;
  border-radius: 100%;
  overflow: hidden;
  border: 1px solid #eee;
}
.avatar-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.avatar-upload {
  margin: 0 auto;
}
</style>
