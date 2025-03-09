<template>
<el-button type="primary" @click="sendHeartbeat">发送心跳包</el-button>
<!-- 设备管理主容器 -->
  <div class="equipment-list">
    <el-card>

    <!-- 筛选条件区域 -->
      <el-row class="filter-row" :gutter="10">

 <!-- 区域选择 -->
        <el-col :span="4">
          <el-select v-model="filters.region" placeholder="区域" style="width: 100%">
            <el-option label="全部区域" value=""></el-option>
            <el-option label="某某科技园" value="某某科技园"></el-option>
          </el-select>
        </el-col>

<!-- 楼栋选择 -->
        <el-col :span="4">
          <el-select v-model="filters.building" placeholder="楼栋" style="width: 100%">
            <el-option label="全部楼栋" value=""></el-option>
            <el-option label="1栋" value="1栋"></el-option>
            <el-option label="2栋" value="2栋"></el-option>
          </el-select>
        </el-col>

<!-- 单元选择 -->
        <el-col :span="4">
          <el-select v-model="filters.unit" placeholder="单元" style="width: 100%">
            <el-option label="全部单元" value=""></el-option>
            <el-option label="1单元" value="1单元"></el-option>
            <el-option label="2单元" value="2单元"></el-option>
          </el-select>
        </el-col>

<!-- 设备类型筛选 -->
        <el-col :span="4">
          <el-select v-model="filters.equipmentType" placeholder="所有类型" style="width: 100%">
            <el-option label="所有类型" value=""></el-option>
            <el-option label="门口机" value="门口机"></el-option>
            <el-option label="室内机" value="室内机"></el-option>
          </el-select>
        </el-col>

<!-- 设备状态筛选 -->
        <el-col :span="4">
          <el-select v-model="filters.equipmentStatus" placeholder="所有设备" style="width: 100%">
            <el-option label="所有设备" value=""></el-option>
            <el-option label="在线" value="在线"></el-option>
            <el-option label="离线" value="离线"></el-option>
          </el-select>
        </el-col>
      </el-row>

<!-- 第二行筛选条件 -->
      <el-row class="filter-row" :gutter="10">

<!-- 设备名称搜索 -->
        <el-col :span="4">
          <el-input v-model="filters.equipmentName" placeholder="设备名称" clearable class="filter-item" />
        </el-col>

<!-- UID搜索 -->
        <el-col :span="4">
          <el-input v-model="filters.uid" placeholder="UID" clearable class="filter-item" />
        </el-col>

<!-- 操作按钮组 -->
        <el-col :span="16" style="text-align: left;">
          <el-button type="primary" @click="searchEquipment">查询</el-button>
          <el-button @click="resetFilters">刷新</el-button>
          <el-button type="danger" @click="batchDeleteEquipment">批量删除</el-button>
          <el-button type="success" @click="addEquipment">添加门禁</el-button>
        </el-col>
      </el-row>

<!-- 设备数据表格 -->
      <el-table :data="equipmentListToShow" style="width: 100%">
        <el-table-column prop="equipmentName" label="设备名称" />
        <el-table-column prop="status" label="状态" :formatter="formatStatus" />
        <el-table-column prop="uid" label="uid" />
        <el-table-column prop="version" label="版本号" />
        <el-table-column prop="equipmentType" label="设备类型" />
        <el-table-column prop="updateTime" label="更新时间" width="160" />

<!-- 操作列 -->
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button type="primary" size="small" @click="upgradeEquipment(scope.row)">升级</el-button>
            <el-button type="warning" size="small" @click="resetEquipment(scope.row)">重置</el-button>
            <el-button type="text" size="small" @click="editEquipment(scope.row)">编辑</el-button>
            <el-button type="text" size="small" @click="deleteEquipment(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

<!-- 分页组件 -->
      <div class="pagination-container">
        <el-pagination
          background
          layout="total, prev, pager, next, jumper"
          :total="total"
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          @current-change="handleCurrentChange"
          @size-change="handleSizeChange"
        />
      </div>
    </el-card>
  </div>
</template>



<script>
import axios from 'axios';

