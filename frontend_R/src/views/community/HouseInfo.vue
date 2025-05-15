<template>
  <div class="house-container">
    <el-card class="house-card">
      <template #header>
        <div class="card-header">
          <span>房屋信息管理</span>
          <el-button type="primary" size="small" @click="handleAdd">添加房屋</el-button>
        </div>
      </template>
      
      <!-- 搜索区域 -->
      <div class="search-box">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="楼栋编号">
            <el-input v-model="searchForm.buildingCode" placeholder="请输入楼栋编号" clearable></el-input>
          </el-form-item>
          <el-form-item label="房屋编号">
            <el-input v-model="searchForm.houseCode" placeholder="请输入房屋编号" clearable></el-input>
          </el-form-item>
          <el-form-item label="所属小区">
            <el-select v-model="searchForm.communityId" placeholder="请选择小区" clearable>
              <el-option
                v-for="item in communityOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 表格区域 -->
      <el-table :data="houseList" border style="width: 100%" v-loading="tableLoading">
        <el-table-column type="index" width="50" label="序号"></el-table-column>
        <el-table-column prop="communityName" label="所属小区"></el-table-column>
        <el-table-column prop="buildingCode" label="楼栋编号"></el-table-column>
        <el-table-column prop="houseCode" label="房屋编号"></el-table-column>
        <el-table-column prop="houseArea" label="房屋面积(㎡)"></el-table-column>
        <el-table-column prop="houseUnit" label="户型"></el-table-column>
        <el-table-column prop="ownerName" label="业主姓名"></el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag :type="scope.row.status === '已入住' ? 'success' : 'info'">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
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
      :title="dialogType === 'add' ? '添加房屋' : '编辑房屋'"
      v-model="dialogVisible"
      width="600px"
    >
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="所属小区" prop="communityId">
          <el-select v-model="formData.communityId" placeholder="请选择小区" style="width: 100%">
            <el-option
              v-for="item in communityOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="楼栋编号" prop="buildingCode">
          <el-input v-model="formData.buildingCode" placeholder="请输入楼栋编号"></el-input>
        </el-form-item>
        <el-form-item label="房屋编号" prop="houseCode">
          <el-input v-model="formData.houseCode" placeholder="请输入房屋编号"></el-input>
        </el-form-item>
        <el-form-item label="房屋面积" prop="houseArea">
          <el-input-number v-model="formData.houseArea" :min="0" :precision="2" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="户型" prop="houseUnit">
          <el-select v-model="formData.houseUnit" placeholder="请选择户型" style="width: 100%">
            <el-option label="一室一厅" value="一室一厅" />
            <el-option label="两室一厅" value="两室一厅" />
            <el-option label="三室一厅" value="三室一厅" />
            <el-option label="三室两厅" value="三室两厅" />
            <el-option label="四室两厅" value="四室两厅" />
          </el-select>
        </el-form-item>
        <el-form-item label="业主姓名" prop="ownerName">
          <el-input v-model="formData.ownerName" placeholder="请输入业主姓名"></el-input>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="formData.status" placeholder="请选择状态" style="width: 100%">
            <el-option label="已入住" value="已入住" />
            <el-option label="未入住" value="未入住" />
            <el-option label="装修中" value="装修中" />
          </el-select>
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
  name: 'HouseInfoView',
  setup() {
    // 搜索表单
    const searchForm = reactive({
      buildingCode: '',
      houseCode: '',
      communityId: ''
    })
    
    // 表格数据
    const houseList = ref([])
    const tableLoading = ref(false)
    
    // 小区选项
    const communityOptions = ref([
      { value: '1', label: '阳光花园' },
      { value: '2', label: '翠湖居' }
    ])
    
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
      communityId: '',
      buildingCode: '',
      houseCode: '',
      houseArea: 0,
      houseUnit: '',
      ownerName: '',
      status: '未入住',
      remark: ''
    })
    
    // 表单验证规则
    const formRules = {
      communityId: [
        { required: true, message: '请选择所属小区', trigger: 'change' }
      ],
      buildingCode: [
        { required: true, message: '请输入楼栋编号', trigger: 'blur' }
      ],
      houseCode: [
        { required: true, message: '请输入房屋编号', trigger: 'blur' }
      ],
      houseArea: [
        { required: true, message: '请输入房屋面积', trigger: 'blur' }
      ],
      houseUnit: [
        { required: true, message: '请选择户型', trigger: 'change' }
      ]
    }
    
    // 获取房屋列表
    const fetchHouseList = async () => {
      tableLoading.value = true
      try {
        // 在实际应用中，这里应该调用API接口获取数据
        // const response = await axios.get('/api/house/list', {
        //   params: {
        //     page: pagination.currentPage,
        //     pageSize: pagination.pageSize,
        //     ...searchForm
        //   }
        // })
        
        // 模拟数据，实际应用中应该使用API返回的数据
        setTimeout(() => {
          houseList.value = [
            {
              id: '1',
              communityId: '1',
              communityName: '阳光花园',
              buildingCode: 'A栋',
              houseCode: 'A-101',
              houseArea: 89.5,
              houseUnit: '两室一厅',
              ownerName: '张三',
              status: '已入住'
            },
            {
              id: '2',
              communityId: '1',
              communityName: '阳光花园',
              buildingCode: 'A栋',
              houseCode: 'A-102',
              houseArea: 120.8,
              houseUnit: '三室两厅',
              ownerName: '李四',
              status: '已入住'
            },
            {
              id: '3',
              communityId: '2',
              communityName: '翠湖居',
              buildingCode: 'B栋',
              houseCode: 'B-201',
              houseArea: 75.3,
              houseUnit: '一室一厅',
              ownerName: '',
              status: '未入住'
            }
          ]
          pagination.total = 3
          tableLoading.value = false
        }, 500)
      } catch (error) {
        console.error('获取房屋列表失败:', error)
        ElMessage.error('获取房屋列表失败')
        tableLoading.value = false
      }
    }
    
    // 搜索
    const handleSearch = () => {
      pagination.currentPage = 1
      fetchHouseList()
    }
    
    // 重置搜索
    const handleReset = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = ''
      })
      pagination.currentPage = 1
      fetchHouseList()
    }
    
    // 添加房屋
    const handleAdd = () => {
      dialogType.value = 'add'
      resetForm()
      dialogVisible.value = true
    }
    
    // 编辑房屋
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
    
    // 删除房屋
    // eslint-disable-next-line no-unused-vars
    const handleDelete = (row) => {
      ElMessageBox.confirm('确认删除该房屋信息吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          // 实际应用中应该调用API接口
          // await axios.delete(`/api/house/${row.id}`)
          ElMessage.success('删除成功')
          fetchHouseList()
        } catch (error) {
          console.error('删除房屋失败:', error)
          ElMessage.error('删除房屋失败')
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
                // await axios.post('/api/house', formData)
                ElMessage.success('添加成功')
              } else {
                // 编辑
                // await axios.put(`/api/house/${formData.id}`, formData)
                ElMessage.success('编辑成功')
              }
              dialogVisible.value = false
              fetchHouseList()
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
      formData.communityId = ''
      formData.buildingCode = ''
      formData.houseCode = ''
      formData.houseArea = 0
      formData.houseUnit = ''
      formData.ownerName = ''
      formData.status = '未入住'
      formData.remark = ''
      if (formRef.value) {
        formRef.value.resetFields()
      }
    }
    
    // 分页处理
    const handleSizeChange = (size) => {
      pagination.pageSize = size
      fetchHouseList()
    }
    
    const handleCurrentChange = (page) => {
      pagination.currentPage = page
      fetchHouseList()
    }
    
    onMounted(() => {
      fetchHouseList()
    })
    
    return {
      searchForm,
      houseList,
      tableLoading,
      communityOptions,
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
.house-container {
  padding: 20px;
  animation: fade-in 0.3s;
}

.house-card {
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
}

.house-card:hover {
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

/* 表单样式 */
:deep(.el-dialog) {
  border-radius: 10px;
  overflow: hidden;
}

:deep(.el-dialog__header) {
  background-color: #f5f7fa;
  margin: 0;
  padding: 15px 20px;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-dialog__body) {
  padding: 20px 30px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-input), :deep(.el-select), :deep(.el-date-editor) {
  border-radius: 4px;
}
</style> 