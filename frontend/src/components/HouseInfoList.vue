<template>
  <div class="house-management">
    <!-- Left Sidebar -->
    <div class="sidebar" :class="{ collapsed: isSidebarCollapsed }">
      <el-card class="tree-card">
        <div class="tree-header">
          <span>区域总览</span>
          <el-button type="primary" size="small" @click="refreshTree">刷新</el-button>
        </div>
        
        <!-- 社区选择器 -->
        <div class="community-selector mb-4">
          <el-select 
            v-model="currentCommunityId" 
            placeholder="请选择社区"
            @change="handleCommunityChange"
            style="width: 100%;"
          >
            <el-option
              v-for="item in communities"
              :key="item.id"
              :label="item.community_name || item.communityName"
              :value="item.id"
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

    <!-- Right Content -->
    <div class="content">
      <el-card>
        <el-row :gutter="20" class="mb-4">
          <el-col :span="18">
            <el-input
              v-model="search.keyword"
              placeholder="请输入房屋信息(房屋名称/区号/栋号/单元号/房间号)"
              clearable
              prefix-icon="el-icon-search"
            />
          </el-col>
          <el-col :span="6">
            <el-button type="primary" @click="searchHouses">查询</el-button>
            <el-button type="primary" @click="resetSearch">重置</el-button>
            <el-button type="success" @click="showAddDialog">添加房屋</el-button>
          </el-col>
        </el-row>

        <el-table :data="houseList" style="width: 100%" v-loading="loading">
          <el-table-column prop="fullName" label="房屋地址" />
          <el-table-column prop="districtNumber" label="区号" />
          <el-table-column prop="buildingNumber" label="栋号" />
          <el-table-column prop="unitNumber" label="单元号" />
          <el-table-column prop="createTime" label="创建时间" />
          <el-table-column label="操作" width="250">
            <template #default="scope">
              <el-button 
                type="primary" 
                size="small" 
                @click="showEditDialog(scope.row)"
              >编辑</el-button>
              <el-button 
                type="danger" 
                size="small" 
                @click="deleteHouse(scope.row)"
              >删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <el-pagination
          background
          layout="prev, pager, next"
          :total="total"
          :current-page="currentPage"
          :page-size="pageSize"
          @current-change="handlePageChange"
        />
      </el-card>
    </div>
    
    <!-- 添加房屋对话框 -->
    <el-dialog
      v-model="addDialog.visible"
      :title="addDialog.title"
      width="500px"
    >
      <el-form 
        :model="addDialog.form" 
        :rules="addDialogRules"
        label-width="100px" 
        ref="addFormRef"
      >
        <!-- 社区选择 -->
        <el-form-item label="所属社区" prop="communityId">
          <el-select 
            v-model="addDialog.form.communityId" 
            placeholder="请选择社区"
            disabled
            style="width: 100%;"
          >
            <el-option
              v-for="item in communities"
              :key="item.id"
              :label="item.community_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>

        <!-- 父级房屋 -->
        <el-form-item label="父级房屋" prop="parentId">
          <el-input 
            v-model="parentHouseName" 
            disabled
            placeholder="自动获取父级房屋"
          ></el-input>
        </el-form-item>

        <!-- 房屋层级 -->
        <el-form-item label="房屋层级" prop="level">
          <el-select 
            v-model="addDialog.form.level" 
            disabled
            style="width: 100%;"
          >
            <el-option label="区" :value="1" />
            <el-option label="栋" :value="2" />
            <el-option label="单元" :value="3" />
            <el-option label="房间" :value="4" />
          </el-select>
        </el-form-item>

        <!-- 区号 -->
        <el-form-item 
          v-if="addDialog.form.level === 1" 
          label="区号" 
          prop="districtNumber"
        >
          <el-input 
            v-model="addDialog.form.districtNumber" 
            placeholder="请输入区号"
            @change="generateFullName"
          >
            <template #append>区</template>
          </el-input>
        </el-form-item>

        <!-- 楼栋号 -->
        <el-form-item 
          v-if="addDialog.form.level === 2" 
          label="楼栋号" 
          prop="buildingNumber"
        >
          <el-input 
            v-model="addDialog.form.buildingNumber" 
            placeholder="请输入楼栋号"
            @change="generateFullName"
          >
            <template #append>栋</template>
          </el-input>
        </el-form-item>

        <!-- 单元号 -->
        <el-form-item 
          v-if="addDialog.form.level === 3" 
          label="单元号" 
          prop="unitNumber"
        >
          <el-input 
            v-model="addDialog.form.unitNumber" 
            placeholder="请输入单元号"
            @change="generateFullName"
          >
            <template #append>单元</template>
          </el-input>
        </el-form-item>

        <!-- 房间号 -->
        <el-form-item 
          v-if="addDialog.form.level === 4" 
          label="房间号" 
          prop="roomNumber"
        >
          <el-input 
            v-model="addDialog.form.roomNumber" 
            placeholder="请输入房间号"
            @change="generateFullName"
          >
            <template #append>室</template>
          </el-input>
        </el-form-item>

        <!-- 完整名称 -->
        <el-form-item label="完整名称" prop="fullName" required>
          <el-input 
            v-model="addDialog.form.fullName" 
            placeholder="自动生成完整名称"
            disabled
          ></el-input>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="closeAddDialog">取消</el-button>
        <el-button type="primary" @click="submitAddHouse" :loading="addDialog.loading">确定</el-button>
      </template>
    </el-dialog>
    
    <!-- 编辑房屋对话框 -->
    <el-dialog
      v-model="editDialog.visible"
      :title="editDialog.title"
      width="500px"
    >
      <el-form :model="editDialog.form" label-width="100px" ref="editFormRef">
        <el-form-item label="名称" prop="fullName" required>
          <el-input v-model="editDialog.form.fullName" placeholder="请输入房屋名称"></el-input>
        </el-form-item>
        
        <el-form-item v-if="editDialog.form.level === 1" label="区号" prop="districtNumber">
          <el-input v-model="editDialog.form.districtNumber" placeholder="请输入区号"></el-input>
        </el-form-item>
        
        <el-form-item v-if="editDialog.form.level === 2" label="楼栋号" prop="buildingNumber">
          <el-input v-model="editDialog.form.buildingNumber" placeholder="请输入楼栋号"></el-input>
        </el-form-item>
        
        <el-form-item v-if="editDialog.form.level === 3" label="单元号" prop="unitNumber">
          <el-input v-model="editDialog.form.unitNumber" placeholder="请输入单元号"></el-input>
        </el-form-item>
        
        <el-form-item v-if="editDialog.form.level === 4" label="房间号" prop="roomNumber">
          <el-input v-model="editDialog.form.roomNumber" placeholder="请输入房间号"></el-input>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="editDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="submitEditHouse">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import { ElMessage } from 'element-plus'

