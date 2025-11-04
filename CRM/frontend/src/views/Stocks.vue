<template>
  <div class="stocks">
    <div class="card">
      <div class="card-header">
        <div class="header-content">
          <span class="title">股票推荐</span>
          <div class="filter-section">
            <select v-model="filterIndustry" class="select">
              <option value="">行业</option>
              <option value="科技">科技</option>
              <option value="金融">金融</option>
              <option value="消费">消费</option>
              <option value="医疗">医疗</option>
              <option value="能源">能源</option>
              <option value="工业">工业</option>
            </select>
            
            <select v-model="filterTrend" class="select">
              <option value="">趋势</option>
              <option value="up">上涨</option>
              <option value="down">下跌</option>
              <option value="sideways">震荡</option>
            </select>
            
            <button class="btn btn-primary" @click="loadStocks">筛选</button>
          </div>
        </div>
      </div>

      <div class="table-container">
        <table class="table" v-if="!loading">
          <thead>
            <tr>
              <th>股票名称</th>
              <th>代码</th>
              <th>行业</th>
              <th>当前价格</th>
              <th>涨跌幅</th>
              <th>市盈率</th>
              <th>市值</th>
              <th>趋势</th>
              <th>推荐指数</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="stock in paginatedStocks" :key="stock.id">
              <td>{{ stock.name }}</td>
              <td>{{ stock.code }}</td>
              <td>{{ stock.industry }}</td>
              <td>¥{{ stock.current_price.toFixed(2) }}</td>
              <td>
                <span :style="{ color: stock.change_percent >= 0 ? '#F56C6C' : '#67C23A' }">
                  {{ stock.change_percent >= 0 ? '+' : '' }}{{ stock.change_percent.toFixed(2) }}%
                </span>
              </td>
              <td>{{ stock.pe_ratio.toFixed(2) }}</td>
              <td>{{ formatMarketCap(stock.market_cap) }}</td>
              <td>
                <span :class="['tag', getTrendTagClass(stock.trend)]">
                  {{ getTrendText(stock.trend) }}
                </span>
              </td>
              <td>
                <div class="rating">
                  <span class="stars">
                    <span v-for="n in 5" :key="n" class="star" :class="{ active: n <= Math.floor(stock.recommendation_score) }">
                      ★
                    </span>
                  </span>
                  <span class="score">{{ stock.recommendation_score }}分</span>
                </div>
              </td>
              <td>
                <button class="btn btn-sm btn-primary" @click="viewStockDetail(stock)">
                  查看详情
                </button>
                <button class="btn btn-sm btn-success" @click="simulateTrade(stock)">
                  模拟交易
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
          共 {{ totalStocks }} 条记录
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

    <!-- 股票详情对话框 -->
    <div v-if="detailDialogVisible" class="modal-overlay" @click="detailDialogVisible = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>股票详情</h3>
          <button class="close-btn" @click="detailDialogVisible = false">×</button>
        </div>
        <div class="modal-body" v-if="selectedStock">
          <div class="detail-grid">
            <div class="detail-item">
              <label>股票名称:</label>
              <span>{{ selectedStock.name }}</span>
            </div>
            <div class="detail-item">
              <label>股票代码:</label>
              <span>{{ selectedStock.code }}</span>
            </div>
            <div class="detail-item">
              <label>所属行业:</label>
              <span>{{ selectedStock.industry }}</span>
            </div>
            <div class="detail-item">
              <label>当前价格:</label>
              <span>¥{{ selectedStock.current_price.toFixed(2) }}</span>
            </div>
            <div class="detail-item">
              <label>涨跌幅:</label>
              <span :style="{ color: selectedStock.change_percent >= 0 ? '#F56C6C' : '#67C23A' }">
                {{ selectedStock.change_percent >= 0 ? '+' : '' }}{{ selectedStock.change_percent.toFixed(2) }}%
              </span>
            </div>
            <div class="detail-item">
              <label>市盈率:</label>
              <span>{{ selectedStock.pe_ratio.toFixed(2) }}</span>
            </div>
            <div class="detail-item">
              <label>市值:</label>
              <span>{{ formatMarketCap(selectedStock.market_cap) }}</span>
            </div>
            <div class="detail-item">
              <label>52周最高:</label>
              <span>¥{{ selectedStock.high_52w.toFixed(2) }}</span>
            </div>
            <div class="detail-item">
              <label>52周最低:</label>
              <span>¥{{ selectedStock.low_52w.toFixed(2) }}</span>
            </div>
            <div class="detail-item">
              <label>趋势:</label>
              <span :class="['tag', getTrendTagClass(selectedStock.trend)]">
                {{ getTrendText(selectedStock.trend) }}
              </span>
            </div>
            <div class="detail-item full-width">
              <label>公司简介:</label>
              <span>{{ selectedStock.description }}</span>
            </div>
          </div>

          <!-- 相似股票推荐 -->
          <div class="similar-section">
            <h4>相似股票推荐</h4>
            <table class="table table-sm">
              <thead>
                <tr>
                  <th>股票名称</th>
                  <th>代码</th>
                  <th>价格</th>
                  <th>涨跌幅</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="stock in similarStocks" :key="stock.id">
                  <td>{{ stock.name }}</td>
                  <td>{{ stock.code }}</td>
                  <td>¥{{ stock.current_price.toFixed(2) }}</td>
                  <td>
                    <span :style="{ color: stock.change_percent >= 0 ? '#F56C6C' : '#67C23A' }">
                      {{ stock.change_percent >= 0 ? '+' : '' }}{{ stock.change_percent.toFixed(2) }}%
                    </span>
                  </td>
                  <td>
                    <button class="btn btn-sm btn-text" @click="viewStockDetail(stock)">查看</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- 模拟交易对话框 -->
    <div v-if="tradeDialogVisible" class="modal-overlay" @click="tradeDialogVisible = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>模拟交易</h3>
          <button class="close-btn" @click="tradeDialogVisible = false">×</button>
        </div>
        <div class="modal-body" v-if="selectedStock">
          <div class="form-group">
            <label>交易类型:</label>
            <div class="radio-group">
              <label class="radio-label">
                <input type="radio" v-model="tradeForm.type" value="buy">
                <span>买入</span>
              </label>
              <label class="radio-label">
                <input type="radio" v-model="tradeForm.type" value="sell">
                <span>卖出</span>
              </label>
            </div>
          </div>
          <div class="form-group">
            <label>交易数量:</label>
            <input 
              type="number" 
              v-model.number="tradeForm.quantity" 
              :min="100"
              :step="100"
              class="input"
            />
            <div class="help-text">
              最小交易单位: 100股
            </div>
          </div>
          <div class="form-group">
            <label>当前价格:</label>
            <span>¥{{ selectedStock.current_price.toFixed(2) }}</span>
          </div>
          <div class="form-group">
            <label>总金额:</label>
            <span class="highlight-primary">
              ¥{{ (tradeForm.quantity * selectedStock.current_price).toFixed(2) }}
            </span>
          </div>
          <div class="modal-footer">
            <button class="btn" @click="tradeDialogVisible = false">取消</button>
            <button class="btn btn-primary" @click="confirmTrade">确认交易</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Stocks',
  data() {
    return {
      stocks: [],
      filteredStocks: [],
      loading: false,
      currentPage: 1,
      pageSize: 10,
      totalStocks: 0,
      
      filterIndustry: '',
      filterTrend: '',
      
      detailDialogVisible: false,
      selectedStock: null,
      similarStocks: [],
      
      tradeDialogVisible: false,
      tradeForm: {
        type: 'buy',
        quantity: 100
      }
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.totalStocks / this.pageSize)
    },
    paginatedStocks() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredStocks.slice(start, end)
    }
  },
  async mounted() {
    await this.loadStocks()
  },
  methods: {
    async loadStocks() {
      this.loading = true
      try {
        // 模拟API调用获取股票数据
        this.stocks = [
          {
            id: 1,
            name: '腾讯控股',
            code: '00700',
            industry: '科技',
            current_price: 320.50,
            change_percent: 2.15,
            pe_ratio: 25.8,
            market_cap: 3800000000000,
            high_52w: 450.00,
            low_52w: 280.00,
            trend: 'up',
            description: '中国领先的互联网增值服务提供商，主要业务包括社交、游戏、数字内容等。',
            recommendation_score: 4.3
          },
          {
            id: 2,
            name: '贵州茅台',
            code: '600519',
            industry: '消费',
            current_price: 1680.00,
            change_percent: -1.25,
            pe_ratio: 35.2,
            market_cap: 2100000000000,
            high_52w: 2000.00,
            low_52w: 1500.00,
            trend: 'sideways',
            description: '中国白酒行业的龙头企业，以生产茅台酒闻名。',
            recommendation_score: 4.1
          },
          {
            id: 3,
            name: '招商银行',
            code: '600036',
            industry: '金融',
            current_price: 32.80,
            change_percent: 0.92,
            pe_ratio: 8.5,
            market_cap: 850000000000,
            high_52w: 40.00,
            low_52w: 28.00,
            trend: 'up',
            description: '中国领先的商业银行之一，以零售业务和财富管理见长。',
            recommendation_score: 4.0
          },
          {
            id: 4,
            name: '宁德时代',
            code: '300750',
            industry: '能源',
            current_price: 185.60,
            change_percent: 3.45,
            pe_ratio: 42.3,
            market_cap: 820000000000,
            high_52w: 220.00,
            low_52w: 160.00,
            trend: 'up',
            description: '全球领先的动力电池系统提供商，专注于新能源汽车动力电池系统。',
            recommendation_score: 4.5
          },
          {
            id: 5,
            name: '恒瑞医药',
            code: '600276',
            industry: '医疗',
            current_price: 45.20,
            change_percent: -0.88,
            pe_ratio: 38.7,
            market_cap: 290000000000,
            high_52w: 60.00,
            low_52w: 40.00,
            trend: 'down',
            description: '中国领先的创新型制药企业，专注于抗肿瘤药、手术用药等。',
            recommendation_score: 3.8
          }
        ]

        // 应用筛选
        this.applyFilters()
        this.totalStocks = this.filteredStocks.length
        
      } catch (error) {
        console.error('加载股票数据失败:', error)
      } finally {
        this.loading = false
      }
    },

    applyFilters() {
      let filtered = [...this.stocks]
      
      if (this.filterIndustry) {
        filtered = filtered.filter(stock => stock.industry === this.filterIndustry)
      }
      
      if (this.filterTrend) {
        filtered = filtered.filter(stock => stock.trend === this.filterTrend)
      }
      
      this.filteredStocks = filtered
    },

    formatMarketCap(cap) {
      if (cap >= 1000000000000) {
        return (cap / 1000000000000).toFixed(2) + '万亿'
      } else if (cap >= 100000000) {
        return (cap / 100000000).toFixed(2) + '亿'
      } else {
        return cap.toLocaleString()
      }
    },

    getTrendTagClass(trend) {
      const classMap = {
        'up': 'tag-success',
        'down': 'tag-danger',
        'sideways': 'tag-warning'
      }
      return classMap[trend] || 'tag-info'
    },

    getTrendText(trend) {
      const textMap = {
        'up': '上涨',
        'down': '下跌',
        'sideways': '震荡'
      }
      return textMap[trend] || '未知'
    },

    async viewStockDetail(stock) {
      this.selectedStock = stock
      this.detailDialogVisible = true
      
      // 模拟获取相似股票
      this.similarStocks = this.stocks
        .filter(s => s.id !== stock.id && s.industry === stock.industry)
        .slice(0, 3)
    },

    simulateTrade(stock) {
      this.selectedStock = stock
      this.tradeForm.quantity = 100
      this.tradeDialogVisible = true
    },

    confirmTrade() {
      const action = this.tradeForm.type === 'buy' ? '买入' : '卖出'
      const totalAmount = this.tradeForm.quantity * this.selectedStock.current_price
      alert(`成功${action} ${this.tradeForm.quantity}股${this.selectedStock.name}，总金额 ¥${totalAmount.toFixed(2)}`)
      this.tradeDialogVisible = false
    },

    handleSizeChange() {
      this.currentPage = 1
    }
  }
}
</script>

<style scoped>
.stocks {
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

.tag-danger {
  background: #f56c6c;
}

.tag-warning {
  background: #e6a23c;
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

.radio-group {
  display: flex;
  gap: 20px;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
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

.highlight-primary {
  color: #409eff;
  font-weight: bold;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #909399;
}
</style>
