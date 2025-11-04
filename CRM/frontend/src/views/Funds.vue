<template>
  <div class="funds">
    <div class="card">
      <div class="card-header">
        <div class="header-content">
          <span class="title">基金推荐</span>
          <div class="filter-section">
            <select v-model="filterRisk" class="select">
              <option value="">风险等级</option>
              <option value="low">低风险</option>
              <option value="medium">中风险</option>
              <option value="high">高风险</option>
            </select>
            
            <select v-model="filterType" class="select">
              <option value="">基金类型</option>
              <option value="股票型">股票型</option>
              <option value="混合型">混合型</option>
              <option value="债券型">债券型</option>
              <option value="货币型">货币型</option>
            </select>
            
            <button class="btn btn-primary" @click="loadFunds">筛选</button>
          </div>
        </div>
      </div>

      <div class="table-container">
        <table class="table" v-if="!loading">
          <thead>
            <tr>
              <th>基金名称</th>
              <th>代码</th>
              <th>类型</th>
              <th>风险等级</th>
              <th>预期收益</th>
              <th>管理费</th>
              <th>最低投资</th>
              <th>推荐指数</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="fund in paginatedFunds" :key="fund.id">
              <td>{{ fund.name }}</td>
              <td>{{ fund.code }}</td>
              <td>{{ fund.type }}</td>
              <td>
                <span :class="['tag', getRiskTagClass(fund.risk_level)]">
                  {{ getRiskText(fund.risk_level) }}
                </span>
              </td>
              <td>
                <span :style="{ color: fund.expected_return > 0.08 ? '#67C23A' : '#E6A23C' }">
                  {{ (fund.expected_return * 100).toFixed(2) }}%
                </span>
              </td>
              <td>{{ (fund.management_fee * 100).toFixed(2) }}%</td>
              <td>¥{{ fund.min_investment.toLocaleString() }}</td>
              <td>
                <div class="rating">
                  <span class="stars">
                    <span v-for="n in 5" :key="n" class="star" :class="{ active: n <= Math.floor(fund.recommendation_score) }">
                      ★
                    </span>
                  </span>
                  <span class="score">{{ fund.recommendation_score }}分</span>
                </div>
              </td>
              <td>
                <button class="btn btn-sm btn-primary" @click="viewFundDetail(fund)">
                  查看详情
                </button>
                <button class="btn btn-sm btn-success" @click="simulateInvestment(fund)">
                  模拟投资
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-if="loading" class="loading">加载中...</div>
      </div>

      <!-- 分页 -->
      <div class="pagination-container">
        <div class="pagination-info">
          共 {{ totalFunds }} 条记录
        </div>
        <div class="pagination-controls">
          <select v-model="pageSize" @change="handleSizeChange" class="select-sm">
            <option value="10">10条/页</option>
            <option value="20">20条/页</option>
            <option value="50">50条/页</option>
            <option value="100">100条/页</option>
          </select>
          
          <button class="btn btn-sm" :disabled="currentPage === 1" @click="currentPage--">
            上一页
          </button>
          
          <span class="page-info">
            第 {{ currentPage }} 页 / 共 {{ totalPages }} 页
          </span>
          
          <button class="btn btn-sm" :disabled="currentPage === totalPages" @click="currentPage++">
            下一页
          </button>
        </div>
      </div>
    </div>

    <!-- 基金详情对话框 -->
    <div v-if="detailDialogVisible" class="modal-overlay" @click="detailDialogVisible = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>基金详情</h3>
          <button class="close-btn" @click="detailDialogVisible = false">×</button>
        </div>
        <div class="modal-body" v-if="selectedFund">
          <div class="detail-grid">
            <div class="detail-item">
              <label>基金名称:</label>
              <span>{{ selectedFund.name }}</span>
            </div>
            <div class="detail-item">
              <label>基金代码:</label>
              <span>{{ selectedFund.code }}</span>
            </div>
            <div class="detail-item">
              <label>基金类型:</label>
              <span>{{ selectedFund.type }}</span>
            </div>
            <div class="detail-item">
              <label>风险等级:</label>
              <span :class="['tag', getRiskTagClass(selectedFund.risk_level)]">
                {{ getRiskText(selectedFund.risk_level) }}
              </span>
            </div>
            <div class="detail-item">
              <label>预期收益:</label>
              <span>{{ (selectedFund.expected_return * 100).toFixed(2) }}%</span>
            </div>
            <div class="detail-item">
              <label>管理费:</label>
              <span>{{ (selectedFund.management_fee * 100).toFixed(2) }}%</span>
            </div>
            <div class="detail-item full-width">
              <label>最低投资:</label>
              <span>¥{{ selectedFund.min_investment.toLocaleString() }}</span>
            </div>
            <div class="detail-item full-width">
              <label>基金描述:</label>
              <span>{{ selectedFund.description }}</span>
            </div>
          </div>

          <!-- 相似基金推荐 -->
          <div class="similar-section">
            <h4>相似基金推荐</h4>
            <table class="table table-sm">
              <thead>
                <tr>
                  <th>基金名称</th>
                  <th>代码</th>
                  <th>预期收益</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="fund in similarFunds" :key="fund.id">
                  <td>{{ fund.name }}</td>
                  <td>{{ fund.code }}</td>
                  <td>{{ (fund.expected_return * 100).toFixed(2) }}%</td>
                  <td>
                    <button class="btn btn-sm btn-text" @click="viewFundDetail(fund)">查看</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- 模拟投资对话框 -->
    <div v-if="investmentDialogVisible" class="modal-overlay" @click="investmentDialogVisible = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>模拟投资</h3>
          <button class="close-btn" @click="investmentDialogVisible = false">×</button>
        </div>
        <div class="modal-body" v-if="selectedFund">
          <div class="form-group">
            <label>投资金额:</label>
            <input 
              type="number" 
              v-model.number="investmentForm.amount" 
              :min="selectedFund.min_investment"
              class="input"
            />
            <div class="help-text">
              最低投资金额: ¥{{ selectedFund.min_investment.toLocaleString() }}
            </div>
          </div>
          <div class="form-group">
            <label>预期收益:</label>
            <span class="highlight-success">
              ¥{{ (investmentForm.amount * selectedFund.expected_return).toFixed(2) }}
            </span>
            <div class="help-text">
              年化收益率: {{ (selectedFund.expected_return * 100).toFixed(2) }}%
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn" @click="investmentDialogVisible = false">取消</button>
            <button class="btn btn-primary" @click="confirmInvestment">确认投资</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Funds',
  data() {
    return {
      funds: [],
      filteredFunds: [],
      loading: false,
      currentPage: 1,
      pageSize: 10,
      totalFunds: 0,
      
      filterRisk: '',
      filterType: '',
      
      detailDialogVisible: false,
      selectedFund: null,
      similarFunds: [],
      
      investmentDialogVisible: false,
      investmentForm: {
        amount: 0
      }
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.totalFunds / this.pageSize)
    },
    paginatedFunds() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredFunds.slice(start, end)
    }
  },
  async mounted() {
    await this.loadFunds()
  },
  methods: {
    async loadFunds() {
      this.loading = true
      try {
        // 模拟API调用获取基金数据
        this.funds = [
          {
            id: 1,
            name: '华夏成长混合基金',
            code: '000001',
            type: '混合型',
            risk_level: 'medium',
            expected_return: 0.086,
            management_fee: 0.015,
            min_investment: 1000,
            description: '主要投资于具有良好成长性的上市公司股票，追求长期资本增值。',
            recommendation_score: 4.5
          },
          {
            id: 2,
            name: '易方达消费行业',
            code: '110022',
            type: '股票型',
            risk_level: 'high',
            expected_return: 0.124,
            management_fee: 0.018,
            min_investment: 1000,
            description: '专注于消费行业投资，把握消费升级带来的投资机会。',
            recommendation_score: 4.2
          },
          {
            id: 3,
            name: '招商安心收益债券',
            code: '217011',
            type: '债券型',
            risk_level: 'low',
            expected_return: 0.045,
            management_fee: 0.008,
            min_investment: 100,
            description: '主要投资于高信用等级的债券，追求稳定收益。',
            recommendation_score: 4.0
          },
          {
            id: 4,
            name: '天弘余额宝货币',
            code: '000198',
            type: '货币型',
            risk_level: 'low',
            expected_return: 0.025,
            management_fee: 0.003,
            min_investment: 1,
            description: '货币市场基金，流动性强，风险极低。',
            recommendation_score: 3.8
          }
        ]

        // 应用筛选
        this.applyFilters()
        this.totalFunds = this.filteredFunds.length
        
      } catch (error) {
        console.error('加载基金数据失败:', error)
      } finally {
        this.loading = false
      }
    },

    applyFilters() {
      let filtered = [...this.funds]
      
      if (this.filterRisk) {
        filtered = filtered.filter(fund => fund.risk_level === this.filterRisk)
      }
      
      if (this.filterType) {
        filtered = filtered.filter(fund => fund.type === this.filterType)
      }
      
      this.filteredFunds = filtered
    },

    getRiskTagClass(riskLevel) {
      const classMap = {
        'low': 'tag-success',
        'medium': 'tag-warning',
        'high': 'tag-danger'
      }
      return classMap[riskLevel] || 'tag-info'
    },

    getRiskText(riskLevel) {
      const textMap = {
        'low': '低风险',
        'medium': '中风险',
        'high': '高风险'
      }
      return textMap[riskLevel] || '未知'
    },

    async viewFundDetail(fund) {
      this.selectedFund = fund
      this.detailDialogVisible = true
      
      // 模拟获取相似基金
      this.similarFunds = this.funds
        .filter(f => f.id !== fund.id && f.type === fund.type)
        .slice(0, 3)
    },

    simulateInvestment(fund) {
      this.selectedFund = fund
      this.investmentForm.amount = fund.min_investment
      this.investmentDialogVisible = true
    },

    confirmInvestment() {
      alert(`成功投资 ¥${this.investmentForm.amount.toLocaleString()} 到 ${this.selectedFund.name}`)
      this.investmentDialogVisible = false
    },

    handleSizeChange() {
      this.currentPage = 1
    }
  }
}
</script>

