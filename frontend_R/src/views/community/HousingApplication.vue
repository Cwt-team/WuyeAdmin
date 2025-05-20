<template>
  <div class="application-container">
    <el-card class="application-card">
      <template #header>
        <div class="card-header">
          <span>业主房屋绑定申请</span>
        </div>
      </template>
      <!-- 搜索区域 -->
      <div class="search-box">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="申请人">
            <el-input v-model="searchForm.name" placeholder="请输入申请人姓名" clearable></el-input>
          </el-form-item>
          <el-form-item label="手机号">
            <el-input v-model="searchForm.phoneNumber" placeholder="请输入手机号" clearable></el-input>
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态" clearable style="width: 120px">
              <el-option label="全部" value=""></el-option>
              <el-option label="待审核" value="待审核"></el-option>
              <el-option label="已审核" value="已审核"></el-option>
              <el-option label="已拒绝" value="已拒绝"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="所属小区">
            <el-select v-model="searchForm.communityId" placeholder="请选择小区" clearable style="width: 200px">
              <el-option v-for="item in communityOptions" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="fetchList">查询</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      <!-- 表格区域 -->
      <el-table :data="applicationList" border style="width: 100%" v-loading="tableLoading">
        <el-table-column type="index" width="50" label="序号"></el-table-column>
        <el-table-column prop="name" label="申请人"></el-table-column>
        <el-table-column prop="phoneNumber" label="手机号"></el-table-column>
        <el-table-column prop="idCard" label="身份证号"></el-table-column>
        <el-table-column prop="communityName" label="所属小区"></el-table-column>
        <el-table-column label="房屋">
          <template #default="scope">
            {{ scope.row.buildingName || '-' }}-{{ scope.row.unitName || '-' }}-{{ scope.row.houseNumber || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="applicationTime" label="申请时间"></el-table-column>
        <el-table-column label="操作" width="220">
          <template #default="scope">
            <el-button size="small" @click="viewDetail(scope.row)">详情</el-button>
            <el-button size="small" type="success" v-if="scope.row.status === '待审核'" @click="approve(scope.row)">通过</el-button>
            <el-button size="small" type="danger" v-if="scope.row.status === '待审核'" @click="openRejectDialog(scope.row)">拒绝</el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页 -->
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
    <!-- 详情弹窗 -->
    <el-dialog title="申请详情" v-model="detailDialogVisible" width="600px">
      <el-descriptions :column="2" border v-if="currentDetail">
        <el-descriptions-item label="申请人">{{ currentDetail.name }}</el-descriptions-item>
        <el-descriptions-item label="手机号">{{ currentDetail.phoneNumber }}</el-descriptions-item>
        <el-descriptions-item label="身份证号">{{ currentDetail.idCard }}</el-descriptions-item>
        <el-descriptions-item label="申请时间">{{ currentDetail.applicationTime }}</el-descriptions-item>
        <el-descriptions-item label="所属小区">{{ currentDetail.communityName }}</el-descriptions-item>
        <el-descriptions-item label="房屋">{{ currentDetail.buildingName }}-{{ currentDetail.unitName }}-{{ currentDetail.houseNumber }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(currentDetail.status)">{{ currentDetail.status }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="业主类型">{{ currentDetail.ownerType }}</el-descriptions-item>
        <el-descriptions-item label="审核反馈">{{ currentDetail.callbackMessage || '无' }}</el-descriptions-item>
        <el-descriptions-item label="证明材料" v-if="currentDetail.informationPhoto">
          <el-image :src="currentDetail.informationPhoto" style="max-width: 100%; max-height: 200px" fit="contain" />
        </el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
    <!-- 拒绝弹窗 -->
    <el-dialog title="拒绝申请" v-model="rejectDialogVisible" width="400px">
      <el-form :model="rejectForm">
        <el-form-item label="拒绝原因" prop="callbackMessage">
          <el-input type="textarea" v-model="rejectForm.callbackMessage" rows="4" placeholder="请填写拒绝原因"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="rejectDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmReject" :loading="submitting">确认拒绝</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import housingApplicationApi from '../../api/housingApplication'
import communityApi from '../../api/community'

const searchForm = reactive({
  name: '',
  phoneNumber: '',
  status: '',
  communityId: ''
})
const communityOptions = ref([])
const applicationList = ref([])
const tableLoading = ref(false)
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})
const detailDialogVisible = ref(false)
const currentDetail = ref(null)
const rejectDialogVisible = ref(false)
const rejectForm = reactive({
  callbackMessage: ''
})
const submitting = ref(false)
let rejectRow = null

// 状态映射
const statusMap = {
  'Pending': '待审核',
  'Approved': '已审核',
  'Returned': '已拒绝',
  'Rejected': '已拒绝',
  '待审核': '待审核',
  '已审核': '已审核',
  '已拒绝': '已拒绝'
}

const fetchCommunityOptions = async () => {
  const res = await communityApi.getCommunityList({ page: 1, size: 100 })
  let list = []
  if (res && res.success && res.data && res.data.list) {
    list = res.data.list
  } else if (res && res.data && res.data.items) {
    list = res.data.items
  } else if (res && res.items) {
    list = res.items
  } else if (Array.isArray(res)) {
    list = res
  } else if (Array.isArray(res.data)) {
    list = res.data
  }
  communityOptions.value = list.map(item => ({
    value: item.id,
    label: item.community_name || item.communityName || item.name || '未命名小区'
  }))
}

const fetchList = async () => {
  tableLoading.value = true
  try {
    const params = {
      page: pagination.currentPage,
      size: pagination.pageSize,
      // 只将状态和小区传给后端，申请人和手机号本地过滤
      status: searchForm.status ? Object.keys(statusMap).find(key => statusMap[key] === searchForm.status) : '',
      communityId: searchForm.communityId
    }
    const res = await housingApplicationApi.getApplicationList(params)
    let data = []
    // 兼容多种返回格式
    if (res && res.applications) {
      data = res.applications
    } else if (res && res.data && res.data.applications) {
      data = res.data.applications
    } else if (res && res.data && Array.isArray(res.data)) {
      data = res.data
    }
    // 状态字段映射为中文
    let filtered = data.map(item => ({
      ...item,
      status: statusMap[item.status] || item.status
    }))
    // 本地模糊过滤
    if (searchForm.name) {
      filtered = filtered.filter(item => item.name && item.name.includes(searchForm.name))
    }
    if (searchForm.phoneNumber) {
      filtered = filtered.filter(item => item.phoneNumber && item.phoneNumber.includes(searchForm.phoneNumber))
    }
    if (searchForm.communityId) {
      filtered = filtered.filter(item =>
        String(item.communityId || item.community_id) === String(searchForm.communityId)
      )
    }
    applicationList.value = filtered
    pagination.total = filtered.length
  } catch (e) {
    ElMessage.error('获取申请列表失败')
  } finally {
    tableLoading.value = false
  }
}

const resetSearch = () => {
  searchForm.name = ''
  searchForm.phoneNumber = ''
  searchForm.status = ''
  searchForm.communityId = ''
  fetchList()
}

const handleSizeChange = (size) => {
  pagination.pageSize = size
  fetchList()
}
const handleCurrentChange = (page) => {
  pagination.currentPage = page
  fetchList()
}

const getStatusType = (status) => {
  switch (status) {
    case '待审核': return 'warning'
    case '已审核': return 'success'
    case '已拒绝': return 'danger'
    default: return 'info'
  }
}

const viewDetail = async (row) => {
  const res = await housingApplicationApi.getApplicationDetail(row.id)
  currentDetail.value = res
  detailDialogVisible.value = true
}

const approve = (row) => {
  ElMessageBox.confirm('确认通过该申请？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    submitting.value = true
    try {
      await housingApplicationApi.approveApplication(row.id)
      ElMessage.success('审批通过')
      fetchList()
    } catch (e) {
      ElMessage.error('操作失败')
    } finally {
      submitting.value = false
    }
  })
}

const openRejectDialog = (row) => {
  rejectRow = row
  rejectForm.callbackMessage = ''
  rejectDialogVisible.value = true
}
const confirmReject = async () => {
  if (!rejectForm.callbackMessage) {
    ElMessage.warning('请填写拒绝原因')
    return
  }
  submitting.value = true
  try {
    await housingApplicationApi.rejectApplication(rejectRow.id, { callbackMessage: rejectForm.callbackMessage })
    ElMessage.success('已拒绝该申请')
    rejectDialogVisible.value = false
    fetchList()
  } catch (e) {
    ElMessage.error('操作失败')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchCommunityOptions()
  fetchList()
})
</script>

<style scoped>
.application-container {
  padding: 20px;
}
.application-card {
  margin-bottom: 20px;
}
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 