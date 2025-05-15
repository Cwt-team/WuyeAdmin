<template>
  <div class="community-container">
    <el-card class="community-card">
      <template #header>
        <div class="card-header">
          <span>小区信息管理</span>
          <el-button type="primary" size="small" @click="handleAdd">添加小区</el-button>
        </div>
      </template>
      
      <!-- 搜索区域 -->
      <div class="search-box">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="小区名称">
            <el-input v-model="searchForm.name" placeholder="请输入小区名称" clearable></el-input>
          </el-form-item>
          <el-form-item label="所在地区">
            <el-input v-model="searchForm.area" placeholder="请输入所在地区" clearable></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 表格区域 -->
      <el-table :data="communityList" border style="width: 100%" v-loading="tableLoading">
        <el-table-column type="index" width="50" label="序号"></el-table-column>
        <el-table-column prop="name" label="小区名称"></el-table-column>
        <el-table-column prop="area" label="所在地区"></el-table-column>
        <el-table-column prop="address" label="详细地址"></el-table-column>
        <el-table-column prop="developer" label="开发商"></el-table-column>
        <el-table-column prop="buildingCount" label="楼栋数量"></el-table-column>
        <el-table-column prop="houseCount" label="房屋数量"></el-table-column>
        <el-table-column prop="createTime" label="创建时间"></el-table-column>
        <el-table-column label="操作" width="180">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页区域 -->
      <div class="pagination-container">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total">
        </el-pagination>
      </div>
    </el-card>
    
    <!-- 添加/编辑对话框 -->
    <el-dialog
      :title="dialogType === 'add' ? '添加小区' : '编辑小区'"
      v-model="dialogVisible"
      width="600px"
    >
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="小区名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入小区名称"></el-input>
        </el-form-item>
        <el-form-item label="所在地区" prop="area">
          <el-input v-model="formData.area" placeholder="请输入所在地区"></el-input>
        </el-form-item>
        <el-form-item label="详细地址" prop="address">
          <el-input v-model="formData.address" placeholder="请输入详细地址"></el-input>
        </el-form-item>
        <el-form-item label="开发商" prop="developer">
          <el-input v-model="formData.developer" placeholder="请输入开发商"></el-input>
        </el-form-item>
        <el-form-item label="楼栋数量" prop="buildingCount">
          <el-input-number v-model="formData.buildingCount" :min="0" :precision="0"></el-input-number>
        </el-form-item>
        <el-form-item label="房屋数量" prop="houseCount">
          <el-input-number v-model="formData.houseCount" :min="0" :precision="0"></el-input-number>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="formData.remark" type="textarea" placeholder="请输入备注信息"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="submitForm" :loading="submitLoading">确 定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
// import axios from 'axios'

