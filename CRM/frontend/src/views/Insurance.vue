<template>
  <div class="insurance">
    <div class="card">
      <div class="card-header">
        <div class="header-content">
          <span class="title">保险推荐</span>
          <div class="filter-section">

          </div>
        </div>
      </div>

      <div class="insurance-grid-container">
        <div class="insurance-grid" v-if="!loading">
          <div class="insurance-card" v-for="insurance in paginatedInsurance" :key="insurance.id">
            <img :src="insurance.image" alt="Insurance Image" class="insurance-image">
            <div class="card-content">
              <h3 class="insurance-name">{{ insurance.name }}</h3>
              <p class="insurance-company">{{ insurance.company }}</p>
              <div class="tags">
                <span class="tag">{{ insurance.type }}</span>
                <span :class="['tag', getCoverageTagClass(insurance.coverage)]">
                  {{ insurance.coverage }}
                </span>
              </div>
              <div class="info-row">
                <span>年保费:</span>
                <span class="price">¥{{ insurance.premium.toLocaleString() }}</span>
              </div>
              <div class="info-row">
                <span>保障金额:</span>
                <span>¥{{ insurance.coverage_amount.toLocaleString() }}</span>
              </div>
            </div>
            <div class="card-actions">
              <button class="btn btn-sm btn-primary" @click="viewInsuranceDetail(insurance)">
                查看详情
              </button>
              <button class="btn btn-sm btn-success" @click="purchaseInsurance(insurance)">
                购买保险
              </button>
            </div>
            <div class="insurance-details-tooltip">
              <h4>{{ insurance.name }}</h4>
              <p><strong>保障期限:</strong> {{ insurance.term }}年</p>
              <p><strong>适用年龄:</strong> {{ insurance.age_range }}</p>
              <p><strong>等待期:</strong> {{ insurance.waiting_period }}天</p>
              <p><strong>保险描述:</strong> {{ insurance.description }}</p>
            </div>
          </div>
        </div>
        <div v-if="loading" class="loading">加载中...</div>
      </div>

      <!-- 分页 -->
      <div class="pagination-container">
        <div class="pagination-info">
          共 {{ totalInsurance }} 条记录
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

    <!-- 保险详情对话框 -->
    <div v-if="detailDialogVisible" class="modal-overlay" @click="detailDialogVisible = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>保险详情</h3>
          <button class="close-btn" @click="detailDialogVisible = false">×</button>
        </div>
        <div class="modal-body" v-if="selectedInsurance">
          <div class="detail-grid">
            <div class="detail-item">
              <label>保险名称:</label>
              <span>{{ selectedInsurance.name }}</span>
            </div>
            <div class="detail-item">
              <label>保险公司:</label>
              <span>{{ selectedInsurance.company }}</span>
            </div>
            <div class="detail-item">
              <label>保险类型:</label>
              <span>{{ selectedInsurance.type }}</span>
            </div>
            <div class="detail-item">
              <label>保障范围:</label>
              <span :class="['tag', getCoverageTagClass(selectedInsurance.coverage)]">
                {{ selectedInsurance.coverage }}
              </span>
            </div>
            <div class="detail-item">
              <label>年保费:</label>
              <span>¥{{ selectedInsurance.premium.toLocaleString() }}</span>
            </div>
            <div class="detail-item">
              <label>保障金额:</label>
              <span>¥{{ selectedInsurance.coverage_amount.toLocaleString() }}</span>
            </div>
            <div class="detail-item">
              <label>保障期限:</label>
              <span>{{ selectedInsurance.term }}年</span>
            </div>
            <div class="detail-item">
              <label>适用年龄:</label>
              <span>{{ selectedInsurance.age_range }}</span>
            </div>
            <div class="detail-item">
              <label>等待期:</label>
              <span>{{ selectedInsurance.waiting_period }}天</span>
            </div>
            <div class="detail-item full-width">
              <label>保险描述:</label>
              <span>{{ selectedInsurance.description }}</span>
            </div>
            <div class="detail-item full-width">
              <label>保障内容:</label>
              <div class="coverage-list">
                <div v-for="(item, index) in selectedInsurance.coverage_details" :key="index" class="coverage-item">
                  • {{ item }}
                </div>
              </div>
            </div>
          </div>

          <!-- 相似保险推荐 -->
          <div class="similar-section">
            <h4>相似保险推荐</h4>
            <table class="table table-sm">
              <thead>
                <tr>
                  <th>保险名称</th>
                  <th>公司</th>
                  <th>年保费</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="insurance in similarInsurance" :key="insurance.id">
                  <td>{{ insurance.name }}</td>
                  <td>{{ insurance.company }}</td>
                  <td>¥{{ insurance.premium.toLocaleString() }}</td>
                  <td>
                    <button class="btn btn-sm btn-text" @click="viewInsuranceDetail(insurance)">查看</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- 模拟购买对话框 -->
    <div v-if="purchaseDialogVisible" class="modal-overlay" @click="purchaseDialogVisible = false">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>模拟购买</h3>
          <button class="close-btn" @click="purchaseDialogVisible = false">×</button>
        </div>
        <div class="modal-body" v-if="selectedInsurance">
          <div class="form-group">
            <label>投保人:</label>
            <input type="text" v-model="purchaseForm.insured_name" placeholder="请输入投保人姓名" class="input" />
          </div>
          <div class="form-group">
            <label>投保年龄:</label>
            <input type="number" v-model.number="purchaseForm.insured_age" :min="18" :max="65" class="input" />
          </div>
          <div class="form-group">
            <label>保障期限:</label>
            <span>{{ selectedInsurance.term }}年</span>
          </div>
          <div class="form-group">
            <label>年保费:</label>
            <span class="highlight-primary">
              ¥{{ selectedInsurance.premium.toLocaleString() }}
            </span>
          </div>
          <div class="form-group">
            <label>总保费:</label>
            <span class="highlight-success">
              ¥{{ (selectedInsurance.premium * selectedInsurance.term).toLocaleString() }}
            </span>
          </div>
          <div class="modal-footer">
            <button class="btn" @click="purchaseDialogVisible = false">取消</button>
            <button class="btn btn-primary" @click="confirmPurchase">确认购买</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from '../api'

