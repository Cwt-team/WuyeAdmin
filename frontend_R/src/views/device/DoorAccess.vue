<template>
  <div class="door-container">
    <el-card class="door-card">
      <template #header>
        <div class="card-header">
          <span>门禁信息管理</span>
          <el-button type="primary" size="small" @click="handleAdd">添加门禁</el-button>
        </div>
      </template>
      
      <!-- 搜索区域 -->
      <div class="search-box">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="门禁名称">
            <el-input v-model="searchForm.name" placeholder="请输入门禁名称" clearable></el-input>
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
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
              <el-option label="正常" value="正常" />
              <el-option label="故障" value="故障" />
              <el-option label="维修中" value="维修中" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 表格区域 -->
      <el-table :data="doorList" border style="width: 100%" v-loading="tableLoading">
        <el-table-column type="index" width="50" label="序号"></el-table-column>
        <el-table-column prop="name" label="门禁名称"></el-table-column>
        <el-table-column prop="communityName" label="所属小区"></el-table-column>
        <el-table-column prop="location" label="位置"></el-table-column>
        <el-table-column prop="deviceCode" label="设备编号"></el-table-column>
        <el-table-column prop="manufacturer" label="生产厂商"></el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="installTime" label="安装时间"></el-table-column>
        <el-table-column label="操作" width="250">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
            <el-button type="warning" size="small" @click="handleMaintenance(scope.row)">报修</el-button>
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
      :title="dialogType === 'add' ? '添加门禁' : '编辑门禁'"
      v-model="dialogVisible"
      width="600px"
    >
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="门禁名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入门禁名称"></el-input>
        </el-form-item>
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
        <el-form-item label="位置" prop="location">
          <el-input v-model="formData.location" placeholder="请输入位置"></el-input>
        </el-form-item>
        <el-form-item label="设备编号" prop="deviceCode">
          <el-input v-model="formData.deviceCode" placeholder="请输入设备编号"></el-input>
        </el-form-item>
        <el-form-item label="生产厂商" prop="manufacturer">
          <el-input v-model="formData.manufacturer" placeholder="请输入生产厂商"></el-input>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="formData.status" placeholder="请选择状态" style="width: 100%">
            <el-option label="正常" value="正常" />
            <el-option label="故障" value="故障" />
            <el-option label="维修中" value="维修中" />
          </el-select>
        </el-form-item>
        <el-form-item label="安装时间" prop="installTime">
          <el-date-picker
            v-model="formData.installTime"
            type="date"
            placeholder="选择日期"
            style="width: 100%"
            value-format="YYYY-MM-DD">
          </el-date-picker>
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

    <!-- 报修对话框 -->
    <el-dialog
      title="门禁报修"
      v-model="maintenanceVisible"
      width="500px"
    >
      <el-form :model="maintenanceForm" :rules="maintenanceRules" ref="maintenanceRef" label-width="100px">
        <el-form-item label="门禁名称">
          <el-input v-model="maintenanceForm.name" disabled></el-input>
        </el-form-item>
        <el-form-item label="故障类型" prop="faultType">
          <el-select v-model="maintenanceForm.faultType" placeholder="请选择故障类型" style="width: 100%">
            <el-option label="刷卡故障" value="刷卡故障" />
            <el-option label="电源问题" value="电源问题" />
            <el-option label="通讯故障" value="通讯故障" />
            <el-option label="机械故障" value="机械故障" />
            <el-option label="其他故障" value="其他故障" />
          </el-select>
        </el-form-item>
        <el-form-item label="故障描述" prop="description">
          <el-input v-model="maintenanceForm.description" type="textarea" placeholder="请详细描述故障情况"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="maintenanceVisible = false">取 消</el-button>
          <el-button type="primary" @click="submitMaintenance" :loading="maintenanceLoading">提 交</el-button>
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
  name: 'DoorAccessView',
  setup() {
    // 搜索表单
    const searchForm = reactive({
      name: '',
      communityId: '',
      status: ''
    })
    
    // 表格数据
    const doorList = ref([])
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
      name: '',
      communityId: '',
      location: '',
      deviceCode: '',
      manufacturer: '',
      status: '正常',
      installTime: '',
      remark: ''
    })
    
    // 表单验证规则
    const formRules = {
      name: [
        { required: true, message: '请输入门禁名称', trigger: 'blur' }
      ],
      communityId: [
        { required: true, message: '请选择所属小区', trigger: 'change' }
      ],
      location: [
        { required: true, message: '请输入位置', trigger: 'blur' }
      ],
      deviceCode: [
        { required: true, message: '请输入设备编号', trigger: 'blur' }
      ],
      status: [
        { required: true, message: '请选择状态', trigger: 'change' }
      ],
      installTime: [
        { required: true, message: '请选择安装时间', trigger: 'change' }
      ]
    }

    // 报修相关
    const maintenanceVisible = ref(false)
    const maintenanceRef = ref(null)
    const maintenanceLoading = ref(false)
    const maintenanceForm = reactive({
      id: '',
      name: '',
      faultType: '',
      description: ''
    })
    const maintenanceRules = {
      faultType: [
        { required: true, message: '请选择故障类型', trigger: 'change' }
      ],
      description: [
        { required: true, message: '请输入故障描述', trigger: 'blur' }
      ]
    }
    
    // 获取门禁列表
    const fetchDoorList = async () => {
      tableLoading.value = true
      try {
        // 在实际应用中，这里应该调用API接口获取数据
        // const response = await axios.get('/api/door/list', {
        //   params: {
        //     page: pagination.currentPage,
        //     pageSize: pagination.pageSize,
        //     ...searchForm
        //   }
        // })
        
        // 模拟数据，实际应用中应该使用API返回的数据
        setTimeout(() => {
          doorList.value = [
            {
              id: '1',
              name: '东门门禁',
              communityName: '阳光花园',
              location: '小区东门入口',
              deviceCode: 'DK2023001',
              manufacturer: '科技安防有限公司',
              status: '正常',
              installTime: '2023-04-15'
            },
            {
              id: '2',
              name: '西门门禁',
              communityName: '阳光花园',
              location: '小区西门入口',
              deviceCode: 'DK2023002',
              manufacturer: '科技安防有限公司',
              status: '维修中',
              installTime: '2023-04-16'
            },
            {
              id: '3',
              name: '北门门禁',
              communityName: '翠湖居',
              location: '小区北门入口',
              deviceCode: 'DK2023003',
              manufacturer: '安全智能科技公司',
              status: '故障',
              installTime: '2023-05-20'
            }
          ]
          pagination.total = 3
          tableLoading.value = false
        }, 500)
      } catch (error) {
        console.error('获取门禁列表失败:', error)
        ElMessage.error('获取门禁列表失败')
        tableLoading.value = false
      }
    }
    
    // 根据状态获取对应的Tag类型
    const getStatusType = (status) => {
      switch (status) {
        case '正常':
          return 'success'
        case '故障':
          return 'danger'
        case '维修中':
          return 'warning'
        default:
          return 'info'
      }
    }
    
    // 搜索
    const handleSearch = () => {
      pagination.currentPage = 1
      fetchDoorList()
    }
    
    // 重置搜索
    const handleReset = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = ''
      })
      pagination.currentPage = 1
      fetchDoorList()
    }
    
    // 添加门禁
    const handleAdd = () => {
      dialogType.value = 'add'
      resetForm()
      dialogVisible.value = true
    }
    
    // 编辑门禁
    const handleEdit = (row) => {
      dialogType.value = 'edit'
      resetForm()
      Object.keys(formData).forEach(key => {
        if (row[key] !== undefined) {
          formData[key] = row[key]
        }
      })
      // 模拟设置小区ID
      if (row.communityName === '阳光花园') {
        formData.communityId = '1'
      } else if (row.communityName === '翠湖居') {
        formData.communityId = '2'
      }
      dialogVisible.value = true
    }
    
    // 删除门禁
    // eslint-disable-next-line no-unused-vars
    const handleDelete = (row) => {
      ElMessageBox.confirm('确认删除该门禁信息吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          // 实际应用中应该调用API接口
          // await axios.delete(`/api/door/${row.id}`)
          ElMessage.success('删除成功')
          fetchDoorList()
        } catch (error) {
          console.error('删除门禁失败:', error)
          ElMessage.error('删除门禁失败')
        }
      }).catch(() => {})
    }

    // 报修门禁
    const handleMaintenance = (row) => {
      maintenanceForm.id = row.id
      maintenanceForm.name = row.name
      maintenanceForm.faultType = ''
      maintenanceForm.description = ''
      maintenanceVisible.value = true
    }

    // 提交报修
    const submitMaintenance = async () => {
      if (!maintenanceRef.value) return
      
      maintenanceRef.value.validate(async (valid) => {
        if (valid) {
          maintenanceLoading.value = true
          try {
            // 在实际应用中，这里应该调用API接口提交数据
            // await axios.post('/api/door/maintenance', maintenanceForm)
            
            setTimeout(() => {
              ElMessage.success('报修提交成功')
              maintenanceVisible.value = false
              // 更新门禁状态
              const door = doorList.value.find(item => item.id === maintenanceForm.id)
              if (door) {
                door.status = '维修中'
              }
              maintenanceLoading.value = false
            }, 500)
          } catch (error) {
            console.error('提交报修失败:', error)
            ElMessage.error('提交报修失败')
            maintenanceLoading.value = false
          }
        }
      })
    }
    
    // 提交表单
    const submitForm = async () => {
      if (!formRef.value) return
      
      formRef.value.validate(async (valid) => {
        if (valid) {
          submitLoading.value = true
          try {
            // 在实际应用中，这里应该调用API接口提交数据
            // const url = dialogType.value === 'add' ? '/api/door/add' : '/api/door/update'
            // await axios.post(url, formData)
            
            setTimeout(() => {
              ElMessage.success(dialogType.value === 'add' ? '添加成功' : '更新成功')
              dialogVisible.value = false
              fetchDoorList()
              submitLoading.value = false
            }, 500)
          } catch (error) {
            console.error('提交门禁数据失败:', error)
            ElMessage.error('提交门禁数据失败')
            submitLoading.value = false
          }
        }
      })
    }
    
    // 重置表单
    const resetForm = () => {
      if (formRef.value) {
        formRef.value.resetFields()
      }
      
      Object.assign(formData, {
        id: '',
        name: '',
        communityId: '',
        location: '',
        deviceCode: '',
        manufacturer: '',
        status: '正常',
        installTime: '',
        remark: ''
      })
    }
    
    // 分页大小改变
    const handleSizeChange = (val) => {
      pagination.pageSize = val
      fetchDoorList()
    }
    
    // 当前页改变
    const handleCurrentChange = (val) => {
      pagination.currentPage = val
      fetchDoorList()
    }
    
    // 初始化
    onMounted(() => {
      fetchDoorList()
    })
    
    return {
      searchForm,
      doorList,
      tableLoading,
      communityOptions,
      pagination,
      dialogVisible,
      dialogType,
      formRef,
      formData,
      formRules,
      submitLoading,
      maintenanceVisible,
      maintenanceRef,
      maintenanceForm,
      maintenanceRules,
      maintenanceLoading,
      getStatusType,
      handleSearch,
      handleReset,
      handleAdd,
      handleEdit,
      handleDelete,
      handleMaintenance,
      submitMaintenance,
      submitForm,
      handleSizeChange,
      handleCurrentChange
    }
  }
}
</script>

