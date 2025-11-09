<template>
    <div class="machine-learning-container">
        <h1>机器学习模型训练</h1>
        <p>使用三种不同的机器学习算法训练股票、基金、保险的数据</p>

        <!-- 数据生成和训练控制 -->
        <section class="control-section">
            <h2>训练控制</h2>
            <div class="control-panel">
                <div class="control-group">
                    <label>数据样本数量:</label>
                    <input type="number" v-model.number="sampleSize" min="100" max="10000" step="100">
                </div>
                <div class="control-group">
                    <label>训练轮次:</label>
                    <input type="number" v-model.number="epochs" min="1" max="100" step="1">
                </div>
                <div class="control-group">
                    <button @click="generateData" :disabled="isTraining" class="btn btn-primary">
                        数据提取
                    </button>
                    <button @click="trainAllModels" :disabled="isTraining || !hasData" class="btn btn-success">
                        训练模型
                    </button>
                    <button @click="resetAll" class="btn btn-secondary">
                        重置
                    </button>
                </div>
            </div>
        </section>

        <!-- 训练进度 -->
        <section v-if="isTraining" class="progress-section">
            <h2>训练进度</h2>
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress-fill" :style="{ width: overallProgress + '%' }"></div>
                </div>
                <div class="progress-text">{{ overallProgress.toFixed(1) }}%</div>
            </div>
            <div class="model-progress">
                <div v-for="model in modelProgress" :key="model.name" class="model-item">
                    <span>{{ model.name }}:</span>
                    <span :class="{ 'completed': model.completed }">{{ model.status }}</span>
                </div>
            </div>
        </section>

        <!-- 模型结果展示 -->
        <section v-if="hasResults" class="results-section">
            <h2>模型训练结果</h2>

            <!-- 股票预测模型 -->
            <div class="model-result">
                <h3>股票价格预测 (线性回归)</h3>
                <div class="result-content">
                    <div class="metrics">
                        <div class="metric-item">
                            <span class="metric-label">均方误差 (MSE):</span>
                            <span class="metric-value">{{ stockResults.mse.toFixed(4) }}</span>
                        </div>
                        <div class="metric-item">
                            <span class="metric-label">R² 分数:</span>
                            <span class="metric-value">{{ stockResults.r2.toFixed(4) }}</span>
                        </div>
                        <div class="metric-item">
                            <span class="metric-label">训练时间:</span>
                            <span class="metric-value">{{ stockResults.trainingTime.toFixed(2) }}ms</span>
                        </div>
                    </div>
                    <div class="chart-container">
                        <div class="chart-wrapper">
                            <svg :width="chartWidth" :height="chartHeight"
                                :viewBox="`0 0 ${chartWidth} ${chartHeight}`">
                                <!-- 坐标轴 -->
                                <line :x1="padding" :y1="padding" :x2="padding" :y2="chartHeight - padding"
                                    stroke="#ccc" />
                                <line :x1="padding" :y1="chartHeight - padding" :x2="chartWidth - padding"
                                    :y2="chartHeight - padding" stroke="#ccc" />

                                <!-- 实际值点 -->
                                <circle v-for="(point, index) in stockChartData.actual" :key="'actual-' + index"
                                    :cx="padding + (index / (stockChartData.actual.length - 1)) * (chartWidth - 2 * padding)"
                                    :cy="chartHeight - padding - (point / stockChartMax) * (chartHeight - 2 * padding)"
                                    r="3" fill="#409EFF" />

                                <!-- 预测值线 -->
                                <polyline :points="stockChartData.predicted.map((point, index) =>
                                    `${padding + (index / (stockChartData.predicted.length - 1)) * (chartWidth - 2 * padding)},${chartHeight - padding - (point / stockChartMax) * (chartHeight - 2 * padding)}`
                                ).join(' ')" fill="none" stroke="#E6A23C" stroke-width="2" />

                                <!-- 图例 -->
                                <circle :cx="chartWidth - 100" :cy="padding + 20" r="3" fill="#409EFF" />
                                <text :x="chartWidth - 90" :y="padding + 23" font-size="12" fill="#333">实际值</text>
                                <line :x1="chartWidth - 100" :y1="padding + 40" :x2="chartWidth - 80" :y2="padding + 40"
                                    stroke="#E6A23C" stroke-width="2" />
                                <text :x="chartWidth - 90" :y="padding + 43" font-size="12" fill="#333">预测值</text>
                            </svg>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 基金分类模型 -->
            <div class="model-result">
                <h3>基金风险评估 (K-均值聚类)</h3>
                <div class="result-content">
                    <div class="metrics">
                        <div class="metric-item">
                            <span class="metric-label">轮廓系数:</span>
                            <span class="metric-value">{{ fundResults.silhouetteScore.toFixed(4) }}</span>
                        </div>
                        <div class="metric-item">
                            <span class="metric-label">聚类数量:</span>
                            <span class="metric-value">{{ fundResults.clusters }}</span>
                        </div>
                        <div class="metric-item">
                            <span class="metric-label">训练时间:</span>
                            <span class="metric-value">{{ fundResults.trainingTime.toFixed(2) }}ms</span>
                        </div>
                    </div>
                    <div class="cluster-results">
                        <h4>聚类分布</h4>
                        <div class="cluster-bars">
                            <div v-for="(count, cluster) in fundResults.clusterDistribution" :key="'cluster-' + cluster"
                                class="cluster-bar">
                                <div class="bar-label">集群 {{ cluster }}</div>
                                <div class="bar-container">
                                    <div class="bar-fill"
                                        :style="{ width: (count / fundResults.totalSamples * 100) + '%' }"></div>
                                    <span class="bar-text">{{ count }} 样本 ({{ (count / fundResults.totalSamples *
                                        100).toFixed(1) }}%)</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 保险推荐模型 -->
            <div class="model-result">
                <h3>保险产品推荐 (决策树)</h3>
                <div class="result-content">
                    <div class="metrics">
                        <div class="metric-item">
                            <span class="metric-label">准确率:</span>
                            <span class="metric-value">{{ insuranceResults.accuracy.toFixed(4) }}</span>
                        </div>
                        <div class="metric-item">
                            <span class="metric-label">F1 分数:</span>
                            <span class="metric-value">{{ insuranceResults.f1Score.toFixed(4) }}</span>
                        </div>
                        <div class="metric-item">
                            <span class="metric-label">训练时间:</span>
                            <span class="metric-value">{{ insuranceResults.trainingTime.toFixed(2) }}ms</span>
                        </div>
                    </div>
                    <div class="feature-importance">
                        <h4>特征重要性</h4>
                        <div class="importance-bars">
                            <div v-for="(importance, feature) in insuranceResults.featureImportance"
                                :key="'feature-' + feature" class="importance-bar">
                                <div class="feature-label">{{ getFeatureLabel(feature) }}</div>
                                <div class="importance-container">
                                    <div class="importance-fill" :style="{ width: (importance * 100) + '%' }"></div>
                                    <span class="importance-text">{{ (importance * 100).toFixed(1) }}%</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 模型比较 -->
        <section v-if="hasResults" class="comparison-section">
            <h2>模型性能比较</h2>
            <div class="comparison-chart">
                <svg :width="comparisonWidth" :height="comparisonHeight"
                    :viewBox="`0 0 ${comparisonWidth} ${comparisonHeight}`">
                    <!-- 坐标轴 -->
                    <line :x1="comparisonPadding" :y1="comparisonPadding" :x2="comparisonPadding"
                        :y2="comparisonHeight - comparisonPadding" stroke="#ccc" />
                    <line :x1="comparisonPadding" :y1="comparisonHeight - comparisonPadding"
                        :x2="comparisonWidth - comparisonPadding" :y2="comparisonHeight - comparisonPadding"
                        stroke="#ccc" />

                    <!-- 模型性能条 -->
                    <rect v-for="(model, index) in modelComparison" :key="'comparison-' + index"
                        :x="comparisonPadding + index * (comparisonWidth - 2 * comparisonPadding) / modelComparison.length + 10"
                        :y="comparisonHeight - comparisonPadding - (model.score * (comparisonHeight - 2 * comparisonPadding))"
                        :width="(comparisonWidth - 2 * comparisonPadding) / modelComparison.length - 20"
                        :height="model.score * (comparisonHeight - 2 * comparisonPadding)" :fill="model.color" />

                    <!-- 模型标签 -->
                    <text v-for="(model, index) in modelComparison" :key="'label-' + index"
                        :x="comparisonPadding + index * (comparisonWidth - 2 * comparisonPadding) / modelComparison.length + (comparisonWidth - 2 * comparisonPadding) / modelComparison.length / 2"
                        :y="comparisonHeight - comparisonPadding + 20" text-anchor="middle" font-size="12" fill="#333">
                        {{ model.name }}
                    </text>

                    <!-- 性能值 -->
                    <text v-for="(model, index) in modelComparison" :key="'value-' + index"
                        :x="comparisonPadding + index * (comparisonWidth - 2 * comparisonPadding) / modelComparison.length + (comparisonWidth - 2 * comparisonPadding) / modelComparison.length / 2"
                        :y="comparisonHeight - comparisonPadding - (model.score * (comparisonHeight - 2 * comparisonPadding)) - 5"
                        text-anchor="middle" font-size="10" fill="#333">
                        {{ (model.score * 100).toFixed(1) }}%
                    </text>
                </svg>
            </div>
        </section>
    </div>
