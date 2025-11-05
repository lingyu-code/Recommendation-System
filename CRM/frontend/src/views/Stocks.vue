<template>
    <div class="stocks">
        <div class="card">
            <div class="card-header">
                <div class="header-content">
                    <span class="title">股票推荐</span>
                    <div class="filter-section">

                    </div>
                </div>
            </div>

            <div class="stock-grid-container">
                <div class="stock-grid" v-if="!loading">
                    <div class="stock-card" v-for="stock in paginatedStocks" :key="stock.id">
                        <div class="card-content">
                            <h3 class="stock-name">{{ stock.name }} ({{ stock.code }})</h3>
                            <p class="stock-industry">{{ stock.industry }}</p>
                            <div class="info-row">
                                <span>当前价格:</span>
                                <span class="price">¥{{ stock.current_price.toFixed(2) }}</span>
                            </div>
                            <div class="info-row">
                                <span>涨跌幅:</span>
                                <span :style="{ color: stock.change_percent >= 0 ? '#F56C6C' : '#67C23A' }">
                                    {{ stock.change_percent >= 0 ? '+' : '' }}{{ stock.change_percent.toFixed(2) }}%
                                </span>
                            </div>
                            <div class="info-row">
                                <span>市盈率:</span>
                                <span>{{ stock.pe_ratio.toFixed(2) }}</span>
                            </div>
                            <div class="info-row">
                                <span>市值:</span>
                                <span>{{ formatMarketCap(stock.market_cap) }}</span>
                            </div>
                        </div>
                        <div class="card-actions">
                            <button class="btn btn-sm btn-primary" @click="viewStockDetail(stock)">
                                查看详情
                            </button>
                            <button class="btn btn-sm btn-success" @click="purchaseStock(stock)">
                                购买股票
                            </button>
                        </div>
                        <div class="stock-details-tooltip">
                            <h4>{{ stock.name }}</h4>
                            <p><strong>52周最高:</strong> ¥{{ stock.high_52w.toFixed(2) }}</p>
                            <p><strong>52周最低:</strong> ¥{{ stock.low_52w.toFixed(2) }}</p>
                            <p><strong>公司简介:</strong> {{ stock.description }}</p>
                        </div>
                    </div>
                </div>
                <div v-if="loading" class="loading">加载中...</div>
            </div>

            <!-- 分页 -->
            <div class="pagination-container">
                <div class="pagination-info">
                    共 {{ totalStocks }} 条记录
                </div>
                <div class="pagination-controls">

                    <button class="btn btn-sm" :disabled="currentPage === 1" @click="changePage(currentPage - 1)">
                        上一页
                    </button>

                    <span class="page-info">
                        第 {{ currentPage }} 页 / 共 {{ totalPages }} 页
                    </span>

                    <button class="btn btn-sm" :disabled="currentPage === totalPages"
                        @click="changePage(currentPage + 1)">
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
                                {{ selectedStock.change_percent >= 0 ? '+' : '' }}{{
                                    selectedStock.change_percent.toFixed(2) }}%
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
                                            {{ stock.change_percent >= 0 ? '+' : '' }}{{ stock.change_percent.toFixed(2)
                                            }}%
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

        <!-- 股票交易对话框 -->
        <div v-if="tradeDialogVisible" class="modal-overlay" @click="tradeDialogVisible = false">
            <div class="modal" @click.stop>
                <div class="modal-header">
                    <h3>股票交易</h3>
                    <button class="close-btn" @click="tradeDialogVisible = false">×</button>
                </div>
                <div class="modal-body" v-if="selectedStock">
                    <div class="form-group">
                        <label>投保人姓名:</label>
                        <input type="text" v-model="tradeForm.policyholder_name" class="input" placeholder="请输入投保人姓名" />
                    </div>
                    <div class="form-group">
                        <label>交易方向:</label>
                        <div class="radio-group">
                            <label class="radio-label">
                                <input type="radio" v-model="tradeForm.direction" value="buy">
                                <span>买入</span>
                            </label>
                            <label class="radio-label">
                                <input type="radio" v-model="tradeForm.direction" value="sell">
                                <span>卖出</span>
                            </label>
                        </div>
                    </div>
                    <div class="form-group">
                        <label>交易数量:</label>
                        <input type="number" v-model.number="tradeForm.quantity" :min="100" :step="100" class="input" />
                        <div class="help-text">
                            最小交易单位: 100股
                        </div>
                    </div>
                    <div class="form-group">
                        <label>股票名称:</label>
                        <span>{{ selectedStock.name }}</span>
                    </div>
                    <div class="form-group">
                        <label>股票代码:</label>
                        <span>{{ selectedStock.code }}</span>
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
import { apiService } from '../api'

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
                policyholder_name: '',
                direction: 'buy',
                quantity: 100
            }
        }
    },
    computed: {
        totalPages() {
            return Math.ceil(this.totalStocks / this.pageSize)
        },
        paginatedStocks() {
            return this.filteredStocks
        }
    },
    async mounted() {
        await this.loadStocks()
    },
    methods: {
        async loadStocks() {
            this.loading = true
            try {
                // 调用 API，传递分页和筛选参数
                const response = await apiService.getStocks({
                    page: this.currentPage,
                    page_size: this.pageSize,
                    industry: this.filterIndustry || undefined,
                    trend: this.filterTrend || undefined
                })

                console.log('API Response:', response)

                if (response && response.results) {
                    // 使用后端返回的真实 StockInfo 数据
                    this.stocks = response.results.map(stock => ({
                        id: stock.id,
                        name: stock.name,
                        code: stock.symbol,
                        industry: stock.industry,
                        // 这些字段在StockInfo模型中不存在，使用默认值显示
                        current_price: 50.0,  // 默认值，实际应该从StockDailyData获取
                        change_percent: 0.0,  // 默认值
                        pe_ratio: 15.0,      // 默认值
                        market_cap: 10000000000, // 默认值
                        high_52w: 60.0,      // 默认值
                        low_52w: 40.0,       // 默认值
                        trend: 'up',         // 默认值
                        description: `${stock.name}是${stock.area}地区${stock.industry}行业的上市公司，于${stock.list_date}上市。`,
                        recommendation_score: 4.0
                    }))
                    console.log('Processed stocks:', this.stocks.slice(0, 3))
                    this.totalStocks = response.count || 0
                    this.applyFilters()
                } else {
                    this.stocks = []
                    this.totalStocks = 0
                }
            } catch (error) {
                console.error('加载股票数据失败:', error)
                this.stocks = []
                this.totalStocks = 0
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

        async purchaseStock(stock) {
            this.selectedStock = stock
            this.tradeForm.quantity = 100
            this.tradeDialogVisible = true
        },

        async confirmTrade() {
            try {
                // 验证必填字段
                if (!this.tradeForm.policyholder_name) {
                    alert('请输入投保人姓名')
                    return
                }

                if (this.tradeForm.quantity < 100) {
                    alert('交易数量不能少于100股')
                    return
                }

                // 使用新的股票交易API，不依赖前端计算
                const purchaseData = {
                    policyholder_name: this.tradeForm.policyholder_name,
                    quantity: this.tradeForm.quantity,
                    direction: this.tradeForm.direction,
                    stock_id: this.selectedStock.id
                }

                console.log('Stock purchase data:', purchaseData)
                console.log('Selected stock:', this.selectedStock)

                const response = await apiService.purchaseStock(purchaseData)

                // 不再依赖 response.success 字段，直接检查响应数据
                if (response && response.message) {
                    const action = this.tradeForm.direction === 'buy' ? '买入' : '卖出'
                    const totalAmount = response.transaction?.total_amount || 0
                    alert(`${response.message}\n${action} ${this.tradeForm.quantity}股${this.selectedStock.name}，总金额 ¥${totalAmount.toFixed(2)}`)
                    this.tradeDialogVisible = false

                    // 重置表单
                    this.tradeForm.policyholder_name = ''
                    this.tradeForm.quantity = 100
                } else {
                    alert(`交易失败: ${response?.message || '未知错误'}`)
                }
            } catch (error) {
                console.error('股票交易失败:', error)
                console.error('Error details:', error.response?.data)
                const errorMessage = error.response?.data?.message || error.response?.data?.errors || '交易失败，请稍后重试'
                alert(`交易失败: ${errorMessage}`)
            }
        },

        handleSizeChange() {
            this.currentPage = 1
        },
        async changePage(page) {
            if (page >= 1 && page <= this.totalPages) {
                this.currentPage = page
                await this.loadStocks()
            }
        },
        async handleSizeChange() {
            this.currentPage = 1
            await this.loadStocks()
        }
    }
}
</script>

<style scoped>
.stock-grid-container {
    padding: 20px;
}

.stock-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
}

.stock-card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 0.3s, box-shadow 0.3s;
}

.stock-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.card-content {
    padding: 20px;
}

.stock-name {
    font-size: 16px;
    font-weight: 600;
    margin: 0 0 8px 0;
    color: #303133;
}

.stock-industry {
    font-size: 12px;
    color: #909399;
    margin: 0 0 12px 0;
}

.info-row {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    color: #606266;
    margin-bottom: 8px;
}

.info-row .price {
    font-weight: 600;
    color: #e6a23c;
}

.card-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    padding: 0 20px 20px 20px;
    border-top: 1px solid #ebeef5;
    padding-top: 15px;
    margin-top: 15px;
}

.stock-details-tooltip {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 60px;
    /* Adjust this value to leave space for the action buttons */
    background: rgba(255, 255, 255, 0.98);
    padding: 20px;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.3s, visibility 0.3s, transform 0.3s;
    transform: translateY(10px);
    overflow-y: auto;
    color: #303133;
}

.stock-card:hover .stock-details-tooltip {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}

.stock-details-tooltip h4 {
    margin: 0 0 10px 0;
    font-size: 16px;
}

.stock-details-tooltip p {
    margin: 0 0 8px 0;
    font-size: 14px;
    line-height: 1.6;
}

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
