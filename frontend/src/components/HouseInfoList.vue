<template>
  <div class="house-management">
    <!-- Left Sidebar -->
    <div class="sidebar">
      <el-card class="tree-card">
        <div class="tree-header">区域总览</div>
        <el-tree
          :data="areaData"
          :props="defaultProps"
          @node-click="handleNodeClick"
          :highlight-current="true"
          node-key="id"
          ref="tree"
        >
          <template #default="{ node, data }">
            <span class="custom-tree-node">
              <span>{{ node.label }}</span>
              <span class="count">({{ data.count || 0 }})</span>
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
          <el-col :span="6">
            <el-input
              v-model="search.keyword"
              placeholder="请输入关键字"
              clearable
            />
          </el-col>
          <el-col :span="12">
            <el-button type="primary" @click="searchHouses">查询</el-button>
            <el-button type="success" @click="addHouse">添加房屋</el-button>
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
                @click="editHouse(scope.row)"
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
        parentId: null
      },
      loading: false,
      houseList: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      areaData: [],
      defaultProps: {
        children: 'children',
        label: 'fullName'
      },
      // 模拟数据
      mockData: [
        {
          id: 1,
          fullName: '阳光花园1区1栋1单元',
          districtNumber: '1',
          buildingNumber: '1',
          unitNumber: '1',
          createTime: '2024-02-08 10:00:00'
        },
        {
          id: 2,
          fullName: '阳光花园1区1栋2单元',
          districtNumber: '1',
          buildingNumber: '1',
          unitNumber: '2',
          createTime: '2024-02-08 10:30:00'
        }
      ],
      mockAreaData: [
        {
          id: 1,
          fullName: '1区',
          count: 2,
          children: [
            {
              id: 2,
              fullName: '1栋',
              count: 2,
              children: [
                {
                  id: 3,
                  fullName: '1单元',
                  count: 0
                }
              ]
            }
          ]
        }
      ],
      isSidebarCollapsed: false
    }
  },
  methods: {
    async fetchHouses() {
      this.loading = true
      try {
        const response = await axios.get('/api/houses', {
          params: {
            keyword: this.search.keyword,
            communityId: this.search.communityId,
            parentId: this.search.parentId,
            page: this.currentPage,
            size: this.pageSize
          }
        })
        
        if (response.data.success) {
          this.houseList = response.data.data
          this.total = response.data.data.length
          this.$message.success('数据加载成功')
        } else {
          throw new Error('获取数据失败')
        }
      } catch (error) {
        console.error('获取房屋列表失败:', error)
        this.$message.warning('获取数据失败，显示模拟数据')
        this.houseList = this.mockData
        this.total = this.mockData.length
      } finally {
        this.loading = false
      }
    },

    async fetchAreaTree() {
      try {
        const response = await axios.get('/api/houses', {
          params: {
            communityId: this.search.communityId
          }
        })
        
        if (response.data.success) {
          this.areaData = this.buildTree(response.data.data)
        } else {
          throw new Error('获取区域树失败')
        }
      } catch (error) {
        console.error('获取区域树失败:', error)
        this.$message.warning('获取区域树失败，显示模拟数据')
        this.areaData = this.mockAreaData
      }
    },

    buildTree(data) {
      // 构建树形结构
      const map = {}
      const result = []

      // 首先创建所有节点的映射
      data.forEach(item => {
        map[item.id] = {
          ...item,
          children: []
        }
      })

      // 构建树形结构
      data.forEach(item => {
        const node = map[item.id]
        if (item.parentId) {
          const parent = map[item.parentId]
          if (parent) {
            parent.children.push(node)
          }
        } else {
          result.push(node)
        }
      })

      return result
    },

    handleNodeClick(data) {
      this.search.parentId = data.id
      this.fetchHouses()
    },

    searchHouses() {
      this.currentPage = 1
      this.fetchHouses()
    },

    async addHouse() {
      // 添加房屋的逻辑
    },

    async editHouse() {
      // 编辑房屋的逻辑
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
          this.fetchAreaTree()
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除房屋失败:', error)
          this.$message.error('删除失败')
        }
      }
    },

    handlePageChange(page) {
      this.currentPage = page
      this.fetchHouses()
    },

    toggleSidebar() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed
    }
  },
  mounted() {
    this.fetchHouses()
    this.fetchAreaTree()
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
  margin-bottom: 15px;
  font-weight: bold;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.custom-tree-node {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.count {
  color: #999;
  font-size: 12px;
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

/* 添加响应式布局 */
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
