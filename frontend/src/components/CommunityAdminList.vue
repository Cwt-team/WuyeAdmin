<template>
  <div class="community-admin-list">
    <el-card>
      <div class="header-section">
        <div class="left">
          <el-select v-model="selectedCompany" placeholder="1545惠氏科技" class="company-select">
            <el-option label="1545惠氏科技" value="1545" />
          </el-select>
        </div>
        <div class="right">
          <el-button type="primary" @click="showAddDialog = true">+ 添加管理员</el-button>
        </div>
      </div>

      <el-table :data="adminList" style="width: 100%" class="admin-table">
        <el-table-column prop="nickname" label="账号别名" />
        <el-table-column prop="username" label="账号" />
        <el-table-column prop="role" label="角色" />
        <el-table-column prop="phone" label="手机号码" />
        <el-table-column prop="email" label="电子邮箱" />
        <el-table-column prop="updateTime" label="更新时间" />
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" text size="small" @click="editAdmin(scope.row)">
              编辑
            </el-button>
            <el-button type="danger" text size="small" @click="deleteAdmin(scope.row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 空数据展示 -->
      <el-empty v-if="adminList.length === 0" description="暂无数据" />

      <el-pagination
        v-if="total > 0"
        background
        layout="sizes, prev, pager, next"
        :total="total"
        :current-page="currentPage"
        :page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />
    </el-card>

    <!-- 添加/编辑管理员对话框 -->
    <el-dialog
      :title="dialogTitle"
      v-model="showAddDialog"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="adminForm"
        :model="adminForm"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="别名" prop="nickname" required>
          <el-input v-model="adminForm.nickname" />
        </el-form-item>
        <el-form-item label="账号" prop="username" required>
          <el-input v-model="adminForm.username" />
        </el-form-item>
        <el-form-item label="角色" prop="role" required>
          <el-select v-model="adminForm.role" class="w-full">
            <el-option label="12312" value="12312" />
          </el-select>
        </el-form-item>
        <el-form-item label="手机号码" prop="phone">
          <el-input v-model="adminForm.phone">
            <template #prepend>
              <el-select v-model="phonePrefix" style="width: 100px">
                <el-option label="+86" value="+86" />
              </el-select>
            </template>
          </el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="submitAdmin">确定</el-button>
      </template>
    </el-dialog>

    <!-- 删除确认对话框 -->
    <el-dialog
      title="确认删除"
      v-model="deleteDialogVisible"
      width="300px"
    >
      <p>确定删除该角色？</p>
      <template #footer>
        <el-button @click="deleteDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmDelete">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage } from 'element-plus'

export default {
  name: 'CommunityAdminList',
  data() {
    return {
      selectedCompany: '1545',
      showAddDialog: false,
      deleteDialogVisible: false,
      deleteAdminData: null, // 存储要删除的管理员信息
      phonePrefix: '+86',
      search: {
        name: '',
        username: ''
      },
      adminForm: {
        nickname: '',
        username: '',
        role: '12312',
        phone: ''
      },
      rules: {
        nickname: [
          { required: true, message: '请输入别名', trigger: 'blur' }
        ],
        username: [
          { required: true, message: '请输入账号', trigger: 'blur' }
        ],
        role: [
          { required: true, message: '请选择角色', trigger: 'change' }
        ]
      },
      adminList: [
        {
          nickname: '12312',
          username: '1292956875494658048',
          role: '10001',
          phone: '',
          email: '',
          updateTime: '1728306541000'
        },
        {
          nickname: '测试用',
          username: '1332724551636881408',
          role: '10001',
          phone: '',
          email: '',
          updateTime: '1737787894000'
        }
      ],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      dialogTitle: '添加小区管理员'
    };
  },
  methods: {
    async fetchAdmins() {
      try {
        const response = await axios.get('/api/admins', {
          params: {
            name: this.search.name,
            username: this.search.username,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        this.adminList = response.data.admins;
        this.total = response.data.total;
        this.$message.success('数据加载成功');
      } catch (error) {
        console.error('获取管理员信息失败:', error);
        this.$message.error('获取管理员信息失败');
        // 使用示例数据
        this.adminList = [
          {
            nickname: '12312',
            username: '1292956875494658048',
            role: '10001',
            phone: '',
            email: '',
            updateTime: '1728306541000'
          },
          {
            nickname: '测试用',
            username: '1332724551636881408',
            role: '10001',
            phone: '',
            email: '',
            updateTime: '1737787894000'
          }
        ];
        this.total = this.adminList.length;
        this.$message.success('已加载模拟数据');
      }
    },
    searchAdmin() {
      this.currentPage = 1;
      this.fetchAdmins();
    },
    async handlePageChange(page) {
      this.currentPage = page;
      this.fetchAdmins();
    },
    editAdmin(row) {
      this.dialogTitle = '编辑小区管理员';
      this.adminForm = {
        nickname: row.nickname,
        username: row.username,
        role: row.role,
        phone: row.phone
      };
      this.showAddDialog = true;
    },
    deleteAdmin(row) {
      this.deleteAdminData = row; // 保存要删除的管理员信息
      this.deleteDialogVisible = true;
    },
    async submitAdmin() {
      this.$refs.adminForm.validate(async (valid) => {
        if (valid) {
          try {
            // 实际项目中这里应该调用API
            // const response = await axios.post('/api/admins', this.adminForm);
            ElMessage.success(this.dialogTitle === '添加小区管理员' ? '添加成功' : '修改成功');
            this.showAddDialog = false;
            this.fetchAdmins();
          } catch (error) {
            ElMessage.error('操作失败');
          }
        }
      });
    },
    async confirmDelete() {
      try {
        // 实际项目中这里应该调用API
        // await axios.delete(`/api/admins/${this.deleteAdminData.username}`);
        ElMessage.success('删除成功');
        this.deleteDialogVisible = false;
        this.deleteAdminData = null; // 重置删除数据
        this.fetchAdmins();
      } catch (error) {
        ElMessage.error('删除失败');
      }
    },
    handleSizeChange(size) {
      this.pageSize = size;
      this.fetchAdmins();
    },
  },
  mounted() {
    this.fetchAdmins();
  },
};
</script>

<style scoped>
.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.company-select {
  width: 200px;
}

.filter-item {
  margin-right: 20px;
}

.admin-table {
  margin-top: 20px;
}

.el-card {
  padding: 20px;
}

:deep(.el-button--text) {
  padding: 0 8px;
}

.w-full {
  width: 100%;
}
</style>