<style scoped>
.door-container {
  padding: 20px;
  animation: fade-in 0.3s;
}

.door-card {
  margin-bottom: 20px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--box-shadow);
  transition: all 0.3s;
  background: var(--card-bg-gradient);
  position: relative;
}

.door-card::before {
  content: '';
  position: absolute;
  right: 0;
  top: 0;
  width: 150px;
  height: 150px;
  background: linear-gradient(135deg, rgba(52, 152, 219, 0.1), rgba(52, 152, 219, 0.03));
  border-radius: 0 0 0 150px;
  z-index: 0;
}

.door-card::after {
  content: '';
  position: absolute;
  right: 20px;
  bottom: 20px;
  width: 100px;
  height: 100px;
  background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNlMGU4ZjUiIHN0cm9rZS13aWR0aD0iMSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0iZmVhdGhlciBmZWF0aGVyLWxvY2siPjxyZWN0IHg9IjMiIHk9IjExIiB3aWR0aD0iMTgiIGhlaWdodD0iMTEiIHJ4PSIyIiByeT0iMiI+PC9yZWN0PjxwYXRoIGQ9Ik03IDExVjdhNSA1IDAgMCAxIDEwIDB2NCI+PC9wYXRoPjwvc3ZnPg==');
  background-repeat: no-repeat;
  background-position: center;
  background-size: 100px;
  opacity: 0.2;
  z-index: 1;
}

