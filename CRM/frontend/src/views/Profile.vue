<template>
  <div class="profile-container">
    <div class="profile-header">
      <h1>个人信息</h1>
      <p>管理您的个人资料和投资偏好</p>
    </div>

    <div class="profile-content">
      <!-- 查看模式 -->
      <div v-if="!isEditing" class="profile-view">
        <div class="profile-card">
          <div class="card-header">
            <h2>基本信息</h2>
            <button @click="startEditing" class="edit-btn">
              <i class="fas fa-edit"></i> 编辑
            </button>
          </div>

          <div class="profile-info">
            <div class="info-row">
              <label>用户名:</label>
              <span>{{ user.username }}</span>
            </div>
            <div class="info-row">
              <label>邮箱:</label>
              <span>{{ user.email || '未设置' }}</span>
            </div>
            <div class="info-row">
              <label>姓名:</label>
              <span>{{ fullName || '未设置' }}</span>
            </div>
            <div class="info-row">
              <label>电话:</label>
              <span>{{ user.phone || '未设置' }}</span>
            </div>
            <div class="info-row">
              <label>年龄:</label>
              <span>{{ user.age || '未设置' }}</span>
            </div>
          </div>
        </div>

        <div class="profile-card">
          <div class="card-header">
            <h2>投资偏好</h2>
          </div>

          <div class="profile-info">
            <div class="info-row">
              <label>风险承受能力:</label>
              <span class="risk-badge" :class="getRiskClass(user.risk_tolerance)">
                {{ getRiskDisplay(user.risk_tolerance) }}
              </span>
            </div>
            <div class="info-row">
              <label>总资产:</label>
              <span class="amount">¥{{ formatAmount(user.total_assets) }}</span>
            </div>
            <div class="info-row">
              <label>投资目标:</label>
              <span>{{ user.investment_goal || '未设置' }}</span>
            </div>
          </div>
        </div>

        <!-- 购买记录 -->
        <div class="profile-card">
          <div class="card-header">
            <h2>购买记录</h2>
            <button @click="loadPurchaseRecords" class="refresh-btn">
              <i class="fas fa-sync-alt"></i> 刷新
            </button>
          </div>

          <div v-if="purchasesLoading" class="loading">
            加载中...
          </div>

          <div v-else-if="purchases.length === 0" class="empty-state">
            <p>暂无购买记录</p>
            <p class="hint">您可以在基金、保险或股票页面进行购买</p>
          </div>

          <div v-else class="purchases-list">
            <div v-for="purchase in purchases" :key="purchase.id" class="purchase-item">
              <div class="purchase-header">
                <span class="product-name">{{ purchase.product_name }}</span>
                <span class="purchase-type" :class="getPurchaseTypeClass(purchase.purchase_type)">
                  {{ purchase.purchase_type_display }}
                </span>
              </div>
              <div class="purchase-details">
                <div class="purchase-amount">
                  <span class="amount-label">金额:</span>
                  <span class="amount-value">¥{{ formatAmount(purchase.amount) }}</span>
                </div>
                <div v-if="purchase.quantity" class="purchase-quantity">
                  <span class="quantity-label">数量:</span>
                  <span class="quantity-value">{{ purchase.quantity }}</span>
                </div>
                <div class="purchase-date">
                  <span class="date-label">购买时间:</span>
                  <span class="date-value">{{ formatDate(purchase.purchase_date) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 编辑模式 -->
      <div v-else class="profile-edit">
        <div class="profile-card">
          <div class="card-header">
            <h2>编辑个人信息</h2>
            <div class="action-buttons">
              <button @click="saveProfile" class="save-btn" :disabled="loading">
                {{ loading ? '保存中...' : '保存' }}
              </button>
              <button @click="cancelEditing" class="cancel-btn">取消</button>
            </div>
          </div>

          <form @submit.prevent="saveProfile" class="profile-form">
            <div class="form-group">
              <label>邮箱:</label>
              <input v-model="editForm.email" type="email" placeholder="请输入邮箱">
            </div>

            <div class="form-group">
              <label>姓:</label>
              <input v-model="editForm.first_name" type="text" placeholder="请输入姓">
            </div>

            <div class="form-group">
              <label>名:</label>
              <input v-model="editForm.last_name" type="text" placeholder="请输入名">
            </div>

            <div class="form-group">
              <label>电话:</label>
              <input v-model="editForm.phone" type="tel" placeholder="请输入电话号码">
            </div>

            <div class="form-group">
              <label>年龄:</label>
              <input v-model="editForm.age" type="number" min="18" max="100" placeholder="请输入年龄">
            </div>

            <div class="form-group">
              <label>风险承受能力:</label>
              <select v-model="editForm.risk_tolerance">
                <option value="low">低风险</option>
                <option value="medium">中风险</option>
                <option value="high">高风险</option>
              </select>
            </div>

            <div class="form-group">
              <label>总资产 (元):</label>
              <input v-model="editForm.total_assets" type="number" min="0" step="1000" placeholder="请输入总资产">
            </div>

            <div class="form-group">
              <label>投资目标:</label>
              <textarea v-model="editForm.investment_goal" placeholder="请输入您的投资目标，例如：长期增值、短期收益、教育基金等"
                rows="3"></textarea>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- 消息提示 -->
    <div v-if="message" class="message" :class="messageType">
      {{ message }}
    </div>
  </div>
</template>

<script>
import { apiService } from '@/api'

export default {
  name: 'Profile',
  data() {
    return {
      user: {
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        phone: '',
        age: null,
        risk_tolerance: 'medium',
        total_assets: 100000,
        investment_goal: ''
      },
      editForm: {
        email: '',
        first_name: '',
        last_name: '',
        phone: '',
        age: null,
        risk_tolerance: 'medium',
        total_assets: 100000,
        investment_goal: ''
      },
      purchases: [],
      purchasesLoading: false,
      isEditing: false,
      loading: false,
      message: '',
      messageType: 'success'
    }
  },
  computed: {
    fullName() {
      if (this.user.first_name && this.user.last_name) {
        return `${this.user.last_name}${this.user.first_name}`
      }
      return ''
    }
  },
  async mounted() {
    await this.loadUserProfile()
    await this.loadPurchaseRecords()
  },
  methods: {
    async loadUserProfile() {
      try {
        const response = await apiService.getProfile()
        if (response.success) {
          this.user = response.user
          // 初始化编辑表单
          Object.assign(this.editForm, response.user)
        }
      } catch (error) {
        console.error('加载用户信息失败:', error)
        this.showMessage('加载用户信息失败', 'error')
      }
    },

    async loadPurchaseRecords() {
      this.purchasesLoading = true
      try {
        const response = await apiService.getPurchaseRecords()
        if (response.success) {
          this.purchases = response.purchases
        }
      } catch (error) {
        console.error('加载购买记录失败:', error)
        this.showMessage('加载购买记录失败', 'error')
      } finally {
        this.purchasesLoading = false
      }
    },

    startEditing() {
      this.isEditing = true
      this.message = ''
    },

    cancelEditing() {
      this.isEditing = false
      // 重置编辑表单为当前用户数据
      Object.assign(this.editForm, this.user)
      this.message = ''
    },

    async saveProfile() {
      this.loading = true
      try {
        const response = await apiService.updateProfile(this.editForm)
        if (response.success) {
          this.user = response.user
          this.isEditing = false
          this.showMessage('个人信息更新成功', 'success')
        } else {
          this.showMessage(response.message || '更新失败', 'error')
        }
      } catch (error) {
        console.error('更新用户信息失败:', error)
        this.showMessage('更新失败，请稍后重试', 'error')
      } finally {
        this.loading = false
      }
    },

    getRiskDisplay(risk) {
      const riskMap = {
        'low': '低风险',
        'medium': '中风险',
        'high': '高风险'
      }
      return riskMap[risk] || '未知'
    },

    getRiskClass(risk) {
      return `risk-${risk}`
    },

    getPurchaseTypeClass(type) {
      return `purchase-${type}`
    },

    formatAmount(amount) {
      if (!amount) return '0.00'
      return parseFloat(amount).toLocaleString('zh-CN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      })
    },

    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    showMessage(msg, type = 'success') {
      this.message = msg
      this.messageType = type
      setTimeout(() => {
        this.message = ''
      }, 3000)
    }
  }
}
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.profile-header {
  text-align: center;
  margin-bottom: 30px;
}

.profile-header h1 {
  color: #333;
  margin-bottom: 10px;
}

.profile-header p {
  color: #666;
  font-size: 16px;
}

.profile-card {
  background: white;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
}

.card-header h2 {
  color: #333;
  margin: 0;
}

.edit-btn,
.save-btn,
.cancel-btn,
.refresh-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.edit-btn {
  background: #007bff;
  color: white;
}

.edit-btn:hover {
  background: #0056b3;
}

.save-btn {
  background: #28a745;
  color: white;
  margin-right: 10px;
}

.save-btn:hover:not(:disabled) {
  background: #218838;
}

.save-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.cancel-btn {
  background: #6c757d;
  color: white;
}

.cancel-btn:hover {
  background: #545b62;
}

.refresh-btn {
  background: #17a2b8;
  color: white;
}

.refresh-btn:hover {
  background: #138496;
}

.profile-info {
  display: grid;
  gap: 16px;
}

.info-row {
  display: flex;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f8f9fa;
}

.info-row label {
  font-weight: 600;
  color: #333;
  min-width: 120px;
  margin-right: 20px;
}

.info-row span {
  color: #666;
}

.risk-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.risk-low {
  background: #d4edda;
  color: #155724;
}

.risk-medium {
  background: #fff3cd;
  color: #856404;
}

.risk-high {
  background: #f8d7da;
  color: #721c24;
}

.amount {
  font-weight: 600;
  color: #28a745;
}

/* 购买记录样式 */
.loading {
  text-align: center;
  padding: 20px;
  color: #666;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #666;
}

.empty-state .hint {
  font-size: 14px;
  color: #999;
  margin-top: 10px;
}

.purchases-list {
  display: grid;
  gap: 16px;
}

.purchase-item {
  border: 1px solid #e9ecef;
  border-radius: 6px;
  padding: 16px;
  background: #f8f9fa;
}

.purchase-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.product-name {
  font-weight: 600;
  color: #333;
  font-size: 16px;
}

.purchase-type {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.purchase-fund {
  background: #e3f2fd;
  color: #1565c0;
}

.purchase-insurance {
  background: #e8f5e8;
  color: #2e7d32;
}

.purchase-stock {
  background: #fff3e0;
  color: #ef6c00;
}

.purchase-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
  font-size: 14px;
}

.purchase-amount,
.purchase-quantity,
.purchase-date {
  display: flex;
  flex-direction: column;
}

.amount-label,
.quantity-label,
.date-label {
  font-weight: 600;
  color: #666;
  margin-bottom: 4px;
}

.amount-value {
  color: #28a745;
  font-weight: 600;
}

.quantity-value,
.date-value {
  color: #333;
}

.profile-form {
  display: grid;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 600;
  margin-bottom: 8px;
  color: #333;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #007bff;
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.message {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 12px 20px;
  border-radius: 4px;
  color: white;
  font-weight: 500;
  z-index: 1000;
  animation: slideIn 0.3s ease-out;
}

.message.success {
  background: #28a745;
}

.message.error {
  background: #dc3545;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }

  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .profile-container {
    padding: 10px;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .action-buttons {
    align-self: flex-end;
  }

  .info-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }

  .info-row label {
    min-width: auto;
  }

  .purchase-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .purchase-details {
    grid-template-columns: 1fr;
  }
}
</style>
