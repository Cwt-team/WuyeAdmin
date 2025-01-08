 <template>
  <div class="house-info-list">
    <div v-if="loading" class="loading-overlay">
      <i class="el-icon-loading loading-spinner"></i>
      <span class="loading-text">加载中...</span>
    </div>
    <el-card>
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input v-model="searchParams.community" placeholder="小区名称" class="filter-item" />
        </el-col>
        <el-col :span="6">
          <el-input v-model="searchParams.building" placeholder="楼栋号" class="filter-item" />
        </el-col>
        <el-col :span="6">
          <el-input v-model="searchParams.houseNumber" placeholder="房屋编号" class="filter-item" />
        </el-col>
        <el-col :span="6">
          <el-button type="primary" @click="searchHouse">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-col>
      </el-row>
      <el-table 
        :data="houseList" 
        style="width: 100%" 
        class="house-table"
        v-loading="loading"
        @selection-change="handleSelectionChange"
        :empty-text="emptyText"
        :row-class-name="tableRowClassName"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="community" label="小区" width="120" />
        <el-table-column prop="building" label="楼栋" width="100" />
        <el-table-column prop="houseNumber" label="房屋编号" width="120" />
        <el-table-column prop="level" label="房产层级" width="100" />
        <el-table-column prop="layout" label="户型" width="120" />
        <el-table-column prop="owner" label="业主" width="120" />
        <el-table-column prop="area" label="面积" width="100" />
        <el-table-column prop="createTime" label="创建时间" width="180" :formatter="formatDate" />
        <el-table-column prop="status" label="状态" width="100" :formatter="formatStatus" />
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button type="text" size="small" @click="viewDetails(scope.row)">查看详情</el-button>
            <el-button type="text" size="small" @click="addTenant(scope.row)">添加租户</el-button>
            <el-button type="text" size="small" @click="deleteHouse(scope.row)" style="color: #f56c6c">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="batch-actions">
        <el-button 
          type="danger" 
          :disabled="selectedHouses.length === 0 || batchLoading"
          :loading="batchLoading"
          @click="batchDelete"
        >
          批量删除 ({{ selectedHouses.length }})
        </el-button>
      </div>
      <el-pagination
        background
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        :current-page="currentPage"
        :page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        @current-change="handlePageChange"
        @size-change="handleSizeChange"
        class="custom-pagination"
      >
        <template #default>
          <span class="pagination-total">共 {{ total }} 条</span>
        </template>
      </el-pagination>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';
import moment from 'moment';