.door-card:hover {
  box-shadow: var(--box-shadow-hover);
  transform: translateY(-3px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-color);
  background: linear-gradient(90deg, var(--bg-color-light), var(--bg-color));
  position: relative;
  z-index: 2;
}

.card-header span {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  position: relative;
  padding-left: 32px;
  display: flex;
  align-items: center;
}

.card-header span::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 24px;
  height: 24px;
  background: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiMzNDk4ZGIiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0iZmVhdGhlciBmZWF0aGVyLWtleSI+PHBhdGggZD0iTTIxIDE2VjhhMiAyIDAgMCAwLTEtMS43M2wtNy00YTIgMiAwIDAgMC0yIDBsLTcgNEEyIDIgMCAwIDAgMyA4djhhMiAyIDAgMCAwIDEgMS43M2w3IDRhMiAyIDAgMCAwIDIgMGw3LTRBMiAyIDAgMCAwIDIxIDE2eiI+PC9wYXRoPjxwb2x5bGluZSBwb2ludHM9IjcuODggMyAxMiA1LjEgMTYuMTIgMyI+PC9wb2x5bGluZT48bGluZSB4MT0iMTIiIHkxPSIyMi4wOCIgeDI9IjEyIiB5Mj0iNSI+PC9saW5lPjwvc3ZnPg==') no-repeat center center;
  background-size: contain;
}