export default {
  name: 'CommunityInfoView',
  setup() {
    // 搜索表单
    const searchForm = reactive({
      name: '',
      area: ''
    })
    
    // 表格数据
    const communityList = ref([])
    const tableLoading = ref(false)
    
    // 分页配置
    const pagination = reactive({
      currentPage: 1,
      pageSize: 10,
      total: 0
    })
    
    // 对话框控制
    const dialogVisible = ref(false)
    const dialogType = ref('add') // 'add' 或 'edit'
    const formRef = ref(null)
    const submitLoading = ref(false)
    
    // 表单数据
    const formData = reactive({
      id: '',
      name: '',
      area: '',
      address: '',
      developer: '',
      buildingCount: 0,
      houseCount: 0,
      remark: ''
    })
    
    // 表单验证规则
    const formRules = {
      name: [
        { required: true, message: '请输入小区名称', trigger: 'blur' },
        { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
      ],
      area: [
        { required: true, message: '请输入所在地区', trigger: 'blur' }
      ],
      address: [
        { required: true, message: '请输入详细地址', trigger: 'blur' }
      ]
    }
    
    // 获取小区列表
    const fetchCommunityList = async () => {
      tableLoading.value = true
      try {
        // 在实际应用中，这里应该调用API接口获取数据
        // const response = await axios.get('/api/community/list', {
        //   params: {
        //     page: pagination.currentPage,
        //     pageSize: pagination.pageSize,
        //     ...searchForm
        //   }
        // })
        
        // 模拟数据，实际应用中应该使用API返回的数据
        setTimeout(() => {
          communityList.value = [
            {
              id: '1',
              name: '阳光花园',
              area: '西湖区',
              address: '杭州市西湖区文三路123号',
              developer: '阳光地产',
              buildingCount: 12,
              houseCount: 360,
              createTime: '2023-05-12'
            },
            {
              id: '2',
              name: '翠湖居',
              area: '滨江区',
              address: '杭州市滨江区江南大道500号',
              developer: '绿城地产',
              buildingCount: 8,
              houseCount: 240,
              createTime: '2023-06-18'
            }
          ]
          pagination.total = 2
          tableLoading.value = false
        }, 500)
      } catch (error) {
        console.error('获取小区列表失败:', error)
        ElMessage.error('获取小区列表失败')
        tableLoading.value = false
      }
    }
    
    // 搜索
    const handleSearch = () => {
      pagination.currentPage = 1
      fetchCommunityList()
    }
    
    // 重置搜索
    const handleReset = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = ''
      })
      pagination.currentPage = 1
      fetchCommunityList()
    }
    
    // 添加小区
    const handleAdd = () => {
      dialogType.value = 'add'
      resetForm()
      dialogVisible.value = true
    }
    
    // 编辑小区
    const handleEdit = (row) => {
      dialogType.value = 'edit'
      resetForm()
      Object.keys(formData).forEach(key => {
        if (row[key] !== undefined) {
          formData[key] = row[key]
        }
      })
      dialogVisible.value = true
    }
    
    // 删除小区
    // eslint-disable-next-line no-unused-vars
    const handleDelete = (row) => {
      ElMessageBox.confirm('确认删除该小区信息吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          // 实际应用中应该调用API接口
          // await axios.delete(`/api/community/${row.id}`)
          ElMessage.success('删除成功')
          fetchCommunityList()
        } catch (error) {
          console.error('删除小区失败:', error)
          ElMessage.error('删除小区失败')
        }
      }).catch(() => {
        // 取消删除
      })
    }
    
    // 表单提交
    const submitForm = () => {
      if (formRef.value) {
        formRef.value.validate(async (valid) => {
          if (valid) {
            submitLoading.value = true
            try {
              // 实际应用中应该调用API接口
              if (dialogType.value === 'add') {
                // 添加
                // await axios.post('/api/community', formData)
                ElMessage.success('添加成功')
              } else {
                // 编辑
                // await axios.put(`/api/community/${formData.id}`, formData)
                ElMessage.success('编辑成功')
              }
              dialogVisible.value = false
              fetchCommunityList()
            } catch (error) {
              console.error('提交表单失败:', error)
              ElMessage.error('提交表单失败')
            } finally {
              submitLoading.value = false
            }
          }
        })
      }
    }
    
    // 重置表单
    const resetForm = () => {
      formData.id = ''
      formData.name = ''
      formData.area = ''
      formData.address = ''
      formData.developer = ''
      formData.buildingCount = 0
      formData.houseCount = 0
      formData.remark = ''
      if (formRef.value) {
        formRef.value.resetFields()
      }
    }
    
    // 分页处理
    const handleSizeChange = (size) => {
      pagination.pageSize = size
      fetchCommunityList()
    }
    
    const handleCurrentChange = (page) => {
      pagination.currentPage = page
      fetchCommunityList()
    }
    
    onMounted(() => {
      fetchCommunityList()
    })
    
    return {
      searchForm,
      communityList,
      tableLoading,
      pagination,
      dialogVisible,
      dialogType,
      formRef,
      formData,
      formRules,
      submitLoading,
      handleSearch,
      handleReset,
      handleAdd,
      handleEdit,
      handleDelete,
      submitForm,
      handleSizeChange,
      handleCurrentChange
    }
  }
}
</script>

<style scoped>
.community-container {
  padding: 20px;
  animation: fade-in 0.3s;
}

.community-card {
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
}

.community-card:hover {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
  transform: translateY(-3px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
}

.card-header span {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  position: relative;
  padding-left: 12px;
}

.card-header span::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 18px;
  background: linear-gradient(to bottom, #409EFF, #53a8ff);
  border-radius: 2px;
}

.search-box {
  margin-bottom: 20px;
  background-color: #f8fafc;
  padding: 20px;
  border-radius: 8px;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
  padding: 10px 0;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 表格样式优化 */
:deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-table__header-wrapper th) {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: 600;
}

:deep(.el-button) {
  transition: all 0.3s;
}

:deep(.el-button:hover) {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style> 