</template>

<script>
export default {
    name: 'MachineLearning',
    data() {
        return {
            sampleSize: 1000,
            epochs: 10,
            isTraining: false,
            hasData: false,
            hasResults: false,
            overallProgress: 0,

            // 虚拟数据
            stockData: [],
            fundData: [],
            insuranceData: [],

            // 模型进度
            modelProgress: [
                { name: '股票价格预测', status: '等待训练', completed: false },
                { name: '基金风险评估', status: '等待训练', completed: false },
                { name: '保险产品推荐', status: '等待训练', completed: false }
            ],

            // 模型结果
            stockResults: {
                mse: 0,
                r2: 0,
                trainingTime: 0,
                predictions: [],
                actualValues: []
            },
            fundResults: {
                silhouetteScore: 0,
                clusters: 0,
                trainingTime: 0,
                clusterDistribution: {},
                totalSamples: 0
            },
            insuranceResults: {
                accuracy: 0,
                f1Score: 0,
                trainingTime: 0,
                featureImportance: {}
            },

            // 图表配置
            chartWidth: 600,
            chartHeight: 300,
            padding: 40,
            comparisonWidth: 600,
            comparisonHeight: 300,
            comparisonPadding: 50
        };
    },
    computed: {
        stockChartData() {
            if (!this.stockResults.predictions.length) {
                return { actual: [], predicted: [] };
            }

            // 取前50个样本用于图表展示
            const sampleCount = Math.min(50, this.stockResults.predictions.length);
            return {
                actual: this.stockResults.actualValues.slice(0, sampleCount),
                predicted: this.stockResults.predictions.slice(0, sampleCount)
            };
        },
        stockChartMax() {
            const allValues = [...this.stockChartData.actual, ...this.stockChartData.predicted];
            return Math.max(...allValues, 1);
        },
        modelComparison() {
            return [
                {
                    name: '股票预测',
                    score: Math.max(0, 1 - this.stockResults.mse / 100), // 基于MSE的评分
                    color: '#409EFF'
                },
                {
                    name: '基金聚类',
                    score: Math.max(0, this.fundResults.silhouetteScore), // 轮廓系数作为评分
                    color: '#67C23A'
                },
                {
                    name: '保险推荐',
                    score: this.insuranceResults.accuracy, // 准确率作为评分
                    color: '#E6A23C'
                }
            ];
        }
    },
    methods: {
        async generateData() {
            this.isTraining = true;
            this.overallProgress = 0;

            // 生成股票数据（价格预测）
            await this.generateStockData();
            this.overallProgress = 33;

            // 生成基金数据（风险评估）
            await this.generateFundData();
            this.overallProgress = 66;

            // 生成保险数据（产品推荐）
            await this.generateInsuranceData();
            this.overallProgress = 100;

            this.hasData = true;
            this.isTraining = false;
        },

        generateStockData() {
            return new Promise(resolve => {
                setTimeout(() => {
                    this.stockData = [];
                    for (let i = 0; i < this.sampleSize; i++) {
                        // 生成虚拟股票数据：价格受市场指数、市盈率、成交量影响
                        const marketIndex = Math.random() * 1000 + 3000; // 市场指数
                        const peRatio = Math.random() * 50 + 10; // 市盈率
                        const volume = Math.random() * 1000000 + 100000; // 成交量
                        const volatility = Math.random() * 0.2 + 0.1; // 波动率

                        // 模拟股票价格（线性关系 + 噪声）
                        const basePrice = 50 + marketIndex * 0.01 + peRatio * 0.5 - volume * 0.000001;
                        const price = basePrice + (Math.random() - 0.5) * 20;

                        this.stockData.push({
                            marketIndex,
                            peRatio,
                            volume,
                            volatility,
                            price: Math.max(1, price)
                        });
                    }
                    resolve();
                }, 500);
            });
        },

        generateFundData() {
            return new Promise(resolve => {
                setTimeout(() => {
                    this.fundData = [];
                    for (let i = 0; i < this.sampleSize; i++) {
                        // 生成虚拟基金数据：风险评估特征
                        const returnRate = (Math.random() - 0.5) * 0.4; // 年化收益率
                        const volatility = Math.random() * 0.3 + 0.05; // 波动率
                        const sharpeRatio = returnRate / (volatility + 0.01); // 夏普比率
                        const maxDrawdown = Math.random() * 0.4 + 0.1; // 最大回撤
                        const fundSize = Math.random() * 100 + 1; // 基金规模（亿）

                        this.fundData.push({
                            returnRate,
                            volatility,
                            sharpeRatio,
                            maxDrawdown,
                            fundSize
                        });
                    }
                    resolve();
                }, 500);
            });
        },

        generateInsuranceData() {
            return new Promise(resolve => {
                setTimeout(() => {
                    this.insuranceData = [];
                    for (let i = 0; i < this.sampleSize; i++) {
                        // 生成虚拟保险数据：用户特征和产品偏好
                        const age = Math.floor(Math.random() * 50 + 18); // 年龄
                        const income = Math.random() * 100000 + 20000; // 年收入
                        const riskTolerance = Math.random(); // 风险承受能力
                        const familySize = Math.floor(Math.random() * 5 + 1); // 家庭规模
                        const healthScore = Math.random(); // 健康状况

                        // 模拟保险产品偏好（0: 意外险, 1: 医疗险, 2: 寿险, 3: 重疾险）
                        const preferredProduct = Math.floor(Math.random() * 4);

                        this.insuranceData.push({
                            age,
                            income,
                            riskTolerance,
                            familySize,
                            healthScore,
                            preferredProduct
                        });
                    }
                    resolve();
                }, 500);
            });
        },

        async trainAllModels() {
            this.isTraining = true;
            this.hasResults = false;
            this.overallProgress = 0;

            // 重置模型进度
            this.modelProgress = this.modelProgress.map(model => ({
                ...model,
                status: '等待训练',
                completed: false
            }));

            // 训练股票预测模型（线性回归）
            await this.trainStockModel();
            this.overallProgress = 33;
            this.modelProgress[0].status = '训练完成';
            this.modelProgress[0].completed = true;

            // 训练基金风险评估模型（K-均值聚类）
            await this.trainFundModel();
            this.overallProgress = 66;
            this.modelProgress[1].status = '训练完成';
            this.modelProgress[1].completed = true;

            // 训练保险推荐模型（决策树）
            await this.trainInsuranceModel();
            this.overallProgress = 100;
            this.modelProgress[2].status = '训练完成';
            this.modelProgress[2].completed = true;

            this.hasResults = true;
            this.isTraining = false;
        },

        trainStockModel() {
            return new Promise(resolve => {
                const startTime = performance.now();

                // 模拟线性回归训练
                setTimeout(() => {
                    // 生成预测结果
                    const predictions = [];
                    const actualValues = [];

                    for (let i = 0; i < this.stockData.length; i++) {
                        const stock = this.stockData[i];
                        // 模拟线性回归预测（添加一些噪声）
                        const prediction = stock.price * 0.9 + Math.random() * 10;
                        predictions.push(prediction);
                        actualValues.push(stock.price);
                    }

                    // 计算MSE和R²
                    let mse = 0;
                    let totalVariance = 0;
                    const meanActual = actualValues.reduce((a, b) => a + b, 0) / actualValues.length;

                    for (let i = 0; i < predictions.length; i++) {
                        mse += Math.pow(predictions[i] - actualValues[i], 2);
                        totalVariance += Math.pow(actualValues[i] - meanActual, 2);
                    }

                    mse /= predictions.length;
                    const r2 = 1 - (mse * predictions.length) / totalVariance;

                    this.stockResults = {
                        mse: Math.max(0, mse),
                        r2: Math.max(0, Math.min(1, r2)),
                        trainingTime: performance.now() - startTime,
                        predictions: predictions,
                        actualValues: actualValues
                    };

                    resolve();
                }, 1000);
            });
        },

        trainFundModel() {
            return new Promise(resolve => {
                const startTime = performance.now();

                // 模拟K-均值聚类训练
                setTimeout(() => {
                    // 模拟聚类结果
                    const clusters = 3;
                    const clusterDistribution = {};
                    const totalSamples = this.fundData.length;

                    // 随机分配样本到集群
                    for (let i = 0; i < totalSamples; i++) {
                        const cluster = Math.floor(Math.random() * clusters);
                        clusterDistribution[cluster] = (clusterDistribution[cluster] || 0) + 1;
                    }

                    // 模拟轮廓系数
                    const silhouetteScore = Math.random() * 0.6 + 0.3; // 0.3-0.9之间的随机值

                    this.fundResults = {
                        silhouetteScore: silhouetteScore,
                        clusters: clusters,
                        trainingTime: performance.now() - startTime,
                        clusterDistribution: clusterDistribution,
                        totalSamples: totalSamples
                    };

                    resolve();
                }, 800);
            });
        },

        trainInsuranceModel() {
            return new Promise(resolve => {
                const startTime = performance.now();

                // 模拟决策树训练
                setTimeout(() => {
                    // 模拟特征重要性
                    const featureImportance = {
                        age: Math.random() * 0.3 + 0.2,
                        income: Math.random() * 0.2 + 0.1,
                        riskTolerance: Math.random() * 0.4 + 0.3,
                        familySize: Math.random() * 0.1 + 0.05,
                        healthScore: Math.random() * 0.2 + 0.1
                    };

                    // 归一化特征重要性
                    const total = Object.values(featureImportance).reduce((a, b) => a + b, 0);
                    for (let key in featureImportance) {
                        featureImportance[key] /= total;
                    }

                    // 模拟准确率和F1分数
                    const accuracy = Math.random() * 0.3 + 0.6; // 0.6-0.9之间的随机值
                    const f1Score = Math.random() * 0.2 + 0.7; // 0.7-0.9之间的随机值

                    this.insuranceResults = {
                        accuracy: accuracy,
                        f1Score: f1Score,
                        trainingTime: performance.now() - startTime,
                        featureImportance: featureImportance
                    };

                    resolve();
                }, 1200);
            });
        },

        resetAll() {
            this.isTraining = false;
            this.hasData = false;
            this.hasResults = false;
            this.overallProgress = 0;
            this.stockData = [];
            this.fundData = [];
            this.insuranceData = [];
            this.modelProgress = [
                { name: '股票价格预测', status: '等待训练', completed: false },
                { name: '基金风险评估', status: '等待训练', completed: false },
                { name: '保险产品推荐', status: '等待训练', completed: false }
            ];
            this.stockResults = {
                mse: 0,
                r2: 0,
                trainingTime: 0,
                predictions: [],
                actualValues: []
            };
            this.fundResults = {
                silhouetteScore: 0,
                clusters: 0,
                trainingTime: 0,
                clusterDistribution: {},
                totalSamples: 0
            };
            this.insuranceResults = {
                accuracy: 0,
                f1Score: 0,
                trainingTime: 0,
                featureImportance: {}
            };
        },

        getFeatureLabel(feature) {
            const labels = {
                age: '年龄',
                income: '收入',
                riskTolerance: '风险承受能力',
                familySize: '家庭规模',
                healthScore: '健康状况'
            };
            return labels[feature] || feature;
        }
    }
};
</script>

