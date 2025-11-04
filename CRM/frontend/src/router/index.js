import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Funds from '../views/Funds.vue'
import Stocks from '../views/Stocks.vue'
import FinancialDiagnosis from '../views/FinancialDiagnosis.vue'
import Insurance from '../views/Insurance.vue'
import Profile from '../views/Profile.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/funds',
    name: 'Funds',
    component: Funds
  },
  {
    path: '/stocks',
    name: 'Stocks',
    component: Stocks
  },
  {
    path: '/financial-diagnosis',
    name: 'FinancialDiagnosis',
    component: FinancialDiagnosis
  },
  {
    path: '/insurance',
    name: 'Insurance',
    component: Insurance
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
  
  if (to.path !== '/login' && !isLoggedIn) {
    next('/login')
  } else if (to.path === '/login' && isLoggedIn) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
