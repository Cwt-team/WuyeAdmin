<template>
  <el-dialog
    :title="isEdit ? '编辑物业管理员' : '添加物业管理员'"
    :model-value="visible"
    @update:model-value="$emit('update:visible', $event)"
    width="50%"
  >
    <el-form
      ref="form"
      :model="localFormData"
      label-width="120px"
      label-position="right"
    >
      <el-form-item label="姓名" prop="name">
        <el-input v-model="localFormData.name" />
      </el-form-item>
      <el-form-item label="手机号" prop="phone">
        <el-input v-model="localFormData.phone" />
      </el-form-item>
      <el-form-item label="角色" prop="role">
        <el-select v-model="localFormData.role" placeholder="请选择角色">
          <el-option label="物业管理员" value="物业管理员" />
          <el-option label="超级管理员" value="超级管理员" />
        </el-select>
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-radio-group v-model="localFormData.status">
          <el-radio label="active">活跃</el-radio>
          <el-radio label="inactive">非活跃</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="备注" prop="remark">
        <el-input
          v-model="localFormData.remark"
          type="textarea"
          :rows="3"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="$emit('close')">取消</el-button>
      <el-button type="primary" @click="handleSubmit">确定</el-button>
    </template>
  </el-dialog>
</template>

<script>
export default {
  name: 'PropertyAdminForm',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    formData: {
      type: Object,
      default: () => ({
        name: '',
        phone: '',
        role: '',
        status: 'active',
        remark: ''
      })
    },
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      localFormData: { ...this.formData }
    };
  },
  watch: {
    formData: {
      handler(newVal) {
        this.localFormData = { ...newVal };
      },
      deep: true
    }
  },
  methods: {
    handleSubmit() {
      this.$emit('submit', { ...this.localFormData });
      this.$emit('close');
    }
  }
};
</script>

<style scoped>
.el-form {
  padding: 20px;
}
</style>
