<template>
  <div class="house-container">
    <!-- 左侧树形结构侧边栏 -->
    <div class="sidebar" :class="{ collapsed: isSidebarCollapsed }">
      <el-card class="tree-card">
        <div class="tree-header">
          <span>区域总览</span>
          <el-button type="primary" size="small" @click="refreshTree">刷新</el-button>
        </div>
        
        <!-- 社区选择器 -->
        <div class="community-selector mb-4">
          <el-select 
            v-model="searchForm.communityId" 
            placeholder="请选择社区"
            @change="handleCommunityChange"
            style="width: 100%;"
          >
            <el-option
              v-for="item in communityOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </div>
        
        <el-tree
          :data="houseTreeData"
          :props="defaultProps"
          @node-click="handleNodeClick"
          :highlight-current="true"
          node-key="id"
          ref="tree"
          show-checkbox
          @check="handleCheck"
          v-loading="treeLoading"
        >
          <template #default="{ node, data }">
            <span class="custom-tree-node">
              <span>{{ node.label }}</span>
              <span class="count" v-if="data.count">({{ data.count }})</span>
            </span>
          </template>
        </el-tree>
      </el-card>
      <div 
        class="toggle-sidebar" 
        :class="{ collapsed: isSidebarCollapsed }"
        @click="toggleSidebar"
      >
        <i :class="isSidebarCollapsed ? 'el-icon-arrow-right' : 'el-icon-arrow-left'"></i>
      </div>
    </div>

    <!-- 右侧内容区域 -->
    <div class="content-container" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
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
            <el-form-item label="关键词">
              <el-input 
                v-model="searchForm.keyword" 
                placeholder="请输入房屋信息(房屋名称/区号/栋号/单元号/房间号)" 
                clearable>
              </el-input>
            </el-form-item>
            <el-form-item label="楼栋编号">
              <el-input v-model="searchForm.buildingCode" placeholder="请输入楼栋编号" clearable></el-input>
            </el-form-item>
            <el-form-item label="房屋编号">
              <el-input v-model="searchForm.houseCode" placeholder="请输入房屋编号" clearable></el-input>
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
          <el-table-column prop="fullName" label="房屋地址"></el-table-column>
          <el-table-column prop="districtNumber" label="区号"></el-table-column>
          <el-table-column prop="buildingNumber" label="栋号"></el-table-column>
          <el-table-column prop="unitNumber" label="单元号"></el-table-column>
          <el-table-column prop="roomNumber" label="房间号"></el-table-column>
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
    </div>
    
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
        
        <!-- 房屋层级选择 -->
        <el-form-item label="房屋层级" prop="level" v-if="dialogType === 'add'">
          <el-select v-model="formData.level" placeholder="请选择房屋层级" style="width: 100%">
            <el-option label="区" :value="1" />
            <el-option label="栋" :value="2" />
            <el-option label="单元" :value="3" />
            <el-option label="房间" :value="4" />
          </el-select>
        </el-form-item>
        
        <!-- 父级房屋 -->
        <el-form-item label="父级房屋" v-if="dialogType === 'add'">
          <el-input v-model="parentHouseName" disabled placeholder="自动获取父级房屋"></el-input>
        </el-form-item>
        
        <el-form-item label="区编号" prop="districtNumber" v-if="formData.level >= 1">
          <el-input v-model="formData.districtNumber" placeholder="请输入区编号"></el-input>
        </el-form-item>
        
        <el-form-item label="楼栋编号" prop="buildingCode" v-if="formData.level >= 2">
          <el-input v-model="formData.buildingCode" placeholder="请输入楼栋编号"></el-input>
        </el-form-item>
        
        <el-form-item label="单元编号" prop="unitNumber" v-if="formData.level >= 3">
          <el-input v-model="formData.unitNumber" placeholder="请输入单元编号"></el-input>
        </el-form-item>
        
        <el-form-item label="房间编号" prop="roomNumber" v-if="formData.level >= 4">
          <el-input v-model="formData.roomNumber" placeholder="请输入房间编号"></el-input>
        </el-form-item>
        
        <el-form-item label="房屋面积" prop="houseArea" v-if="formData.level >= 4">
          <el-input-number v-model="formData.houseArea" :min="0" :precision="2" style="width: 100%"></el-input-number>
        </el-form-item>
        
        <el-form-item label="户型" prop="houseUnit" v-if="formData.level >= 4">
          <el-select v-model="formData.houseUnit" placeholder="请选择户型" style="width: 100%">
            <el-option label="一室一厅" value="一室一厅" />
            <el-option label="两室一厅" value="两室一厅" />
            <el-option label="三室一厅" value="三室一厅" />
            <el-option label="三室两厅" value="三室两厅" />
            <el-option label="四室两厅" value="四室两厅" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="业主姓名" prop="ownerName" v-if="formData.level >= 4">
          <el-input v-model="formData.ownerName" placeholder="请输入业主姓名"></el-input>
        </el-form-item>
        
        <el-form-item label="状态" prop="status" v-if="formData.level >= 4">
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
import houseApi from '../../api/house'
import communityApi from '../../api/community'

