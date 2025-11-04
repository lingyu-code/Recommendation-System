<template>
  <div class="login-container">
    <div class="login-form">
      <h2>金融智能推荐系统</h2>
      <el-form :model="loginForm" :rules="rules" ref="loginFormRef" class="demo-loginForm">
        <el-form-item prop="username">
          <el-input v-model="loginForm.username" placeholder="用户名" size="large">
            <template #prefix>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input 
            v-model="loginForm.password" 
            type="password" 
            placeholder="密码" 
            size="large"
            show-password
          >
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button 
            type="primary" 
            style="width: 100%;" 
            size="large"
            @click="handleLogin"
            :loading="loading"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="demo-accounts">
        <h4>演示账户：</h4>
        <p>用户名: demo1, 密码: 123456 (低风险偏好)</p>
        <p>用户名: demo2, 密码: 123456 (中风险偏好)</p>
        <p>用户名: demo3, 密码: 123456 (高风险偏好)</p>
      </div>
    </div>
  </div>
</template>

<script>
import { User, Lock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { mapActions } from 'vuex'

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
            // 模拟登录验证
            const demoUsers = {
              'demo1': { id: 1, name: '张三', risk: 'low' },
              'demo2': { id: 2, name: '李四', risk: 'medium' },
              'demo3': { id: 3, name: '王五', risk: 'high' }
            }
            
            if (this.loginForm.password === '123456' && demoUsers[this.loginForm.username]) {
              const user = demoUsers[this.loginForm.username]
              
              // 使用Vuex store存储用户信息
              this.login({
                name: user.name,
                avatar: '',
                risk: user.risk
              })
              
              // 存储用户信息到localStorage（用于持久化）
              localStorage.setItem('isLoggedIn', 'true')
              localStorage.setItem('userId', user.id.toString())
              localStorage.setItem('userName', user.name)
              localStorage.setItem('userRisk', user.risk)
              
              ElMessage.success('登录成功！')
              
              // 跳转到仪表盘
              this.$router.push('/dashboard')
            } else {
              ElMessage.error('用户名或密码错误')
            }
          } catch (error) {
            ElMessage.error('登录失败，请稍后重试')
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
</style>
