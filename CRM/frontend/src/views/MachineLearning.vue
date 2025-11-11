<template>
    <div class="machine-learning-container">
        <h1>机器学习演示</h1>

        <div class="section">
            <h2>股票价格预测 (回归)</h2>
            <div class="controls">
                <label for="stockSelector">选择股票:</label>
                <select id="stockSelector" v-model="selectedStock" @change="generateDataAndPredict">
                    <option v-for="stock in stockOptions" :key="stock.value" :value="stock.value">
                        {{ stock.label }}
                    </option>
                </select>
                <button @click="generateNewRandomStock">生成股票数据预测</button>
            </div>
            <div class="chart-container">
                <canvas id="regressionChart"></canvas>
            </div>
        </div>

        <div class="section">
            <h2>基金聚类分析 (K-Means)</h2>
            <div class="controls">
                <label for="numClusters">聚类数量 (K):</label>
                <input type="number" id="numClusters" v-model.number="numClusters" min="2" max="10">
                <label for="numFunds">基金数量:</label>
                <input type="number" id="numFunds" v-model.number="numFunds" min="20" max="500">
                <button @click="generateFundDataAndCluster">生成基金数据聚类</button>
            </div>
            <div class="chart-container">
                <canvas id="clusterChart"></canvas>
            </div>
        </div>

        <div class="section">
            <h2>保险决策树</h2>
            <div class="controls">
                <label for="numInsuranceClients">客户数量:</label>
                <input type="number" id="numInsuranceClients" v-model.number="numInsuranceClients" min="20" max="500">
                <label for="maxDepth">最大树深度:</label>
                <input type="number" id="maxDepth" v-model.number="maxDepth" min="1" max="5">
                <button @click="generateInsuranceDataAndTree">构建保险数据决策树</button>
            </div>
            <div class="chart-container">
                <canvas id="decisionTreeChart"></canvas>
            </div>
        </div>
    </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
    name: 'MachineLearning',
    data() {
        const stockOptions = [];
        for (let i = 1; i <= 200; i++) {
            stockOptions.push({ label: `股票 ${i}`, value: `stock_${i}` });
        }

        return {
            // Regression Data
            numDataPoints: 100,
            initialPrice: 100,
            volatility: 0.02, // Daily price change percentage
            regressionChart: null,
            data: [],
            predictions: [],
            predictedSlope: 0,
            predictedIntercept: 0,
            stockOptions: stockOptions,
            selectedStock: stockOptions[0].value,

            // Clustering Data
            numClusters: 3,
            numFunds: 100,
            fundData: [], // { x: return, y: risk, cluster: null }
            centroids: [], // { x: return, y: risk }
            clusterChart: null,

            // Decision Tree Data
            numInsuranceClients: 100,
            maxDepth: 3,
            insuranceData: [], // { age, income, children, buysInsurance }
            decisionTree: null, // Stores the built decision tree
            decisionTreeChart: null,
        };
    },
    mounted() {
        this.generateDataAndPredict();
        this.generateFundDataAndCluster();
        this.generateInsuranceDataAndTree();
    },
    methods: {
        // --- Regression Methods ---
        generateStockData() {
            this.data = [];
            let currentPrice = this.initialPrice + (Math.random() * 20 - 10); // Add some randomness to initial price
            for (let i = 0; i < this.numDataPoints; i++) {
                const x = i; // Time/Index
                const dailyChange = (Math.random() * 2 - 1) * this.volatility * currentPrice;
                currentPrice += dailyChange;
                this.data.push({ x, y: currentPrice });
            }
        },

        generateNewRandomStock() {
            this.generateStockData();
            this.performRegression();
            this.renderRegressionChart();
        },

        performRegression() {
            if (this.data.length === 0) {
                this.predictions = [];
                this.predictedSlope = 0;
                this.predictedIntercept = 0;
                return;
            }

            let sumX = 0;
            let sumY = 0;
            let sumXY = 0;
            let sumXX = 0;
            const n = this.data.length;

            for (const point of this.data) {
                sumX += point.x;
                sumY += point.y;
                sumXY += point.x * point.y;
                sumXX += point.x * point.x;
            }

            const denominator = (n * sumXX - sumX * sumX);
            if (denominator === 0) {
                this.predictedSlope = 0;
                this.predictedIntercept = sumY / n;
            } else {
                this.predictedSlope = (n * sumXY - sumX * sumY) / denominator;
                this.predictedIntercept = (sumY - this.predictedSlope * sumX) / n;
            }

            this.predictions = this.data.map(point => ({
                x: point.x,
                y: this.predictedSlope * point.x + this.predictedIntercept,
            }));
        },

        generateDataAndPredict() {
            this.generateStockData();
            this.performRegression();
            this.renderRegressionChart();
        },

        renderRegressionChart() {
            const ctx = document.getElementById('regressionChart').getContext('2d');

            if (this.regressionChart) {
                this.regressionChart.destroy();
            }

            this.regressionChart = new Chart(ctx, {
                type: 'scatter',
                data: {
                    datasets: [
                        {
                            label: `股票数据 (${this.selectedStock.toUpperCase()})`,
                            data: this.data,
                            backgroundColor: 'rgba(75, 192, 192, 0.6)',
                            borderColor: 'rgba(75, 192, 192, 1)',
                            pointRadius: 3,
                            showLine: true,
                            tension: 0.4,
                        },
                        {
                            label: `回归线 (y = ${this.predictedSlope.toFixed(2)}x + ${this.predictedIntercept.toFixed(2)})`,
                            data: this.predictions,
                            type: 'line',
                            fill: false,
                            borderColor: 'red',
                            tension: 0.1,
                            pointRadius: 0,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            type: 'linear',
                            position: 'bottom',
                            title: {
                                display: true,
                                text: '时间/索引',
                            },
                        },
                        y: {
                            title: {
                                display: true,
                                text: '股票价格',
                            },
                        },
                    },
                },
            });
        },

        // --- Clustering Methods ---
        generateFundData() {
            this.fundData = [];
            for (let i = 0; i < this.numFunds; i++) {
                // Generate random return and risk for funds
                const x = Math.random() * 20 - 5; // Returns between -5% and 15%
                const y = Math.random() * 15 + 2; // Risk between 2% and 17%
                this.fundData.push({ x, y, cluster: null });
            }
        },

        initializeCentroids() {
            this.centroids = [];
            const shuffledData = [...this.fundData].sort(() => 0.5 - Math.random());
            for (let i = 0; i < this.numClusters; i++) {
                this.centroids.push({ x: shuffledData[i].x, y: shuffledData[i].y });
            }
        },

        assignToClusters() {
            for (const fund of this.fundData) {
                let minDistance = Infinity;
                let closestCentroid = -1;

                for (let i = 0; i < this.centroids.length; i++) {
                    const centroid = this.centroids[i];
                    const distance = Math.sqrt(
                        Math.pow(fund.x - centroid.x, 2) + Math.pow(fund.y - centroid.y, 2)
                    );
                    if (distance < minDistance) {
                        minDistance = distance;
                        closestCentroid = i;
                    }
                }
                fund.cluster = closestCentroid;
            }
        },

        updateCentroids() {
            const newCentroids = Array(this.numClusters)
                .fill(null)
                .map(() => ({ x: 0, y: 0, count: 0 }));

            for (const fund of this.fundData) {
                if (fund.cluster !== null) {
                    newCentroids[fund.cluster].x += fund.x;
                    newCentroids[fund.cluster].y += fund.y;
                    newCentroids[fund.cluster].count++;
                }
            }

            for (let i = 0; i < this.numClusters; i++) {
                if (newCentroids[i].count > 0) {
                    this.centroids[i].x = newCentroids[i].x / newCentroids[i].count;
                    this.centroids[i].y = newCentroids[i].y / newCentroids[i].count;
                }
            }
        },

        performKMeans() {
            if (this.fundData.length === 0 || this.numClusters < 2) {
                return;
            }

            this.initializeCentroids();

            for (let i = 0; i < 10; i++) { // Iterate a few times for convergence
                this.assignToClusters();
                this.updateCentroids();
            }
        },

        generateFundDataAndCluster() {
            this.generateFundData();
            this.performKMeans();
            this.renderClusterChart();
        },

        renderClusterChart() {
            const ctx = document.getElementById('clusterChart').getContext('2d');

            if (this.clusterChart) {
                this.clusterChart.destroy();
            }

            const datasets = [];
            const colors = [
                'red', 'blue', 'green', 'purple', 'orange', 'brown', 'pink', 'cyan', 'magenta', 'lime'
            ];

            for (let i = 0; i < this.numClusters; i++) {
                datasets.push({
                    label: `聚类 ${i + 1}`,
                    data: this.fundData.filter(fund => fund.cluster === i),
                    backgroundColor: colors[i % colors.length],
                    pointRadius: 5,
                });
            }

            // Add centroids to the chart
            datasets.push({
                label: '中心点',
                data: this.centroids,
                backgroundColor: 'black',
                borderColor: 'black',
                pointStyle: 'crossRot',
                pointRadius: 10,
                pointBorderWidth: 3,
            });

            this.clusterChart = new Chart(ctx, {
                type: 'scatter',
                data: {
                    datasets: datasets,
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            type: 'linear',
                            position: 'bottom',
                            title: {
                                display: true,
                                text: '预期收益 (%)',
                            },
                        },
                        y: {
                            title: {
                                display: true,
                                text: '风险 (波动率 %)',
                            },
                        },
                    },
                },
            });
        },

        // --- Decision Tree Methods ---
        generateInsuranceData() {
            this.insuranceData = [];
            for (let i = 0; i < this.numInsuranceClients; i++) {
                const age = Math.floor(Math.random() * 60) + 20; // 20-79
                const income = Math.floor(Math.random() * 100000) + 20000; // 20k-120k
                const children = Math.floor(Math.random() * 4); // 0-3

                // Simple rule for buying insurance: older, higher income, more children
                let buysInsurance = 0;
                if (age > 45 && income > 60000) {
                    buysInsurance = 1;
                } else if (age > 30 && children > 1) {
                    buysInsurance = 1;
                } else if (income > 80000) {
                    buysInsurance = 1;
                }
                if (Math.random() < 0.2) { // Add some noise
                    buysInsurance = 1 - buysInsurance;
                }

                this.insuranceData.push({ age, income, children, buysInsurance });
            }
        },

        // Simplified Decision Tree (ID3-like, for demonstration)
        buildDecisionTree(data, features, target, depth) {
            if (depth > this.maxDepth || data.length === 0 || new Set(data.map(d => d[target])).size === 1) {
                const counts = {};
                data.forEach(d => {
                    counts[d[target]] = (counts[d[target]] || 0) + 1;
                });
                return { type: 'leaf', prediction: Object.keys(counts).reduce((a, b) => counts[a] > counts[b] ? a : b) };
            }

            let bestFeature = null;
            let maxGain = -1;

            for (const feature of features) {
                const gain = this.calculateInformationGain(data, feature, target);
                if (gain > maxGain) {
                    maxGain = gain;
                    bestFeature = feature;
                }
            }

            if (bestFeature === null) {
                const counts = {};
                data.forEach(d => {
                    counts[d[target]] = (counts[d[target]] || 0) + 1;
                });
                return { type: 'leaf', prediction: Object.keys(counts).reduce((a, b) => counts[a] > counts[b] ? a : b) };
            }

            const node = { type: 'node', feature: bestFeature, children: {} };
            const uniqueValues = [...new Set(data.map(d => d[bestFeature]))].sort((a, b) => a - b);

            // For numerical features, create binary splits
            if (typeof data[0][bestFeature] === 'number') {
                // Simple median split for demonstration
                const median = uniqueValues[Math.floor(uniqueValues.length / 2)];
                const leftData = data.filter(d => d[bestFeature] <= median);
                const rightData = data.filter(d => d[bestFeature] > median);

                if (leftData.length > 0) {
                    node.children[`<= ${median}`] = this.buildDecisionTree(leftData, features.filter(f => f !== bestFeature), target, depth + 1);
                }
                if (rightData.length > 0) {
                    node.children[`> ${median}`] = this.buildDecisionTree(rightData, features.filter(f => f !== bestFeature), target, depth + 1);
                }
            } else {
                // For categorical features (not used in this random data, but good practice)
                for (const value of uniqueValues) {
                    const subset = data.filter(d => d[bestFeature] === value);
                    node.children[value] = this.buildDecisionTree(subset, features.filter(f => f !== bestFeature), target, depth + 1);
                }
            }
            return node;
        },

        calculateInformationGain(data, feature, target) {
            const entropyBefore = this.calculateEntropy(data, target);
            const uniqueValues = [...new Set(data.map(d => d[feature]))];
            let entropyAfter = 0;

            for (const value of uniqueValues) {
                const subset = data.filter(d => d[feature] === value);
                const proportion = subset.length / data.length;
                entropyAfter += proportion * this.calculateEntropy(subset, target);
            }
            return entropyBefore - entropyAfter;
        },

        calculateEntropy(data, target) {
            const counts = {};
            data.forEach(d => {
                counts[d[target]] = (counts[d[target]] || 0) + 1;
            });

            let entropy = 0;
            for (const label in counts) {
                const proportion = counts[label] / data.length;
                entropy -= proportion * Math.log2(proportion);
            }
            return entropy;
        },

        // Predict method for the decision tree
        predict(tree, client) {
            if (tree.type === 'leaf') {
                return tree.prediction;
            }
            const featureValue = client[tree.feature];
            for (const rule in tree.children) {
                if (rule.includes('<=')) {
                    const threshold = parseFloat(rule.replace('<= ', ''));
                    if (featureValue <= threshold) {
                        return this.predict(tree.children[rule], client);
                    }
                } else if (rule.includes('>')) {
                    const threshold = parseFloat(rule.replace('> ', ''));
                    if (featureValue > threshold) {
                        return this.predict(tree.children[rule], client);
                    }
                } else if (featureValue == rule) { // For categorical, if implemented
                    return this.predict(tree.children[rule], client);
                }
            }
            // Fallback if no rule matches (shouldn't happen with a well-formed tree)
            return tree.prediction; // Return the most common prediction from the root
        },

        generateInsuranceDataAndTree() {
            this.generateInsuranceData();
            const features = ['age', 'income', 'children'];
            const target = 'buysInsurance';
            this.decisionTree = this.buildDecisionTree(this.insuranceData, features, target, 0);
            this.renderDecisionTreeChart();
        },

        renderDecisionTreeChart() {
            const ctx = document.getElementById('decisionTreeChart').getContext('2d');

            if (this.decisionTreeChart) {
                this.decisionTreeChart.destroy();
            }

            const datasets = [
                {
                    label: '预测不购买保险',
                    data: [],
                    backgroundColor: 'rgba(255, 99, 132, 0.6)', // Red for No
                    pointRadius: 5,
                },
                {
                    label: '预测购买保险',
                    data: [],
                    backgroundColor: 'rgba(75, 192, 192, 0.6)', // Green for Yes
                    pointRadius: 5,
                },
            ];

            this.insuranceData.forEach(client => {
                const prediction = this.predict(this.decisionTree, client);
                if (prediction == 0) {
                    datasets[0].data.push({ x: client.age, y: client.income });
                } else {
                    datasets[1].data.push({ x: client.age, y: client.income });
                }
            });

            this.decisionTreeChart = new Chart(ctx, {
                type: 'scatter',
                data: {
                    datasets: datasets,
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            type: 'linear',
                            position: 'bottom',
                            title: {
                                display: true,
                                text: '年龄',
                            },
                        },
                        y: {
                            type: 'linear',
                            title: {
                                display: true,
                                text: '收入',
                            },
                        },
                    },
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    const client = context.raw;
                                    const originalClient = this.insuranceData.find(d => d.age === client.x && d.income === client.y);
                                    return `年龄: ${client.x}, 收入: ${client.y}, 子女: ${originalClient.children}, 购买保险: ${originalClient.buysInsurance === 1 ? '是' : '否'} (预测: ${context.dataset.label.includes('购买') ? '是' : '否'})`;
                                }.bind(this),
                            },
                        },
                    },
                },
            });
        },
    },
};
</script>

<style scoped>
.machine-learning-container {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
    font-family: Arial, sans-serif;
}

h1 {
    text-align: center;
    color: #333;
    margin-bottom: 40px;
}

.section {
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 30px;
    margin-bottom: 40px;
}

.section h2 {
    text-align: center;
    color: #007bff;
    margin-bottom: 30px;
}

.controls {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
    align-items: center;
    margin-bottom: 40px;
}

.controls label {
    font-weight: bold;
    color: #555;
    min-width: 120px;
}

.controls input[type="number"],
.controls select {
    flex-grow: 1;
    padding: 8px 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 16px;
    max-width: 200px;
}

.controls select {
    background-color: #e9ecef;
    color: #333;
    border: 1px solid #ced4da;
    min-width: 150px;
}

.controls button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s ease;
}

.controls button:hover {
    background-color: #0056b3;
}

.chart-container {
    position: relative;
    height: 500px;
    width: 100%;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 20px;
}
</style>
