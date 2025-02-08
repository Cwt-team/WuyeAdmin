<template>
  <div class="community-info-list">
    <el-card>
      <el-row :gutter="20" class="mb-4">
        <el-col :span="6">
          <el-input
            v-model="search.keyword"
            placeholder="请输入小区名称/编号"
            clearable
          />
        </el-col>
        <el-col :span="6">
          <el-input
            v-model="search.location"
            placeholder="请输入所在城市"
            clearable
          />
        </el-col>
        <el-col :span="12">
          <el-button type="primary" @click="searchCommunity">查询</el-button>
          <el-button type="success" @click="addCommunity">添加小区</el-button>
        </el-col>
      </el-row>

      <el-table :data="communityList" style="width: 100%" v-loading="loading">
        <el-table-column prop="code" label="小区编号" />
        <el-table-column prop="name" label="小区名称" />
        <el-table-column prop="location" label="所在城市" />
        <el-table-column prop="createTime" label="创建时间" />
        <el-table-column label="操作" width="250">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editCommunity(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteCommunity(scope.row)">删除</el-button>
            <el-button type="info" size="small" @click="showConfig(scope.row)">配置</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        background
        layout="sizes, prev, pager, next"
        :total="total"
        :current-page="currentPage"
        :page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />

      <!-- 配置弹窗 -->
      <el-dialog 
        :title="dialogTitle" 
        v-model="showConfigDialog" 
        width="500px"
      >
        <el-form 
          :model="configForm" 
          label-width="140px"
          :rules="configRules"
          ref="configFormRef"
        >
          <el-form-item label="小区ID" v-if="configForm.id">
            <el-input v-model="configForm.id" disabled />
          </el-form-item>
          <el-form-item label="小区名称" prop="name">
            <el-input v-model="configForm.name" />
          </el-form-item>
          <el-form-item label="所在城市" prop="location">
            <el-input v-model="configForm.location" />
          </el-form-item>
          <el-form-item label="管理机数量" prop="managerMachineCount">
            <el-input-number v-model="configForm.managerMachineCount" :min="0" />
          </el-form-item>
          <el-form-item label="室内机数量" prop="indoorMachineCount">
            <el-input-number v-model="configForm.indoorMachineCount" :min="0" />
          </el-form-item>
          <el-form-item label="门禁卡类型" prop="accessCardType">
            <el-select v-model="configForm.accessCardType">
              <el-option label="NFC" value="NFC" />
              <el-option label="IC" value="IC" />
              <el-option label="ID" value="ID" />
            </el-select>
          </el-form-item>
          <el-form-item label="人脸识别" prop="appRecordFace">
            <el-switch v-model="configForm.appRecordFace" />
          </el-form-item>
          <el-form-item label="同步配置" prop="isSameStep">
            <el-switch v-model="configForm.isSameStep" />
          </el-form-item>
          <el-form-item label="记录上传" prop="isRecordUpload">
            <el-switch v-model="configForm.isRecordUpload" />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="showConfigDialog = false">取消</el-button>
            <el-button type="primary" @click="submitConfig">确定</el-button>
          </span>
        </template>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CommunityInfoList',
  data() {
    return {
      search: {
        keyword: '',
        location: ''
      },
      communityList: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      loading: false,
      showConfigDialog: false,
      dialogTitle: '',
      configForm: {
        id: null,
        name: '',
        location: '',
        managerMachineCount: 0,
        indoorMachineCount: 0,
        accessCardType: 'NFC',
        appRecordFace: true,
        isSameStep: true,
        isRecordUpload: true
      },
      configRules: {
        name: [{ required: true, message: '请输入小区名称', trigger: 'blur' }],
        location: [{ required: true, message: '请输入所在城市', trigger: 'blur' }]
      },
      mockData: [
        {
          id: 1,
          code: 'YG001',
          name: '阳光花园',
          location: '北京市朝阳区',
          createTime: '2024-06-07 09:48:00'
        },
        {
          id: 2,
          code: 'XF002',
          name: '幸福家园',
          location: '上海市浦东新区',
          createTime: '2024-06-07 10:00:00'
        }
      ]
    }
  },
  methods: {
    async fetchCommunities() {
      this.loading = true
      try {
        const response = await axios.get('/api/communities', {
          params: {
            keyword: this.search.keyword,
            location: this.search.location,
            page: this.currentPage,
            size: this.pageSize
          }
        })
        
        if (response.data) {
          this.communityList = response.data.items
          this.total = response.data.total
          this.$message.success('数据加载成功')
        }
      } catch (error) {
        console.error('获取小区列表失败:', error)
        this.$message.error('获取数据失败，显示模拟数据')
        this.communityList = this.mockData
        this.total = this.mockData.length
      } finally {
        this.loading = false
      }
    },

    async addCommunity() {
      this.dialogTitle = '添加小区'
      this.configForm = {
        id: null,
        name: '',
        location: '',
        managerMachineCount: 0,
        indoorMachineCount: 0,
        accessCardType: 'NFC',
        appRecordFace: true,
        isSameStep: true,
        isRecordUpload: true
      }
      this.showConfigDialog = true
    },

    async editCommunity(row) {
      this.dialogTitle = '编辑小区'
      this.configForm = { ...row }
      this.showConfigDialog = true
    },

    async deleteCommunity(row) {
      try {
        await this.$confirm('确认删除该小区吗？', '提示', {
          type: 'warning'
        })
        
        const response = await axios.delete(`/api/communities/${row.id}`)
        if (response.data.success) {
          this.$message.success('删除成功')
          this.fetchCommunities()
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除小区失败:', error)
          this.$message.error('删除失败')
        }
      }
    },

    async submitConfig() {
      try {
        const formRef = this.$refs.configFormRef
        await formRef.validate()
        
        if (this.configForm.id) {
          // 编辑
          const response = await axios.put(`/api/communities/${this.configForm.id}`, this.configForm)
          if (response.data.success) {
            this.$message.success('更新成功')
          }
        } else {
          // 新增
          const response = await axios.post('/api/communities', this.configForm)
          if (response.data.success) {
            this.$message.success('添加成功')
          }
        }
        
        this.showConfigDialog = false
        this.fetchCommunities()
      } catch (error) {
        if (error.message) {
          this.$message.error(error.message)
        } else {
          console.error('保存小区配置失败:', error)
          this.$message.error('保存失败')
        }
      }
    },

    searchCommunity() {
      this.currentPage = 1
      this.fetchCommunities()
    },

    handleSizeChange(size) {
      this.pageSize = size
      this.fetchCommunities()
    },

    handlePageChange(page) {
      this.currentPage = page
      this.fetchCommunities()
    },

    showConfig(row) {
      this.dialogTitle = '小区配置'
      this.configForm = { ...row }
      this.showConfigDialog = true
    }
  },
  mounted() {
    this.fetchCommunities()
  }
}
</script>

<style scoped>
.community-info-list {
  padding: 20px;
}
.mb-4 {
  margin-bottom: 16px;
}
.dialog-footer {
  text-align: right;
  margin-top: 20px;
}
</style>
