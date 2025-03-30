<template>
  <div class="account-settings">
    <el-card>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>个人信息中心</el-breadcrumb-item>
        <el-breadcrumb-item>账号设置</el-breadcrumb-item>
      </el-breadcrumb>

      <el-form :model="accountForm" label-width="120px">
        <el-form-item label="用户名">
          <el-input v-model="accountForm.username" disabled />
        </el-form-item>
        <el-form-item label="绑定安全手机">
          <el-input v-model="accountForm.phoneNumber" disabled>
            <template #append>
              <el-button @click="openReplacePhoneDialog">替换手机</el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="绑定安全邮箱">
          <el-input v-model="accountForm.email" disabled>
            <template #append>
              <el-button @click="openReplaceEmailDialog">替换邮箱</el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-button @click="openChangePasswordDialog">修改密码</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-dialog title="修改密码" v-model="changePasswordDialogVisible" width="30%">
      <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="100px">
        <el-form-item label="当前密码" prop="oldPassword">
          <el-input type="password" v-model="passwordForm.oldPassword" autocomplete="off"/>
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input type="password" v-model="passwordForm.newPassword" autocomplete="off"/>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input type="password" v-model="passwordForm.confirmPassword" autocomplete="off"/>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="changePasswordDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitChangePassword">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog title="替换手机号" v-model="replacePhoneDialogVisible" width="30%">
      <el-form :model="phoneForm" :rules="phoneRules" ref="phoneFormRef" label-width="100px">
        <el-form-item label="新手机号" prop="newPhone">
          <el-input v-model="phoneForm.newPhone" autocomplete="off"/>
        </el-form-item>
        <el-form-item label="验证码" prop="verifyCode">
          <el-input v-model="phoneForm.verifyCode" autocomplete="off">
            <template #append>
              <el-button @click="sendPhoneCode" :disabled="phoneCodeSending">
                {{ phoneCodeButtonText }}
              </el-button>
            </template>
          </el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="replacePhoneDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitReplacePhone">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog title="替换邮箱" v-model="replaceEmailDialogVisible" width="30%">
      <el-form :model="emailForm" :rules="emailRules" ref="emailFormRef" label-width="100px">
        <el-form-item label="新邮箱" prop="newEmail">
          <el-input v-model="emailForm.newEmail" autocomplete="off"/>
        </el-form-item>
        <el-form-item label="验证码" prop="verifyCode">
          <el-input v-model="emailForm.verifyCode" autocomplete="off">
            <template #append>
              <el-button @click="sendEmailCode" :disabled="emailCodeSending">
                {{ emailCodeButtonText }}
              </el-button>
            </template>
          </el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="replaceEmailDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitReplaceEmail">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AccountSettings',
  data() {
    return {
      accountForm: {
        username: '',
        phoneNumber: '',
        email: '',
      },
      changePasswordDialogVisible: false,
      passwordForm: {
        oldPassword: '',
        newPassword: '',
        confirmPassword: '',
      },
      passwordRules: {
        oldPassword: [
          {required: true, message: '请输入当前密码', trigger: 'blur'},
        ],
        newPassword: [
          {required: true, message: '请输入新密码', trigger: 'blur'},
          {min: 6, message: '密码长度至少为 6 个字符', trigger: 'blur'},
        ],
        confirmPassword: [
          {required: true, message: '请确认密码', trigger: 'blur'},
          {
            validator: (rule, value, callback) => {
              if (value !== this.passwordForm.newPassword) {
                callback(new Error('两次输入的密码不一致'));
              } else {
                callback();
              }
            },
            trigger: 'blur',
          },
        ],
      },
      passwordFormRef: null,
      replacePhoneDialogVisible: false,
      phoneForm: {
        newPhone: '',
        verifyCode: '',
      },
      phoneRules: {
        newPhone: [
          {required: true, message: '请输入新手机号', trigger: 'blur'},
          {pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur'},
        ],
        verifyCode: [
          {required: true, message: '请输入验证码', trigger: 'blur'},
          {len: 6, message: '验证码长度应为6位', trigger: 'blur'},
        ],
      },
      phoneCodeSending: false,
      phoneCodeButtonText: '发送验证码',
      phoneCodeTimer: null,
      replaceEmailDialogVisible: false,
      emailForm: {
        newEmail: '',
        verifyCode: '',
      },
      emailRules: {
        newEmail: [
          {required: true, message: '请输入新邮箱', trigger: 'blur'},
          {type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur'},
        ],
        verifyCode: [
          {required: true, message: '请输入验证码', trigger: 'blur'},
          {len: 6, message: '验证码长度应为6位', trigger: 'blur'},
        ],
      },
      emailCodeSending: false,
      emailCodeButtonText: '发送验证码',
      emailCodeTimer: null,
    };
  },
  methods: {
    async fetchAccountSettings() {
      try {
        const response = await axios.get('/api/personal-info');
        if (response.status === 200) {
          this.accountForm = {
            username: response.data.username || '',
            phoneNumber: response.data.phoneNumber || '',
            email: response.data.email || ''
          };
        }
      } catch (error) {
        console.error('获取账号设置信息失败:', error);
        this.$message.error('获取账号设置信息失败');
      }
    },
    openChangePasswordDialog() {
      this.passwordForm = {
        oldPassword: '',
        newPassword: '',
        confirmPassword: '',
      };
      this.changePasswordDialogVisible = true;
    },
    openReplacePhoneDialog() {
      this.phoneForm = {
        newPhone: '',
        verifyCode: '',
      };
      this.replacePhoneDialogVisible = true;
    },
    openReplaceEmailDialog() {
      this.emailForm = {
        newEmail: '',
        verifyCode: '',
      };
      this.replaceEmailDialogVisible = true;
    },
    async submitChangePassword() {
      this.$refs.passwordFormRef.validate(async (valid) => {
        if (valid) {
          try {
            await axios.put('/api/personal-info/password', {
              oldPassword: this.passwordForm.oldPassword,
              newPassword: this.passwordForm.newPassword
            });
            this.$message.success('密码修改成功，请重新登录');
            this.changePasswordDialogVisible = false;
            
            // 跳转到登录页面
            setTimeout(() => {
              this.$router.push('/login');
            }, 1500);
          } catch (error) {
            console.error('修改密码失败:', error);
            this.$message.error(error.response?.data?.error || '修改密码失败');
          }
        } else {
          return false;
        }
      });
    },
    async sendPhoneCode() {
      // 先验证手机号
      this.$refs.phoneFormRef.validateField('newPhone', async (errorMsg) => {
        if (!errorMsg) {
          try {
            this.phoneCodeSending = true;
            // 发送验证码
            await axios.post('/api/send-phone-code', {
              phone: this.phoneForm.newPhone
            });
            this.$message.success('验证码已发送');
            
            // 倒计时
            let countdown = 60;
            this.phoneCodeButtonText = `重新发送(${countdown}s)`;
            this.phoneCodeTimer = setInterval(() => {
              countdown--;
              if (countdown <= 0) {
                clearInterval(this.phoneCodeTimer);
                this.phoneCodeButtonText = '发送验证码';
                this.phoneCodeSending = false;
              } else {
                this.phoneCodeButtonText = `重新发送(${countdown}s)`;
              }
            }, 1000);
          } catch (error) {
            console.error('发送验证码失败:', error);
            this.$message.error(error.response?.data?.error || '发送验证码失败');
            this.phoneCodeSending = false;
          }
        }
      });
    },
    async submitReplacePhone() {
      this.$refs.phoneFormRef.validate(async (valid) => {
        if (valid) {
          try {
            await axios.put('/api/update-phone', this.phoneForm);
            this.$message.success('手机号更新成功');
            this.replacePhoneDialogVisible = false;
            this.fetchAccountSettings();
          } catch (error) {
            console.error('更新手机号失败:', error);
            this.$message.error(error.response?.data?.error || '更新手机号失败');
          }
        } else {
          return false;
        }
      });
    },
    async sendEmailCode() {
      // 先验证邮箱
      this.$refs.emailFormRef.validateField('newEmail', async (errorMsg) => {
        if (!errorMsg) {
          try {
            this.emailCodeSending = true;
            // 发送验证码
            await axios.post('/api/send-email-code', {
              email: this.emailForm.newEmail
            });
            this.$message.success('验证码已发送');
            
            // 倒计时
            let countdown = 60;
            this.emailCodeButtonText = `重新发送(${countdown}s)`;
            this.emailCodeTimer = setInterval(() => {
              countdown--;
              if (countdown <= 0) {
                clearInterval(this.emailCodeTimer);
                this.emailCodeButtonText = '发送验证码';
                this.emailCodeSending = false;
              } else {
                this.emailCodeButtonText = `重新发送(${countdown}s)`;
              }
            }, 1000);
          } catch (error) {
            console.error('发送验证码失败:', error);
            this.$message.error(error.response?.data?.error || '发送验证码失败');
            this.emailCodeSending = false;
          }
        }
      });
    },
    async submitReplaceEmail() {
      this.$refs.emailFormRef.validate(async (valid) => {
        if (valid) {
          try {
            await axios.put('/api/update-email', this.emailForm);
            this.$message.success('邮箱更新成功');
            this.replaceEmailDialogVisible = false;
            this.fetchAccountSettings();
          } catch (error) {
            console.error('更新邮箱失败:', error);
            this.$message.error(error.response?.data?.error || '更新邮箱失败');
          }
        } else {
          return false;
        }
      });
    },
  },
  mounted() {
    this.fetchAccountSettings();
  },
  beforeUnmount() {
    // 清除倒计时
    if (this.phoneCodeTimer) {
      clearInterval(this.phoneCodeTimer);
    }
    if (this.emailCodeTimer) {
      clearInterval(this.emailCodeTimer);
    }
  }
};
</script>

<style scoped>
.account-settings {
  padding: 20px;
}
</style>