<style scoped>
.funds {
  padding: 20px;
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.card-header {
  padding: 20px;
  border-bottom: 1px solid #ebeef5;
  background: #f5f7fa;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.filter-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.select {
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background: white;
  min-width: 120px;
}

.select-sm {
  padding: 4px 8px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background: white;
}

.btn {
  padding: 8px 16px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  transition: all 0.3s;
}

.btn:hover {
  background: #f5f7fa;
}

.btn-primary {
  background: #409eff;
  color: white;
  border-color: #409eff;
}

.btn-primary:hover {
  background: #66b1ff;
}

.btn-success {
  background: #67c23a;
  color: white;
  border-color: #67c23a;
}

.btn-success:hover {
  background: #85ce61;
}

.btn-sm {
  padding: 4px 8px;
  font-size: 12px;
}

.btn-text {
  background: transparent;
  border: none;
  color: #409eff;
}

.btn-text:hover {
  background: transparent;
  color: #66b1ff;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.table-container {
  padding: 20px;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ebeef5;
}

.table th {
  background: #f5f7fa;
  font-weight: 600;
  color: #606266;
}

.table-sm th,
.table-sm td {
  padding: 8px;
  font-size: 12px;
}

.tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  color: white;
}

.tag-success {
  background: #67c23a;
}

.tag-warning {
  background: #e6a23c;
}

.tag-danger {
  background: #f56c6c;
}

.tag-info {
  background: #909399;
}

.rating {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stars {
  color: #c0c4cc;
}

.star.active {
  color: #f7ba2a;
}

.score {
  font-size: 12px;
  color: #909399;
}

.pagination-container {
  padding: 20px;
  border-top: 1px solid #ebeef5;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.page-info {
  font-size: 14px;
  color: #606266;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  min-width: 500px;
  max-width: 80vw;
  max-height: 80vh;
  overflow: auto;
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #909399;
}

.close-btn:hover {
  color: #606266;
}

.modal-body {
  padding: 20px;
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid #ebeef5;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-item.full-width {
  grid-column: 1 / -1;
}

.detail-item label {
  font-weight: 600;
  color: #606266;
  font-size: 14px;
}

.similar-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

.similar-section h4 {
  margin: 0 0 16px 0;
  font-size: 16px;
  color: #303133;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #606266;
}

.input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  box-sizing: border-box;
}

.help-text {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.highlight-success {
  color: #67c23a;
  font-weight: bold;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #909399;
}
</style>
