<template>
  <div class="financial-diagnosis">
    <el-card>
      <template #header>
        <div class="header-content">
          <span>理财诊断</span>
          <el-button type="primary" @click="startDiagnosis" :disabled="diagnosisStarted">
            {{ diagnosisStarted ? '诊断中...' : '开始诊断' }}
          </el-button>
        </div>
      </template>

      <!-- 诊断步骤 -->
      <div v-if="diagnosisStarted" class="diagnosis-steps">
        <el-steps :active="currentStep" align-center>
          <el-step title="基本信息" description="填写个人基本信息"></el-step>
          <el-step title="财务状况" description="评估当前财务状况"></el-step>
          <el-step title="风险偏好" description="测试风险承受能力"></el-step>
          <el-step title="理财目标" description="设定理财目标"></el-step>
          <el-step title="诊断结果" description="获取个性化建议"></el-step>
        </el-steps>

        <!-- 步骤内容 -->
        <div class="step-content">
          <!-- 步骤1: 基本信息 -->
          <div v-if="currentStep === 1" class="step-form">
            <h3>基本信息</h3>
            <el-form :model="basicInfo" label-width="100px">
              <el-form-item label="年龄">
                <el-input-number
                  v-model="basicInfo.age"
                  :min="18"
                  :max="80"
                  style="width: 200px"
                />
              </el-form-item>
              <el-form-item label="职业">
                <el-select v-model="basicInfo.occupation" placeholder="请选择职业" style="width: 200px">
                  <el-option label="学生" value="学生"></el-option>
                  <el-option label="上班族" value="上班族"></el-option>
                  <el-option label="自由职业" value="自由职业"></el-option>
                  <el-option label="退休" value="退休"></el-option>
                  <el-option label="其他" value="其他"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="年收入">
                <el-input-number
                  v-model="basicInfo.income"
                  :min="0"
                  :step="10000"
                  style="width: 200px"
                />
                <span style="margin-left: 10px">元</span>
              </el-form-item>
              <el-form-item label="婚姻状况">
                <el-radio-group v-model="basicInfo.marital_status">
                  <el-radio label="未婚">未婚</el-radio>
                  <el-radio label="已婚">已婚</el-radio>
                  <el-radio label="离异">离异</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="家庭成员">
                <el-input-number
                  v-model="basicInfo.family_members"
                  :min="1"
                  :max="10"
                  style="width: 200px"
                />
              </el-form-item>
            </el-form>
          </div>

          <!-- 步骤2: 财务状况 -->
          <div v-if="currentStep === 2" class="step-form">
            <h3>财务状况</h3>
            <el-form :model="financialStatus" label-width="120px">
              <el-form-item label="月支出">
                <el-input-number
                  v-model="financialStatus.monthly_expenses"
                  :min="0"
                  :step="1000"
                  style="width: 200px"
                />
                <span style="margin-left: 10px">元</span>
              </el-form-item>
              <el-form-item label="现有存款">
                <el-input-number
                  v-model="financialStatus.savings"
                  :min="0"
                  :step="10000"
                  style="width: 200px"
                />
                <span style="margin-left: 10px">元</span>
              </el-form-item>
              <el-form-item label="负债总额">
                <el-input-number
                  v-model="financialStatus.debt"
                  :min="0"
                  :step="10000"
                  style="width: 200px"
                />
                <span style="margin-left: 10px">元</span>
              </el-form-item>
              <el-form-item label="投资经验">
                <el-radio-group v-model="financialStatus.investment_experience">
                  <el-radio label="无经验">无经验</el-radio>
                  <el-radio label="1-3年">1-3年</el-radio>
                  <el-radio label="3-5年">3-5年</el-radio>
                  <el-radio label="5年以上">5年以上</el-radio>
                </el-radio-group>
              </el-form-item>
            </el-form>
          </div>

          <!-- 步骤3: 风险偏好 -->
          <div v-if="currentStep === 3" class="step-form">
            <h3>风险偏好测试</h3>
            <div class="risk-questions">
              <div v-for="(question, index) in riskQuestions" :key="index" class="question-item">
                <p>{{ question.text }}</p>
                <el-radio-group v-model="riskAnswers[index]">
                  <el-radio 
                    v-for="(option, optIndex) in question.options" 
                    :key="optIndex" 
                    :label="option.score"
                    style="display: block; margin: 10px 0;"
                  >
                    {{ option.text }}
                  </el-radio>
                </el-radio-group>
              </div>
            </div>
          </div>

          <!-- 步骤4: 理财目标 -->
          <div v-if="currentStep === 4" class="step-form">
            <h3>理财目标</h3>
            <el-form :model="financialGoals" label-width="120px">
              <el-form-item label="短期目标(1年内)">
                <el-input
                  v-model="financialGoals.short_term"
                  type="textarea"
                  :rows="3"
                  placeholder="例如：购买新车、旅游等"
                  style="width: 400px"
                />
              </el-form-item>
              <el-form-item label="中期目标(1-5年)">
                <el-input
                  v-model="financialGoals.mid_term"
                  type="textarea"
                  :rows="3"
                  placeholder="例如：购房首付、结婚等"
                  style="width: 400px"
                />
              </el-form-item>
              <el-form-item label="长期目标(5年以上)">
                <el-input
                  v-model="financialGoals.long_term"
                  type="textarea"
                  :rows="3"
                  placeholder="例如：子女教育、养老规划等"
                  style="width: 400px"
                />
              </el-form-item>
              <el-form-item label="期望收益率">
                <el-slider
                  v-model="financialGoals.expected_return"
                  :min="3"
                  :max="20"
                  :step="1"
                  show-stops
                  style="width: 400px"
                />
                <span style="margin-left: 20px">{{ financialGoals.expected_return }}%</span>
              </el-form-item>
            </el-form>
          </div>

          <!-- 步骤5: 诊断结果 -->
          <div v-if="currentStep === 5" class="diagnosis-result">
            <h3>理财诊断结果</h3>
            <el-row :gutter="20">
              <el-col :span="8">
                <el-card>
                  <template #header>
                    <span>风险等级</span>
                  </template>
                  <div class="risk-level">
                    <div class="risk-icon" :class="diagnosisResult.riskLevel">
                      <i class="el-icon-warning"></i>
                    </div>
                    <h4>{{ diagnosisResult.riskLevelText }}</h4>
                    <p>{{ diagnosisResult.riskDescription }}</p>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-card>
                  <template #header>
                    <span>资产配置建议</span>
                  </template>
                  <div class="allocation-chart">
                    <div 
                      v-for="(item, index) in diagnosisResult.assetAllocation" 
                      :key="index"
                      class="allocation-item"
                      :style="{ backgroundColor: item.color }"
                    >
                      <span>{{ item.name }}: {{ item.percentage }}%</span>
                    </div>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-card>
                  <template #header>
                    <span>财务健康度</span>
                  </template>
                  <div class="health-score">
                    <el-progress
                      type="circle"
                      :percentage="diagnosisResult.healthScore"
                      :color="diagnosisResult.healthColor"
                    />
                    <p>{{ diagnosisResult.healthText }}</p>
                  </div>
                </el-card>
              </el-col>
            </el-row>

            <!-- 详细建议 -->
            <el-card style="margin-top: 20px;">
              <template #header>
                <span>个性化建议</span>
              </template>
              <div class="recommendations">
                <div v-for="(recommendation, index) in diagnosisResult.recommendations" :key="index" class="recommendation-item">
                  <h4>{{ recommendation.title }}</h4>
                  <p>{{ recommendation.content }}</p>
                </div>
              </div>
            </el-card>

            <!-- 推荐产品 -->
            <el-card style="margin-top: 20px;">
              <template #header>
                <span>推荐产品</span>
              </template>
              <el-table :data="diagnosisResult.recommendedProducts" style="width: 100%">
                <el-table-column prop="type" label="类型" width="100"></el-table-column>
                <el-table-column prop="name" label="产品名称" width="200"></el-table-column>
                <el-table-column prop="description" label="描述"></el-table-column>
                <el-table-column prop="suitability" label="匹配度" width="100">
                  <template #default="scope">
                    <el-tag :type="scope.row.suitability > 80 ? 'success' : scope.row.suitability > 60 ? 'warning' : 'info'">
                      {{ scope.row.suitability }}%
                    </el-tag>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </div>
        </div>

        <!-- 导航按钮 -->
        <div class="step-actions" style="margin-top: 20px; text-align: center;">
          <el-button @click="prevStep" :disabled="currentStep === 1">上一步</el-button>
          <el-button type="primary" @click="nextStep" v-if="currentStep < 5">
            {{ currentStep === 4 ? '完成诊断' : '下一步' }}
          </el-button>
          <el-button type="success" @click="saveDiagnosis" v-if="currentStep === 5">
            保存诊断结果
          </el-button>
        </div>
      </div>

      <!-- 未开始诊断时的提示 -->
      <div v-else class="welcome-section">
        <div class="welcome-content">
          <h2>欢迎使用理财诊断系统</h2>
          <p>通过简单的问答，我们将为您提供个性化的理财建议和产品推荐</p>
          <div class="features">
            <el-row :gutter="20">
              <el-col :span="6">
                <div class="feature-item">
                  <i class="el-icon-user"></i>
                  <h4>个性化评估</h4>
                  <p>基于您的个人情况定制分析</p>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="feature-item">
                  <i class="el-icon-data-analysis"></i>
                  <h4>专业分析</h4>
                  <p>多维度财务健康度评估</p>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="feature-item">
                  <i class="el-icon-present"></i>
                  <h4>智能推荐</h4>
                  <p>匹配最适合的金融产品</p>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="feature-item">
                  <i class="el-icon-document"></i>
                  <h4>详细报告</h4>
                  <p>生成完整的理财规划报告</p>
                </div>
              </el-col>
            </el-row>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'FinancialDiagnosis',
  data() {
    return {
      diagnosisStarted: false,
      currentStep: 1,
      
      // 基本信息
      basicInfo: {
        age: 30,
        occupation: '',
        income: 0,
        marital_status: '未婚',
        family_members: 1
      },
      
      // 财务状况
      financialStatus: {
        monthly_expenses: 0,
        savings: 0,
        debt: 0,
        investment_experience: '无经验'
      },
      
      // 风险偏好问题
      riskQuestions: [
        {
          text: '您能接受的投资亏损程度是多少？',
          options: [
            { text: '不能接受任何亏损', score: 1 },
            { text: '能接受10%以内的亏损', score: 2 },
            { text: '能接受20%以内的亏损', score: 3 },
            { text: '能接受30%以上的亏损', score: 4 }
          ]
        },
        {
          text: '您的投资期限偏好是？',
          options: [
            { text: '1年以内', score: 1 },
            { text: '1-3年', score: 2 },
            { text: '3-5年', score: 3 },
            { text: '5年以上', score: 4 }
          ]
        },
        {
          text: '您对投资收益的期望是？',
          options: [
            { text: '保本为主，收益次要', score: 1 },
            { text: '略高于银行存款', score: 2 },
            { text: '与市场平均水平相当', score: 3 },
            { text: '追求高收益，愿意承担高风险', score: 4 }
          ]
        }
      ],
      riskAnswers: [1, 1, 1],
      
      // 理财目标
      financialGoals: {
        short_term: '',
        mid_term: '',
        long_term: '',
        expected_return: 8
      },
      
      // 诊断结果
      diagnosisResult: {
        riskLevel: 'conservative',
        riskLevelText: '保守型',
        riskDescription: '适合低风险投资产品',
        healthScore: 65,
        healthColor: '#E6A23C',
        healthText: '一般',
        assetAllocation: [
          { name: '存款', percentage: 40, color: '#409EFF' },
          { name: '债券', percentage: 30, color: '#67C23A' },
          { name: '基金', percentage: 20, color: '#E6A23C' },
          { name: '股票', percentage: 10, color: '#F56C6C' }
        ],
        recommendations: [
          {
            title: '建立紧急备用金',
            content: '建议准备3-6个月的生活支出作为紧急备用金'
          },
          {
            title: '控制债务比例',
            content: '当前债务水平较高，建议优先偿还高息债务'
          },
          {
            title: '多元化投资',
            content: '根据您的风险偏好，建议采用保守型资产配置'
          }
        ],
        recommendedProducts: [
          {
            type: '基金',
            name: '货币市场基金',
            description: '低风险，流动性好，适合短期资金管理',
            suitability: 85
          },
          {
            type: '保险',
            name: '意外伤害保险',
            description: '提供意外风险保障，保费低廉',
            suitability: 78
          },
          {
            type: '理财产品',
            name: '保本型理财',
            description: '本金安全，收益稳定',
            suitability: 90
          }
        ]
      }
    }
  },
  methods: {
    startDiagnosis() {
      this.diagnosisStarted = true
      this.currentStep = 1
    },
    
    nextStep() {
      if (this.currentStep < 5) {
        this.currentStep++
        
        // 如果是最后一步，计算诊断结果
        if (this.currentStep === 5) {
          this.calculateDiagnosisResult()
        }
      }
    },
    
    prevStep() {
      if (this.currentStep > 1) {
        this.currentStep--
      }
    },
    
    calculateDiagnosisResult() {
      // 计算风险得分
      const riskScore = this.riskAnswers.reduce((sum, score) => sum + score, 0)
      
      // 根据风险得分确定风险等级
      if (riskScore <= 3) {
        this.diagnosisResult.riskLevel = 'conservative'
        this.diagnosisResult.riskLevelText = '保守型'
        this.diagnosisResult.riskDescription = '适合低风险投资产品，注重本金安全'
        this.diagnosisResult.assetAllocation = [
          { name: '存款', percentage: 40, color: '#409EFF' },
          { name: '债券', percentage: 30, color: '#67C23A' },
          { name: '基金', percentage: 20, color: '#E6A23C' },
          { name: '股票', percentage: 10, color: '#F56C6C' }
        ]
      } else if (riskScore <= 6) {
        this.diagnosisResult.riskLevel = 'moderate'
        this.diagnosisResult.riskLevelText = '稳健型'
        this.diagnosisResult.riskDescription = '适合低风险投资产品，注重本金安全'
        this.diagnosisResult.assetAllocation = [
          { name: '存款', percentage: 30, color: '#409EFF' },
          { name: '债券', percentage: 35, color: '#67C23A' },
          { name: '基金', percentage: 25, color: '#E6A23C' },
          { name: '股票', percentage: 10, color: '#F56C6C' }
        ]
      } else if (riskScore <= 9) {
        this.diagnosisResult.riskLevel = 'aggressive'
        this.diagnosisResult.riskLevelText = '积极型'
        this.diagnosisResult.riskDescription = '适合高风险投资产品，追求高收益'
        this.diagnosisResult.assetAllocation = [
          { name: '存款', percentage: 20, color: '#409EFF' },
          { name: '债券', percentage: 25, color: '#67C23A' },
          { name: '基金', percentage: 30, color: '#E6A23C' },
          { name: '股票', percentage: 25, color: '#F56C6C' }
        ]
      } else {
        this.diagnosisResult.riskLevel = 'very_aggressive'
        this.diagnosisResult.riskLevelText = '非常积极型'
        this.diagnosisResult.riskDescription = '适合高风险投资产品，愿意承担较大波动'
        this.diagnosisResult.assetAllocation = [
          { name: '存款', percentage: 10, color: '#409EFF' },
          { name: '债券', percentage: 20, color: '#67C23A' },
          { name: '基金', percentage: 30, color: '#E6A23C' },
          { name: '股票', percentage: 40, color: '#F56C6C' }
        ]
      }

      // 计算财务健康度
      const savingsRatio = this.financialStatus.savings / this.basicInfo.income
      const debtRatio = this.financialStatus.debt / this.basicInfo.income
      
      let healthScore = 70
      if (savingsRatio > 0.5) healthScore += 15
      else if (savingsRatio > 0.3) healthScore += 10
      else if (savingsRatio > 0.1) healthScore += 5
      
      if (debtRatio < 0.3) healthScore += 10
      else if (debtRatio < 0.5) healthScore += 5
      else healthScore -= 10
      
      this.diagnosisResult.healthScore = Math.min(100, Math.max(0, healthScore))
      
      if (this.diagnosisResult.healthScore >= 80) {
        this.diagnosisResult.healthColor = '#67C23A'
        this.diagnosisResult.healthText = '优秀'
      } else if (this.diagnosisResult.healthScore >= 60) {
        this.diagnosisResult.healthColor = '#E6A23C'
        this.diagnosisResult.healthText = '良好'
      } else {
        this.diagnosisResult.healthColor = '#F56C6C'
        this.diagnosisResult.healthText = '需要改善'
      }
    },
    
    saveDiagnosis() {
      this.$message.success('诊断结果已保存')
      this.diagnosisStarted = false
      this.currentStep = 1
    }
  }
}
</script>

