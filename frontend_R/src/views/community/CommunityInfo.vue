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
          <el-row :gutter="20">
            <el-col :span="6">
              <el-form-item label="小区名称/编号">
                <el-input v-model="searchForm.keyword" placeholder="请输入小区名称/编号" clearable>
                  <template #prefix v-if="searchForm.keyword"><el-icon><Search /></el-icon></template>
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="所在城市">
                <el-input v-model="searchForm.location" placeholder="请输入所在城市" clearable style="width: 100%" />
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="门禁卡类型">
                <el-select v-model="searchForm.accessCardType" placeholder="选择门禁卡类型" clearable style="width: 100%">
                  <el-option label="NFC" value="NFC" />
                  <el-option label="IC卡" value="IC卡" />
                  <el-option label="NONE" value="NONE" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="6">
              <el-form-item label="APP人脸录入">
                <el-select v-model="searchForm.appRecordFace" placeholder="选择人脸录入状态" clearable style="width: 100%">
                  <el-option label="开启" :value="1" />
                  <el-option label="关闭" :value="0" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="记录上传">
                <el-select v-model="searchForm.isRecordUpload" placeholder="选择记录上传状态" clearable style="width: 100%">
                  <el-option label="开启" :value="1" />
                  <el-option label="关闭" :value="0" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="配置同步">
                <el-select v-model="searchForm.isSameStep" placeholder="选择配置同步状态" clearable style="width: 100%">
                  <el-option label="已同步" :value="1" />
                  <el-option label="未同步" :value="0" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item>
                <el-button type="primary" @click="handleSearch" class="custom-button search-btn">查询</el-button>
                <el-button @click="handleReset" class="custom-button reset-btn">重置</el-button>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>
      
      <!-- 表格区域 -->
      <el-table :data="communityList" border style="width: 100%" v-loading="tableLoading">
        <el-table-column type="index" width="50" label="序号"></el-table-column>
        <el-table-column prop="code" label="小区编号"></el-table-column>
        <el-table-column prop="name" label="小区名称"></el-table-column>
        <el-table-column prop="area" label="所在地区"></el-table-column>
        <el-table-column prop="buildingCount" label="楼栋数量"></el-table-column>
        <el-table-column prop="houseCount" label="房屋数量"></el-table-column>
        <el-table-column prop="accessCardType" label="门禁卡类型"></el-table-column>
        <el-table-column prop="appRecordFace" label="APP人脸录入">
          <template #default="scope">
            <el-tag :type="scope.row.appRecordFace === 1 ? 'success' : 'info'">
              {{ scope.row.appRecordFace === 1 ? '开启' : '关闭' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="isSameStep" label="配置同步">
          <template #default="scope">
            <el-tag :type="scope.row.isSameStep === 1 ? 'success' : 'warning'">
              {{ scope.row.isSameStep === 1 ? '已同步' : '未同步' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间"></el-table-column>
        <el-table-column label="操作" width="180">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleEdit(scope.row)" class="custom-button edit-btn">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(scope.row)" class="custom-button delete-btn">删除</el-button>
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
        <el-form-item label="开发商" prop="developer" v-if="false">
          <el-input v-model="formData.developer" placeholder="请输入开发商"></el-input>
        </el-form-item>
        <el-form-item label="楼栋数量" prop="buildingCount">
          <el-input-number v-model="formData.buildingCount" :min="0" :precision="0"></el-input-number>
        </el-form-item>
        <el-form-item label="房屋数量" prop="houseCount">
          <el-input-number v-model="formData.houseCount" :min="0" :precision="0"></el-input-number>
        </el-form-item>
        <el-form-item label="门禁卡类型" prop="accessCardType">
          <el-select v-model="formData.accessCardType" placeholder="请选择门禁卡类型">
            <el-option label="NFC" value="NFC"></el-option>
            <el-option label="IC卡" value="IC卡"></el-option>
            <el-option label="NONE" value="NONE"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="APP人脸录入" prop="appRecordFace">
          <el-switch v-model="formData.appRecordFace" :active-value="1" :inactive-value="0"></el-switch>
        </el-form-item>
        <el-form-item label="配置同步状态" prop="isSameStep">
          <el-switch v-model="formData.isSameStep" :active-value="1" :inactive-value="0"></el-switch>
        </el-form-item>
        <el-form-item label="记录上传开关" prop="isRecordUpload">
          <el-switch v-model="formData.isRecordUpload" :active-value="1" :inactive-value="0"></el-switch>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="formData.remark" type="textarea" placeholder="请输入备注信息"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false" class="custom-button cancel-btn">取 消</el-button>
          <el-button type="primary" @click="submitForm" :loading="submitLoading" class="custom-button confirm-btn">确 定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import communityApi from '../../api/community'
import { Search } from '@element-plus/icons-vue'

export default {
  name: 'CommunityInfoView',
  components: {
    Search
  },
  setup() {
    // 搜索表单
    const searchForm = reactive({
      keyword: '',
      location: '',
      accessCardType: '',
      appRecordFace: null,
      isRecordUpload: null,
      isSameStep: null
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
      remark: '',
      accessCardType: 'NFC',
      appRecordFace: 1,
      isSameStep: 1,
      isRecordUpload: 1
    })
    
    // 表单验证规则
    const formRules = {
      name: [
        { required: true, message: '请输入小区名称', trigger: 'blur' },
        { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
      ],
      location: [
        { required: true, message: '请输入所在城市', trigger: 'blur' }
      ],
      address: [
        { required: true, message: '请输入详细地址', trigger: 'blur' }
      ]
    }
    
    // 获取小区列表
    const fetchCommunityList = async () => {
      tableLoading.value = true
      try {
        // 调用API接口获取数据
        const response = await communityApi.getCommunityList({
          page: pagination.currentPage,
          size: pagination.pageSize,
          keyword: searchForm.keyword,
          location: searchForm.location,
          accessCardType: searchForm.accessCardType || null,
          appRecordFace: searchForm.appRecordFace || null,
          isRecordUpload: searchForm.isRecordUpload || null,
          isSameStep: searchForm.isSameStep || null
        })
        
        // 处理后端返回的数据格式
        // 后端直接返回 {items: [...], total: 22} 的格式
        if (response.success && response.data) {
          // 如果response被request.js处理过，已经有标准格式
          communityList.value = response.data.list || []
          pagination.total = response.data.total || 0
        } else if (response.items) {
          // 直接处理后端原始返回格式
          // 将后端返回的数据格式转换为前端所需的格式
          communityList.value = response.items.map(item => communityApi.transformCommunityData(item))
          pagination.total = response.total || 0
        } else {
          communityList.value = []
          pagination.total = 0
          ElMessage.error('获取小区列表失败：数据格式不正确')
        }
      } catch (error) {
        console.error('获取小区列表失败:', error)
        ElMessage.error('获取小区列表失败，请稍后重试')
      } finally {
        tableLoading.value = false
      }
    }
    
    // 处理添加小区
    const handleAdd = () => {
      dialogType.value = 'add'
      resetForm()
      dialogVisible.value = true
    }
    
    // 处理编辑小区
    const handleEdit = (row) => {
      dialogType.value = 'edit'
      resetForm()
      // 复制行数据到表单
      formData.id = row.id
      formData.name = row.name
      formData.area = row.area
      formData.address = row.address
      formData.developer = row.developer || ''
      formData.buildingCount = row.buildingCount
      formData.houseCount = row.houseCount
      formData.remark = row.remark || ''
      formData.accessCardType = row.accessCardType
      formData.appRecordFace = row.appRecordFace
      formData.isSameStep = row.isSameStep
      formData.isRecordUpload = row.isRecordUpload
      
      dialogVisible.value = true
    }
    
    // 处理删除小区
    const handleDelete = (row) => {
      ElMessageBox.confirm('确定要删除该小区吗？删除后不可恢复', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          const response = await communityApi.deleteCommunity(row.id)
          if (response.success === true) {
            ElMessage.success('删除成功')
            fetchCommunityList()
          } else if (response.success === undefined && !response.error) {
            // 如果后端没有返回success字段，但也没有返回error，则认为成功
            ElMessage.success('删除成功')
            fetchCommunityList()
          } else {
            ElMessage.error(response.message || response.error || '删除失败')
          }
        } catch (error) {
          console.error('删除小区失败:', error)
          ElMessage.error('删除小区失败，请稍后重试')
        }
      }).catch(() => {
        // 取消删除
      })
    }
    
    // 提交表单
    const submitForm = async () => {
      if (!formRef.value) return
      
      try {
        await formRef.value.validate()
        
        submitLoading.value = true
        let response
        
        if (dialogType.value === 'add') {
          // 添加小区
          response = await communityApi.createCommunity(formData)
        } else {
          // 编辑小区
          response = await communityApi.updateCommunity(formData.id, formData)
        }
        
        if (response.success === true) {
          ElMessage.success(dialogType.value === 'add' ? '添加成功' : '更新成功')
          dialogVisible.value = false
          fetchCommunityList()
        } else if (response.success === undefined && !response.error) {
          // 如果后端没有返回success字段，但也没有返回error，则认为成功
          ElMessage.success(dialogType.value === 'add' ? '添加成功' : '更新成功')
          dialogVisible.value = false
          fetchCommunityList()
        } else {
          ElMessage.error(response.message || response.error || (dialogType.value === 'add' ? '添加失败' : '更新失败'))
        }
      } catch (error) {
        console.error(dialogType.value === 'add' ? '添加小区失败:' : '更新小区失败:', error)
        ElMessage.error(dialogType.value === 'add' ? '添加小区失败，请稍后重试' : '更新小区失败，请稍后重试')
      } finally {
        submitLoading.value = false
      }
    }
    
    // 重置表单
    const resetForm = () => {
      Object.keys(formData).forEach(key => {
        if (key === 'id') {
          formData[key] = ''
        } else if (key === 'buildingCount' || key === 'houseCount') {
          formData[key] = 0
        } else {
          formData[key] = ''
        }
      })
      
      if (formRef.value) {
        formRef.value.resetFields()
      }
    }
    
    // 处理搜索
    const handleSearch = () => {
      pagination.currentPage = 1
      fetchCommunityList()
    }
    
    // 处理重置
    const handleReset = () => {
      searchForm.keyword = ''
      searchForm.location = ''
      searchForm.accessCardType = ''
      searchForm.appRecordFace = null
      searchForm.isRecordUpload = null
      searchForm.isSameStep = null
      pagination.currentPage = 1
      fetchCommunityList()
    }
    
    // 处理页码变化
    const handleCurrentChange = (currentPage) => {
      pagination.currentPage = currentPage
      fetchCommunityList()
    }
    
    // 处理每页条数变化
    const handleSizeChange = (pageSize) => {
      pagination.pageSize = pageSize
      pagination.currentPage = 1
      fetchCommunityList()
    }
    
    // 初始化
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
      handleCurrentChange,
      handleSizeChange
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
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--box-shadow);
  transition: all 0.3s;
  background: var(--card-bg-gradient);
  position: relative;
}

.community-card::after {
  content: '';
  position: absolute;
  right: 0;
  bottom: 0;
  width: 140px;
  height: 140px;
  background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNmMGYyZjUiIHN0cm9rZS13aWR0aD0iMSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0iZmVhdGhlciBmZWF0aGVyLWhvbWUiPjxwYXRoIGQ9Ik0zIDlsOS03IDkgN3Y4YTIgMiAwIDAgMS0yIDJINWEyIDIgMCAwIDEtMi0yeiI+PC9wYXRoPjxwb2x5bGluZSBwb2ludHM9IjkgMjIgOSAxMiAxNSAxMiAxNSAyMiI+PC9wb2x5bGluZT48L3N2Zz4=');
  background-repeat: no-repeat;
  background-position: right bottom;
  background-size: 140px;
  opacity: 0.15;
  pointer-events: none;
}

.community-card:hover {
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
}

.card-header span {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  position: relative;
  padding-left: 12px;
  display: flex;
  align-items: center;
}

.card-header span::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 18px;
  background: linear-gradient(to bottom, #409EFF, #64b5f6);
  border-radius: 2px;
}

.search-box {
  margin-bottom: 20px;
  background-color: rgba(248, 250, 252, 0.8);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.03);
  border: 1px solid var(--border-color-light);
  backdrop-filter: blur(5px);
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
  background-color: var(--primary-light) !important;
  transform: translateY(-2px);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  position: relative;
  z-index: 2;
}

:deep(.el-button) {
  transition: all 0.3s;
}

:deep(.el-button:hover) {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 表单元素增强样式 */
:deep(.el-input__inner), :deep(.el-textarea__inner) {
  border-radius: 4px;
  transition: all 0.3s;
}

:deep(.el-input__inner:focus), :deep(.el-textarea__inner:focus) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

:deep(.el-form-item) {
  position: relative;
  margin-bottom: 25px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--text-regular);
}

/* 添加表格行交替颜色 */
:deep(.el-table__row:nth-child(even)) {
  background-color: var(--primary-lighter);
}

/* 简单选择框样式 */
.simple-select {
  width: 100%;
}

:deep(.simple-select .el-input__inner) {
  border-radius: 4px;
  border: 1px solid #DCDFE6;
  box-shadow: none;
}

:deep(.simple-select.el-select .el-input.is-focus .el-input__inner) {
  border-color: #409EFF;
}

:deep(.simple-select .el-select__placeholder) {
  color: #909399;
}

/* 确保选中值显示 */
:deep(.el-select-dropdown__item) {
  padding: 0 15px;
}

:deep(.el-select .el-select__tags) {
  max-width: 90%;
}

:deep(.el-select .el-input__inner) {
  box-sizing: border-box;
  cursor: pointer;
  padding-right: 30px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #606266 !important;
}

:deep(.el-select .el-select-v2__placeholder) {
  color: #909399;
}

:deep(.el-select:hover .el-input__inner) {
  border-color: #c0c4cc;
}

:deep(.el-select .el-input.is-focus .el-input__inner) {
  border-color: #409EFF;
}

:deep(.el-select .el-input__suffix) {
  top: 0;
  right: 5px;
  height: 100%;
}

/* 自定义按钮样式 */
.custom-button {
  border-radius: 8px;
  padding: 8px 16px;
  font-weight: 500;
  transition: all 0.3s ease;
  border: none;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.custom-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.custom-button:active {
  transform: translateY(1px);
}

/* 查询按钮 */
.search-btn {
  background: #3b82f6;
  color: white;
}

.search-btn:hover {
  background: #2563eb;
}

/* 重置按钮 */
.reset-btn {
  background: #f3f4f6;
  color: #4b5563;
}

.reset-btn:hover {
  background: #e5e7eb;
}

/* 编辑按钮 */
.edit-btn {
  background: #10b981;
  color: white;
}

.edit-btn:hover {
  background: #059669;
}

/* 删除按钮 */
.delete-btn {
  background: #f43f5e;
  color: white;
}

.delete-btn:hover {
  background: #e11d48;
}

/* 取消按钮 */
.cancel-btn {
  background: #f3f4f6;
  color: #4b5563;
}

.cancel-btn:hover {
  background: #e5e7eb;
}

/* 确认按钮 */
.confirm-btn {
  background: #3b82f6;
  color: white;
}

.confirm-btn:hover {
  background: #2563eb;
}
</style> 