export default {
  name: 'Insurance',
  data() {
    return {
      images: [
        '家庭1.png', '家庭2.png', '家庭3.png', '家庭4.png',
        '汽车1.png', '汽车2.png', '汽车3.png', '汽车4.png',
        '运动1.png', '运动2.png', '运动3.png', '运动4.png',
        '职场4.png', '职场男性1.png', '职场男性2.png', '职场男性3.png', '职场男性4.png',
        '职场女性1.png', '职场女性2.png', '职场女性3.png'
      ],
      insurance: [],
      filteredInsurance: [],   // ✅ 加上这个
      loading: false,
      currentPage: 1,
      pageSize: 10,
      totalInsurance: 0,

      filterType: '',
      filterCoverage: '',

      detailDialogVisible: false,
      selectedInsurance: null,
      similarInsurance: [],

      purchaseDialogVisible: false,
      purchaseForm: {
        insured_name: '',
        insured_age: 30
      }
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.totalInsurance / this.pageSize)
    },
    paginatedInsurance() {
      return this.filteredInsurance   // ✅ 用过滤后的数据
    }
  },
  async mounted() {
    await this.loadInsurance()
  },
  methods: {
    async loadInsurance() {
      this.loading = true
      try {
        // 调用 API，传递分页和筛选参数
        const response = await apiService.getInsuranceProducts({
          page: this.currentPage,
          page_size: this.pageSize,
          type: this.filterType || undefined,
          coverage: this.filterCoverage || undefined
        })

        if (response && response.results) {
          this.insurance = response.results.map(insurance => ({
            image: `/images/${this.images[Math.floor(Math.random() * this.images.length)]}`,
            id: insurance.id,
            name: insurance.name,
            company: this.extractCompany(insurance.name),
            type: insurance.category,
            coverage: this.calculateCoverage(insurance),
            premium: this.calculatePremium(insurance),
            coverage_amount: this.calculateCoverageAmount(insurance),
            term: this.calculateTerm(insurance),
            age_range: this.calculateAgeRange(insurance),
            waiting_period: this.calculateWaitingPeriod(insurance),
            description: insurance.coverage_summary,
            coverage_details: this.parseCoverageDetails(insurance),
            recommendation_score: this.calculateRecommendationScore(insurance)
          }))
          this.totalInsurance = response.count || 0
          this.applyFilters()   // ✅ 加上
        } else {
          this.insurance = []
          this.totalInsurance = 0
        }
      } catch (error) {
        console.error('加载保险数据失败:', error)
        this.insurance = []
        this.totalInsurance = 0
      } finally {
        this.loading = false
      }
    },

    // 从保险名称中提取公司名称
    extractCompany(name) {
      const companies = ['平安', '人寿', '太平洋', '太平', '新华', '泰康', '友邦']
      for (const company of companies) {
        if (name.includes(company)) {
          return company + '保险'
        }
      }
      return '未知保险公司'
    },

    // 根据保险类型计算保障范围
    calculateCoverage(insurance) {
      const coverageMap = {
        '人寿保险': '全面',
        '健康保险': '全面',
        '意外保险': '基础',
        '财产保险': '基础',
        '养老保险': '高端'
      }
      return coverageMap[insurance.category] || '基础'
    },

    // 计算保费
    calculatePremium(insurance) {
      const basePremium = insurance.base_premium
      if (basePremium && basePremium.includes('元')) {
        const match = basePremium.match(/(\d+)元/)
        if (match) {
          return parseInt(match[1])
        }
      }
      // 根据保险类型返回默认保费
      const defaultPremiums = {
        '人寿保险': 5000,
        '健康保险': 8000,
        '意外保险': 300,
        '财产保险': 800,
        '养老保险': 20000
      }
      return defaultPremiums[insurance.category] || 1000
    },

    // 计算保障金额
    calculateCoverageAmount(insurance) {
      const payout = insurance.payout_limit
      if (payout && payout.includes('万')) {
        const match = payout.match(/(\d+)万/)
        if (match) {
          return parseInt(match[1]) * 10000
        }
      }
      // 根据保险类型返回默认保障金额
      const defaultAmounts = {
        '人寿保险': 1000000,
        '健康保险': 500000,
        '意外保险': 200000,
        '财产保险': 500000,
        '养老保险': 1000000
      }
      return defaultAmounts[insurance.category] || 100000
    },

    // 计算保障期限
    calculateTerm(insurance) {
      // 从保险描述中提取期限
      const coverage = insurance.coverage_summary
      if (coverage && coverage.includes('年')) {
        const match = coverage.match(/(\d+)年/)
        if (match) {
          return parseInt(match[1])
        }
      }
      // 根据保险类型返回默认期限
      const defaultTerms = {
        '人寿保险': 30,
        '健康保险': 20,
        '意外保险': 1,
        '财产保险': 1,
        '养老保险': 20
      }
      return defaultTerms[insurance.category] || 10
    },

    // 计算适用年龄范围
    calculateAgeRange(insurance) {
      const basePremium = insurance.base_premium
      if (basePremium && basePremium.includes('岁')) {
        const match = basePremium.match(/(\d+)-(\d+)岁/)
        if (match) {
          return `${match[1]}-${match[2]}岁`
        }
      }
      // 根据保险类型返回默认年龄范围
      const defaultRanges = {
        '人寿保险': '18-60岁',
        '健康保险': '18-55岁',
        '意外保险': '18-65岁',
        '财产保险': '不限',
        '养老保险': '30-50岁'
      }
      return defaultRanges[insurance.category] || '18-60岁'
    },

    // 计算等待期
    calculateWaitingPeriod(insurance) {
      // 根据保险类型返回默认等待期
      const defaultPeriods = {
        '人寿保险': 90,
        '健康保险': 180,
        '意外保险': 0,
        '财产保险': 0,
        '养老保险': 0
      }
      return defaultPeriods[insurance.category] || 90
    },

    // 解析保障内容详情
    parseCoverageDetails(insurance) {
      const details = []
      if (insurance.coverage_summary) {
        details.push(insurance.coverage_summary)
      }
      if (insurance.payout_limit) {
        details.push(`赔付上限: ${insurance.payout_limit}`)
      }
      if (insurance.deductible_and_ratio) {
        details.push(`免赔额: ${insurance.deductible_and_ratio}`)
      }
      if (insurance.tags) {
        details.push(`特色: ${insurance.tags}`)
      }
      return details.length > 0 ? details : ['详细保障内容请咨询保险公司']
    },

    // 计算推荐分数
    calculateRecommendationScore(insurance) {
      let score = 3.0

      // 根据保险类型加分
      const typeBonus = {
        '健康保险': 0.5,
        '人寿保险': 0.3,
        '养老保险': 0.4,
        '意外保险': 0.2,
        '财产保险': 0.1
      }
      score += typeBonus[insurance.category] || 0

      // 根据标签加分
      if (insurance.tags) {
        const tags = insurance.tags.split(',')
        if (tags.includes('热门') || tags.includes('推荐')) {
          score += 0.3
        }
        if (tags.includes('保障全面')) {
          score += 0.2
        }
      }

      return Math.min(score, 5.0)
    },

    applyFilters() {
      let filtered = [...this.insurance]

      if (this.filterType) {
        filtered = filtered.filter(item => item.type === this.filterType)
      }

      if (this.filterCoverage) {
        filtered = filtered.filter(item => item.coverage === this.filterCoverage)
      }

      this.filteredInsurance = filtered
    },

    getCoverageTagClass(coverage) {
      const classMap = {
        '基础': 'tag-info',
        '全面': 'tag-warning',
        '高端': 'tag-success'
      }
      return classMap[coverage] || 'tag-info'
    },

    viewInsuranceDetail(insurance) {
      this.selectedInsurance = insurance
      this.detailDialogVisible = true

      // 模拟获取相似保险
      this.similarInsurance = this.insurance
        .filter(item => item.id !== insurance.id && item.type === insurance.type)
        .slice(0, 3)
    },

    async purchaseInsurance(insurance) {
      this.selectedInsurance = insurance
      this.purchaseForm.insured_name = ''
      this.purchaseForm.insured_age = 30
      this.purchaseDialogVisible = true
    },

    async confirmPurchase() {
      if (!this.purchaseForm.insured_name) {
        alert('请输入投保人姓名')
        return
      }

      try {
        const totalPremium = this.selectedInsurance.premium * this.selectedInsurance.term
        const purchaseData = {
          product_type: 'insurance',
          product_id: this.selectedInsurance.id,
          amount: totalPremium,
          quantity: this.selectedInsurance.term // 保障期限作为数量
        }

        const response = await apiService.purchaseProduct(purchaseData)

        if (response.success) {
          alert(`成功为${this.purchaseForm.insured_name}购买${this.selectedInsurance.name}，总保费 ¥${totalPremium.toLocaleString()}`)
          this.purchaseDialogVisible = false
        } else {
          alert(`购买失败: ${response.message}`)
        }
      } catch (error) {
        console.error('购买保险失败:', error)
        alert('购买失败，请稍后重试')
      }
    },

    async changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
        await this.loadInsurance()
      }
    },
    async handleSizeChange() {
      this.currentPage = 1
      await this.loadInsurance()
    }

  }
}
</script>

