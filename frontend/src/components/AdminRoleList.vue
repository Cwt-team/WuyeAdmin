<template>
  <div class="admin-role-list">
    <el-card>
      <div class="header-section">
        <el-input
          v-model="search"
          placeholder="搜索角色名称"
          class="filter-item"
          style="width: 200px"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button type="primary" @click="handleAdd">+ 添加角色</el-button>
      </div>

      <el-table :data="roleList" style="width: 100%" class="role-table">
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="id" label="标识 (ID)" />
        <el-table-column prop="sortNo" label="排序编号" />
        <el-table-column prop="createTime" label="创建时间" />
        <el-table-column prop="description" label="描述" />
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button
              type="primary"
              text
              size="small"
              @click="handlePermissions(scope.row)"
            >
              权限
            </el-button>
            <el-button
              type="primary"
              text
              size="small"
              @click="handleEdit(scope.row)"
            >
              编辑
            </el-button>
            <el-button
              type="danger"
              text
              size="small"
              @click="handleDelete(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-if="total > 0"
        background
        layout="prev, pager, next"
        :total="total"
        :current-page="currentPage"
        :page-size="pageSize"
        @current-change="handlePageChange"
      />
    </el-card>

    <!-- 添加/编辑角色对话框 -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="roleForm"
        :model="roleForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="角色名称" prop="name" required>
          <el-input v-model="roleForm.name" />
        </el-form-item>
        <el-form-item label="排序编号" prop="sortNo" required>
          <el-input v-model="roleForm.sortNo" />
        </el-form-item>
        <el-form-item label="角色描述" prop="description">
          <el-input v-model="roleForm.description" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitRole">确定</el-button>
      </template>
    </el-dialog>

    <!-- 删除确认对话框 -->
    <el-dialog
      title="确认删除"
      v-model="deleteDialogVisible"
      width="300px"
    >
      <p>确定要删除该角色？</p>
      <template #footer>
        <el-button @click="deleteDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmDelete">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'AdminRoleList',
  components: {
    Search
  },
  data() {
    return {
      search: '',
      roleList: [
        {
          name: '12312',
          id: '1292956875494658048',
          sortNo: '10001',
          createTime: '1728306541000',
          description: '123'
        },
        {
          name: '测试用',
          id: '1332724551636881408',
          sortNo: '10001',
          createTime: '1737787894000',
          description: ''
        }
      ],
      total: 2,
      currentPage: 1,
      pageSize: 10,
      dialogVisible: false,
      deleteDialogVisible: false,
      dialogTitle: '添加角色',
      roleForm: {
        name: '',
        sortNo: '',
        description: ''
      },
      deleteId: null,
      rules: {
        name: [
          { required: true, message: '请输入角色名称', trigger: 'blur' }
        ],
        sortNo: [
          { required: true, message: '请输入排序编号', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    async fetchRoles() {
      try {
        // 实际项目中这里应该调用API
        // const response = await axios.get('/api/roles', {
        //   params: {
        //     search: this.search,
        //     page: this.currentPage,
        //     size: this.pageSize
        //   }
        // });
        // this.roleList = response.data.list;
        // this.total = response.data.total;
      } catch (error) {
        ElMessage.error('获取角色列表失败')
      }
    },

    handleAdd() {
      this.dialogTitle = '添加角色'
      this.roleForm = {
        name: '',
        sortNo: '',
        description: ''
      }
      this.dialogVisible = true
    },

    handleEdit(row) {
      this.dialogTitle = '编辑角色'
      this.roleForm = {
        name: row.name,
        sortNo: row.sortNo,
        description: row.description
      }
      this.dialogVisible = true
    },

    handleDelete(row) {
      this.deleteId = row.id
      this.deleteDialogVisible = true
    },

    handlePermissions(row) {
      // 权限管理逻辑
      console.log('管理权限:', row)
    },

    async submitRole() {
      this.$refs.roleForm.validate(async (valid) => {
        if (valid) {
          try {
            // 实际项目中这里应该调用API
            // const response = await axios.post('/api/roles', this.roleForm);
            ElMessage.success(this.dialogTitle === '添加角色' ? '添加成功' : '修改成功')
            this.dialogVisible = false
            this.fetchRoles()
          } catch (error) {
            ElMessage.error('操作失败')
          }
        }
      })
    },

    async confirmDelete() {
      try {
        // 实际项目中这里应该调用API
        // await axios.delete(`/api/roles/${this.deleteId}`);
        ElMessage.success('删除成功')
        this.deleteDialogVisible = false
        this.fetchRoles()
      } catch (error) {
        ElMessage.error('删除失败')
      }
    },

    handlePageChange(page) {
      this.currentPage = page
      this.fetchRoles()
    }
  },
  mounted() {
    this.fetchRoles()
  }
}
</script>

<style scoped>
.header-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.role-table {
  margin-bottom: 20px;
}

:deep(.el-button--text) {
  padding: 0 8px;
}
</style>

