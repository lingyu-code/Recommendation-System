import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Funds from '../views/Funds.vue'
import Stocks from '../views/Stocks.vue'
import FinancialDiagnosis from '../views/FinancialDiagnosis.vue'
import Insurance from '../views/Insurance.vue'
import Profile from '../views/Profile.vue'
import Dashboard from '../views/Dashboard.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
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
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
