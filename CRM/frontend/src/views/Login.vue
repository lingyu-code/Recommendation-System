<template>
  <div class="login-container">
    <div class="login-form">
      <h2>金融智能推荐系统</h2>
      <el-form :model="loginForm" :rules="rules" ref="loginFormRef" class="demo-loginForm">
        <el-form-item prop="username">
          <el-input v-model="loginForm.username" placeholder="用户名" size="large">
            <template #prefix>
              <el-icon>
                <User />
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="密码" size="large" show-password>
            <template #prefix>
              <el-icon>
                <Lock />
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" style="width: 100%;" size="large" @click="handleLogin" :loading="loading">
            登录
          </el-button>
        </el-form-item>
      </el-form>

      <div class="register-link">
        <span>没有账号？</span>
        <el-link type="primary" @click="$router.push('/register')">立即注册</el-link>
      </div>
    </div>
  </div>
</template>

<script>
import { User, Lock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { mapActions } from 'vuex'
import { apiService } from '@/api'

export default {
  name: 'Login',
  components: {
    User,
    Lock
  },
  data() {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      },
      loading: false
    }
  },
  methods: {
    ...mapActions(['login']),
    async handleLogin() {
      this.$refs.loginFormRef.validate(async (valid) => {
        if (valid) {
          this.loading = true
          try {
            // 调用JWT登录API
            const response = await apiService.login(this.loginForm)

            // JWT返回access和refresh tokens
            const { access, refresh } = response

            // 存储tokens到localStorage
            localStorage.setItem('access_token', access)
            localStorage.setItem('refresh_token', refresh)

            // 获取用户信息
            const profileResponse = await apiService.getProfile()
            if (profileResponse.success) {
              const user = profileResponse.user

              // 使用Vuex store存储用户信息
              this.login({
                id: user.id,
                username: user.username,
                name: user.first_name && user.last_name ? `${user.last_name}${user.first_name}` : user.username,
                email: user.email,
                phone: user.phone,
                age: user.age,
                risk_tolerance: user.risk_tolerance,
                total_assets: user.total_assets,
                investment_goal: user.investment_goal
              })

              // 存储用户信息到localStorage（用于持久化）
              localStorage.setItem('isLoggedIn', 'true')
              localStorage.setItem('userId', user.id.toString())
              localStorage.setItem('userName', user.username)
              localStorage.setItem('userRisk', user.risk_tolerance)

              ElMessage.success('登录成功！')

              // 跳转到仪表盘
              this.$router.push('/dashboard')
            } else {
              ElMessage.error('获取用户信息失败')
            }
          } catch (error) {
            console.error('Login error:', error)
            if (error.response && error.response.data) {
              // JWT返回的错误格式
              if (error.response.data.detail) {
                ElMessage.error(error.response.data.detail)
              } else {
                ElMessage.error('用户名或密码错误')
              }
            } else {
              ElMessage.error('登录失败，请稍后重试')
            }
          } finally {
            this.loading = false
          }
        }
      })
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-form {
  background: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  width: 400px;
}

.login-form h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.demo-accounts {
  margin-top: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 5px;
  border-left: 4px solid #409EFF;
}

.demo-accounts h4 {
  margin: 0 0 10px 0;
  color: #333;
}

.demo-accounts p {
  margin: 5px 0;
  font-size: 12px;
  color: #666;
}

.register-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
}

.register-link .el-link {
  margin-left: 5px;
}
</style>
