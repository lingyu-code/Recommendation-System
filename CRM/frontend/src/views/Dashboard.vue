<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <!-- 用户信息卡片 -->
      <el-col :span="6">
        <el-card class="user-card">
          <div class="user-info">
            <el-avatar :size="60" :src="userAvatar"></el-avatar>
            <div class="user-details">
              <h3>{{ userName }}</h3>
              <p>风险偏好: {{ riskLevelText }}</p>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 资产概览 -->
      <el-col :span="6">
        <el-card>
          <template #header>
            <span>总资产</span>
          </template>
          <div class="stat-card">
            <h2 style="color: #67C23A;">¥{{ totalAssets.toLocaleString() }}</h2>
            <p>较上月 +5.2%</p>
          </div>
        </el-card>
      </el-col>

      <!-- 今日收益 -->
      <el-col :span="6">
        <el-card>
          <template #header>
            <span>今日收益</span>
          </template>
          <div class="stat-card">
            <h2 style="color: #E6A23C;">¥{{ todayProfit.toLocaleString() }}</h2>
            <p>较昨日 +1.8%</p>
          </div>
        </el-card>
      </el-col>

      <!-- 推荐产品数 -->
      <el-col :span="6">
        <el-card>
          <template #header>
            <span>推荐产品</span>
          </template>
          <div class="stat-card">
            <h2 style="color: #409EFF;">{{ recommendedProducts }}</h2>
            <p>个性化推荐</p>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <!-- 资产分布图表 -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>资产分布</span>
          </template>
          <div ref="assetChart" style="height: 300px;"></div>
        </el-card>
      </el-col>

      <!-- 收益趋势图表 -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>收益趋势</span>
          </template>
          <div ref="profitChart" style="height: 300px;"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <!-- 推荐产品列表 -->
      <el-col :span="24">
        <el-card>
          <template #header>
            <span>个性化推荐</span>
          </template>
          <el-tabs v-model="activeTab">
            <el-tab-pane label="基金推荐" name="funds">
              <el-table :data="recommendedFunds" style="width: 100%">
                <el-table-column prop="name" label="基金名称" width="200"></el-table-column>
                <el-table-column prop="code" label="代码" width="120"></el-table-column>
                <el-table-column prop="type" label="类型" width="120"></el-table-column>
                <el-table-column prop="risk_level" label="风险等级" width="100">
                  <template #default="scope">
                    <el-tag :type="getRiskTagType(scope.row.risk_level)">
                      {{ scope.row.risk_level }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="expected_return" label="预期收益" width="120">
                  <template #default="scope">
                    {{ (scope.row.expected_return * 100).toFixed(2) }}%
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="120">
                  <template #default="scope">
                    <el-button type="primary" size="small" @click="viewFundDetail(scope.row)">
                      查看详情
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>

            <el-tab-pane label="股票推荐" name="stocks">
              <el-table :data="recommendedStocks" style="width: 100%">
                <el-table-column prop="name" label="股票名称" width="200"></el-table-column>
                <el-table-column prop="code" label="代码" width="120"></el-table-column>
                <el-table-column prop="industry" label="行业" width="120"></el-table-column>
                <el-table-column prop="pe_ratio" label="市盈率" width="100"></el-table-column>
                <el-table-column prop="dividend_yield" label="股息率" width="100">
                  <template #default="scope">
                    {{ (scope.row.dividend_yield * 100).toFixed(2) }}%
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="120">
                  <template #default="scope">
                    <el-button type="primary" size="small" @click="viewStockDetail(scope.row)">
                      查看详情
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>

            <el-tab-pane label="保险推荐" name="insurance">
              <el-table :data="recommendedInsurance" style="width: 100%">
                <el-table-column prop="name" label="保险名称" width="200"></el-table-column>
                <el-table-column prop="type" label="类型" width="120"></el-table-column>
                <el-table-column prop="premium" label="保费" width="120">
                  <template #default="scope">
                    ¥{{ scope.row.premium.toLocaleString() }}
                  </template>
                </el-table-column>
                <el-table-column prop="duration" label="期限" width="100">
                  <template #default="scope">
                    {{ scope.row.duration }}年
                  </template>
                </el-table-column>
                <el-table-column prop="risk_level" label="风险等级" width="100">
                  <template #default="scope">
                    <el-tag :type="getRiskTagType(scope.row.risk_level)">
                      {{ scope.row.risk_level }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="120">
                  <template #default="scope">
                    <el-button type="primary" size="small" @click="viewInsuranceDetail(scope.row)">
                      查看详情
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { apiService } from '../api'

export default {
  name: 'Dashboard',
  data() {
    return {
      userName: localStorage.getItem('userName') || '用户',
      userAvatar: '',
      totalAssets: 156800,
      todayProfit: 2345,
      recommendedProducts: 12,
      activeTab: 'funds',

      recommendedFunds: [],
      recommendedStocks: [],
      recommendedInsurance: [],

      assetChart: null,
      profitChart: null,
      loading: false
    }
  },
  computed: {
    riskLevelText() {
      const risk = localStorage.getItem('userRisk')
      const riskMap = {
        'low': '保守型',
        'medium': '稳健型',
        'high': '进取型'
      }
      return riskMap[risk] || '未知'
    }
  },
  async mounted() {
    await this.loadRecommendations()
    this.initCharts()
  },
  beforeUnmount() {
    if (this.assetChart) {
      this.assetChart.dispose()
    }
    if (this.profitChart) {
      this.profitChart.dispose()
    }
  },
  methods: {
    async loadRecommendations() {
      const userId = localStorage.getItem('userId')
      if (!userId) return

      this.loading = true
      try {
        // 获取用户风险偏好
        const userRisk = localStorage.getItem('userRisk') || 'medium'

        // 调用真实API获取推荐数据
        const userData = {
          age: 30,
          risk_tolerance: userRisk,
          total_assets: 100000,
          investment_goal: '财富增值',
          limit: 5
        }

        const response = await apiService.getRecommendations(userData)

        // 设置推荐数据 - 检查响应结构
        if (response && typeof response === 'object') {
          this.recommendedFunds = response.funds || []
          this.recommendedStocks = response.stocks || []
          this.recommendedInsurance = response.insurance || []
        } else {
          // 如果响应不是对象，使用空数组
          this.recommendedFunds = []
          this.recommendedStocks = []
          this.recommendedInsurance = []
        }

        // 更新推荐产品数量
        this.recommendedProducts = this.recommendedFunds.length +
          this.recommendedStocks.length +
          this.recommendedInsurance.length

      } catch (error) {
        console.error('加载推荐数据失败:', error)
        // 如果API调用失败，显示空数据
        this.recommendedFunds = []
        this.recommendedStocks = []
        this.recommendedInsurance = []
      } finally {
        this.loading = false
      }
    },

    initCharts() {
      // 资产分布图表
      this.assetChart = echarts.init(this.$refs.assetChart)
      const assetOption = {
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: '资产分布',
            type: 'pie',
            radius: '50%',
            data: [
              { value: 35, name: '股票' },
              { value: 25, name: '基金' },
              { value: 20, name: '债券' },
              { value: 15, name: '现金' },
              { value: 5, name: '保险' }
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      this.assetChart.setOption(assetOption)

      // 收益趋势图表
      this.profitChart = echarts.init(this.$refs.profitChart)
      const profitOption = {
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '月收益',
            type: 'line',
            data: [1200, 1800, 1500, 2200, 1900, 2300, 2500],
            smooth: true,
            lineStyle: {
              color: '#409EFF'
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgba(64, 158, 255, 0.3)' },
                { offset: 1, color: 'rgba(64, 158, 255, 0.1)' }
              ])
            }
          }
        ]
      }
      this.profitChart.setOption(profitOption)
    },

    getRiskTagType(riskLevel) {
      const typeMap = {
        'low': 'success',
        'medium': 'warning',
        'high': 'danger'
      }
      return typeMap[riskLevel] || 'info'
    },

    viewFundDetail(fund) {
      this.$router.push(`/funds?fundId=${fund.id}`)
    },

    viewStockDetail(stock) {
      this.$router.push(`/stocks?stockId=${stock.id}`)
    },

    viewInsuranceDetail(insurance) {
      this.$router.push(`/insurance?insuranceId=${insurance.id}`)
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.user-card {
  text-align: center;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.user-details h3 {
  margin: 0;
  color: #333;
}

.user-details p {
  margin: 5px 0 0 0;
  color: #666;
  font-size: 14px;
}

.stat-card {
  text-align: center;
}

.stat-card h2 {
  margin: 0;
  font-size: 24px;
}

.stat-card p {
  margin: 5px 0 0 0;
  color: #999;
  font-size: 12px;
}
</style>
