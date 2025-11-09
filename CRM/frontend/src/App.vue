<template>
  <div id="app">
    <el-container>
      <!-- 侧边栏导航 -->
      <el-aside width="200px" style="background-color: #304156; min-height: 100vh;">
        <el-menu default-active="1" class="el-menu-vertical-demo" background-color="#304156" text-color="#bfcbd9"
          active-text-color="#409EFF" router>
          <div class="logo">
            <h2 style="color: white; text-align: center; padding: 20px 0;">金融推荐系统</h2>
          </div>

          <el-sub-menu index="1">
            <template #title>
              <el-icon>
                <location />
              </el-icon>
              <span>投资中心</span>
            </template>
            <el-menu-item index="/funds">基金推荐</el-menu-item>
            <el-menu-item index="/stocks">股票推荐</el-menu-item>
          </el-sub-menu>

          <el-menu-item index="/dashboard">
            <el-icon>
              <home-filled />
            </el-icon>
            <span>推荐总览</span>
          </el-menu-item>

          <el-sub-menu index="2">
            <template #title>
              <el-icon>
                <setting />
              </el-icon>
              <span>理财规划</span>
            </template>
            <el-menu-item index="/financial-diagnosis">理财诊断</el-menu-item>
            <el-menu-item index="/insurance">保险推荐</el-menu-item>
            <el-menu-item index="/machine-learning">机器学习</el-menu-item>
          </el-sub-menu>

          <el-menu-item index="/profile">
            <el-icon>
              <user />
            </el-icon>
            <span>个人中心</span>
          </el-menu-item>

          <el-menu-item index="/login" v-if="!isLoggedIn">
            <el-icon>
              <login />
            </el-icon>
            <span>登录</span>
          </el-menu-item>

          <el-menu-item index="/logout" v-if="isLoggedIn" @click="handleLogout">
            <el-icon>
              <logout />
            </el-icon>
            <span>退出登录</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 主内容区域 -->
      <el-container>
        <el-header style="background-color: #fff; border-bottom: 1px solid #e6e6e6;">
          <div class="header-content">
            <h3>{{ currentRouteName }}</h3>
            <div class="user-info" v-if="isLoggedIn">
              <el-avatar :size="32" :src="userAvatar"></el-avatar>
              <span style="margin-left: 10px;">欢迎，{{ userName }}</span>
            </div>
          </div>
        </el-header>

        <el-main style="background-color: #f0f2f5; padding: 20px;">
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { Location, Setting, User, Login, Logout, HomeFilled } from '@element-plus/icons-vue'
import { mapState, mapActions } from 'vuex'

export default {
  name: 'App',
  components: {
    Location,
    Setting,
    User,
    Login,
    Logout,
    HomeFilled
  },
  computed: {
    ...mapState(['isLoggedIn', 'userName', 'userAvatar']),
    currentRouteName() {
      const routeNames = {
        '/funds': '基金推荐',
        '/stocks': '股票推荐',
        '/financial-diagnosis': '理财诊断',
        '/insurance': '保险推荐',
        '/profile': '个人中心',
        '/login': '登录',
        '/dashboard': '推荐总览',
        '/machine-learning': '机器学习模型训练'
      }
      return routeNames[this.$route.path] || '金融推荐系统'
    }
  },
  methods: {
    ...mapActions(['logout', 'login']),
    handleLogout() {
      this.logout()
      localStorage.removeItem('isLoggedIn')
      localStorage.removeItem('userId')
      localStorage.removeItem('userName')
      localStorage.removeItem('userRisk')
      this.$router.push('/login')
    }
  },
  mounted() {
    // 检查localStorage中的登录状态
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
    const userName = localStorage.getItem('userName')

    if (isLoggedIn && userName) {
      this.login({
        name: userName,
        avatar: '',
        risk: localStorage.getItem('userRisk') || 'medium'
      })
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.logo {
  border-bottom: 1px solid #475669;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.user-info {
  display: flex;
  align-items: center;
}

.el-menu-vertical-demo {
  border-right: none;
}

.el-header {
  padding: 0 20px;
}

.el-main {
  min-height: calc(100vh - 60px);
}
</style>
