<template>
  <div class="equipment-list-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>门禁设备管理</span>
          <el-button type="primary" size="small" @click="sendHeartbeat">发送心跳包</el-button>
        </div>
      </template>

      <!-- 第一行筛选条件 -->
      <el-row class="filter-row" :gutter="10">
        <el-col :span="4">
          <el-select v-model="filters.region" placeholder="选择区域" clearable class="filter-item">
            <el-option label="A区" value="A" />
            <el-option label="B区" value="B" />
            <el-option label="C区" value="C" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filters.building" placeholder="选择楼栋" clearable class="filter-item">
            <el-option label="1栋" value="1" />
            <el-option label="2栋" value="2" />
            <el-option label="3栋" value="3" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filters.unit" placeholder="选择单元" clearable class="filter-item">
            <el-option label="1单元" value="1" />
            <el-option label="2单元" value="2" />
            <el-option label="3单元" value="3" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filters.equipmentType" placeholder="设备类型" clearable class="filter-item">
            <el-option label="门口机" value="Entrance Machine" />
            <el-option label="围墙机" value="Fencing Machine" />
            <el-option label="室内机" value="Indoor Machine" />
            <el-option label="其他" value="Other" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filters.equipmentStatus" placeholder="设备状态" clearable class="filter-item">
            <el-option label="在线" value="online" />
            <el-option label="离线" value="offline" />
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

        <!-- 小区编码搜索 -->
        <el-col :span="4">
          <el-input v-model="filters.communityCode" placeholder="小区编码" clearable class="filter-item" />
        </el-col>

        <!-- 所属小区搜索 -->
        <el-col :span="4">
          <el-input v-model="filters.communityName" placeholder="所属小区" clearable class="filter-item" />
        </el-col>

        <!-- 操作按钮组 -->
        <el-col :span="8" style="text-align: left;">
          <el-button type="primary" @click="searchEquipment">查询</el-button>
          <el-button @click="resetFilters">刷新</el-button>
          <el-button type="danger" @click="batchDeleteEquipment">批量删除</el-button>
          <el-button type="success" @click="addEquipment">添加门禁</el-button>
        </el-col>
      </el-row>

      <!-- 设备数据表格 -->
      <el-table 
        :data="equipmentListToShow" 
        style="width: 100%" 
        v-loading="loading"
        @selection-change="handleSelectionChange"
        border
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="equipmentName" label="设备名称" min-width="120" />
        <el-table-column prop="status" label="状态" width="80">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'online' ? 'success' : 'danger'">
              {{ formatStatus(scope.row) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="communityCode" label="小区编码" min-width="100" />
        <el-table-column prop="communityName" label="所属小区" min-width="120" />
        <el-table-column prop="uid" label="uid" min-width="120" />
        <el-table-column prop="ip" label="IP" min-width="120" />
        <el-table-column prop="createTime" label="创建时间" min-width="160" />
        <el-table-column prop="lastStatusTime" label="最新设备状态" min-width="120">
          <template #default="scope">
            <div class="status-indicator">
              <span 
                class="status-dot" 
                :class="scope.row.status === 'online' ? 'online' : 'offline'"
              ></span>
              {{ scope.row.status === 'online' ? '在线' : '离线' }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="faceDownloadTime" label="人脸下载时间" min-width="160" />
        <el-table-column prop="version" label="版本号" min-width="100" />
        <el-table-column prop="equipmentType" label="设备类型" min-width="100">
          <template #default="scope">
            {{ getDeviceTypeText(scope.row.equipmentType) }}
          </template>
        </el-table-column>
        <el-table-column prop="updateTime" label="更新时间" min-width="160" />
        <el-table-column prop="lastStatusTime" label="状态更新时间" min-width="160">
          <template #default="scope">
            {{ formatDateTime(scope.row.lastStatusTime) }}
          </template>
        </el-table-column>

        <!-- 操作列 -->
        <el-table-column label="操作" fixed="right" min-width="320">
          <template #default="scope">
            <el-button 
              type="primary" 
              size="small" 
              @click="upgradeEquipment(scope.row)">
              升级
            </el-button>
            <el-button 
              type="warning" 
              size="small" 
              @click="resetEquipment(scope.row)">
              重置
            </el-button>
            <el-button 
              type="success" 
              size="small" 
              @click="downloadFace(scope.row)">
              人脸下载
            </el-button>
            <el-button 
              type="info" 
              size="small" 
              @click="editEquipment(scope.row)">
              编辑
            </el-button>
            <el-button 
              type="danger" 
              size="small" 
              @click="deleteEquipment(scope.row)">
              删除
            </el-button>
            <el-button 
              type="primary" 
              size="small" 
              :loading="scope.row._checking" 
              @click="checkDeviceStatus(scope.row)"
            >
              检查状态
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          background
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          :page-size="pageSize"
          :current-page="currentPage"
          :page-sizes="[10, 20, 50, 100]"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 添加/编辑设备对话框 -->
    <el-dialog 
      :title="dialogTitle" 
      v-model="dialogVisible" 
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form :model="equipmentForm" :rules="formRules" ref="equipmentFormRef" label-width="100px">
        <el-form-item label="设备名称" prop="equipmentName">
          <el-input v-model="equipmentForm.equipmentName" placeholder="请输入设备名称" />
        </el-form-item>
        <el-form-item label="设备类型" prop="equipmentType">
          <el-select v-model="equipmentForm.equipmentType" placeholder="请选择设备类型" style="width: 100%">
            <el-option label="门口机" value="Entrance Machine" />
            <el-option label="围墙机" value="Fencing Machine" />
            <el-option label="室内机" value="Indoor Machine" />
            <el-option label="其他" value="Other" />
          </el-select>
        </el-form-item>
        <el-form-item label="所属小区" prop="communityName">
          <el-input v-model="equipmentForm.communityName" placeholder="请输入所属小区" />
        </el-form-item>
        <el-form-item label="小区编码" prop="communityCode">
          <el-input v-model="equipmentForm.communityCode" placeholder="请输入小区编码" />
        </el-form-item>
        <el-form-item label="UID" prop="uid">
          <el-input v-model="equipmentForm.uid" placeholder="请输入UID" />
        </el-form-item>
        <el-form-item label="IP地址" prop="ip">
          <el-input v-model="equipmentForm.ip" placeholder="请输入IP地址" />
        </el-form-item>
        <el-form-item label="版本号" prop="version">
          <el-input v-model="equipmentForm.version" placeholder="请输入版本号" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitEquipmentForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
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
        communityCode: '',
        communityName: '',
      },
      equipmentList: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      loading: false,
      showSampleData: false,
      multipleSelection: [], // 多选数据
      dialogVisible: false,
      dialogTitle: '',
      equipmentForm: {
        id: null,
        equipmentName: '',
        equipmentType: '',
        communityName: '',
        communityCode: '',
        uid: '',
        ip: '',
        version: '',
        status: 'online'
      },
      formRules: {
        equipmentName: [
          { required: true, message: '请输入设备名称', trigger: 'blur' }
        ],
        equipmentType: [
          { required: true, message: '请选择设备类型', trigger: 'change' }
        ],
        communityName: [
          { required: true, message: '请输入所属小区', trigger: 'blur' }
        ],
        communityCode: [
          { required: true, message: '请输入小区编码', trigger: 'blur' }
        ],
        uid: [
          { required: true, message: '请输入UID', trigger: 'blur' }
        ],
        ip: [
          { required: true, message: '请输入IP地址', trigger: 'blur' },
          { pattern: /^(\d{1,3}\.){3}\d{1,3}$/, message: 'IP地址格式不正确', trigger: 'blur' }
        ]
      },
      sampleEquipmentList: [
        { 
          id: 1,
          equipmentName: '示例设备 1', 
          status: 'online', 
          communityCode: 'COMM001',
          communityName: '阳光花园',
          uid: 'sample001', 
          ip: '192.168.1.101',
          createTime: '2023-10-20 08:30:00',
          lastStatusTime: '2023-10-26 09:45:00',
          faceDownloadTime: '2023-10-25 14:20:00',
          version: '2.0', 
          equipmentType: 'Entrance Machine', 
          updateTime: '2023-10-26 10:00:00' 
        },
        { 
          id: 2,
          equipmentName: '示例设备 2', 
          status: 'offline', 
          communityCode: 'COMM001',
          communityName: '阳光花园',
          uid: 'sample002', 
          ip: '192.168.1.102',
          createTime: '2023-10-15 10:20:00',
          lastStatusTime: '2023-10-25 16:30:00',
          faceDownloadTime: '2023-10-24 11:15:00',
          version: '1.5', 
          equipmentType: 'Indoor Machine', 
          updateTime: '2023-10-25 14:30:00' 
        },
        { 
          id: 3,
          equipmentName: '示例设备 3', 
          status: 'online', 
          communityCode: 'COMM002',
          communityName: '翠湖庭院',
          uid: 'sample003', 
          ip: '192.168.1.103',
          createTime: '2023-10-18 14:45:00',
          lastStatusTime: '2023-10-24 17:50:00',
          faceDownloadTime: '2023-10-23 09:30:00',
          version: '2.1', 
          equipmentType: 'Fencing Machine', 
          updateTime: '2023-10-24 18:00:00' 
        },
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
    getDeviceTypeText(type) {
      const types = {
        'Entrance Machine': '门口机',
        'Fencing Machine': '围墙机',
        'Indoor Machine': '室内机',
        'Other': '其他'
      };
      return types[type] || type;
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    async sendHeartbeat(device = null) {
      try {
        // 如果传入了特定设备，则只测试该设备
        if (device) {
          this.testDeviceStatus(device);
          return;
        }
        
        // 否则测试所有设备
        this.loading = true;
        const response = await axios.post('/api/sendHeartbeat/all');
        
        if (response.data.result === "0") {
          this.$message.success('心跳包发送成功，正在等待设备响应');
          // 5秒后刷新设备列表，以获取最新状态
          setTimeout(() => {
            this.fetchEquipment();
          }, 5000);
        } else {
          this.$message.error('心跳包发送失败: ' + response.data.message);
        }
      } catch (error) {
        console.error('发送心跳包失败:', error);
        this.$message.error('发送心跳包失败，请检查网络连接');
      } finally {
        this.loading = false;
      }
    },
    async testDeviceStatus(device) {
      if (!device.ip) {
        this.$message.warning(`设备 ${device.equipmentName} 没有IP地址，无法测试`);
        return;
      }
      
      try {
        this.$set(device, '_testing', true); // 添加测试中标记
        
        const response = await axios.post('/api/sendHeartbeat/device', {
          deviceIp: device.ip,
          devicePort: 7998, // 使用默认端口，也可以从设备配置中获取
          communityCode: device.communityCode,
          uid: device.uid
        });
        
        if (response.data.result === "0") {
          this.$message.success(`设备 ${device.equipmentName} 心跳包发送成功`);
          
          // 3秒后查询该设备的最新状态
          setTimeout(async () => {
            try {
              const statusResponse = await axios.get(`/api/equipment/${device.id}/status`);
              if (statusResponse.data.status === 'online') {
                this.$message.success(`设备 ${device.equipmentName} 在线`);
                // 更新本地设备状态
                this.$set(device, 'status', 'online');
                this.$set(device, 'lastStatusTime', new Date().toLocaleString());
              } else {
                this.$message.warning(`设备 ${device.equipmentName} 离线`);
                this.$set(device, 'status', 'offline');
              }
            } catch (error) {
              console.error('获取设备状态失败:', error);
              this.$message.error(`获取设备 ${device.equipmentName} 状态失败`);
            } finally {
              this.$set(device, '_testing', false);
            }
          }, 3000);
        } else {
          this.$message.error(`设备 ${device.equipmentName} 心跳包发送失败: ${response.data.message}`);
          this.$set(device, '_testing', false);
        }
      } catch (error) {
        console.error('测试设备状态失败:', error);
        this.$message.error(`测试设备 ${device.equipmentName} 状态失败`);
        this.$set(device, '_testing', false);
      }
    },
    async fetchEquipment() {
      this.loading = true;
      this.showSampleData = false;
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
            communityCode: this.filters.communityCode,
            communityName: this.filters.communityName,
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
        this.showSampleData = true;
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
        communityCode: '',
        communityName: '',
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
      this.dialogTitle = '添加门禁设备';
      this.equipmentForm = {
        id: null,
        equipmentName: '',
        equipmentType: '',
        communityName: '',
        communityCode: '',
        uid: '',
        ip: '',
        version: '',
        status: 'online'
      };
      this.dialogVisible = true;
    },
    editEquipment(row) {
      this.dialogTitle = '编辑门禁设备';
      this.equipmentForm = { ...row };
      this.dialogVisible = true;
    },
    async submitEquipmentForm() {
      try {
        await this.$refs.equipmentFormRef.validate();
        
        if (this.equipmentForm.id) {
          // 编辑设备
          await axios.put(`/api/equipment/${this.equipmentForm.id}`, this.equipmentForm);
          this.$message.success('设备更新成功');
        } else {
          // 添加设备
          await axios.post('/api/equipment', this.equipmentForm);
          this.$message.success('设备添加成功');
        }
        
        this.dialogVisible = false;
        this.fetchEquipment();
      } catch (error) {
        if (error === false) {
          // 表单验证失败
          return;
        }
        console.error('保存设备信息失败:', error);
        this.$message.error('保存设备信息失败');
      }
    },
    async batchDeleteEquipment() {
      if (this.multipleSelection.length === 0) {
        this.$message.warning('请至少选择一个设备');
        return;
      }
      
      try {
        await this.$confirm('确定要删除选中的设备吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        });
        
        const ids = this.multipleSelection.map(item => item.id);
        await axios.delete('/api/equipment/batch', { data: { ids } });
        this.$message.success('批量删除成功');
        this.fetchEquipment();
      } catch (error) {
        if (error !== 'cancel') {
          console.error('批量删除设备失败:', error);
          this.$message.error('批量删除设备失败');
        }
      }
    },
    async upgradeEquipment(row) {
      try {
        await this.$confirm(`确定要升级设备 "${row.equipmentName}" 吗？`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        });
        
        await axios.post(`/api/equipment/${row.id}/upgrade`);
        this.$message.success('设备升级指令已发送');
      } catch (error) {
        if (error !== 'cancel') {
          console.error('升级设备失败:', error);
          this.$message.error('升级设备失败');
        }
      }
    },
    async resetEquipment(row) {
      try {
        await this.$confirm(`确定要重置设备 "${row.equipmentName}" 吗？`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        });
        
        await axios.post(`/api/equipment/${row.id}/reset`);
        this.$message.success('设备重置指令已发送');
      } catch (error) {
        if (error !== 'cancel') {
          console.error('重置设备失败:', error);
          this.$message.error('重置设备失败');
        }
      }
    },
    async downloadFace(row) {
      try {
        await this.$confirm(`确定要为设备 "${row.equipmentName}" 下载人脸数据吗？`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'info'
        });
        
        await axios.post(`/api/equipment/${row.id}/download-face`);
        this.$message.success(`正在为设备 ${row.equipmentName} 下载人脸数据`);
      } catch (error) {
        if (error !== 'cancel') {
          console.error('下载人脸数据失败:', error);
          this.$message.error('下载人脸数据失败');
        }
      }
    },
    async deleteEquipment(row) {
      try {
        await this.$confirm(`确定要删除设备 "${row.equipmentName}" 吗？`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        });
        
        await axios.delete(`/api/equipment/${row.id}`);
        this.$message.success('设备删除成功');
        this.fetchEquipment();
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除设备失败:', error);
          this.$message.error('删除设备失败');
        }
      }
    },
    async checkDeviceStatus(row) {
      try {
        this.$set(row, '_checking', true);
        
        const response = await axios.post(`/api/equipment/${row.id}/check-status`);
        
        if (response.data.result === "0") {
          this.$message.success(`设备 ${row.equipmentName} 状态检查成功`);
          row.status = response.data.status;
          row.lastStatusTime = response.data.lastStatusTime;
        } else {
          this.$message.error(`设备 ${row.equipmentName} 状态检查失败: ${response.data.message}`);
        }
      } catch (error) {
        console.error('检查设备状态失败:', error);
        this.$message.error('检查设备状态失败');
      } finally {
        this.$set(row, '_checking', false);
      }
    },
    formatDateTime(dateTime) {
      if (!dateTime) return '';
      const date = new Date(dateTime);
      return date.toLocaleString();
    },
  },
  mounted() {
    this.fetchEquipment();
  },
};
</script>

<style scoped>
.equipment-list-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-row {
  margin-bottom: 15px;
}

.filter-item {
  width: 100%;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}

/* 状态指示器样式 */
.status-indicator {
  display: flex;
  align-items: center;
}

.status-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 6px;
}

.status-dot.online {
  background-color: #67C23A; /* 绿色，表示在线 */
}

.status-dot.offline {
  background-color: #F56C6C; /* 红色，表示离线 */
}
</style>