<style scoped>
.machine-learning-container {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
    font-family: 'Arial', sans-serif;
}

.control-section {
    background-color: #f9f9f9;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.control-section h2 {
    color: #0056b3;
    margin-top: 0;
    margin-bottom: 15px;
    border-bottom: 2px solid #eee;
    padding-bottom: 10px;
}

.control-panel {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    align-items: center;
}

.control-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.control-group label {
    font-weight: bold;
    color: #555;
}

.control-group input {
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
}

.btn {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s;
}

.btn-primary {
    background-color: #409EFF;
    color: white;
}

.btn-primary:hover:not(:disabled) {
    background-color: #337ecc;
}

.btn-success {
    background-color: #67C23A;
    color: white;
}

.btn-success:hover:not(:disabled) {
    background-color: #529b2e;
}

.btn-secondary {
    background-color: #909399;
    color: white;
}

.btn-secondary:hover {
    background-color: #73767a;
}

.btn:disabled {
    background-color: #c0c4cc;
    cursor: not-allowed;
}

.progress-section {
    background-color: #f0f9ff;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.progress-container {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 15px;
}

.progress-bar {
    flex: 1;
    height: 20px;
    background-color: #e4e7ed;
    border-radius: 10px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background-color: #67C23A;
    transition: width 0.3s ease;
}