export default {
  name: 'HouseInfoList',
  data() {
    return {
      loading: false,
      batchLoading: false,
      emptyText: '暂无数据',
      searchParams: {
        community: '',
        building: '',
        houseNumber: ''
      },
      houseList: [],
      selectedHouses: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
    };
  },
  methods: {
    async fetchHouses() {
      this.loading = true;
      try {
        const response = await axios.get('/api/houses', {
          params: {
            ...this.searchParams,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        this.houseList = response.data.houses;
        this.total = response.data.total;
        this.$message.success('数据加载成功');
      } catch (error) {
        console.error('获取房屋信息失败:', error);
        this.$message.error('获取房屋信息失败');
        // 添加模拟数据
        this.houseList = [
          {
            id: 1,
            community: '阳光花园',
            building: '1栋',
            houseNumber: '101',
            level: '1层',
            layout: '三室一厅',
            owner: '张三',
            area: 120,
            createTime: '2023-01-01 10:00:00',
            status: 'occupied'
          },
          {
            id: 2,
            community: '幸福家园',
            building: '2栋',
            houseNumber: '202',
            level: '2层',
            layout: '两室一厅',
            owner: '李四',
            area: 90,
            createTime: '2023-02-01 14:00:00',
            status: 'vacant'
          },
          {
            id: 3,
            community: '和谐小区',
            building: '3栋',
            houseNumber: '303',
            level: '3层',
            layout: '四室两厅',
            owner: '王五',
            area: 150,
            createTime: '2023-03-01 09:00:00',
            status: 'occupied'
          },
          {
            id: 4,
            community: '平安小区',
            building: '4栋',
            houseNumber: '404',
            level: '4层',
            layout: '一室一厅',
            owner: '赵六',
            area: 60,
            createTime: '2023-04-01 16:00:00',
            status: 'vacant'
          }
        ];
        this.total = this.houseList.length;
        this.$message.success('已加载模拟数据');
      } finally {
        this.loading = false;
      }
    },
    resetSearch() {
      this.searchParams = {
        community: '',
        building: '',
        houseNumber: ''
      };
      this.currentPage = 1;
      this.fetchHouses();
    },
    handleSelectionChange(selection) {
      this.selectedHouses = selection;
    },
    async batchDelete() {
      try {
        await this.$confirm('确定要删除选中的房屋信息吗？', '提示', {
          type: 'warning'
        });
        this.batchLoading = true;
        const houseIds = this.selectedHouses.map(house => house.id);
        await axios.delete('/api/houses', { data: { ids: houseIds } });
        this.$message.success('删除成功');
        this.selectedHouses = [];
        await this.fetchHouses();
      } catch (error) {
        if (error !== 'cancel') {
          this.$message.error('删除失败');
        }
      } finally {
        this.batchLoading = false;
      }
    },
    async deleteHouse(house) {
      try {
        await this.$confirm('确定要删除该房屋信息吗？', '提示', {
          type: 'warning'
        });
        this.loading = true;
        await axios.delete(`/api/houses/${house.id}`);
        this.$message.success('删除成功');
        await this.fetchHouses();
      } catch (error) {
        if (error !== 'cancel') {
          this.$message.error('删除失败');
        }
      } finally {
        this.loading = false;
      }
    },
    async addTenant(house) {
      try {
        const { value } = await this.$prompt('请输入租户姓名', '添加租户', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputPattern: /^.{2,20}$/,
          inputErrorMessage: '姓名长度应在2-20个字符之间'
        });
        
        this.loading = true;
        await axios.post(`/api/houses/${house.id}/tenants`, {
          name: value
        });
        
        this.$notify({
          title: '成功',
          message: `已成功添加租户 ${value}`,
          type: 'success',
          duration: 2000
        });
        
        await this.fetchHouses();
      } catch (error) {
        if (error !== 'cancel') {
          this.$notify.error({
            title: '错误',
            message: '添加租户失败，请稍后重试',
            duration: 2000
          });
        }
      } finally {
        this.loading = false;
      }
    },
    formatDate(row, column, cellValue) {
      return cellValue ? moment(cellValue).format('YYYY-MM-DD HH:mm') : '';
    },
    searchHouse() {
      this.currentPage = 1;
      this.fetchHouses();
    },
    async handlePageChange(page) {
      this.currentPage = page;
      this.fetchHouses();
    },
    formatStatus(row, column, cellValue) {
      return cellValue === 'occupied' ? '已入住' : '未入住';
    },
    viewDetails(row) {
      this.$router.push({
        name: 'HouseDetail',
        params: { id: row.id }
      });
    },
    
    tableRowClassName({ row }) {
      return row.status === 'occupied' ? 'occupied-row' : '';
    },
  },
  mounted() {
    this.fetchHouses();
  },
};
</script>

<style scoped>
.house-info-list {
  height: 100%;
  padding: 20px;
}

.el-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.filter-item {
  margin-right: 10px;
  width: 100%;
}

.house-table {
  flex: 1;
  margin-top: 16px;
}

.batch-actions {
  margin: 16px 0;
  padding: 12px;
  background-color: #f5f7fa;
  border-radius: 4px;
  text-align: right;
}

.el-table {
  font-size: 13px;
}

.el-table .cell {
  padding: 6px 0;
}

.el-table .el-table__row {
  height: 40px;
}

.el-table .el-table__row:hover {
  background-color: #f5f7fa;
}

.el-table--striped .el-table__body tr.el-table__row--striped td {
  background-color: #fafafa;
}

.no-data {
  padding: 40px 0;
  text-align: center;
  color: #909399;
}

.no-data-icon {
  font-size: 40px;
  margin-bottom: 16px;
}

.custom-pagination {
  margin-top: 16px;
  padding: 16px 0;
  text-align: right;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 16px;
}

.pagination-total {
  font-size: 14px;
  color: #606266;
  margin-right: 16px;
}

.custom-pagination .el-pagination__total {
  margin-right: auto;
}

.custom-pagination .el-pagination__sizes {
  margin: 0 16px;
}

.custom-pagination .el-pagination__jump {
  margin-left: 16px;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.loading-spinner {
  font-size: 40px;
  color: #409EFF;
  margin-bottom: 16px;
  animation: spin 1s linear infinite;
}

.loading-text {
  font-size: 16px;
  color: #606266;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.el-button--text {
  padding: 0 4px;
  margin-right: 8px;
}

.el-button--danger {
  margin-left: 8px;
}

.occupied-row {
  background-color: #f0f9eb;
}

.occupied-row:hover {
  background-color: #e1f3d8 !important;
}
</style>
