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
      <el-form :model="addDialog.form" label-width="100px" ref="addFormRef">
        <el-form-item label="名称" prop="fullName" required>
          <el-input v-model="addDialog.form.fullName" placeholder="请输入房屋名称"></el-input>
        </el-form-item>
        
        <el-form-item v-if="addDialog.form.level === 1" label="区号" prop="districtNumber">
          <el-input v-model="addDialog.form.districtNumber" placeholder="请输入区号"></el-input>
        </el-form-item>
        
        <el-form-item v-if="addDialog.form.level === 2" label="楼栋号" prop="buildingNumber">
          <el-input v-model="addDialog.form.buildingNumber" placeholder="请输入楼栋号"></el-input>
        </el-form-item>
        
        <el-form-item v-if="addDialog.form.level === 3" label="单元号" prop="unitNumber">
          <el-input v-model="addDialog.form.unitNumber" placeholder="请输入单元号"></el-input>
        </el-form-item>
        
        <el-form-item v-if="addDialog.form.level === 4" label="房间号" prop="roomNumber">
          <el-input v-model="addDialog.form.roomNumber" placeholder="请输入房间号"></el-input>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="addDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="submitAddHouse">确定</el-button>
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
      
      this.addDialog.visible = true;
    },
    
    // 提交添加房屋表单
    async submitAddHouse() {
      if (!this.addDialog.form.fullName) {
        this.$message.warning('房屋名称不能为空');
        return;
      }
      
      try {
        const response = await axios.post('/api/houses', this.addDialog.form);
        
        if (response.data.success) {
          this.$message.success('添加成功');
          this.addDialog.visible = false;
          await this.fetchHouseTree();
          await this.fetchHouses();
        } else {
          throw new Error(response.data.error || '添加失败');
        }
      } catch (error) {
        console.error('添加房屋失败:', error);
        this.$message.error('添加失败: ' + (error.message || '未知错误'));
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
      if (!this.editDialog.form.fullName) {
        this.$message.warning('房屋名称不能为空');
        return;
      }
      
      try {
        const formData = {
          fullName: this.editDialog.form.fullName,
          level: this.editDialog.form.level,
          parentId: this.editDialog.form.parentId
        };
        
        // 根据房屋级别添加相应字段
        if (this.editDialog.form.level === 1) {
          formData.districtNumber = this.editDialog.form.districtNumber;
        } else if (this.editDialog.form.level === 2) {
          formData.buildingNumber = this.editDialog.form.buildingNumber;
        } else if (this.editDialog.form.level === 3) {
          formData.unitNumber = this.editDialog.form.unitNumber;
        } else if (this.editDialog.form.level === 4 && this.editDialog.form.roomNumber) {
          // 更新房屋全名中的房间号部分
          const nameParts = this.editDialog.form.fullName.split('室');
          if (nameParts.length > 0) {
            const prefix = this.editDialog.form.fullName.substring(0, this.editDialog.form.fullName.lastIndexOf('单元') + 2);
            this.editDialog.form.fullName = prefix + this.editDialog.form.roomNumber + '室';
          }
        }
        
        console.log('提交的表单数据:', this.editDialog.form);
        console.log('发送到后端的数据:', formData);
        
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
          type: 'warning'
        })
        
        const response = await axios.delete(`/api/houses/${row.id}`)
        if (response.data.success) {
          this.$message.success('删除成功')
          this.fetchHouses()
          this.fetchHouseTree()
        } else {
          throw new Error(response.data.error || '删除失败')
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除房屋失败:', error)
          this.$message.error('删除失败: ' + (error.message || '未知错误'))
        }
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