.search-box {
  margin-bottom: 20px;
  background-color: rgba(248, 250, 252, 0.8);
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.03);
  border: 1px solid var(--border-color-light);
  backdrop-filter: blur(5px);
  position: relative;
  overflow: hidden;
}

.search-box::after {
  content: '';
  position: absolute;
  top: -20px;
  right: -20px;
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, rgba(52, 152, 219, 0.05), rgba(52, 152, 219, 0.02));
  border-radius: 50%;
  z-index: 0;
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

/* 状态标签定制样式 */
:deep(.el-tag--success) {
  background-color: rgba(103, 194, 58, 0.1);
  border-color: rgba(103, 194, 58, 0.2);
  color: #67c23a;
  border-radius: 12px;
  padding: 6px 12px;
}

:deep(.el-tag--danger) {
  background-color: rgba(245, 108, 108, 0.1);
  border-color: rgba(245, 108, 108, 0.2);
  color: #f56c6c;
  border-radius: 12px;
  padding: 6px 12px;
}

:deep(.el-tag--warning) {
  background-color: rgba(230, 162, 60, 0.1);
  border-color: rgba(230, 162, 60, 0.2);
  color: #e6a23c;
  border-radius: 12px;
  padding: 6px 12px;
}

/* 表格样式优化 */
:deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: var(--box-shadow-light);
}

:deep(.el-table__header-wrapper th) {
  background-color: var(--bg-color-darker) !important;
  color: var(--text-regular);
  font-weight: 600;
  padding: 12px 0;
}

:deep(.el-table__row) {
  transition: all 0.3s;
}

:deep(.el-table__row:hover) {
  transform: translateY(-2px);
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  z-index: 2;
  position: relative;
  background-color: var(--primary-light) !important;
}

/* 表格行交替颜色 */
:deep(.el-table__row:nth-child(even)) {
  background-color: var(--primary-lighter);
}

:deep(.el-button) {
  transition: all 0.3s;
}

:deep(.el-button:hover) {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 对话框样式 */
:deep(.el-dialog) {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--box-shadow-hover);
}

:deep(.el-dialog__header) {
  background-color: var(--bg-color);
  margin: 0;
  padding: 18px 20px;
  border-bottom: 1px solid var(--border-color);
}

:deep(.el-dialog__title) {
  font-weight: 600;
  color: var(--text-primary);
}

:deep(.el-dialog__body) {
  padding: 24px 30px;
}

:deep(.el-form-item) {
  margin-bottom: 22px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  padding-bottom: 8px;
}

:deep(.el-input), :deep(.el-select), :deep(.el-date-editor) {
  border-radius: 8px;
  width: 100%;
}

:deep(.el-input__inner), :deep(.el-textarea__inner) {
  border-radius: 8px;
  transition: all 0.3s;
}

:deep(.el-input__inner:focus), :deep(.el-textarea__inner:focus) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

/* 报修按钮特殊样式 */
:deep(.el-button--warning) {
  background: linear-gradient(135deg, #f39c12, #e67e22);
  border: none;
  color: white;
  box-shadow: 0 4px 10px rgba(230, 126, 34, 0.3);
}

:deep(.el-button--warning:hover) {
  background: linear-gradient(135deg, #f39c12, #e67e22);
  box-shadow: 0 6px 14px rgba(230, 126, 34, 0.4);
}

/* 添加维修表单特色样式 */
:deep(.maintenance-form .el-form-item__label) {
  color: #e67e22;
}
</style>  