export default {
  name: 'HouseInfoList',
  data() {
    return {
      search: {
        keyword: '',
        communityId: null,
        parentId: null,
        parentIds: null,
        roomId: null,
        districtNumber: '',
        buildingNumber: '',
        unitNumber: '',
        roomNumber: ''
      },
      loading: false,
      houseList: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      houseTreeData: [],
      defaultProps: {
        children: 'children',
        label: 'fullName'
      },
      currentCommunityId: null,
      communities: [],
      isSidebarCollapsed: false,
      
      // 添加房屋对话框
      addDialog: {
        visible: false,
        title: '添加房屋',
        loading: false,
        form: {
          communityId: null,
          parentId: null,
          districtNumber: '',
          buildingNumber: '',
          unitNumber: '',
          roomNumber: '',
          fullName: '',
          level: 1
        }
      },
      
      // 表单验证规则
      addDialogRules: {
        districtNumber: [
          { required: true, message: '请输入区号', trigger: 'blur' },
          { pattern: /^\d+$/, message: '区号必须为数字', trigger: 'blur' }
        ],
        buildingNumber: [
          { required: true, message: '请输入楼栋号', trigger: 'blur' },
          { pattern: /^\d+$/, message: '楼栋号必须为数字', trigger: 'blur' }
        ],
        unitNumber: [
          { required: true, message: '请输入单元号', trigger: 'blur' },
          { pattern: /^\d+$/, message: '单元号必须为数字', trigger: 'blur' }
        ],
        roomNumber: [
          { required: true, message: '请输入房间号', trigger: 'blur' },
          { pattern: /^\d+$/, message: '房间号必须为数字', trigger: 'blur' }
        ]
      },
      
      parentHouseName: '', // 父级房屋名称
      
      // 编辑房屋对话框
      editDialog: {
        visible: false,
        title: '编辑房屋',
        form: {
          id: null,
          communityId: null,
          parentId: null,
          districtNumber: '',
          buildingNumber: '',
          unitNumber: '',
          roomNumber: '',
          fullName: '',
          level: 1
        }
      }
    }
  },
  methods: {
    async fetchCommunities() {
      try {
        const response = await axios.get('/api/communities', {
          params: {
            page: 1,
            size: 100
          }
        });
        
        // 处理不同格式的API返回
        if (response.data && response.data.items) {
          // 返回格式为 {items: [...], total: 20}
          this.communities = response.data.items.map(item => ({
            id: item.id,
            community_name: item.communityName
          }));
        } else if (Array.isArray(response.data)) {
          // 返回格式为 [{id: 1, community_name: "xxx"}, ...]
          this.communities = response.data;
        } else {
          throw new Error('未知的API返回格式');
        }
        
        console.log('获取社区列表成功', this.communities);
        
        if (this.communities.length > 0) {
          this.currentCommunityId = this.communities[0].id;
          this.$forceUpdate();
          this.fetchHouseTree();
          this.fetchHouses();
        } else {
          this.$message.warning('没有可用的社区数据');
        }
      } catch (error) {
        console.error('获取社区列表失败:', error);
        this.$message.error('获取社区列表失败: ' + error.message);
      }
    },

    async fetchHouses() {
      this.loading = true
      try {
        const params = {
          keyword: this.search.keyword,
          communityId: this.currentCommunityId,
          page: this.currentPage,
          pageSize: this.pageSize,
          districtNumber: this.search.districtNumber,
          buildingNumber: this.search.buildingNumber,
          unitNumber: this.search.unitNumber,
          roomNumber: this.search.roomNumber
        };
        
        if (this.search.roomId) {
          params.roomId = this.search.roomId;
        } else if (this.search.parentIds && this.search.parentIds.length > 0) {
          params.parentIds = this.search.parentIds.join(',');
        } else if (this.search.parentId) {
          params.parentId = this.search.parentId;
        }
        
        const response = await axios.get('/api/houses', { params });
        
        if (response.data.success) {
          this.houseList = response.data.data.items || [];
          this.total = response.data.data.total || 0;
        } else {
          throw new Error(response.data.error || '获取数据失败');
        }
      } catch (error) {
        console.error('获取房屋列表失败:', error);
        this.$message.error('获取房屋列表失败');
        this.houseList = [];
        this.total = 0;
      } finally {
        this.loading = false;
      }
    },

    async fetchHouseTree() {
      if (!this.currentCommunityId) {
        console.log('社区ID未设置，无法获取房屋树');
        this.houseTreeData = [];
        return;
      }
      
      try {
        this.loading = true;
        const response = await axios.get(`/api/houses/tree/${this.currentCommunityId}`);
        
        if (response.data.success) {
          this.houseTreeData = response.data.data || [];
          console.log('房屋树数据加载成功', this.houseTreeData);
        } else {
          throw new Error(response.data.error || '获取房屋树结构失败');
        }
      } catch (error) {
        console.error('获取房屋树失败:', error);
        this.$message.error('获取房屋树失败: ' + (error.message || '未知错误'));
        this.houseTreeData = [];
      } finally {
        this.loading = false;
      }
    },

    async refreshTree() {
      try {
        await this.fetchHouseTree()
        this.$message.success('刷新成功')
      } catch (error) {
        this.$message.error('刷新失败')
      }
    },

    handleNodeClick(data) {
      this.search.parentId = data.id
      this.search.parentIds = null
      this.$refs.tree.setCheckedKeys([])
      
      if (data.level === 4) {
        this.search.roomId = data.id
      } else {
        this.search.roomId = null
      }
      
      this.fetchHouses()
    },

    handleCheck(data, { checkedNodes }) {
      const leafIds = checkedNodes
        .filter(node => !node.children || node.children.length === 0)
        .map(node => node.id)
      
      this.search.parentIds = leafIds.length > 0 ? leafIds : null
      this.search.parentId = null
      this.fetchHouses()
    },

    searchHouses() {
      this.currentPage = 1
      this.fetchHouses()
    },

    // 显示添加房屋对话框
    showAddDialog() {
      const currentNode = this.$refs.tree.getCurrentNode();
      
      // 重置表单
      this.addDialog.form = {
        communityId: this.currentCommunityId,
        parentId: currentNode ? currentNode.id : null,
        districtNumber: '',
        buildingNumber: '',
        unitNumber: '',
        roomNumber: '',
        fullName: '',
        level: currentNode ? currentNode.level + 1 : 1
      };
      
      // 设置父级房屋名称
      this.parentHouseName = currentNode ? currentNode.fullName : '无';
      
      // 设置对话框标题
      this.addDialog.title = this.getLevelTitle(this.addDialog.form.level);
      
      this.addDialog.visible = true;
      
      // 重置表单校验
      if (this.$refs.addFormRef) {
        this.$refs.addFormRef.resetFields();
      }
    },
    
    // 根据层级获取标题
    getLevelTitle(level) {
      const titles = {
        1: '添加区',
        2: '添加楼栋',
        3: '添加单元',
        4: '添加房间'
      };
      return titles[level] || '添加房屋';
    },
    
    // 生成完整名称
    generateFullName() {
      const form = this.addDialog.form;
      const community = this.communities.find(c => c.id === form.communityId);
      const currentNode = this.$refs.tree.getCurrentNode();
      
      if (!community) return;
      
      let fullName = '';
      
      // 如果有父节点，使用父节点的信息构建名称
      if (currentNode) {
        // 获取父节点的完整路径信息
        const parentFullName = currentNode.fullName;
        
        if (form.level === 4) {
          // 对于房间，使用父节点的单元信息
          const unitPart = parentFullName.split('单元')[0];
          fullName = `${unitPart}单元${form.roomNumber}室`;
        } else {
          fullName = community.community_name;
          if (form.level >= 1 && form.districtNumber) {
            fullName += `${form.districtNumber}区`;
          }
          if (form.level >= 2 && form.buildingNumber) {
            fullName += `${form.buildingNumber}栋`;
          }
          if (form.level >= 3 && form.unitNumber) {
            fullName += `${form.unitNumber}单元`;
          }
        }
      } else {
        // 如果没有父节点，从头构建名称
        fullName = community.community_name;
        if (form.level >= 1 && form.districtNumber) {
          fullName += `${form.districtNumber}区`;
        }
      }
      
      this.addDialog.form.fullName = fullName;
    },
    
    // 关闭对话框
    closeAddDialog() {
      this.addDialog.visible = false;
      this.addDialog.loading = false;
      if (this.$refs.addFormRef) {
        this.$refs.addFormRef.resetFields();
      }
    },
    
    // 提交添加房屋
    async submitAddHouse() {
      try {
        // 表单验证
        await this.$refs.addFormRef.validate();
        
        this.addDialog.loading = true;
        
        // 构建提交数据
        const formData = {
          communityId: this.addDialog.form.communityId,
          parentId: this.addDialog.form.parentId,
          fullName: this.addDialog.form.fullName,
          level: this.addDialog.form.level
        };
        
        // 根据层级添加对应字段
        switch (this.addDialog.form.level) {
          case 1:
            formData.districtNumber = this.addDialog.form.districtNumber;
            break;
          case 2:
            formData.buildingNumber = this.addDialog.form.buildingNumber;
            break;
          case 3:
            formData.unitNumber = this.addDialog.form.unitNumber;
            break;
          case 4:
            formData.roomNumber = this.addDialog.form.roomNumber;
            break;
        }
        
        const response = await axios.post('/api/houses', formData);
        
        if (response.data.success) {
          this.$message.success('添加成功');
          this.closeAddDialog();
          await this.fetchHouses();
          await this.fetchHouseTree();
        } else {
          throw new Error(response.data.error || '添加失败');
        }
      } catch (error) {
        console.error('添加房屋失败:', error);
        this.$message.error(error.message || '添加失败');
      } finally {
        this.addDialog.loading = false;
      }
    },
    
    // 显示编辑房屋对话框
    showEditDialog(row) {
      this.editDialog.form = {
        id: row.id,
        communityId: row.communityId,
        districtNumber: row.districtNumber || '',
        buildingNumber: row.buildingNumber || '',
        unitNumber: row.unitNumber || '',
        roomNumber: row.roomNumber || '',
        fullName: row.fullName,
        level: row.level,
        parentId: row.parentId
      };
      
      this.editDialog.visible = true;
    },
    
    // 提交编辑房屋表单
    async submitEditHouse() {
      try {
        if (!this.editDialog.form.fullName) {
          this.$message.warning('房屋名称不能为空');
          return;
        }
        
        // 构建提交数据
        const formData = {
          fullName: this.editDialog.form.fullName,
          level: this.editDialog.form.level,
          parentId: this.editDialog.form.parentId
        };
        
        // 根据层级添加相应字段
        if (this.editDialog.form.level === 1) {
          formData.districtNumber = this.editDialog.form.districtNumber;
        } else if (this.editDialog.form.level === 2) {
          formData.buildingNumber = this.editDialog.form.buildingNumber;
        } else if (this.editDialog.form.level === 3) {
          formData.unitNumber = this.editDialog.form.unitNumber;
        } else if (this.editDialog.form.level === 4) {
          formData.roomNumber = this.editDialog.form.roomNumber;
          // 更新房屋全名中的房间号部分
          formData.fullName = this.editDialog.form.fullName.replace(/\d+室$/, `${this.editDialog.form.roomNumber}室`);
        }

        const response = await axios.put(`/api/houses/${this.editDialog.form.id}`, formData);
        
        if (response.data.success) {
          this.$message.success('编辑成功');
          this.editDialog.visible = false;
          await this.fetchHouses();
          await this.fetchHouseTree();
        } else {
          throw new Error(response.data.error || '编辑失败');
        }
      } catch (error) {
        console.error('编辑房屋失败:', error);
        this.$message.error('编辑失败: ' + (error.message || '未知错误'));
      }
    },

    async deleteHouse(row) {
      try {
        await this.$confirm('确认删除该房屋信息吗？', '提示', {
          type: 'warning',
          confirmButtonText: '确定',
          cancelButtonText: '取消'
        });
        
        const response = await axios.delete(`/api/houses/${row.id}`);
        if (response.data.success) {
          this.$message.success('删除成功');
          await this.fetchHouses();
          await this.fetchHouseTree();
        } else {
          // 显示具体的错误信息
          throw new Error(response.data.error || '删除失败');
        }
      } catch (error) {
        if (error === 'cancel') {
          return;
        }
        // 显示友好的错误提示
        const errorMsg = error.response?.data?.error || error.message || '删除失败';
        this.$message.error(errorMsg);
        console.error('删除房屋失败:', error);
      }
    },

    handlePageChange(page) {
      this.currentPage = page
      this.fetchHouses()
    },

    toggleSidebar() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed
    },

    handleCommunityChange() {
      console.log('切换社区为:', this.currentCommunityId);
      this.search.parentId = null;
      this.search.parentIds = null;
      this.search.roomId = null;
      if (this.$refs.tree) {
        this.$refs.tree.setCheckedKeys([]);
      }
      this.fetchHouseTree();
      this.fetchHouses();
    },

    resetSearch() {
      this.search = {
        keyword: '',
        communityId: this.currentCommunityId,
        parentId: null,
        parentIds: null,
        roomId: null,
        districtNumber: '',
        buildingNumber: '',
        unitNumber: '',
        roomNumber: ''
      };
      this.currentPage = 1;
      this.fetchHouses();
    }
  },
  mounted() {
    this.fetchCommunities();

    // 前端添加 axios 拦截器
    axios.interceptors.response.use(
      response => response,
      error => {
        console.error('请求失败:', error);
        const message = error.response?.data?.error || '操作失败';
        ElMessage.error(message);
        return Promise.reject(error);
      }
    );
  }
}
</script>

<style scoped>
.house-management {
  display: flex;
  padding: 20px;
  height: calc(100vh - 84px);
  background-color: var(--el-bg-color);
}

.sidebar {
  width: 300px;
  transition: width 0.3s;
  margin-right: 20px;
}

.sidebar.collapsed {
  width: 0;
  margin-right: 0;
}

.content {
  flex: 1;
  overflow: auto;
  background-color: var(--el-bg-color);
}

.tree-card {
  height: 100%;
  overflow: auto;
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

.filter-row {
  margin-bottom: 20px;
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

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.7);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.loading-spinner {
  font-size: 32px;
  margin-bottom: 10px;
}

.loading-text {
  color: var(--el-text-color-secondary);
}

@media screen and (max-width: 768px) {
  .house-management {
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
