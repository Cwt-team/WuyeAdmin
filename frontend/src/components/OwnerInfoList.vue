  <template>
    <div class="owner-info-list">
      <el-card>
        <el-row class="filter-row">
          <el-col :span="6">
            <el-input v-model="filter.house" placeholder="房屋信息" class="filter-item" />
          </el-col>
          <el-col :span="6">
            <el-input v-model="filter.name" placeholder="姓名/手机号" class="filter-item" />
          </el-col>
          <el-col :span="4">
            <el-button type="primary" @click="searchOwners">查询</el-button>
          </el-col>
          <el-col :span="8">
            <el-button-group>
              <el-button type="success" @click="exportTemplate">导出模版</el-button>
              <el-button type="warning" @click="exportOwners">导出业主</el-button>
              <el-upload
                action="/api/owners/import"
                :show-file-list="false"
                :before-upload="beforeUpload"
                :on-success="handleImportSuccess"
                :on-error="handleImportError"
              >
                <el-button type="info">导入业主</el-button>
              </el-upload>
            </el-button-group>
          </el-col>
        </el-row>

        <el-table :data="ownerList" style="width: 100%">
          <el-table-column prop="houseName" label="房屋信息" />
          <el-table-column prop="name" label="姓名" />
          <el-table-column prop="gender" label="性别">
            <template #default="scope">
              {{ scope.row.gender === 'M' ? '男' : '女' }}
            </template>
          </el-table-column>
          <el-table-column prop="idCard" label="身份证号" />
          <el-table-column prop="phone" label="手机号" />
          <el-table-column prop="ownerType" label="业主类型" />
          <el-table-column prop="updateTime" label="更新时间" />
          <el-table-column label="操作" width="300">
            <template #default="scope">
              <el-button-group>
                <el-button type="primary" size="small" @click="handlePermission(scope.row)">权限</el-button>
                <el-button type="success" size="small" @click="handleFace(scope.row)">人脸</el-button>
                <el-button type="warning" size="small" @click="editOwner(scope.row)">编辑</el-button>
                <el-button type="danger" size="small" @click="deleteOwner(scope.row)">删除</el-button>
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

      <!-- 权限管理对话框 -->
      <el-dialog
        v-model="permissionDialog.visible"
        :title="permissionDialog.title"
        width="500px"
      >
        <el-form :model="permissionDialog.form" label-width="100px">
          <el-form-item label="有效期">
            <el-radio-group v-model="permissionDialog.form.validPeriod">
              <el-radio label="永久有效">永久有效</el-radio>
              <el-radio label="临时有效">临时有效</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="呼叫功能">
            <el-switch v-model="permissionDialog.form.callingEnabled" />
          </el-form-item>
          <el-form-item label="手机转接">
            <el-switch v-model="permissionDialog.form.pstnEnabled" />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="permissionDialog.visible = false">取消</el-button>
          <el-button type="primary" @click="savePermission">确定</el-button>
        </template>
      </el-dialog>

      <!-- 人脸管理对话框 -->
      <el-dialog
        v-model="faceDialog.visible"
        :title="faceDialog.title"
        width="500px"
      >
        <div class="face-upload">
          <el-upload
            class="avatar-uploader"
            action="#"
            :show-file-list="false"
            :before-upload="handleFaceUpload"
          >
            <img v-if="faceDialog.imageUrl" :src="faceDialog.imageUrl" class="avatar">
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </div>
        <template #footer>
          <el-button @click="faceDialog.visible = false">关闭</el-button>
        </template>
      </el-dialog>

      <!-- 编辑业主对话框 -->
      <el-dialog
        v-model="editDialog.visible"
        :title="editDialog.title"
        width="600px"
      >
        <el-form
          ref="editForm"
          :model="editDialog.form"
          :rules="editDialog.rules"
          label-width="100px"
        >
          <el-form-item label="姓名" prop="name">
            <el-input v-model="editDialog.form.name" />
          </el-form-item>
          <el-form-item label="性别" prop="gender">
            <el-radio-group v-model="editDialog.form.gender">
              <el-radio label="M">男</el-radio>
              <el-radio label="F">女</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="手机号" prop="phone">
            <el-input v-model="editDialog.form.phone" />
          </el-form-item>
          <el-form-item label="身份证号" prop="idCard">
            <el-input v-model="editDialog.form.idCard" />
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="editDialog.form.email" />
          </el-form-item>
          <el-form-item label="户籍城市" prop="city">
            <el-input v-model="editDialog.form.city" />
          </el-form-item>
          <el-form-item label="详细地址" prop="address">
            <el-input v-model="editDialog.form.address" type="textarea" />
          </el-form-item>
          <el-form-item label="业主类型" prop="ownerType">
            <el-select v-model="editDialog.form.ownerType">
              <el-option label="业主" value="业主" />
              <el-option label="租户" value="租户" />
            </el-select>
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="editDialog.visible = false">取消</el-button>
          <el-button type="primary" @click="saveOwner">确定</el-button>
        </template>
      </el-dialog>
    </div>
  </template>

  <script>
  import axios from 'axios';

  export default {
    name: 'OwnerInfoList',
    data() {
      return {
        filter: {
          house: '',
          name: '',
        },
        ownerList: [],
        total: 0,
        currentPage: 1,
        pageSize: 10,
        loading: false,

        // 权限管理对话框
        permissionDialog: {
          visible: false,
          title: '权限管理',
          form: {
            validPeriod: '永久有效',
            callingEnabled: true,
            pstnEnabled: false
          },
          currentOwner: null
        },

        // 人脸管理对话框
        faceDialog: {
          visible: false,
          title: '人脸管理',
          imageUrl: '',
          currentOwner: null
        },

        // 编辑对话框
        editDialog: {
          visible: false,
          title: '编辑业主',
          form: {
            name: '',
            gender: 'M',
            phone: '',
            idCard: '',
            email: '',
            city: '',
            address: '',
            ownerType: '业主'
          },
          rules: {
            name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
            phone: [{ required: true, message: '请输入手机号', trigger: 'blur' }],
            gender: [{ required: true, message: '请选择性别', trigger: 'change' }]
          },
          currentOwner: null
        }
      };
    },

  methods: {
    // 获取业主列表（已修改部分）
    async fetchOwners() {
      this.loading = true;
      try {
        const response = await axios.get('/api/owners', {
          params: {
            house: this.filter.house,
            name: this.filter.name,
            page: this.currentPage,
            size: this.pageSize
          }
        });
        this.ownerList = response.data.owners;
        this.total = response.data.total;
        this.$message.success('数据读取成功');
      } catch (error) {
        console.error('获取业主列表失败:', error);
        this.$message.error('数据读取失败，展示模拟数据');
        // 生成完整模拟数据
        this.ownerList = [
          {
            id: 999,
            houseName: '模拟花园1栋101',
            name: '张三',
            gender: 'M',
            idCard: '110101199003078888',
            phone: '13800138000',
            ownerType: '业主',
            updateTime: '2023-10-01 12:00:00',
            faceImage: '',
            email: 'zhangsan@example.com',
            city: '北京',
            address: '北京市朝阳区模拟街道1号'
          },
          {
            id: 1000,
            houseName: '模拟花园2栋202',
            name: '李四',
            gender: 'F',
            idCard: '310115198510128888',
            phone: '13900139000',
            ownerType: '租户',
            updateTime: '2023-10-01 14:00:00',
            faceImage: '',
            email: 'lisi@example.com',
            city: '上海',
            address: '上海市浦东新区模拟路88号'
          }
        ];
        this.total = this.ownerList.length;
      } finally {
        this.loading = false;
      }
    },


      // 权限管理
      async handlePermission(row) {
        this.permissionDialog.currentOwner = row;
        try {
          const response = await axios.get(`/api/owners/${row.id}/permission`);
          if (response.data.success) {
            this.permissionDialog.form = response.data.data;
          }
        } catch (error) {
          console.error('获取权限信息失败:', error);
          this.$message.error('获取权限信息失败');
        }
        this.permissionDialog.visible = true;
      },

      // 保存权限设置
      async savePermission() {
        try {
          const owner = this.permissionDialog.currentOwner;
          await axios.put(`/api/owners/${owner.id}/permission`, this.permissionDialog.form);
          this.$message.success('保存权限成功');
          this.permissionDialog.visible = false;
          this.fetchOwners();
        } catch (error) {
          console.error('保存权限失败:', error);
          this.$message.error('保存权限失败');
        }
      },

      // 人脸管理
      async handleFace(row) {
        this.faceDialog.currentOwner = row;
        this.faceDialog.imageUrl = row.faceImage || '';
        this.faceDialog.visible = true;
      },

      // 上传人脸图片
      async handleFaceUpload(file) {
        const formData = new FormData();
        formData.append('face', file);
        try {
          const owner = this.faceDialog.currentOwner;
          const response = await axios.post(`/api/owners/${owner.id}/face`, formData);
          if (response.data.success) {
            this.$message.success('上传人脸成功');
            this.faceDialog.imageUrl = response.data.faceImage;
            this.fetchOwners();
          }
        } catch (error) {
          console.error('上传人脸失败:', error);
          this.$message.error('上传人脸失败');
        }
      },

      // 编辑业主
      editOwner(row) {
        this.editDialog.currentOwner = row;
        this.editDialog.form = {
          name: row.name,
          gender: row.gender,
          phone: row.phone,
          idCard: row.idCard || '',
          email: row.email || '',
          city: row.city || '',
          address: row.address || '',
          ownerType: row.ownerType
        };
        this.editDialog.visible = true;
      },

      // 保存业主信息
      async saveOwner() {
        try {
          const owner = this.editDialog.currentOwner;
          await axios.put(`/api/owners/${owner.id}`, this.editDialog.form);
          this.$message.success('保存成功');
          this.editDialog.visible = false;
          this.fetchOwners();
        } catch (error) {
          console.error('保存失败:', error);
          this.$message.error('保存失败');
        }
      },

      // 删除业主
      async deleteOwner(row) {
        try {
          await this.$confirm('确认删除该业主?', '提示', {
            type: 'warning'
          });
          await axios.delete(`/api/owners/${row.id}`);
          this.$message.success('删除成功');
          this.fetchOwners();
        } catch (error) {
          if (error !== 'cancel') {
            console.error('删除失败:', error);
            this.$message.error('删除失败');
          }
        }
      },

      // 分页处理
      handlePageChange(page) {
        this.currentPage = page;
        this.fetchOwners();
      },

      // 搜索
      searchOwners() {
        this.currentPage = 1;
        this.fetchOwners();
      },

      // 导出模板
      async exportTemplate() {
        try {
          const response = await axios.get('/api/owners/export-template', {
            responseType: 'blob'
          });
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          link.download = '业主导入模板.xlsx';
          link.click();
          window.URL.revokeObjectURL(url);
        } catch (error) {
          console.error('导出模板失败:', error);
          this.$message.error('导出模板失败');
        }
      },

      // 导出业主
      async exportOwners() {
        try {
          const response = await axios.get('/api/owners/export', {
            responseType: 'blob'
          });
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          link.download = '业主信息.xlsx';
          link.click();
          window.URL.revokeObjectURL(url);
        } catch (error) {
          console.error('导出失败:', error);
          this.$message.error('导出失败');
        }
      },

      // 导入前检查
      beforeUpload(file) {
        const isExcel = file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' ||
                        file.type === 'application/vnd.ms-excel';
        if (!isExcel) {
          this.$message.error('只能上传 Excel 文件!');
          return false;
        }
        return true;
      },

      // 导入成功处理
      handleImportSuccess(response) {
        if (response.success) {
          this.$message.success('导入成功');
          this.fetchOwners();
        } else {
          this.$message.error(response.message || '导入失败');
        }
      },

      // 导入失败处理
      handleImportError() {
        this.$message.error('导入失败');
      }
    },

    created() {
      this.fetchOwners();
    }
  };
  </script>

  <style scoped>
  .owner-info-list {
    padding: 20px;
  }

  .filter-row {
    margin-bottom: 20px;
  }

  .filter-item {
    margin-right: 10px;
  }

  .el-button-group {
    margin-left: 10px;
  }

  .el-button + .el-button {
    margin-left: 10px;
  }

  .avatar-uploader {
    text-align: center;
  }

  .avatar-uploader .avatar {
    width: 178px;
    height: 178px;
    display: block;
  }

  .avatar-uploader .el-upload {
    border: 1px dashed var(--el-border-color);
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: var(--el-transition-duration-fast);
  }

  .avatar-uploader .el-upload:hover {
    border-color: var(--el-color-primary);
  }

  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    text-align: center;
  }

  .face-upload {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 200px;
  }
  </style>
