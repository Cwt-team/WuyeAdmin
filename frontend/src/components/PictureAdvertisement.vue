<template>
  <div class="picture-advertisement-list">
    <el-card>
      <el-alert
        title="提示：请上传分辨率为1920*1080的图片，大小不要超过2M，图片将自动循环展示。"
        type="info"
        :closable="false"
        style="margin-bottom: 15px;"
      />
      <el-row class="filter-row">
        <el-col :span="4">
          <el-input v-model="filter.title" placeholder="广告标题" class="filter-item" />
        </el-col>
        <el-col :span="4">
          <el-select v-model="filter.orientation" placeholder="屏幕方向" clearable class="filter-item">
            <el-option label="横向" value="horizontal"></el-option>
            <el-option label="竖向" value="vertical"></el-option>
          </el-select>
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="searchAdvertisements">查询</el-button>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="6" v-for="(advertisement, index) in advertisementList" :key="index">
          <div class="advertisement-item">
            <img :src="advertisement.imageUrl" class="image" />
            <div class="actions">
              <el-button type="primary" size="small" @click="replaceAdvertisement(advertisement)">替换</el-button>
              <el-button type="text" size="small" @click="editAdvertisement(advertisement)">编辑</el-button>
              <el-button type="danger" size="small" @click="deleteAdvertisement(advertisement)">删除</el-button>
            </div>
            <div class="title">{{ advertisement.title }}</div>
          </div>
        </el-col>
      </el-row>

      <el-pagination
        background
        layout="prev, pager, next"
        :total="advertisementList === mockAdvertisementList ? mockTotal : total"
        :current-page="currentPage"
        :page-size="pageSize"
        @current-change="handlePageChange"
      />
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'PictureAdvertisement',
  data() {
    return {
      filter: {
        title: '',
        orientation: '',
      },
      advertisementList: [],
      mockAdvertisementList: [
        {
          title: '示例广告1',
          imageUrl: 'https://via.placeholder.com/1920x1080/cccccc/ffffff?text=Mock+Ad+1',
        },
        {
          title: '示例广告2',
          imageUrl: 'https://via.placeholder.com/1920x1080/aaaaaa/ffffff?text=Mock+Ad+2',
        },
        {
          title: '示例广告3',
          imageUrl: 'https://via.placeholder.com/1920x1080/888888/ffffff?text=Mock+Ad+3',
        },
      ],
      total: 0,
      mockTotal: 3,
      currentPage: 1,
      pageSize: 10,
    };
  },
  methods: {
    async fetchAdvertisements() {
      try {
        const response = await axios.get('/api/advertisements', {
          params: {
            title: this.filter.title,
            orientation: this.filter.orientation,
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        if (response.status === 200) {
          this.advertisementList = response.data.advertisements;
          this.total = response.data.total;
        } else {
          this.$message.error(`获取广告数据失败，状态码: ${response.status}`);
          this.showMockData();
        }
      } catch (error) {
        console.error('获取广告信息失败:', error);
        this.$message.error('获取广告数据失败，已显示示例数据。');
        this.showMockData();
      }
    },
    searchAdvertisements() {
      this.currentPage = 1;
      this.fetchAdvertisements();
    },
    handlePageChange(page) {
      this.currentPage = page;
      this.fetchAdvertisements();
    },
    replaceAdvertisement(advertisement) {
      console.log('替换广告:', advertisement);
      // TODO: 实现图片替换的逻辑
    },
    editAdvertisement(advertisement) {
      console.log('编辑广告:', advertisement);
      // TODO: 实现编辑广告的逻辑
    },
    deleteAdvertisement(advertisement) {
      console.log('删除广告:', advertisement);
      // TODO: 实现删除广告的逻辑
    },
    showMockData() {
      this.advertisementList = this.mockAdvertisementList;
      this.total = this.mockTotal;
    },
  },
  mounted() {
    this.fetchAdvertisements();
  },
};
</script>

<style scoped>
/* ... 之前的 CSS 样式 */
.filter-row {
  margin-bottom: 20px;
}

.filter-item {
  margin-right: 10px;
}

.advertisement-item {
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
}

.advertisement-item .image {
  width: 100%;
  display: block;
}

.advertisement-item .actions {
  padding: 10px;
  text-align: center;
}

.advertisement-item .actions .el-button {
  margin: 0 5px;
}

.advertisement-item .title {
  padding: 0 10px 10px;
  text-align: center;
  font-size: 12px;
  color: #999;
}
</style>
