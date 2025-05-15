<template>
  <div class="owner-container">
    <el-card class="owner-card">
      <template #header>
        <div class="card-header">
          <span>业主信息管理</span>
          <el-button type="primary" size="small" @click="handleAdd">添加业主</el-button>
        </div>
      </template>
      
      <!-- 搜索区域 -->
      <div class="search-box">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="业主姓名">
            <el-input v-model="searchForm.name" placeholder="请输入业主姓名" clearable></el-input>
          </el-form-item>
          <el-form-item label="联系电话">
            <el-input v-model="searchForm.phone" placeholder="请输入联系电话" clearable></el-input>
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
      <el-table :data="ownerList" border style="width: 100%" v-loading="tableLoading">
        <el-table-column type="index" width="50" label="序号"></el-table-column>
        <el-table-column prop="name" label="业主姓名"></el-table-column>
        <el-table-column prop="gender" label="性别">
          <template #default="scope">
            {{ scope.row.gender === 1 ? '男' : '女' }}
          </template>
        </el-table-column>
        <el-table-column prop="phone" label="联系电话"></el-table-column>
        <el-table-column prop="idCard" label="身份证号">
          <template #default="scope">
            {{ formatIdCard(scope.row.idCard) }}
          </template>
        </el-table-column>
        <el-table-column prop="communityName" label="所属小区"></el-table-column>
        <el-table-column prop="houseInfo" label="房屋信息"></el-table-column>
        <el-table-column prop="createTime" label="创建时间"></el-table-column>
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
      :title="dialogType === 'add' ? '添加业主' : '编辑业主'"
      v-model="dialogVisible"
      width="600px"
    >
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="业主姓名" prop="name">
          <el-input v-model="formData.name" placeholder="请输入业主姓名"></el-input>
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-radio-group v-model="formData.gender">
            <el-radio :label="1">男</el-radio>
            <el-radio :label="2">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="formData.phone" placeholder="请输入联系电话"></el-input>
        </el-form-item>
        <el-form-item label="身份证号" prop="idCard">
          <el-input v-model="formData.idCard" placeholder="请输入身份证号"></el-input>
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
        <el-form-item label="房屋信息" prop="houseId">
          <el-select 
            v-model="formData.houseId" 
            placeholder="请选择房屋" 
            style="width: 100%"
            :disabled="!formData.communityId"
            filterable
          >
            <el-option
              v-for="item in houseOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
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
import { ref, reactive, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
// import axios from 'axios'

export default {
  name: 'OwnerInfoView',
  setup() {
    // 搜索表单
    const searchForm = reactive({
      name: '',
      phone: '',
      communityId: ''
    })
    
    // 表格数据
    const ownerList = ref([])
    const tableLoading = ref(false)
    
    // 小区选项
    const communityOptions = ref([
      { value: '1', label: '阳光花园' },
      { value: '2', label: '翠湖居' }
    ])
    
    // 房屋选项
    const houseOptions = ref([])
    
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
      gender: 1,
      phone: '',
      idCard: '',
      communityId: '',
      houseId: '',
      remark: ''
    })
    
    // 表单验证规则
    const formRules = {
      name: [
        { required: true, message: '请输入业主姓名', trigger: 'blur' },
        { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
      ],
      gender: [
        { required: true, message: '请选择性别', trigger: 'change' }
      ],
      phone: [
        { required: true, message: '请输入联系电话', trigger: 'blur' },
        { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
      ],
      idCard: [
        { required: true, message: '请输入身份证号', trigger: 'blur' },
        { pattern: /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/, message: '请输入正确的身份证号码', trigger: 'blur' }
      ],
      communityId: [
        { required: true, message: '请选择所属小区', trigger: 'change' }
      ],
      houseId: [
        { required: true, message: '请选择房屋', trigger: 'change' }
      ]
    }
    
    // 监听小区选择变化，更新房屋选项
    watch(() => formData.communityId, (newValue) => {
      if (newValue) {
        fetchHouseOptions(newValue)
      } else {
        houseOptions.value = []
        formData.houseId = ''
      }
    })
    
    // 获取房屋选项
    const fetchHouseOptions = async (communityId) => {
      try {
        // 实际应用中应该调用API接口
        // const response = await axios.get(`/api/house/listByCommunity/${communityId}`)
        // houseOptions.value = response.data.map(item => ({
        //   value: item.id,
        //   label: `${item.buildingCode}-${item.houseCode}`
        // }))
        
        // 模拟数据
        if (communityId === '1') {
          houseOptions.value = [
            { value: '101', label: 'A1-101' },
            { value: '102', label: 'A1-102' },
            { value: '201', label: 'A2-201' }
          ]
        } else if (communityId === '2') {
          houseOptions.value = [
            { value: '301', label: 'B1-301' },
            { value: '302', label: 'B1-302' }
          ]
        }
      } catch (error) {
        console.error('获取房屋选项失败:', error)
        ElMessage.error('获取房屋选项失败')
      }
    }
    
    // 获取业主列表
    const fetchOwnerList = async () => {
      tableLoading.value = true
      try {
        // 在实际应用中，这里应该调用API接口获取数据
        // const response = await axios.get('/api/owner/list', {
        //   params: {
        //     page: pagination.currentPage,
        //     pageSize: pagination.pageSize,
        //     ...searchForm
        //   }
        // })
        
        // 模拟数据，实际应用中应该使用API返回的数据
        setTimeout(() => {
          ownerList.value = [
            {
              id: '1',
              name: '张三',
              gender: 1,
              phone: '13800138000',
              idCard: '330102198801012345',
              communityName: '阳光花园',
              houseInfo: 'A1-101',
              createTime: '2023-05-15'
            },
            {
              id: '2',
              name: '李四',
              gender: 2,
              phone: '13900139000',
              idCard: '330102199001023456',
              communityName: '翠湖居',
              houseInfo: 'B1-301',
              createTime: '2023-06-20'
            }
          ]
          pagination.total = 2
          tableLoading.value = false
        }, 500)
      } catch (error) {
        console.error('获取业主列表失败:', error)
        ElMessage.error('获取业主列表失败')
        tableLoading.value = false
      }
    }
    
    // 搜索
    const handleSearch = () => {
      pagination.currentPage = 1
      fetchOwnerList()
    }
    
    // 重置搜索
    const handleReset = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = ''
      })
      pagination.currentPage = 1
      fetchOwnerList()
    }
    
    // 添加业主
    const handleAdd = () => {
      dialogType.value = 'add'
      resetForm()
      dialogVisible.value = true
    }
    
    // 编辑业主
    const handleEdit = (row) => {
      dialogType.value = 'edit'
      resetForm()
      Object.keys(formData).forEach(key => {
        if (row[key] !== undefined) {
          formData[key] = row[key]
        }
      })
      // 模拟设置小区和房屋ID
      if (row.communityName === '阳光花园') {
        formData.communityId = '1'
        formData.houseId = '101'
      } else if (row.communityName === '翠湖居') {
        formData.communityId = '2'
        formData.houseId = '301'
      }
      dialogVisible.value = true
    }
    
    // 删除业主
    // eslint-disable-next-line no-unused-vars
    const handleDelete = (row) => {
      ElMessageBox.confirm('确认删除该业主信息吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          // 实际应用中应该调用API接口
          // await axios.delete(`/api/owner/${row.id}`)
          ElMessage.success('删除成功')
          fetchOwnerList()
        } catch (error) {
          console.error('删除业主失败:', error)
          ElMessage.error('删除业主失败')
        }
      }).catch(() => {})
    }
    
    // 提交表单
    const submitForm = async () => {
      if (!formRef.value) return
      
      formRef.value.validate(async (valid) => {
        if (valid) {
          submitLoading.value = true
          try {
            // 在实际应用中，这里应该调用API接口提交数据
            // const url = dialogType.value === 'add' ? '/api/owner/add' : '/api/owner/update'
            // await axios.post(url, formData)
            
            setTimeout(() => {
              ElMessage.success(dialogType.value === 'add' ? '添加成功' : '更新成功')
              dialogVisible.value = false
              fetchOwnerList()
              submitLoading.value = false
            }, 500)
          } catch (error) {
            console.error('提交业主数据失败:', error)
            ElMessage.error('提交业主数据失败')
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
        gender: 1,
        phone: '',
        idCard: '',
        communityId: '',
        houseId: '',
        remark: ''
      })
    }
    
    // 格式化身份证号（保留前4位和后4位，中间用*代替）
    const formatIdCard = (idCard) => {
      if (!idCard) return ''
      if (idCard.length <= 8) return idCard
      return idCard.substr(0, 4) + '********' + idCard.substr(-4)
    }
    
    // 分页大小改变
    const handleSizeChange = (val) => {
      pagination.pageSize = val
      fetchOwnerList()
    }
    
    // 当前页改变
    const handleCurrentChange = (val) => {
      pagination.currentPage = val
      fetchOwnerList()
    }
    
    // 初始化
    onMounted(() => {
      fetchOwnerList()
    })
    
    return {
      searchForm,
      ownerList,
      tableLoading,
      communityOptions,
      houseOptions,
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
      handleCurrentChange,
      formatIdCard
    }
  }
}
</script>

<style scoped>
.owner-container {
  padding: 20px;
  animation: fade-in 0.3s;
}

.owner-card {
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
  position: relative;
}

.owner-card:hover {
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
  display: flex;
  align-items: center;
}

.card-header span::before {
  content: '\f007'; /* FontAwesome用户图标 */
  font-family: 'FontAwesome', sans-serif;
  margin-right: 8px;
  color: #409EFF;
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

:deep(.el-table__row:hover td) {
  background-color: #ecf5ff !important;
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
  border-radius: 10px;
  overflow: hidden;
}

:deep(.el-dialog__header) {
  background-color: #f5f7fa;
  margin: 0;
  padding: 15px 20px;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-dialog__title) {
  font-weight: 600;
  color: #303133;
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