<style scoped>
.financial-diagnosis {
  padding: 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.diagnosis-steps {
  margin-bottom: 30px;
}

.step-form {
  padding: 20px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  margin: 20px 0;
}

.risk-questions .question-item {
  margin-bottom: 30px;
  padding: 15px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
}

.diagnosis-result {
  padding: 20px 0;
}

.risk-level {
  text-align: center;
  padding: 20px;
}

.risk-icon {
  font-size: 48px;
  margin-bottom: 15px;
}

.risk-icon.conservative {
  color: #67C23A;
}

.risk-icon.moderate {
  color: #E6A23C;
}

.risk-icon.aggressive {
  color: #F56C6C;
}

.risk-icon.very_aggressive {
  color: #F56C6C;
}

.allocation-chart {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.allocation-item {
  padding: 8px 12px;
  border-radius: 4px;
  color: white;
  font-weight: bold;
  text-align: center;
}

.health-score {
  text-align: center;
  padding: 20px;
}

.recommendations {
  padding: 10px;
}

.recommendation-item {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.recommendation-item:last-child {
  border-bottom: none;
}

.welcome-section {
  text-align: center;
  padding: 40px 20px;
}

.welcome-content h2 {
  color: #303133;
  margin-bottom: 15px;
}

.welcome-content p {
  color: #606266;
  font-size: 16px;
  margin-bottom: 30px;
}

.features {
  margin-top: 40px;
}

.feature-item {
  text-align: center;
  padding: 20px;
}

.feature-item i {
  font-size: 48px;
  color: #409EFF;
  margin-bottom: 15px;
}

.feature-item h4 {
  color: #303133;
  margin-bottom: 10px;
}

.feature-item p {
  color: #606266;
  font-size: 14px;
}

.step-actions {
  margin-top: 30px;
  text-align: center;
}
</style>
