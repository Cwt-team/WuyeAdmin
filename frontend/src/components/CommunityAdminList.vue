<template>
  <div class="community-admin-list">
    <el-card>
      <div class="header-section">
        <div class="left">
          <el-select v-model="selectedCompany" placeholder="请选择小区" class="company-select" @change="fetchAdmins">
            <el-option 
              v-for="item in communityOptions" 
              :key="item.id" 
              :label="item.community_name" 
              :value="item.id.toString()" 
            />
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
            <el-option
              v-for="role in roleOptions"
              :key="role.id"
              :label="role.name"
              :value="role.id"
            />
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
// import { ElMessage } from 'element-plus'

export default {
  name: 'CommunityAdminList',
  data() {
    return {
      selectedCompany: '',
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
      dialogTitle: '添加小区管理员',
      roleOptions: [], // 添加角色选项数组
      communityOptions: [], // 添加小区选项数组
    };
  },
  methods: {
    async fetchAdmins() {
      try {
        const response = await axios.get('/api/admins', {
          params: {
            name: this.search.name,
            username: this.search.username,
            communityId: this.selectedCompany,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        if (response.data.success) {
          this.adminList = response.data.data.admins;
          this.total = response.data.data.total;
          this.$message.success('数据加载成功');
        } else {
          throw new Error(response.data.message);
        }
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
            // 添加communityId字段
            const adminData = {
              ...this.adminForm,
              communityId: parseInt(this.selectedCompany)
            };
            
            const url = this.dialogTitle === '添加小区管理员' ? '/api/admins' : `/api/admins/${this.adminForm.id}`;
            const method = this.dialogTitle === '添加小区管理员' ? 'post' : 'put';
            const response = await axios[method](url, adminData);
            
            if (response.data.success) {
              this.$message.success(response.data.message);
              this.showAddDialog = false;
              this.fetchAdmins();
            } else {
              throw new Error(response.data.message);
            }
          } catch (error) {
            console.error('保存管理员失败:', error);
            this.$message.error(error.response?.data?.message || '操作失败');
          }
        }
      });
    },
    async confirmDelete() {
      try {
        const response = await axios.delete(`/api/admins/${this.deleteAdminData.id}`);
        if (response.data.success) {
          this.$message.success('删除成功');
          this.deleteDialogVisible = false;
          this.deleteAdminData = null;
          this.fetchAdmins();
        } else {
          throw new Error(response.data.message);
        }
      } catch (error) {
        console.error('删除管理员失败:', error);
        this.$message.error(error.response?.data?.message || '删除失败');
      }
    },
    handleSizeChange(size) {
      this.pageSize = size;
      this.fetchAdmins();
    },
    async fetchRoles() {
      try {
        const response = await axios.get('/api/admin-roles');
        if (response.data.success) {
          this.roleOptions = response.data.data.list;
        }
      } catch (error) {
        console.error('获取角色列表失败:', error);
        this.$message.error('获取角色列表失败');
      }
    },
    async fetchCommunities() {
      try {
        const response = await axios.get('/api/communities');
        if (response.data.success) {
          this.communityOptions = response.data.data.list;
          if (this.communityOptions.length > 0) {
            this.selectedCompany = this.communityOptions[0].id.toString();
            this.fetchAdmins();
          }
        } else {
          throw new Error(response.data.message);
        }
      } catch (error) {
        console.error('获取小区列表失败:', error);
        this.$message.error('获取小区列表失败');
        // 使用模拟数据
        this.communityOptions = [
          { id: 1, community_name: '阳光花园' },
          { id: 2, community_name: '翡翠湾' },
          { id: 3, community_name: '康庄小区' }
        ];
        this.selectedCompany = '1';
      }
    },
  },
  mounted() {
    this.fetchAdmins();
    this.fetchRoles();
    this.fetchCommunities();
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
