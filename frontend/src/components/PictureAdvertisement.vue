<template>
  <div class="picture-advertisement-list">
    <el-card>
      <el-alert
        title="提示：图片分辨率横屏不大于1280*800，竖屏不大于800*1280，如果图片变形需要自己调节一下。"
        type="info"
        :closable="false"
        style="margin-bottom: 15px;"
      />
      <el-row class="filter-row" :gutter="20">
        <el-col :span="6">
          <el-input v-model="filter.title" placeholder="广告标题" class="filter-item" />
        </el-col>
        <el-col :span="6">
          <el-select v-model="filter.orientation" placeholder="屏幕方向" clearable class="filter-item">
            <el-option label="横向" value="horizontal" />
            <el-option label="竖向" value="vertical" />
          </el-select>
        </el-col>
        <el-col :span="2">
          <el-button type="primary" :loading="loading" @click="searchAdvertisements">查询</el-button>
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

      <div class="pagination-container">
        <el-pagination
          background
          layout="total, prev, pager, next, sizes"
          :total="total"
          :current-page="currentPage"
          :page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          @current-change="handlePageChange"
          @size-change="handleSizeChange"
        />
      </div>
    </el-card>

    <!-- 图片上传对话框 -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="500px"
    >
      <el-form :model="uploadForm" label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="uploadForm.title" />
        </el-form-item>
        <el-form-item label="图片">
          <el-upload
            class="advertisement-uploader"
            :action="uploadUrl"
            :show-file-list="false"
            :on-success="handleUploadSuccess"
            :before-upload="beforeUpload"
          >
            <img v-if="uploadForm.imageUrl" :src="uploadForm.imageUrl" class="preview-image">
            <el-icon v-else class="uploader-icon"><plus /></el-icon>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitUpload">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import { Plus } from '@element-plus/icons-vue'

export default {
  name: 'PictureAdvertisement',
  components: {
    Plus
  },
  data() {
    return {
      loading: false,
      filter: {
        title: '',
        orientation: ''
      },
      advertisementList: [],
      total: 0,
      currentPage: 1,
      pageSize: 10,
      dialogVisible: false,
      dialogTitle: '',
      uploadForm: {
        title: '',
        imageUrl: '',
        orientation: 'horizontal'
      },
      uploadUrl: '/api/upload',
      currentId: null,
      // 示例数据
      mockData: [
        {
          id: 1,
          title: '横屏广告1',
          imageUrl: 'https://via.placeholder.com/1280x800',
          orientation: 'horizontal'
        },
        {
          id: 2,
          title: '竖屏广告1',
          imageUrl: 'https://via.placeholder.com/800x1280',
          orientation: 'vertical'
        }
      ]
    }
  },
  methods: {
    async fetchAdvertisements() {
      this.loading = true
      try {
        const response = await axios.get('/api/advertisements', {
          params: {
            title: this.filter.title,
            orientation: this.filter.orientation,
            page: this.currentPage,
            size: this.pageSize
          }
        })
        this.advertisementList = response.data.records
        this.total = response.data.total
        this.$message.success('获取数据成功')
      } catch (error) {
        console.error('获取广告列表失败:', error)
        this.$message.warning('获取数据库失败，已展示示例数据')
        this.advertisementList = this.mockData
        this.total = this.mockData.length
      } finally {
        this.loading = false
      }
    },
    searchAdvertisements() {
      this.currentPage = 1
      this.fetchAdvertisements()
    },
    handlePageChange(page) {
      this.currentPage = page
      this.fetchAdvertisements()
    },
    handleSizeChange(size) {
      this.pageSize = size
      this.fetchAdvertisements()
    },
    replaceAdvertisement(advertisement) {
      console.log('替换广告:', advertisement)
      // TODO: 实现图片替换的逻辑
    },
    editAdvertisement(advertisement) {
      console.log('编辑广告:', advertisement)
      // TODO: 实现编辑广告的逻辑
    },
    deleteAdvertisement(advertisement) {
      console.log('删除广告:', advertisement)
      // TODO: 实现删除广告的逻辑
    },
    handleUploadSuccess(res, file) {
      this.uploadForm.imageUrl = URL.createObjectURL(file.raw)
    },
    beforeUpload(file) {
      const isLt2M = file.size / 1024 / 1024 < 2
      if (!isLt2M) {
        this.$message.error('上传图片大小不能超过 2MB!')
      }
      return isLt2M
    },
    submitUpload() {
      // TODO: 实现图片上传的逻辑
    }
  },
  mounted() {
    this.fetchAdvertisements()
  }
}
</script>

<style scoped>
.picture-advertisement-list {
  padding: 20px;
}

.filter-row {
  margin-bottom: 20px;
}

.filter-item {
  width: 100%;
}

.advertisement-item {
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
}

.advertisement-item .image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  display: block;
}

.advertisement-item .actions {
  padding: 10px;
  text-align: center;
}

.advertisement-item .title {
  padding: 10px;
  text-align: center;
  color: #666;
}

.advertisement-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.advertisement-uploader:hover {
  border-color: #409EFF;
}

.preview-image {
  width: 200px;
  height: 200px;
  display: block;
}

.uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 200px;
  height: 200px;
  line-height: 200px;
  text-align: center;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style>
