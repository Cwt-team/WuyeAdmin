<template>
  <div class="maintenance-report" ref="maintenanceReport">
    <!-- 搜索表单 -->
    <el-form :inline="true" class="search-form">
      <el-form-item label="社区">
        <el-select 
          v-model="filters.community" 
          placeholder="请选择社区" 
          clearable 
          @change="handleCommunityChange"
          class="large-select"
        >
          <el-option
            v-for="item in communities"
            :key="item.id"
            :label="item.community_name"
            :value="item.id"
          />
        </el-select>
      </el-form-item>
      
      <!-- 新增楼栋查询 -->
      <el-form-item label="楼栋">
        <el-select 
          v-model="filters.building" 
          placeholder="请选择楼栋" 
          clearable
          :disabled="!filters.community"
          @change="handleBuildingChange"
          class="large-select"
        >
          <el-option
            v-for="item in buildingOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>

      <!-- 新增房间号查询 -->
      <el-form-item label="房间号">
        <el-select 
          v-model="filters.roomNumber" 
          placeholder="请选择房间号" 
          clearable
          :disabled="!filters.building"
          class="large-select"
        >
          <el-option
            v-for="item in roomOptions"
            :key="item.room_number"
            :label="item.house_full_name"
            :value="item.room_number"
          />
        </el-select>
      </el-form-item>
      
      <el-form-item label="状态">
        <el-select 
          v-model="filters.status" 
          placeholder="请选择状态" 
          clearable
          class="large-select"
        >
          <el-option
            v-for="item in statusOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>
      
      <el-form-item label="报修时间">
        <el-date-picker
          v-model="filters.dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="handleSearch">查询</el-button>
        <el-button @click="handleReset">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 数据表格 -->
    <el-table
      v-loading="loading"
      :data="requests"
      border
      :max-height="tableHeight"
      class="maintenance-table"
    >
      <el-table-column prop="request_number" label="报修单号" width="150" />
      <el-table-column prop="reporter_name" label="报修人" width="100" />
      <el-table-column prop="reporter_phone" label="联系电话" width="120" />
      <el-table-column prop="title" label="报修标题" width="150" />
      <el-table-column prop="typeText" label="报修类型" width="100" />
      <el-table-column prop="priorityText" label="优先级" width="80" />
      <el-table-column prop="description" label="问题描述" show-overflow-tooltip />
      <el-table-column prop="statusText" label="状态" width="100" />
      <el-table-column prop="report_time" label="报修时间" width="160" />
      <el-table-column prop="house_full_name" label="房屋位置" width="200" />
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button
            v-if="row.status === 'pending'"
            size="small"
            type="primary"
            @click="handleProcess(row)"
          >
            受理
          </el-button>
          <el-button
            v-if="row.status === 'processing'"
            size="small"
            type="success"
            @click="handleComplete(row)"
          >
            完成
          </el-button>
          <el-button
            v-if="row.status === 'pending'"
            size="small"
            type="danger"
            @click="handleCancel(row)"
          >
            取消
          </el-button>
          <el-button
            size="small"
            @click="handleDetail(row)"
          >
            详情
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination-container">
      <el-pagination
        :current-page="pagination.currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pagination.pageSize"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />
    </div>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="报修详情"
      width="50%"
    >
      <div v-if="currentRequest" class="detail-container">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="报修单号">{{ currentRequest.request_number }}</el-descriptions-item>
          <el-descriptions-item label="报修人">{{ currentRequest.reporter_name }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ currentRequest.reporter_phone }}</el-descriptions-item>
          <el-descriptions-item label="房屋位置">{{ currentRequest.house_full_name }}</el-descriptions-item>
          <el-descriptions-item label="报修标题">{{ currentRequest.title }}</el-descriptions-item>
          <el-descriptions-item label="报修类型">{{ currentRequest.typeText }}</el-descriptions-item>
          <el-descriptions-item label="优先级">{{ currentRequest.priorityText }}</el-descriptions-item>
          <el-descriptions-item label="状态">{{ currentRequest.statusText }}</el-descriptions-item>
          <el-descriptions-item label="问题描述" :span="2">{{ currentRequest.description }}</el-descriptions-item>
          <el-descriptions-item label="报修时间">{{ currentRequest.report_time }}</el-descriptions-item>
          <el-descriptions-item label="期望上门时间">{{ currentRequest.expected_time }}</el-descriptions-item>
          <el-descriptions-item label="处理人" v-if="currentRequest.handler_name">{{ currentRequest.handler_name }}</el-descriptions-item>
          <el-descriptions-item label="处理人电话" v-if="currentRequest.handler_phone">{{ currentRequest.handler_phone }}</el-descriptions-item>
          <el-descriptions-item label="处理备注" v-if="currentRequest.notes" :span="2">{{ currentRequest.notes }}</el-descriptions-item>
        </el-descriptions>
        
        <div v-if="currentRequest.images" class="images-container">
          <h4>相关图片</h4>
          <el-image
            v-for="(img, index) in JSON.parse(currentRequest.images)"
            :key="index"
            :src="img"
            :preview-src-list="JSON.parse(currentRequest.images)"
            fit="cover"
            class="preview-image"
          />
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MaintenanceReport',
  data() {
    return {
      requests: [],
      loading: false,
      currentRequest: null,
      detailDialogVisible: false,
      filters: {
        community: '',
        building: '',    // 新增楼栋筛选
        roomNumber: '',  // 新增房间号筛选
        status: '',
        dateRange: [],
      },
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      statusOptions: [
        { value: 'pending', label: '待处理' },
        { value: 'processing', label: '处理中' },
        { value: 'completed', label: '已完成' },
        { value: 'cancelled', label: '已取消' }
      ],
      typeOptions: [
        { value: 'water_electric', label: '水电维修' },
        { value: 'decoration', label: '装修维修' },
        { value: 'public_facility', label: '公共设施' },
        { value: 'clean', label: '保洁服务' },
        { value: 'security', label: '安保服务' },
        { value: 'other', label: '其他' }
      ],
      priorityOptions: [
        { value: 'low', label: '低' },
        { value: 'normal', label: '普通' },
        { value: 'high', label: '高' },
        { value: 'urgent', label: '紧急' }
      ],
      communities: [],
      tableHeight: 500,
      resizeTimer: null,
      buildingOptions: [],
      roomOptions: []
    };
  },
  methods: {
    async fetchData() {
      this.loading = true;
      try {
        const params = {
          page: this.pagination.currentPage,
          size: this.pagination.pageSize,
          community: this.filters.community,
          building: this.filters.building,         // 新增楼栋参数
          roomNumber: this.filters.roomNumber,     // 新增房间号参数
          status: this.filters.status,
          startDate: this.filters.dateRange[0],
          endDate: this.filters.dateRange[1]
        };

        const response = await axios.get('/api/maintenance', { params });
        
        this.requests = response.data.items.map(item => ({
          ...item,
          statusText: this.getStatusText(item.status),
          typeText: this.getTypeText(item.type),
          priorityText: this.getPriorityText(item.priority)
        }));
        
        this.pagination.total = response.data.total;
      } catch (error) {
        console.error('获取报修列表失败:', error);
        this.$message.error('获取报修列表失败');
      } finally {
        this.loading = false;
      }
    },

    async fetchCommunities() {
      try {
        this.loading = true;
        const response = await axios.get('/api/maintenance/communities');
        
        if (!response.data || response.data.length === 0) {
          this.$message.warning('暂无可用社区数据');
          return;
        }

        this.communities = response.data.map(item => ({
          id: item.id,
          community_name: item.community_name,
          address: item.address
        }));

      } catch (error) {
        console.error('获取社区列表失败:', error);
        this.$message.error(error.response?.data?.message || '获取社区列表失败');
      } finally {
        this.loading = false;
      }
    },

    getStatusText(status) {
      const statusMap = {
        pending: '待处理',
        processing: '处理中',
        completed: '已完成',
        cancelled: '已取消',
        rejected: '已驳回'
      };
      return statusMap[status] || status;
    },

    getTypeText(type) {
      const found = this.typeOptions.find(option => option.value === type);
      return found ? found.label : type;
    },

    getPriorityText(priority) {
      const option = this.priorityOptions.find(opt => opt.value === priority);
      return option ? option.label : priority;
    },

    async handleProcess(row) {
      try {
        const { value: formData } = await this.$prompt('请输入处理信息', '受理报修', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputType: 'text',
          inputPlaceholder: '请输入处理备注'
        });

        await axios.post('/api/maintenance/process', {
          id: row.id,
          handler_name: '当前登录用户名',
          handler_phone: '当前登录用户电话',
          notes: formData
        });

        this.$message.success('报修已受理');
        this.fetchData();
      } catch (error) {
        if (error !== 'cancel') {
          console.error('受理报修失败:', error);
          this.$message.error('受理报修失败');
        }
      }
    },

    handlePageChange(page) {
      this.pagination.currentPage = page;
      this.fetchData();
    },

    handleSizeChange(size) {
      this.pagination.pageSize = size;
      this.pagination.currentPage = 1;
      this.fetchData();
    },

    handleSearch() {
      this.pagination.currentPage = 1;
      this.fetchData();
    },

    handleReset() {
      this.filters = {
        community: '',
        building: '',    // 重置楼栋
        roomNumber: '',  // 重置房间号
        status: '',
        dateRange: []
      };
      this.handleSearch();
    },

    handleDetail(row) {
      this.currentRequest = row;
      this.detailDialogVisible = true;
    },

    async handleComplete(row) {
      try {
        const notes = await this.$prompt('请输入完成备注', '完成报修', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputPlaceholder: '请输入完成备注'
        }).then(({ value }) => value);
        
        if (!notes) {
          this.$message.warning('请输入完成备注');
          return;
        }
        
        await axios.post(`/api/maintenance/${row.id}/complete`, {
          notes,
          handler_name: this.currentUser.name, // 假设有当前用户信息
          handler_phone: this.currentUser.phone
        });
        
        this.$message.success('报修已完成');
        this.fetchData();
      } catch (error) {
        if (error !== 'cancel') {
          console.error('报修完成处理失败:', error);
          this.$message.error('报修完成处理失败');
        }
      }
    },

    async handleCancel(row) {
      try {
        await this.$confirm('确认取消此报修?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        });
        
        await axios.post(`/api/maintenance/${row.id}/cancel`);
        
        this.$message.success('报修已取消');
        this.fetchData();
      } catch (error) {
        if (error !== 'cancel') {
          console.error('取消报修失败:', error);
          this.$message.error('取消报修失败');
        }
      }
    },

    initTableHeight() {
      this.handleResize();
      window.addEventListener('resize', this.handleResize);
    },
    
    handleResize() {
      if (this.resizeTimer) {
        clearTimeout(this.resizeTimer);
      }
      
      this.resizeTimer = setTimeout(() => {
        if (this.$refs.maintenanceReport) {
          const offset = 240; // 预留空间给其他元素
          this.tableHeight = window.innerHeight - this.$refs.maintenanceReport.getBoundingClientRect().top - offset;
        }
      }, 100);
    },

    // 监听社区选择变化
    async handleCommunityChange(communityId) {
      if (!communityId) {
        this.buildingOptions = [];
        this.filters.building = '';
        this.filters.roomNumber = '';
        return;
      }
      
      console.log('社区变更，ID:', communityId); // 添加日志
      await this.fetchBuildings(communityId);
    },

    // 监听楼栋选择变化
    async handleBuildingChange(buildingNumber) {
      this.filters.roomNumber = '';
      this.roomOptions = [];
      
      if (buildingNumber) {
        await this.fetchRooms(this.filters.community, buildingNumber);
      }
    },

    // 获取楼栋列表
    async fetchBuildings(communityId) {
      try {
        console.log('正在获取楼栋数据，社区ID:', communityId);
        const response = await axios.get(`/api/maintenance/buildings/${communityId}`);
        console.log('获取到的楼栋数据:', response.data);
        
        this.buildingOptions = response.data.map(item => ({
          value: item.building_number,
          label: item.house_full_name
        }));
        
        // 如果只有一个楼栋，自动选择
        if (this.buildingOptions.length === 1) {
          this.filters.building = this.buildingOptions[0].value;
        }
      } catch (error) {
        console.error('获取楼栋列表失败:', error);
        this.$message.error('获取楼栋列表失败');
      }
    },

    // 获取房间列表
    async fetchRooms(communityId, buildingNumber) {
      try {
        const response = await axios.get(`/api/maintenance/rooms/${communityId}/${buildingNumber}`);
        this.roomOptions = response.data.map(item => ({
          value: item.room_number,      // 使用 room_number 作为值
          label: item.house_full_name,  // 使用完整名称作为显示
          id: item.id,                  // 保存 id 用于提交报修
          ownerName: item.owner_name,   // 保存业主信息
          ownerPhone: item.owner_phone  // 保存联系电话
        }));
      } catch (error) {
        console.error('获取房间列表失败:', error);
        this.$message.error('获取房间列表失败');
      }
    }
  },
  mounted() {
    this.initTableHeight();
    this.fetchCommunities();
    this.fetchData();
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize);
    if (this.resizeTimer) {
      clearTimeout(this.resizeTimer);
    }
  },
  watch: {
    'filters.community'(newVal) {
      this.handleCommunityChange(newVal);
    }
  }
};
</script>

<style scoped>
.maintenance-report {
  height: 100%;
  padding: 20px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

.maintenance-table {
  margin-top: 20px;
  flex: 1;
}

.search-form {
  margin-bottom: 20px;
}

.separator {
  margin: 0 10px;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
  flex-shrink: 0;
}

.detail-container {
  padding: 20px;
}

.images-container {
  margin-top: 20px;
}

.preview-image {
  width: 100px;
  height: 100px;
  margin: 5px;
  border-radius: 4px;
  cursor: pointer;
}

.large-select {
  width: 200px;
}
</style>