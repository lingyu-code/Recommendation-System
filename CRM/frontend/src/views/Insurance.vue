<template>
  <div class="insurance">
    <div class="card">
      <div class="card-header">
        <div class="header-content">
          <span class="title">保险推荐</span>
          <div class="filter-section">
            <select v-model="filterType" class="select">
              <option value="">保险类型</option>
              <option value="人寿保险">人寿保险</option>
              <option value="健康保险">健康保险</option>
              <option value="意外保险">意外保险</option>
              <option value="财产保险">财产保险</option>
              <option value="养老保险">养老保险</option>
            </select>
            
            <select v-model="filterCoverage" class="select">
              <option value="">保障范围</option>
              <option value="基础">基础</option>
              <option value="全面">全面</option>
              <option value="高端">高端</option>
            </select>
            
            <button class="btn btn-primary" @click="loadInsurance">筛选</button>
          </div>
        </div>
      </div>

      <div class="table-container">
        <table class="table" v-if="!loading">
          <thead>
            <tr>
              <th>保险名称</th>
              <th>保险公司</th>
              <th>保险类型</th>
              <th>保障范围</th>
              <th>年保费</th>
              <th>保障金额</th>
              <th>保障期限</th>
              <th>适用年龄</th>
              <th>推荐指数</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="insurance in paginatedInsurance" :key="insurance.id">
              <td>{{ insurance.name }}</td>
              <td>{{ insurance.company }}</td>
              <td>{{ insurance.type }}</td>
              <td>
                <span :class="['tag', getCoverageTagClass(insurance.coverage)]">
                  {{ insurance.coverage }}
                </span>
              </td>
              <td>¥{{ insurance.premium.toLocaleString() }}</td>
              <td>¥{{ insurance.coverage_amount.toLocaleString() }}</td>
              <td>{{ insurance.term }}年</td>
              <td>{{ insurance.age_range }}</td>
              <td>
                <div class="rating">
                  <span class="stars">
                    <span v-for="n in 5" :key="n" class="star" :class="{ active: n <= Math.floor(insurance.recommendation_score) }">
                      ★
                    </span>
                  </span>
                  <span class="score">{{ insurance.recommendation_score }}分</span>
                </div>
              </td>
              <td>
                <button class="btn btn-sm btn-primary" @click="viewInsuranceDetail(insurance)">
                  查看详情
                </button>
                <button class="btn btn-sm btn-success" @click="simulatePurchase(insurance)">
                  模拟购买
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
          共 {{ totalInsurance }} 条记录
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
            <input 
              type="text" 
              v-model="purchaseForm.insured_name" 
              placeholder="请输入投保人姓名"
              class="input"
            />
          </div>
          <div class="form-group">
            <label>投保年龄:</label>
            <input 
              type="number" 
              v-model.number="purchaseForm.insured_age" 
              :min="18"
              :max="65"
              class="input"
            />
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
export default {
  name: 'Insurance',
  data() {
    return {
      insurance: [],
      filteredInsurance: [],
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
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredInsurance.slice(start, end)
    }
  },
  mounted() {
    this.loadInsurance()
  },
  methods: {
    loadInsurance() {
      this.loading = true
      try {
        // 模拟保险数据
        this.insurance = [
          {
            id: 1,
            name: '平安福终身寿险',
            company: '平安保险',
            type: '人寿保险',
            coverage: '全面',
            premium: 5000,
            coverage_amount: 1000000,
            term: 30,
            age_range: '18-60岁',
            waiting_period: 90,
            description: '提供终身保障的人寿保险产品，包含身故、全残保障。',
            coverage_details: [
              '身故保障100万元',
              '全残保障100万元',
              '重大疾病提前给付',
              '意外身故双倍赔付'
            ],
            recommendation_score: 4.2
          },
          {
            id: 2,
            name: '康宁终身重疾险',
            company: '中国人寿',
            type: '健康保险',
            coverage: '全面',
            premium: 8000,
            coverage_amount: 500000,
            term: 20,
            age_range: '18-55岁',
            waiting_period: 180,
            description: '覆盖120种重大疾病的终身健康保险，提供全面的健康保障。',
            coverage_details: [
              '120种重大疾病保障',
              '轻症疾病额外赔付',
              '疾病终末期保障',
              '保费豁免功能'
            ],
            recommendation_score: 4.5
          },
          {
            id: 3,
            name: '意外伤害综合保险',
            company: '太平洋保险',
            type: '意外保险',
            coverage: '基础',
            premium: 300,
            coverage_amount: 200000,
            term: 1,
            age_range: '18-65岁',
            waiting_period: 0,
            description: '提供意外伤害、意外医疗、意外住院津贴等综合保障。',
            coverage_details: [
              '意外身故20万元',
              '意外伤残最高20万元',
              '意外医疗2万元',
              '意外住院津贴100元/天'
            ],
            recommendation_score: 4.0
          },
          {
            id: 4,
            name: '家财综合保险',
            company: '太平保险',
            type: '财产保险',
            coverage: '基础',
            premium: 800,
            coverage_amount: 500000,
            term: 1,
            age_range: '不限',
            waiting_period: 0,
            description: '为家庭财产提供火灾、盗窃、水渍等风险保障。',
            coverage_details: [
              '房屋主体保障50万元',
              '室内财产保障10万元',
              '盗抢险保障5万元',
              '管道破裂水渍险'
            ],
            recommendation_score: 3.8
          },
          {
            id: 5,
            name: '养老年金保险',
            company: '新华保险',
            type: '养老保险',
            coverage: '高端',
            premium: 20000,
            coverage_amount: 1000000,
            term: 20,
            age_range: '30-50岁',
            waiting_period: 0,
            description: '为退休生活提供稳定现金流，确保晚年生活质量。',
            coverage_details: [
              '60岁开始领取养老金',
              '保证领取20年',
              '身故保险金',
              '保单贷款功能'
            ],
            recommendation_score: 4.3
          }
        ]

        // 应用筛选
        this.applyFilters()
        this.totalInsurance = this.filteredInsurance.length
        
      } catch (error) {
        console.error('加载保险数据失败:', error)
      } finally {
        this.loading = false
      }
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

    simulatePurchase(insurance) {
      this.selectedInsurance = insurance
      this.purchaseForm.insured_name = ''
      this.purchaseForm.insured_age = 30
      this.purchaseDialogVisible = true
    },

    confirmPurchase() {
      if (!this.purchaseForm.insured_name) {
        alert('请输入投保人姓名')
        return
      }
      
      const totalPremium = this.selectedInsurance.premium * this.selectedInsurance.term
      alert(`成功为${this.purchaseForm.insured_name}购买${this.selectedInsurance.name}，总保费 ¥${totalPremium.toLocaleString()}`)
      this.purchaseDialogVisible = false
    },

    handleSizeChange() {
      this.currentPage = 1
    }
  }
}
</script>

<style scoped>
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