<style scoped>
.insurance-grid-container {
  padding: 20px;
}

.insurance-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.insurance-image {
  width: 100%;
  height: 150px;
  object-fit: contain;
}

.insurance-card {
  position: relative;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: transform 0.3s, box-shadow 0.3s;
}

.insurance-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.insurance-card:hover .insurance-details-tooltip {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.card-content {
  padding: 20px;
}

.insurance-name {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: #303133;
}

.insurance-company {
  font-size: 12px;
  color: #909399;
  margin: 0 0 12px 0;
}

.tags {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
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

.insurance-details-tooltip {
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

.insurance-details-tooltip h4 {
  margin: 0 0 10px 0;
  font-size: 16px;
}

.insurance-details-tooltip p {
  margin: 0 0 8px 0;
  font-size: 14px;
  line-height: 1.6;
}

.insurance {
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

.loading {
  text-align: center;
  padding: 40px;
  color: #909399;
}

.pagination-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-top: 1px solid #ebeef5;
}

.pagination-info {
  color: #606266;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.page-info {
  color: #606266;
  margin: 0 10px;
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
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #ebeef5;
}

.modal-header h3 {
  margin: 0;
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

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 20px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-item label {
  font-weight: 600;
  color: #606266;
  font-size: 14px;
}

.detail-item span {
  color: #303133;
}

.full-width {
  grid-column: 1 / -1;
}

.coverage-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.coverage-item {
  color: #606266;
}

.similar-section {
  border-top: 1px solid #ebeef5;
  padding-top: 20px;
}

.similar-section h4 {
  margin: 0 0 16px 0;
  color: #303133;
}

.form-group {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.form-group label {
  width: 100px;
  font-weight: 600;
  color: #606266;
}

.input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}

.input:focus {
  outline: none;
  border-color: #409eff;
}

.highlight-primary {
  color: #409eff;
  font-weight: 600;
}

.highlight-success {
  color: #67c23a;
  font-weight: 600;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

.tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.tag-info {
  background: #f4f4f5;
  color: #909399;
}

.tag-warning {
  background: #fdf6ec;
  color: #e6a23c;
}

.tag-success {
  background: #f0f9eb;
  color: #67c23a;
}

.rating {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stars {
  display: flex;
}

.star {
  color: #dcdfe6;
  font-size: 14px;
}

.star.active {
  color: #f7ba2a;
}

.score {
  color: #909399;
  font-size: 12px;
}
</style>