export default {
  name: 'HouseInfoView',
  setup() {
    console.log('=== HouseInfo 组件初始化 ===')

    // 搜索表单
    const searchForm = reactive({
      buildingCode: '',
      houseCode: '',
      communityId: '',
      parentId: null,
      parentIds: null,
      roomId: null,
      districtNumber: '',
      buildingNumber: '',
      unitNumber: '',
      roomNumber: '',
      keyword: ''
    })
    
    // 表格数据
    const houseList = ref([])
    const tableLoading = ref(false)
    const treeLoading = ref(false)
    
    // 房屋树形结构数据
    const houseTreeData = ref([])
    const defaultProps = {
      children: 'children',
      label: 'fullName'
    }
    
    // 侧边栏折叠状态
    const isSidebarCollapsed = ref(false)
    
    // 小区选项
    const communityOptions = ref([])
    
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
    const tree = ref(null)
    
    // 父级房屋名称
    const parentHouseName = ref('无')
    
    // 表单数据
    const formData = reactive({
      id: '',
      communityId: '',
      parentId: null,
      level: 1,
      districtNumber: '',
      buildingCode: '',
      unitNumber: '',
      roomNumber: '',
      houseArea: 0,
      houseUnit: '',
      ownerName: '',
      status: '未入住',
      remark: '',
      fullName: ''
    })
    
    // 表单验证规则
    const formRules = {
      communityId: [
        { required: true, message: '请选择所属小区', trigger: 'change' }
      ],
      level: [
        { required: true, message: '请选择房屋层级', trigger: 'change' }
      ],
      districtNumber: [
        { required: true, message: '请输入区编号', trigger: 'blur' }
      ],
      buildingCode: [
        { required: true, message: '请输入楼栋编号', trigger: 'blur' }
      ],
      unitNumber: [
        { required: true, message: '请输入单元编号', trigger: 'blur' }
      ],
      roomNumber: [
        { required: true, message: '请输入房间编号', trigger: 'blur' }
      ]
    }
    
    // 获取社区列表
    const fetchCommunities = async () => {
      try {
        console.log('开始获取社区列表')
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
        
        if (communityOptions.value.length > 0) {
          searchForm.communityId = communityOptions.value[0].value
          console.log('设置默认社区ID:', searchForm.communityId)
          handleCommunityChange()
        } else {
          ElMessage.warning('没有可用的社区，请先创建社区')
        }
      } catch (error) {
        console.error('获取社区列表失败:', error)
        ElMessage.error('获取社区列表失败')
        communityOptions.value = []
      }
    }
    
    // 获取房屋树形结构
    const fetchHouseTree = async () => {
      if (!searchForm.communityId) {
        houseTreeData.value = []
        return
      }
      
      treeLoading.value = true
      try {
        console.log('获取房屋树形结构，社区ID:', searchForm.communityId)
        const response = await houseApi.getHouseTree(searchForm.communityId)
        console.log('房屋树形结构响应:', response)
        
        // 判断返回数据是否为空
        if (!response) {
          console.error('API返回空数据')
          houseTreeData.value = []
          ElMessage.warning('获取房屋树结构数据为空')
          return
        }
        
        // 检查响应中是否有items字段（从截图看房屋列表接口有这个字段，树结构可能也有）
        if (response.items) {
          console.log('找到树结构items数据:', response.items)
          houseTreeData.value = response.items
        }
        // 处理标准响应格式
        else if (response.success && response.data) {
          houseTreeData.value = response.data
        }
        // 数组格式
        else if (Array.isArray(response)) {
          houseTreeData.value = response
        }
        // 其他可能的格式
        else if (typeof response === 'object') {
          // 可能直接返回了对象
          console.log('尝试直接使用返回对象作为树结构')
          if (response.children || response.level) {
            // 看起来像是单个树节点对象
            houseTreeData.value = [response]
          } else {
            console.warn('无法识别的树结构响应格式:', response)
            houseTreeData.value = []
            ElMessage.warning('获取房屋树结构数据格式不识别')
          }
        } else {
          houseTreeData.value = []
          ElMessage.warning('获取房屋树结构数据为空')
        }
        
        // 如果成功获取到树结构数据
        if (houseTreeData.value && houseTreeData.value.length > 0) {
          console.log('获取到树结构数据，开始映射字段名称')
          mapFieldNames(houseTreeData.value)
          // 初始化时只显示社区下的区域，不做额外查询
          // 而不是子节点
          searchForm.parentId = null
        } else {
          console.warn('未获取到有效的树结构数据')
        }
      } catch (error) {
        console.error('获取房屋树结构失败:', error)
        ElMessage.error('获取房屋树结构失败')
        houseTreeData.value = []
      } finally {
        treeLoading.value = false
      }
    }
    
    // 字段名称映射函数
    const mapFieldNames = (nodes) => {
      if (!nodes || !Array.isArray(nodes)) return
      
      nodes.forEach(node => {
        // 确保每个节点都有level字段
        if (node.level === undefined) {
          // 根据节点结构推断其层级
          if (node.roomNumber || node.houseCode) {
            node.level = 4; // 房间级别
          } else if (node.unitNumber) {
            node.level = 3; // 单元级别
          } else if (node.buildingNumber || node.buildingCode) {
            node.level = 2; // 楼栋级别
          } else if (node.districtNumber) {
            node.level = 1; // 区级别
          } else {
            node.level = 0; // 默认为社区级别
          }
        }
        
        // 映射字段名称 (buildingCode -> buildingNumber)
        if (node.buildingCode !== undefined && node.buildingNumber === undefined) {
          node.buildingNumber = node.buildingCode
        }
        
        // 处理房屋编号
        if (node.houseCode !== undefined && node.roomNumber === undefined) {
          node.roomNumber = node.houseCode
        }
        
        // 递归处理子节点
        if (node.children && node.children.length > 0) {
          mapFieldNames(node.children)
        }
      })
    }
    
    // 刷新树
    const refreshTree = async () => {
      await fetchHouseTree()
      ElMessage.success('刷新成功')
    }
    
    // 树节点点击事件
    const handleNodeClick = (data) => {
      console.log('点击树节点:', data)
      
      // 重置搜索条件
      searchForm.keyword = ''
      searchForm.buildingCode = ''
      searchForm.houseCode = ''
      searchForm.districtNumber = ''
      searchForm.buildingNumber = ''
      searchForm.unitNumber = ''
      searchForm.roomNumber = ''
      
      // 判断是否为叶子节点（没有children或children为空数组）
      const isLeafNode = !data.children || data.children.length === 0
      
      // 根据点击的节点层级设置当前层级
      currentLevel.value = data.level
      
      // 不同级别节点不同处理
      if (data.level === 0 || !data.level) {
        // 如果是社区节点或根节点，显示所有区域
        if (data.id) {
          searchForm.communityId = data.id
        }
        searchForm.parentId = null
        searchForm.roomId = null
      } else if (data.level === 4 || (data.roomNumber && data.roomNumber.length > 0)) {
        // 房间级节点，查询该房间信息
        console.log('点击房间节点:', data.id, data.fullName)
        searchForm.roomId = data.id
        searchForm.parentId = null
        
        // 设置房间号，用于API过滤
        if (data.roomNumber) {
          searchForm.roomNumber = data.roomNumber
          searchForm.houseCode = data.roomNumber
        } else if (data.houseCode) {
          searchForm.roomNumber = data.houseCode
          searchForm.houseCode = data.houseCode
        }
        
        // 设置单元、楼栋和区号信息
        if (data.unitNumber) searchForm.unitNumber = data.unitNumber
        if (data.buildingNumber || data.buildingCode) {
          searchForm.buildingNumber = data.buildingNumber || data.buildingCode
          searchForm.buildingCode = data.buildingNumber || data.buildingCode
        }
        if (data.districtNumber) searchForm.districtNumber = data.districtNumber
      } else {
        // 其他节点，查询其子节点
        searchForm.parentId = data.id
        searchForm.roomId = null
        
        // 根据当前节点级别设置查询参数
        if (data.level === 1) {
          // 区级节点，设置区号，查询该区下的所有楼栋
          console.log('查询区级子节点:', data.districtNumber)
          searchForm.districtNumber = data.districtNumber
        } else if (data.level === 2) {
          // 楼栋级节点
          if (data.buildingNumber || data.buildingCode) {
            searchForm.buildingCode = data.buildingNumber || data.buildingCode
            searchForm.buildingNumber = data.buildingNumber || data.buildingCode
          }
          if (data.districtNumber) searchForm.districtNumber = data.districtNumber
        } else if (data.level === 3) {
          // 单元级节点
          if (data.unitNumber) searchForm.unitNumber = data.unitNumber
          if (data.buildingNumber || data.buildingCode) {
            searchForm.buildingCode = data.buildingNumber || data.buildingCode
            searchForm.buildingNumber = data.buildingNumber || data.buildingCode
          }
          if (data.districtNumber) searchForm.districtNumber = data.districtNumber
        }
      }
      searchForm.parentIds = null
      
      console.log('节点点击后搜索条件:', {...searchForm}, '层级:', currentLevel.value, '是叶子节点:', isLeafNode)
      
      // 重置选中的节点
      if (tree.value) {
        tree.value.setCheckedKeys([])
      }
      
      fetchHouseList()
    }
    
    // 树节点勾选事件
    const handleCheck = (data, { checkedNodes }) => {
      const leafIds = checkedNodes
        .filter(node => !node.children || node.children.length === 0)
        .map(node => node.id)
      
      searchForm.parentIds = leafIds.length > 0 ? leafIds : null
      searchForm.parentId = null
      searchForm.roomId = null
      
      fetchHouseList()
    }
    
    // 获取房屋列表
    const fetchHouseList = async () => {
      tableLoading.value = true
      try {
        const params = {
          page: pagination.currentPage,
          size: pagination.pageSize,
          communityId: searchForm.communityId,
          keyword: searchForm.keyword
        }
        
        // 添加条件参数
        if (searchForm.buildingCode) params.buildingCode = searchForm.buildingCode
        if (searchForm.buildingNumber) params.buildingNumber = searchForm.buildingNumber
        if (searchForm.houseCode) params.houseCode = searchForm.houseCode
        if (searchForm.roomNumber) params.roomNumber = searchForm.roomNumber
        if (searchForm.districtNumber) params.districtNumber = searchForm.districtNumber
        if (searchForm.unitNumber) params.unitNumber = searchForm.unitNumber
        
        // 处理查询关系
        if (searchForm.roomId) {
          // 如果是查询特定房间，使用roomId查询
          params.id = searchForm.roomId
          console.log('查询特定房间信息:', searchForm.roomId)
        } else if (searchForm.parentId) {
          // 如果指定了父级ID，查询其子节点
          params.parentId = searchForm.parentId
          console.log('查询父级下的房屋:', searchForm.parentId)
        } else if (searchForm.parentIds && searchForm.parentIds.length > 0) {
          // 如果指定了多个父级ID，使用in查询
          params.parentIds = searchForm.parentIds.join(',')
        }

        console.log('请求参数:', params)
        
        // 使用API获取数据
        const response = await houseApi.getHouseList(params)
        console.log('API响应:', response)
        
        // 判断返回数据是否为空
        if (!response) {
          console.error('API返回空数据')
          houseList.value = []
          pagination.total = 0
          return
        }
        
        let data = null
        let total = 0
        
        // 特殊处理房间查询
        if (searchForm.roomId && (typeof response === 'object' && !Array.isArray(response))) {
          // 单个房间对象，直接使用
          console.log('房间查询结果:', response)
          
          // 检查是否有items字段（通常用于列表）
          if (response.items && response.items.length > 0) {
            data = response.items
            total = response.total || data.length
          } else if (response.data && !Array.isArray(response.data)) {
            // 标准响应格式，data字段为单个对象
            data = [response.data]
            total = 1
          } else if (response.id) {
            // 直接是房间对象
            data = [response]
            total = 1
          } else {
            // 无法识别的响应格式
            data = []
            total = 0
          }
        } else {
          // 从不同的结构中提取数据（列表查询）
          if (response.items) {
            console.log('从items字段提取数据')
            data = response.items
            total = response.total || data.length
          } else if (response.data && response.data.items) {
            console.log('从data.items字段提取数据')
            data = response.data.items
            total = response.data.total || data.length
          } else if (response.data && Array.isArray(response.data)) {
            console.log('从data数组提取数据')
            data = response.data
            total = data.length
          } else if (response.data && response.data.list) {
            console.log('从data.list字段提取数据')
            data = response.data.list
            total = response.data.total || data.length
          } else if (Array.isArray(response)) {
            console.log('从response数组提取数据')
            data = response
            total = response.length
          } else if (response.id && searchForm.roomId) {
            // 直接返回了单个房间对象
            console.log('提取单个房间对象')
            data = [response]
            total = 1
          } else {
            console.warn('无法识别的响应格式:', response)
            data = []
            total = 0
          }
        }
        
        // 更新列表数据和分页信息
        houseList.value = data || []
        pagination.total = total
        
        // 映射字段名，确保数据能正确显示
        if (houseList.value.length > 0) {
          mapDataFields(houseList.value)
        }
        
        console.log('处理后的表格数据:', houseList.value.length, '条记录')
        
      } catch (error) {
        console.error('获取房屋列表失败:', error)
        ElMessage.error('获取房屋列表失败')
        houseList.value = []
        pagination.total = 0
      } finally {
        tableLoading.value = false
      }
    }
    
    // 切换社区
    const handleCommunityChange = () => {
      // 重置所有搜索条件
      searchForm.parentId = null
      searchForm.parentIds = null
      searchForm.roomId = null
      searchForm.keyword = ''
      searchForm.buildingCode = ''
      searchForm.houseCode = ''
      searchForm.districtNumber = ''
      
      // 重置当前层级
      currentLevel.value = null
      
      // 重置选中的节点
      if (tree.value) {
        tree.value.setCheckedKeys([])
        tree.value.setCurrentKey(null)
      }
      
      // 重置分页
      pagination.currentPage = 1
      
      console.log('社区切换，重置参数，选中社区ID:', searchForm.communityId)
      
      // 获取树结构和初始列表
      fetchHouseTree()
      fetchHouseList()
    }
    
    // 搜索
    const handleSearch = () => {
      pagination.currentPage = 1
      fetchHouseList()
    }
    
    // 重置搜索条件
    const handleReset = () => {
      searchForm.buildingCode = ''
      searchForm.houseCode = ''
      searchForm.parentId = null
      searchForm.parentIds = null
      searchForm.roomId = null
      searchForm.districtNumber = ''
      searchForm.buildingNumber = ''
      searchForm.unitNumber = ''
      searchForm.roomNumber = ''
      searchForm.keyword = ''
      
      // 重置当前层级
      currentLevel.value = null
      
      // 重置选中的节点
      if (tree.value) {
        tree.value.setCheckedKeys([])
      }
      
      pagination.currentPage = 1
      fetchHouseList()
    }
    
    // 添加房屋
    const handleAdd = () => {
      dialogType.value = 'add'
      
      // 获取当前选中的节点
      const currentNode = tree.value ? tree.value.getCurrentNode() : null
      
      // 重置表单
      formData.id = ''
      formData.communityId = searchForm.communityId
      formData.parentId = currentNode ? currentNode.id : null
      formData.level = currentNode ? currentNode.level + 1 : 1
      formData.districtNumber = ''
      formData.buildingCode = ''
      formData.buildingNumber = ''
      formData.unitNumber = ''
      formData.roomNumber = ''
      formData.houseArea = 0
      formData.houseUnit = ''
      formData.ownerName = ''
      formData.status = '未入住'
      formData.remark = ''
      formData.fullName = ''
      
      // 设置父级房屋名称
      parentHouseName.value = currentNode ? currentNode.fullName : '无'
      
      dialogVisible.value = true
      
      // 重置表单校验
      if (formRef.value) {
        formRef.value.resetFields()
      }
    }
    
    // 编辑房屋
    const handleEdit = (row) => {
      dialogType.value = 'edit'
      
      // 填充表单数据
      formData.id = row.id
      formData.communityId = row.communityId
      formData.buildingCode = row.buildingCode
      formData.houseCode = row.houseCode
      formData.houseArea = row.houseArea
      formData.houseUnit = row.houseUnit
      formData.ownerName = row.ownerName
      formData.status = row.status
      formData.remark = row.remark || ''
      
      dialogVisible.value = true
      
      // 重置表单校验
      if (formRef.value) {
        formRef.value.resetFields()
      }
    }
    
    // 提交表单
    const submitForm = () => {
      if (formRef.value) {
        formRef.value.validate(async (valid) => {
          if (valid) {
            submitLoading.value = true
            try {
              // 构建房屋完整名称
              if (dialogType.value === 'add') {
                generateFullName()
              }
              
              if (dialogType.value === 'add') {
                // 添加
                await houseApi.createHouse(formData)
                ElMessage.success('添加成功')
              } else {
                // 编辑
                await houseApi.updateHouse(formData.id, formData)
                ElMessage.success('编辑成功')
              }
              
              dialogVisible.value = false
              fetchHouseList()
              fetchHouseTree()
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
    
    // 生成完整名称
    const generateFullName = () => {
      const community = communityOptions.value.find(c => c.value === formData.communityId)
      const currentNode = tree.value ? tree.value.getCurrentNode() : null
      
      if (!community) return
      
      let fullName = ''
      
      // 如果有父节点，使用父节点的信息构建名称
      if (currentNode) {
        // 获取父节点的完整路径信息
        const parentFullName = currentNode.fullName
        
        if (formData.level === 4) {
          // 对于房间，使用父节点的单元信息
          const unitPart = parentFullName.split('单元')[0]
          fullName = `${unitPart}单元${formData.roomNumber}室`
        } else {
          fullName = community.label
          if (formData.level >= 1 && formData.districtNumber) {
            fullName += `${formData.districtNumber}区`
          }
          if (formData.level >= 2 && formData.buildingCode) {
            fullName += `${formData.buildingCode}栋`
          }
          if (formData.level >= 3 && formData.unitNumber) {
            fullName += `${formData.unitNumber}单元`
          }
        }
      } else {
        // 如果没有父节点，从头构建名称
        fullName = community.label
        if (formData.level >= 1 && formData.districtNumber) {
          fullName += `${formData.districtNumber}区`
        }
      }
      
      formData.fullName = fullName
    }
    
    // 删除房屋
    const handleDelete = (row) => {
      ElMessageBox.confirm('确认删除该房屋信息吗？删除后不可恢复!', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await houseApi.deleteHouse(row.id)
          ElMessage.success('删除成功')
          fetchHouseList()
          fetchHouseTree()
        } catch (error) {
          console.error('删除房屋失败:', error)
          ElMessage.error('删除房屋失败')
        }
      }).catch(() => {
        // 取消删除，不做操作
      })
    }
    
    // 切换侧边栏折叠状态
    const toggleSidebar = () => {
      isSidebarCollapsed.value = !isSidebarCollapsed.value
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
    
    // 添加判断字段是否显示的方法
    const showFieldByLevel = (level) => {
      // 如果未选择节点，显示所有字段
      if (!currentLevel.value) return true
      
      // 当前点击的节点层级与字段层级对应时显示，或者更低层级显示更高层级的字段
      return currentLevel.value >= level
    }
    
    // 在setup中添加
    const currentLevel = ref(null)
    
    // 字段名称映射函数，确保数据对象的字段名称一致
    const mapDataFields = (dataList) => {
      if (!dataList || !Array.isArray(dataList)) return;
      
      console.log('映射前的数据:', JSON.stringify(dataList.slice(0, 2)));
      
      // 遍历数据列表，映射字段名
      dataList.forEach(item => {
        // 确保每个节点都有level字段
        if (item.level === undefined) {
          // 根据节点结构推断其层级
          if (item.roomNumber || item.houseCode) {
            item.level = 4; // 房间级别
          } else if (item.unitNumber) {
            item.level = 3; // 单元级别
          } else if (item.buildingNumber || item.buildingCode) {
            item.level = 2; // 楼栋级别
          } else if (item.districtNumber) {
            item.level = 1; // 区级别
          } else {
            item.level = 0; // 默认为社区级别
          }
        }
        
        // 建筑编号字段映射
        if (item.buildingNumber === undefined) {
          if (item.buildingCode !== undefined) {
            item.buildingNumber = item.buildingCode;
          } else if (item.building_number !== undefined) {
            item.buildingNumber = item.building_number;
          } else if (item.building !== undefined) {
            item.buildingNumber = item.building;
          }
        }
        
        // 确保buildingCode也有值
        if (item.buildingCode === undefined && item.buildingNumber !== undefined) {
          item.buildingCode = item.buildingNumber;
        }
        
        // 房间编号字段映射
        if (item.roomNumber === undefined) {
          if (item.houseCode !== undefined) {
            item.roomNumber = item.houseCode;
          } else if (item.room_number !== undefined) {
            item.roomNumber = item.room_number;
          } else if (item.room !== undefined) {
            item.roomNumber = item.room;
          }
        }
        
        // 确保houseCode也有值
        if (item.houseCode === undefined && item.roomNumber !== undefined) {
          item.houseCode = item.roomNumber;
        }
        
        // 区号字段映射
        if (item.districtNumber === undefined) {
          if (item.district_number !== undefined) {
            item.districtNumber = item.district_number;
          } else if (item.district !== undefined) {
            item.districtNumber = item.district;
          }
        }
        
        // 单元号字段映射
        if (item.unitNumber === undefined) {
          if (item.unit_number !== undefined) {
            item.unitNumber = item.unit_number;
          } else if (item.unit !== undefined) {
            item.unitNumber = item.unit;
          }
        }
        
        // 房屋地址/全名字段映射
        if (item.fullName === undefined) {
          // 尝试不同的字段名
          if (item.houseName) {
            item.fullName = item.houseName;
          } else if (item.house_name) {
            item.fullName = item.house_name;
          } else if (item.name) {
            item.fullName = item.name;
          } else if (item.address) {
            item.fullName = item.address;
          } else {
            // 如果没有找到合适的字段，尝试构建一个
            let name = '';
            if (item.communityName) name = item.communityName + ' ';
            if (item.districtNumber) name += `${item.districtNumber}区`;
            if (item.buildingNumber) name += `${item.buildingNumber}栋`;
            if (item.unitNumber) name += `${item.unitNumber}单元`;
            if (item.roomNumber) name += `${item.roomNumber}室`;
            
            if (name) {
              item.fullName = name;
            }
          }
        }
        
        // 创建时间字段映射
        if (item.createTime === undefined) {
          if (item.create_time !== undefined) {
            item.createTime = item.create_time;
          } else if (item.createtime !== undefined) {
            item.createTime = item.createtime;
          } else if (item.createdAt !== undefined) {
            item.createTime = item.createdAt;
          } else if (item.created_at !== undefined) {
            item.createTime = item.created_at;
          }
        }
      });
      
      console.log('映射后的数据:', JSON.stringify(dataList.slice(0, 2)));
      
      return dataList;
    }
    
    onMounted(() => {
      console.log('=== HouseInfo 组件挂载 ===')
      fetchCommunities()
    })
    
    return {
      searchForm,
      houseList,
      tableLoading,
      treeLoading,
      communityOptions,
      pagination,
      dialogVisible,
      dialogType,
      formRef,
      formData,
      formRules,
      submitLoading,
      houseTreeData,
      defaultProps,
      isSidebarCollapsed,
      tree,
      parentHouseName,
      handleSearch,
      handleReset,
      handleAdd,
      handleEdit,
      handleDelete,
      submitForm,
      handleSizeChange,
      handleCurrentChange,
      fetchHouseTree,
      refreshTree,
      handleNodeClick,
      handleCheck,
      toggleSidebar,
      handleCommunityChange,
      currentLevel,
      showFieldByLevel,
      mapDataFields
    }
  }
}
</script>

<style scoped>
.house-container {
  display: flex;
  padding: 20px;
  height: calc(100vh - 100px);
  background-color: var(--el-bg-color);
}

.sidebar {
  width: 300px;
  transition: width 0.3s;
  margin-right: 20px;
  height: 100%;
  position: relative;
}

.sidebar.collapsed {
  width: 0;
  margin-right: 0;
  overflow: hidden;
}

.content-container {
  flex: 1;
  overflow: auto;
  transition: margin-left 0.3s;
}

.content-container.sidebar-collapsed {
  margin-left: 0;
}

.tree-card {
  height: 100%;
  overflow: auto;
  border-radius: 12px;
}

.tree-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 10px;
  margin-bottom: 15px;
}

.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-right: 8px;
}

.count {
  color: var(--el-text-color-secondary);
  font-size: 12px;
  margin-left: 5px;
}

.mb-4 {
  margin-bottom: 16px;
}

.toggle-sidebar {
  position: absolute;
  left: 300px;
  top: 50%;
  transform: translateY(-50%);
  background: var(--el-color-primary);
  color: white;
  width: 20px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 0 4px 4px 0;
  transition: left 0.3s;
  z-index: 1;
}

.toggle-sidebar.collapsed {
  left: 0;
}

.house-card {
  margin-bottom: 20px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--box-shadow);
  transition: all 0.3s;
  background: var(--card-bg-gradient);
  position: relative;
}

.house-card:hover {
  box-shadow: var(--box-shadow-hover);
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

@media screen and (max-width: 768px) {
  .house-container {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    margin-bottom: 20px;
  }
  
  .tree-card {
    height: 300px;
  }
  
  .toggle-sidebar {
    display: none;
  }
}
</style> 