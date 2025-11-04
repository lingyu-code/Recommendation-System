<template>
  <div class="profile">
    <el-row :gutter="20">
      <!-- 个人信息 -->
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="header-content">
              <span>个人信息</span>
              <el-button type="primary" size="small" @click="editProfile">
                编辑信息
              </el-button>
            </div>
          </template>

          <div class="user-info">
            <div class="avatar-section">
              <el-avatar :size="80" :src="userInfo.avatar" />
              <div class="user-name">
                <h3>{{ userInfo.name }}</h3>
                <p>{{ userInfo.role }}</p>
              </div>
            </div>

            <el-descriptions :column="1" border>
              <el-descriptions-item label="用户ID">
                {{ userInfo.id }}
              </el-descriptions-item>
              <el-descriptions-item label="年龄">
                {{ userInfo.age }}岁
              </el-descriptions-item>
              <el-descriptions-item label="职业">
                {{ userInfo.occupation }}
              </el-descriptions-item>
              <el-descriptions-item label="年收入">
                ¥{{ userInfo.income.toLocaleString() }}
              </el-descriptions-item>
              <el-descriptions-item label="风险等级">
                <el-tag :type="getRiskLevelTagType(userInfo.riskLevel)">
                  {{ userInfo.riskLevel }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="注册时间">
                {{ userInfo.registerTime }}
              </el-descriptions-item>
            </el-descriptions>
          </div>
        </el-card>

        <!-- 资产概览 -->
        <el-card style="margin-top: 20px;">
          <template #header>
            <span>资产概览</span>
          </template>
          <div class="asset-overview">
            <div class="asset-item">
              <div class="asset-icon total">
                <i class="el-icon-money"></i>
              </div>
              <div class="asset-info">
                <div class="asset-value">¥{{ totalAssets.toLocaleString() }}</div>
                <div class="asset-label">总资产</div>
              </div>
            </div>
            <div class="asset-item">
              <div class="asset-icon profit">
                <i class="el-icon-trend-charts"></i>
              </div>
              <div class="asset-info">
                <div class="asset-value">+{{ totalProfit.toLocaleString() }}</div>
                <div class="asset-label">总收益</div>
              </div>
            </div>
            <div class="asset-item">
              <div class="asset-icon rate">
                <i class="el-icon-data-line"></i>
              </div>
              <div class="asset-info">
                <div class="asset-value">{{ profitRate }}%</div>
                <div class="asset-label">收益率</div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 投资组合 -->
      <el-col :span="16">
        <el-card>
          <template #header>
            <span>投资组合</span>
          </template>
          <div class="portfolio">
            <el-table :data="portfolio" style="width: 100%">
              <el-table-column prop="type" label="类型" width="100">
                <template #default="scope">
                  <el-tag :type="getProductTypeTagType(scope.row.type)">
                    {{ scope.row.type }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="name" label="产品名称" width="200"></el-table-column>
              <el-table-column prop="amount" label="投资金额" width="120">
                <template #default="scope">
                  ¥{{ scope.row.amount.toLocaleString() }}
                </template>
              </el-table-column>
              <el-table-column prop="currentValue" label="当前价值" width="120">
                <template #default="scope">
                  ¥{{ scope.row.currentValue.toLocaleString() }}
                </template>
              </el-table-column>
              <el-table-column prop="profit" label="收益" width="100">
                <template #default="scope">
                  <span :class="scope.row.profit >= 0 ? 'profit-positive' : 'profit-negative'">
                    {{ scope.row.profit >= 0 ? '+' : '' }}{{ scope.row.profit.toLocaleString() }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column prop="profitRate" label="收益率" width="100">
                <template #default="scope">
                  <span :class="scope.row.profitRate >= 0 ? 'profit-positive' : 'profit-negative'">
                    {{ scope.row.profitRate >= 0 ? '+' : '' }}{{ scope.row.profitRate }}%
                  </span>
                </template>
              </el-table-column>
              <el-table-column prop="purchaseDate" label="购买日期" width="120"></el-table-column>
              <el-table-column label="操作" width="120">
                <template #default="scope">
                  <el-button type="text" @click="viewProductDetail(scope.row)">详情</el-button>
                  <el-button type="text" @click="sellProduct(scope.row)">卖出</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>

        <!-- 投资历史 -->
        <el-card style="margin-top: 20px;">
          <template #header>
            <span>投资历史</span>
          </template>
          <div class="investment-history">
            <el-timeline>
              <el-timeline-item
                v-for="(record, index) in investmentHistory"
                :key="index"
                :timestamp="record.time"
                :type="record.type"
              >
                <div class="history-item">
                  <div class="history-content">
                    <span class="action">{{ record.action }}</span>
                    <span class="product">{{ record.product }}</span>
                    <span class="amount">¥{{ record.amount.toLocaleString() }}</span>
                  </div>
                  <div class="history-detail">
                    {{ record.detail }}
                  </div>
                </div>
              </el-timeline-item>
            </el-timeline>
          </div>
        </el-card>

        <!-- 推荐记录 -->
        <el-card style="margin-top: 20px;">
          <template #header>
            <span>推荐记录</span>
          </template>
          <div class="recommendation-history">
            <el-table :data="recommendationHistory" style="width: 100%">
              <el-table-column prop="date" label="日期" width="120"></el-table-column>
              <el-table-column prop="type" label="类型" width="100">
                <template #default="scope">
                  <el-tag :type="getProductTypeTagType(scope.row.type)" size="small">
                    {{ scope.row.type }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="product" label="产品名称" width="200"></el-table-column>
              <el-table-column prop="score" label="推荐分数" width="100">
                <template #default="scope">
                  <el-rate
                    :model-value="scope.row.score"
                    disabled
                    show-score
                    text-color="#ff9900"
                    score-template="{value}"
                  />
                </template>
              </el-table-column>
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="getStatusTagType(scope.row.status)" size="small">
                    {{ scope.row.status }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="120">
                <template #default="scope">
                  <el-button type="text" @click="viewRecommendation(scope.row)">查看</el-button>
                  <el-button 
                    type="text" 
                    @click="purchaseRecommendation(scope.row)"
                    v-if="scope.row.status === '未购买'"
                  >
                    购买
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 编辑个人信息对话框 -->
    <el-dialog v-model="editDialogVisible" title="编辑个人信息" width="500px">
      <el-form :model="editForm" label-width="100px">
        <el-form-item label="姓名">
          <el-input v-model="editForm.name" />
        </el-form-item>
        <el-form-item label="年龄">
          <el-input-number v-model="editForm.age" :min="18" :max="80" />
        </el-form-item>
        <el-form-item label="职业">
          <el-select v-model="editForm.occupation" placeholder="请选择职业">
            <el-option label="学生" value="学生"></el-option>
            <el-option label="上班族" value="上班族"></el-option>
            <el-option label="自由职业" value="自由职业"></el-option>
            <el-option label="退休" value="退休"></el-option>
            <el-option label="其他" value="其他"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="年收入">
          <el-input-number v-model="editForm.income" :min="0" :step="10000" />
          <span style="margin-left: 10px">元</span>
        </el-form-item>
        <el-form-item label="风险等级">
          <el-radio-group v-model="editForm.riskLevel">
            <el-radio label="保守型">保守型</el-radio>
            <el-radio label="稳健型">稳健型</el-radio>
            <el-radio label="积极型">积极型</el-radio>
            <el-radio label="非常积极型">非常积极型</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveProfile">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'Profile',
  data() {
    return {
      userInfo: {
        id: 'U10001',
        name: '张三',
        role: '普通用户',
        avatar: '',
        age: 35,
        occupation: '上班族',
        income: 200000,
        riskLevel: '稳健型',
        registerTime: '2024-01-15'
      },
      totalAssets: 285000,
      totalProfit: 18500,
      profitRate: 6.95,
      portfolio: [
        {
          id: 1,
          type: '基金',
          name: '华夏成长混合基金',
          amount: 50000,
          currentValue: 53500,
          profit: 3500,
          profitRate: 7.0,
          purchaseDate: '2024-03-10'
        },
        {
          id: 2,
          type: '股票',
          name: '贵州茅台',
          amount: 80000,
          currentValue: 92000,
          profit: 12000,
          profitRate: 15.0,
          purchaseDate: '2024-02-15'
        },
        {
          id: 3,
          type: '保险',
          name: '平安福终身寿险',
          amount: 150000,
          currentValue: 150000,
          profit: 0,
          profitRate: 0,
          purchaseDate: '2024-01-20'
        },
        {
          id: 4,
          type: '理财产品',
          name: '保本型理财',
          amount: 5000,
          currentValue: 5100,
          profit: 100,
          profitRate: 2.0,
          purchaseDate: '2024-04-05'
        }
      ],
      investmentHistory: [
        {
          time: '2024-04-05 14:30',
          type: 'success',
          action: '购买',
          product: '保本型理财',
          amount: 5000,
          detail: '购买保本型理财产品，预期年化收益率3.5%'
        },
        {
          time: '2024-03-10 10:15',
          type: 'success',
          action: '购买',
          product: '华夏成长混合基金',
          amount: 50000,
          detail: '购买混合型基金，追求长期稳定增长'
        },
        {
          time: '2024-02-15 09:45',
          type: 'success',
          action: '购买',
          product: '贵州茅台股票',
          amount: 80000,
          detail: '购买优质蓝筹股，看好长期价值'
        },
        {
          time: '2024-01-20 16:20',
          type: 'info',
          action: '购买',
          product: '平安福终身寿险',
          amount: 150000,
          detail: '购买终身寿险，提供家庭保障'
        }
      ],
      recommendationHistory: [
        {
          id: 1,
          date: '2024-04-10',
          type: '基金',
          product: '易方达消费行业股票',
          score: 4.2,
          status: '未购买'
        },
        {
          id: 2,
          date: '2024-04-08',
          type: '股票',
          product: '招商银行',
          score: 4.0,
          status: '已购买'
        },
        {
          id: 3,
          date: '2024-04-05',
          type: '保险',
          product: '意外伤害保险',
          score: 3.8,
          status: '未购买'
        },
        {
          id: 4,
          date: '2024-04-01',
          type: '理财产品',
          product: '货币市场基金',
          score: 4.5,
          status: '已购买'
        }
      ],
      editDialogVisible: false,
      editForm: {
        name: '',
        age: 0,
        occupation: '',
        income: 0,
        riskLevel: ''
      }
    }
  },
  mounted() {
    this.loadUserData()
  },
  methods: {
    loadUserData() {
      // 模拟加载用户数据
      console.log('加载用户数据')
    },
    
    editProfile() {
      this.editForm = { ...this.userInfo }
      this.editDialogVisible = true
    },
    
    saveProfile() {
      this.userInfo = { ...this.editForm }
      this.$message.success('个人信息更新成功')
      this.editDialogVisible = false
    },
    
    getRiskLevelTagType(level) {
      const typeMap = {
        '保守型': 'info',
        '稳健型': 'success',
        '积极型': 'warning',
        '非常积极型': 'danger'
      }
      return typeMap[level] || 'info'
    },
    
    getProductTypeTagType(type) {
      const typeMap = {
        '基金': 'primary',
        '股票': 'success',
        '保险': 'warning',
        '理财产品': 'info'
      }
      return typeMap[type] || 'info'
    },
    
    getStatusTagType(status) {
      const typeMap = {
        '已购买': 'success',
        '未购买': 'info'
      }
      return typeMap[status] || 'info'
    },
    
    viewProductDetail(product) {
      this.$message.info(`查看${product.name}详情`)
    },
    
    sellProduct(product) {
      this.$confirm(`确定要卖出${product.name}吗？`, '确认卖出', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message.success(`成功卖出${product.name}`)
      })
    },
    
    viewRecommendation(recommendation) {
      this.$message.info(`查看${recommendation.product}推荐详情`)
    },
    
    purchaseRecommendation(recommendation) {
      this.$confirm(`确定要购买${recommendation.product}吗？`, '确认购买', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info'
      }).then(() => {
        recommendation.status = '已购买'
        this.$message.success(`成功购买${recommendation.product}`)
      })
    }
  }
}
</script>

<style scoped>
.profile {
  padding: 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info {
  padding: 10px 0;
}

.avatar-section {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 10px;
}

.user-name {
  margin-left: 15px;
}

.user-name h3 {
  margin: 0 0 5px 0;
  color: #303133;
}

.user-name p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.asset-overview {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
}

.asset-item {
  display: flex;
  align-items: center;
  flex: 1;
  text-align: center;
}

.asset-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-size: 24px;
  color: white;
}

.asset-icon.total {
  background-color: #409EFF;
}

.asset-icon.profit {
  background-color: #67C23A;
}

.asset-icon.rate {
  background-color: #E6A23C;
}

.asset-value {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.asset-label {
  font-size: 14px;
  color: #909399;
}

.portfolio {
  padding: 10px 0;
}

.profit-positive {
  color: #67C23A;
  font-weight: bold;
}

.profit-negative {
  color: #F56C6C;
  font-weight: bold;
}

.investment-history {
  padding: 10px 0;
}

.history-item {
  padding: 5px 0;
}

.history-content {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.history-content .action {
  font-weight: bold;
  color: #303133;
}

.history-content .product {
  color: #409EFF;
}

.history-content .amount {
  color: #67C23A;
  font-weight: bold;
}

.history-detail {
  color: #606266;
  font-size: 14px;
}

.recommendation-history {
  padding: 10px 0;
}
</style>
