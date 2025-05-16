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
        <el-table-column prop="name" label="业主姓名">
          <template #default="scope">
            <div class="owner-avatar">
              {{ scope.row.name.charAt(0) }}
            </div>
            {{ scope.row.name }}
          </template>
        </el-table-column>
        <el-table-column prop="gender" label="性别">
          <template #default="scope">
            <div :class="['gender-tag', scope.row.gender === 1 ? 'male' : 'female']">
              {{ scope.row.gender === 1 ? '男' : '女' }}
            </div>
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
import ownerApi from '../../api/owner'
import communityApi from '../../api/community'
import houseApi from '../../api/house'

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
    const communityOptions = ref([])
    
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
        // 调用API获取房屋列表
        const response = await houseApi.getHouseOptions(communityId)
        
        console.log('房屋选项响应:', response)
        
        let data = []
        
        // 处理不同响应格式
        if (response && response.success && response.data) {
          if (Array.isArray(response.data)) {
            data = response.data
          } else if (response.data.items && Array.isArray(response.data.items)) {
            data = response.data.items
          } else if (response.data.list && Array.isArray(response.data.list)) {
            data = response.data.list
          }
        } else if (response && response.items && Array.isArray(response.items)) {
          data = response.items
        } else if (Array.isArray(response)) {
          data = response
        }
        
        // 过滤出房间级别的房屋
        const rooms = data.filter(house => 
          house.level === 4 || house.roomNumber || house.houseCode
        )
        
        houseOptions.value = rooms.map(house => ({
          value: house.id,
          label: house.fullName || `${house.buildingNumber || house.buildingCode || ''}栋${house.unitNumber || ''}单元${house.roomNumber || house.houseCode || ''}室`
        }))
        
        if (houseOptions.value.length === 0) {
          // 如果没有获取到房间，尝试以其他方式获取房屋列表
          const treeResponse = await houseApi.getHouseTree(communityId)
          
          if (treeResponse) {
            // 从树形结构中提取所有房间
            const extractRooms = (nodes) => {
              if (!nodes || !Array.isArray(nodes)) return []
              
              let rooms = []
              
              nodes.forEach(node => {
                if (node.level === 4 || node.roomNumber || node.houseCode) {
                  rooms.push(node)
                }
                
                if (node.children && node.children.length > 0) {
                  rooms = rooms.concat(extractRooms(node.children))
                }
              })
              
              return rooms
            }
            
            let treeData = []
            
            if (treeResponse.success && treeResponse.data) {
              treeData = treeResponse.data
            } else if (Array.isArray(treeResponse)) {
              treeData = treeResponse
            }
            
            const roomsFromTree = extractRooms(treeData)
            
            houseOptions.value = roomsFromTree.map(house => ({
              value: house.id,
              label: house.fullName || `${house.buildingNumber || house.buildingCode || ''}栋${house.unitNumber || ''}单元${house.roomNumber || house.houseCode || ''}室`
            }))
          }
        }
      } catch (error) {
        console.error('获取房屋选项失败:', error)
        ElMessage.error('获取房屋选项失败')
        houseOptions.value = []
      }
    }
    
    // 获取业主列表
    const fetchOwnerList = async () => {
      tableLoading.value = true
      try {
        // 构建查询参数
        const params = {
          page: pagination.currentPage,
          size: pagination.pageSize,
          name: searchForm.name,
          phone: searchForm.phone
        }
        
        // 添加社区ID过滤条件
        if (searchForm.communityId) {
          params.communityId = searchForm.communityId
        }
        
        // 调用API获取业主列表
        const response = await ownerApi.getOwnerList(params)
        console.log('业主列表响应:', response)
        
        let data = []
        let total = 0
        
        // 处理不同格式的响应数据
        if (response && response.success && response.data) {
          // 标准响应格式
          if (Array.isArray(response.data)) {
            data = response.data
            total = data.length
          } else if (response.data.owners && Array.isArray(response.data.owners)) {
            data = response.data.owners
            total = response.data.total || data.length
          } else if (response.data.list && Array.isArray(response.data.list)) {
            data = response.data.list
            total = response.data.total || data.length
          } else if (response.data.items && Array.isArray(response.data.items)) {
            data = response.data.items
            total = response.data.total || data.length
          }
        } else if (response && response.owners && Array.isArray(response.owners)) {
          // 直接返回owners数组
          data = response.owners
          total = response.total || data.length
        } else if (response && response.items && Array.isArray(response.items)) {
          // 直接返回items数组
          data = response.items
          total = response.total || data.length
        } else if (Array.isArray(response)) {
          // 直接返回数组
          data = response
          total = data.length
        }
        
        // 转换数据格式，适配前端显示
        ownerList.value = data.map(item => {
          // 处理性别字段，将M/F转换为1/2
          let gender = item.gender
          if (typeof gender === 'string') {
            gender = gender === 'M' ? 1 : (gender === 'F' ? 2 : 1)
          }
          
          return {
            id: item.id,
            name: item.name,
            gender: gender,
            phone: item.phoneNumber || item.phone,
            idCard: item.idCard,
            communityId: item.communityId,
            communityName: item.communityName || 
              (item.communityInfo ? item.communityInfo.name : ''),
            houseId: item.houseId,
            houseInfo: item.houseInfo || 
              (item.house ? item.house.fullName : ''),
            createTime: item.createTime || item.createdAt || item.updateTime || item.updatedAt
          }
        })
        
        // 更新分页信息
        pagination.total = total
      } catch (error) {
        console.error('获取业主列表失败:', error)
        ElMessage.error('获取业主列表失败')
        ownerList.value = []
        pagination.total = 0
      } finally {
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
    const handleEdit = async (row) => {
      dialogType.value = 'edit'
      resetForm()
      
      // 复制基本信息
      Object.keys(formData).forEach(key => {
        if (row[key] !== undefined) {
          formData[key] = row[key]
        }
      })
      
      // 如果有communityId，获取房屋选项
      if (row.communityId) {
        await fetchHouseOptions(row.communityId)
      }
      
      // 显示对话框
      dialogVisible.value = true
    }
    
    // 删除业主
    const handleDelete = (row) => {
      ElMessageBox.confirm('确认删除该业主信息吗？删除后将无法恢复!', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          // 调用API删除业主
          await ownerApi.deleteOwner(row.id)
          ElMessage.success('删除业主成功')
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
            const formToSubmit = {
              ...formData,
              // 确保字段名称与API一致
              phoneNumber: formData.phone
            }
            
            if (dialogType.value === 'add') {
              // 添加业主
              await ownerApi.createOwner(formToSubmit)
              ElMessage.success('添加业主成功')
            } else {
              // 更新业主
              await ownerApi.updateOwner(formData.id, formToSubmit)
              ElMessage.success('更新业主成功')
            }
            
            dialogVisible.value = false
            fetchOwnerList()
          } catch (error) {
            console.error('提交业主数据失败:', error)
            ElMessage.error('提交业主数据失败')
          } finally {
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
    
    // 格式化业主信息
    const formatOwnerInfo = (owner) => {
      // 处理业主信息字段映射
      return {
        id: owner.id,
        name: owner.name,
        gender: typeof owner.gender === 'string' ? (owner.gender === 'M' ? 1 : 2) : owner.gender,
        phone: owner.phoneNumber || owner.phone,
        idCard: owner.idCard,
        email: owner.email || '',
        city: owner.city || '',
        address: owner.address || '',
        communityId: owner.communityId,
        communityName: owner.communityName || (owner.communityInfo ? owner.communityInfo.name : ''),
        houseId: owner.houseId,
        houseInfo: owner.houseInfo || (owner.house ? owner.house.fullName : ''),
        ownerType: owner.ownerType || '业主',
        createTime: owner.createTime || owner.createdAt || '',
        remark: owner.remark || ''
      }
    }
    
    // 获取社区列表
    const fetchCommunities = async () => {
      try {
        const response = await communityApi.getCommunityList({
          page: 1,
          size: 100
        })
        
        console.log('社区列表响应:', response)
        
        if (response && response.success && response.data) {
          if (response.data.list && response.data.list.length > 0) {
            communityOptions.value = response.data.list.map(item => ({
              value: item.id,
              label: item.name || item.communityName
            }))
          }
        } else if (response && response.items && response.items.length > 0) {
          communityOptions.value = response.items.map(item => ({
            value: item.id,
            label: item.communityName || item.name
          }))
        } else if (Array.isArray(response) && response.length > 0) {
          communityOptions.value = response.map(item => ({
            value: item.id,
            label: item.name || item.communityName
          }))
        } else {
          communityOptions.value = []
          ElMessage.warning('未获取到社区数据')
        }
      } catch (error) {
        console.error('获取社区列表失败:', error)
        ElMessage.error('获取社区列表失败')
        communityOptions.value = []
      }
    }
    
    // 初始化
    onMounted(() => {
      fetchCommunities()
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
      formatIdCard,
      formatOwnerInfo
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
  content: "\f007"; /* FontAwesome用户图标 */
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

/* 添加表格内特殊效果 - 业主头像样式 */
:deep(.owner-avatar) {
  display: inline-flex;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3498db, #2ecc71);
  color: white;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 8px;
  font-size: 14px;
  box-shadow: 0 2px 6px rgba(52, 152, 219, 0.3);
}

/* 添加自定义标签样式 */
:deep(.gender-tag) {
  display: inline-flex;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 12px;
  align-items: center;
}

:deep(.gender-tag.male) {
  background-color: rgba(52, 152, 219, 0.1);
  color: #3498db;
}

:deep(.gender-tag.female) {
  background-color: rgba(231, 76, 60, 0.1);
  color: #e74c3c;
}

:deep(.gender-tag.male::before), 
:deep(.gender-tag.female::before) {
  content: "";
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 5px;
}

:deep(.gender-tag.male::before) {
  background-color: #3498db;
}

:deep(.gender-tag.female::before) {
  background-color: #e74c3c;
}

/* 修改表单样式，增加优雅效果 */
:deep(.el-form-item__content) {
  transition: all 0.3s;
}

:deep(.el-form-item:hover .el-form-item__content) {
  transform: translateX(5px);
}

:deep(.el-radio__input.is-checked .el-radio__inner) {
  background: linear-gradient(90deg, #3498db, #2ecc71);
  border-color: transparent;
}

:deep(.el-radio__inner::after) {
  transform: translate(-50%, -50%) scale(0.8);
}
</style> 