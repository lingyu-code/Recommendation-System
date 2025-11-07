<template>
  <div class="funds">
    <div class="card">
      <div class="card-header">
        <div class="header-content">
          <span class="title">基金推荐</span>
          <div class="filter-section">

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
                <button class="btn btn-sm btn-primary" @click="viewFundDetail(fund)">
                  查看详情
                </button>
                <button class="btn btn-sm btn-success" @click="purchaseFund(fund)">
                  购买基金
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

          <button class="btn btn-sm" :disabled="currentPage === 1" @click="changePage(currentPage - 1)">
            上一页
          </button>

          <span class="page-info">
            第 {{ currentPage }} 页 / 共 {{ totalPages }} 页
          </span>

          <button class="btn btn-sm" :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)">
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

    <!-- 购买基金对话框 -->
    <div v-if="investmentDialogVisible" class="modal-overlay" @click="investmentDialogVisible = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>购买基金</h3>
          <button class="close-btn" @click="investmentDialogVisible = false">×</button>
        </div>
        <div class="modal-body" v-if="selectedFund">
          <div class="form-group">
            <label>投资金额:</label>
            <input type="number" v-model.number="investmentForm.amount" :min="selectedFund.min_investment"
              class="input" />
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
import { apiService } from '../api'

export default {
  name: 'Funds',
  data() {
    return {
      funds: [],
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
    // 后端分页，直接用 funds
    paginatedFunds() {
      return this.funds
    }
  },
  async mounted() {
    await this.loadFunds()
  },
  methods: {
    // Simple seeded pseudo-random number generator
    seededRandom(seed) {
      let x = Math.sin(seed) * 10000;
      return x - Math.floor(x);
    },

    async loadFunds() {
      this.loading = true
      try {
        // 调用 API，传递分页和筛选参数
        const response = await apiService.getFunds({
          page: this.currentPage,
          page_size: this.pageSize,
          risk: this.filterRisk || undefined,
          type: this.filterType || undefined
        })

        if (response && response.results) {
          this.funds = response.results.map(fund => {
            let seed = fund.code.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
            const getRandom = () => this.seededRandom(seed++);

            const riskLevels = ['low', 'medium', 'high'];
            const randomRiskLevel = riskLevels[Math.floor(getRandom() * riskLevels.length)];

            const expectedReturn = parseFloat((getRandom() * 0.15 + 0.03).toFixed(4)); // 3% - 18%
            const managementFee = parseFloat((getRandom() * 0.02 + 0.005).toFixed(4)); // 0.5% - 2.5%
            const minInvestment = Math.round((getRandom() * 9 + 1) * 1000); // 1000 - 10000
            const recommendationScore = parseFloat((getRandom() * 5).toFixed(1)); // 0.0 - 5.0

            return {
              id: fund.id,
              name: fund.name,
              code: fund.code,
              type: fund.fund_type,
              risk_level: randomRiskLevel,
              expected_return: expectedReturn,
              management_fee: managementFee,
              min_investment: minInvestment,
              description: `${fund.name}由${fund.managers}管理，${fund.company}发行。`,
              recommendation_score: recommendationScore
            };
          });
          this.totalFunds = response.count || 0
        } else {
          this.funds = []
          this.totalFunds = 0
        }
      } catch (error) {
        console.error('加载基金数据失败:', error)
        this.funds = []
        this.totalFunds = 0
      } finally {
        this.loading = false
      }
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
      this.similarFunds = this.funds
        .filter(f => f.id !== fund.id && f.type === fund.type)
        .slice(0, 3)
    },

    async purchaseFund(fund) {
      this.selectedFund = fund
      this.investmentForm.amount = fund.min_investment
      this.investmentDialogVisible = true
    },

    async confirmInvestment() {
      try {
        const purchaseData = {
          product_type: 'fund',
          product_id: this.selectedFund.id,
          amount: this.investmentForm.amount,
          quantity: this.investmentForm.amount / 1.0 // 基金份额计算
        }

        const response = await apiService.purchaseProduct(purchaseData)

        if (response.success) {
          alert(`成功购买基金 ¥${this.investmentForm.amount.toLocaleString()} 到 ${this.selectedFund.name}`)
          this.investmentDialogVisible = false
        } else {
          alert(`购买失败: ${response.message}`)
        }
      } catch (error) {
        console.error('购买基金失败:', error)
        alert('购买失败，请稍后重试')
      }
    },

    async handleSizeChange() {
      this.currentPage = 1
      await this.loadFunds()
    },

    async changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
        await this.loadFunds()
      }
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