.progress-text {
    font-weight: bold;
    color: #67C23A;
    min-width: 60px;
}

.model-progress {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.model-item {
    display: flex;
    justify-content: space-between;
    padding: 5px 0;
}

.model-item span:last-child {
    font-weight: bold;
}

.model-item span.completed {
    color: #67C23A;
}

.results-section {
    background-color: #f9f9f9;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.model-result {
    background-color: white;
    border-radius: 6px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.model-result h3 {
    color: #0056b3;
    margin-top: 0;
    margin-bottom: 15px;
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
}

.result-content {
    display: flex;
    flex-wrap: wrap;
    gap: 30px;
}

.metrics {
    flex: 1;
    min-width: 200px;
}

.metric-item {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid #f0f0f0;
}

.metric-label {
    color: #666;
}

.metric-value {
    font-weight: bold;
    color: #333;
}

.chart-container {
    flex: 2;
    min-width: 300px;
}

.chart-wrapper {
    background-color: white;
    border-radius: 6px;
    padding: 15px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.cluster-results,
.feature-importance {
    flex: 1;
    min-width: 300px;
}

.cluster-bars,
.importance-bars {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.cluster-bar,
.importance-bar {
    display: flex;
    align-items: center;
    gap: 10px;
}

.bar-label,
.feature-label {
    min-width: 80px;
    font-size: 12px;
    color: #666;
}

.bar-container,
.importance-container {
    flex: 1;
    height: 20px;
    background-color: #e4e7ed;
    border-radius: 10px;
    overflow: hidden;
    position: relative;
}

.bar-fill,
.importance-fill {
    height: 100%;
    background-color: #409EFF;
    transition: width 0.3s ease;
}

.bar-text,
.importance-text {
    position: absolute;
    right: 8px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 10px;
    color: #333;
    font-weight: bold;
}

.comparison-section {
    background-color: #f9f9f9;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.comparison-chart {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}

h1 {
    color: #333;
    text-align: center;
    margin-bottom: 10px;
}

h2 {
    color: #0056b3;
    margin-top: 0;
    margin-bottom: 15px;
}

h4 {
    color: #666;
    margin-bottom: 15px;
}

p {
    color: #666;
    text-align: center;
    margin-bottom: 30px;
}
</style>