export default {
  name: 'EquipmentList',
  data() {
    return {
      filters: {
        region: '',
        building: '',
        unit: '',
        equipmentType: '',
        equipmentStatus: '',
        equipmentName: '',
        uid: '',
      },
      equipmentList: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      loading: false, // 添加加载状态
      showSampleData: false, // 添加一个标识来指示是否显示示例数据
      sampleEquipmentList: [
        { equipmentName: '示例设备 1', status: 'online', uid: 'sample001', version: '2.0', equipmentType: '门口机', updateTime: '2023-10-26 10:00:00' },
        { equipmentName: '示例设备 2', status: 'offline', uid: 'sample002', version: '1.5', equipmentType: '室内机', updateTime: '2023-10-25 14:30:00' },
        { equipmentName: '示例设备 3', status: 'online', uid: 'sample003', version: '2.1', equipmentType: '门口机', updateTime: '2023-10-24 18:00:00' },
      ],
      sampleTotal: 3,
    };
  },
  computed: {
    equipmentListToShow() {
      return this.showSampleData ? this.sampleEquipmentList : this.equipmentList;
    }
  },
  methods: {
    formatStatus(row) {
      return row.status === 'online' ? '在线' : '离线';
    },
    async sendHeartbeat() {
      try {
        const response = await axios.post('/api/sendHeartbeat', {
          communityId: "123456",       // 替换为实际值
          deviceCode: "200111",        // 替换为实际值
          cmd: "heart",
          softVer: "1.02.03.04",      // 替换为实际值
          name: "阳光花园",            // 替换为实际值
          deviceSn: "asjkdfiouasdjk123" // 替换为实际值
        });
        this.$message.success(response.data.message);
      } catch (error) {
        console.error('发送心跳包失败:', error);
        this.$message.error('发送心跳包失败');
      }
    },
    async fetchEquipment() {
      this.loading = true;
      this.showSampleData = false; // 尝试获取数据时重置示例数据状态
      try {
        const response = await axios.get('/api/equipment', {
          params: {
            region: this.filters.region,
            building: this.filters.building,
            unit: this.filters.unit,
            equipmentType: this.filters.equipmentType,
            equipmentStatus: this.filters.equipmentStatus,
            equipmentName: this.filters.equipmentName,
            uid: this.filters.uid,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        this.equipmentList = response.data.items;
        this.total = response.data.total;
      } catch (error) {
        console.error('获取设备信息失败:', error);
        this.$message.error('获取设备信息失败，已展示示例数据。');
        this.equipmentList = this.sampleEquipmentList;
        this.total = this.sampleTotal;
        this.showSampleData = true; // 设置为显示示例数据
      } finally {
        this.loading = false;
      }
    },
    searchEquipment() {
      this.currentPage = 1;
      this.fetchEquipment();
    },
    resetFilters() {
      this.filters = {
        region: '',
        building: '',
        unit: '',
        equipmentType: '',
        equipmentStatus: '',
        equipmentName: '',
        uid: '',
      };
      this.searchEquipment();
    },
    handleCurrentChange(page) {
      this.currentPage = page;
      this.fetchEquipment();
    },
    handleSizeChange(size) {
      this.pageSize = size;
      this.currentPage = 1;
      this.fetchEquipment();
    },
    addEquipment() {
      console.log('添加门禁');
      // TODO: Implement add equipment logic
    },
    batchDeleteEquipment() {
      console.log('批量删除设备');
      // TODO: Implement batch delete logic, potentially with selected rows
    },
    upgradeEquipment(row) {
      console.log('升级设备:', row);
      // TODO: Implement upgrade equipment logic
    },
    resetEquipment(row) {
      console.log('重置设备:', row);
      // TODO: Implement reset equipment logic
    },
    editEquipment(row) {
      console.log('编辑设备:', row);
      // TODO: Implement edit equipment logic, potentially navigate to an edit page
    },
    deleteEquipment(row) {
      console.log('删除设备:', row);
      // TODO: Implement delete equipment logic
    },
  },
  mounted() {
    this.fetchEquipment();
  },
};
</script>

<style scoped>
.filter-row {
  margin-bottom: 15px;
}

.filter-item {
  margin-right: 10px;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style>
