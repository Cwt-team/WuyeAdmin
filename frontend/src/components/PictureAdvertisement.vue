<template>
  <div class="picture-advertisement-list">
    <el-card>
      <p>提示：请上传分辨率为1920*1080的图片，大小不要超过2M，图片将自动循环展示。</p>
      <el-row class="filter-row">
        <el-col :span="4">
          <el-input v-model="filter.title" placeholder="广告标题" class="filter-item" />
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="searchAdvertisements">查询</el-button>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="6" v-for="(advertisement, index) in advertisementList" :key="index">
          <el-card :body-style="{ padding: '0px' }">
            <img :src="advertisement.imageUrl" class="image" />
            <div style="padding: 14px;">
              <span>{{ advertisement.title }}</span>
              <div class="bottom clearfix">
                <el-button type="text" class="button" @click="editAdvertisement(advertisement)">编辑</el-button>
                <el-button type="text" class="button" @click="deleteAdvertisement(advertisement)">删除</el-button>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

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
</template>

<script>
import axios from 'axios';

export default {
  name: 'PictureAdvertisement',
  data() {
    return {
      filter: {
        title: '',
      },
      advertisementList: [
        {
          title: '广告1',
          imageUrl: 'https://via.placeholder.com/1920x1080',
        },
        {
          title: '广告2',
          imageUrl: 'https://via.placeholder.com/1920x1080',
        },
      ],
      total: 2,
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
            page: this.currentPage,
            size: this.pageSize,
          },
        });
        this.advertisementList = response.data.advertisements;
        this.total = response.data.total;
      } catch (error) {
        console.error('获取广告信息失败:', error);
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
    editAdvertisement(advertisement) {
      console.log('编辑广告:', advertisement);
    },
    deleteAdvertisement(advertisement) {
      console.log('删除广告:', advertisement);
    },
  },
  mounted() {
    this.fetchAdvertisements();
  },
};
</script>

<style scoped>
.image {
  width: 100%;
}
.filter-row {
  margin-bottom: 20px;
}
.filter-item {
  margin-right: 10px;
}
.button {
  float: right;
  padding: 0;
}
.bottom {
  margin-top: 10px;
  text-align: right;
}
.el-card {
  margin-bottom: 20px;
}
</style>
