<template>
    <div class="dashboard-container">
        <h1>金融仪表盘</h1>
        <p>欢迎来到您的个性化推荐仪表盘</p>


        <section class="recommendation-section">
            <h2>购买记录总览</h2>
            <div v-if="purchaseChartData.length > 0" class="chart-container">
                <div class="chart-wrapper">
                    <!-- Bar Chart SVG -->
                    <svg :width="purchaseChartWidth" :height="purchaseChartHeight"
                        :viewBox="`0 0 ${purchaseChartWidth} ${purchaseChartHeight}`">
                        <!-- X Axis -->
                        <line :x1="purchaseChartPadding" :y1="purchaseChartHeight - purchaseChartPadding"
                            :x2="purchaseChartWidth - purchaseChartPadding"
                            :y2="purchaseChartHeight - purchaseChartPadding" stroke="#ccc" />
                        <!-- Y Axis -->
                        <line :x1="purchaseChartPadding" :y1="purchaseChartPadding" :x2="purchaseChartPadding"
                            :y2="purchaseChartHeight - purchaseChartPadding" stroke="#ccc" />

                        <!-- Y Axis Labels -->
                        <text v-for="(label, index) in purchaseChartYScale" :key="'y-label-' + index"
                            :x="purchaseChartPadding - 5" :y="label.y" text-anchor="end" font-size="10" fill="#666"
                            alignment-baseline="middle">
                            {{ label.text }}
                        </text>

                        <!-- Bars -->
                        <rect v-for="(data, index) in purchaseChartData" :key="'bar-' + index"
                            :x="purchaseChartPadding + (index * (purchaseChartWidth - 2 * purchaseChartPadding) / purchaseChartData.length) + 5"
                            :y="purchaseChartPadding + (purchaseChartHeight - 2 * purchaseChartPadding) - (data.amount / purchaseChartMaxAmount) * (purchaseChartHeight - 2 * purchaseChartPadding)"
                            :width="(purchaseChartWidth - 2 * purchaseChartPadding) / purchaseChartData.length - 10"
                            :height="(data.amount / purchaseChartMaxAmount) * (purchaseChartHeight - 2 * purchaseChartPadding)"
                            fill="#409EFF" />

                        <!-- X Axis Labels -->
                        <text v-for="(label, index) in purchaseChartXScale" :key="'x-label-' + index" :x="label.x"
                            :y="purchaseChartHeight - purchaseChartPadding + 15" text-anchor="middle" font-size="10"
                            fill="#666">
                            {{ label.text }}
                        </text>
                    </svg>

                </div>
            </div>
            <p v-else>No purchase records available for visualization.</p>
        </section>

        <section class="recommendation-section">
            <h2>资产配置比较</h2>
            <div v-if="userAssetAllocation.length > 0 && scientificAssetAllocation.length > 0" class="chart-container">
                <div class="chart-wrapper">
                    <div class="pie-chart-wrapper">
                        <h3>你的配置</h3>
                        <svg :width="pieChartSize + 200" :height="pieChartSize + 200">
                            <g transform="translate(50, 50) rotate(-90, 100, 100)">
                                <path
                                    v-for="(slice, index) in generatePieChartSlices(userAssetAllocation, pieChartSize)"
                                    :key="'user-slice-' + index" :d="slice.path" :fill="slice.color"></path>
                            </g>
                            <g transform="translate(50, 50)">
                                <template
                                    v-for="(slice, index) in generatePieChartSlices(userAssetAllocation, pieChartSize)"
                                    :key="'user-slice-group-' + index">
                                    <line :x1="slice.lineStartX" :y1="slice.lineStartY" :x2="slice.lineEndX"
                                        :y2="slice.lineEndY" stroke="#666" stroke-width="1" />
                                    <text :x="slice.labelX" :y="slice.labelY" text-anchor="start" font-size="10"
                                        fill="#333">
                                        {{ slice.type === 'fund' ? '基金' : slice.type === 'insurance' ? '保险' : '股票'
                                        }} ({{ slice.percentage }}%)
                                    </text>
                                </template>
                            </g>
                        </svg>
                        <div class="legend">
                            <div v-for="(item, index) in userAssetAllocation" :key="'user-legend-' + index"
                                class="legend-item">
                                <span class="legend-color" :style="{ backgroundColor: item.color }"></span>
                                {{ item.type === 'fund' ? '基金' : item.type === 'insurance' ? '保险' : '股票' }}
                            </div>
                        </div>
                    </div>
                    <div class="pie-chart-wrapper">
                        <h3>科学的配置</h3>
                        <svg :width="pieChartSize + 200" :height="pieChartSize + 200">
                            <g transform="translate(50, 50) rotate(-90, 100, 100)">
                                <path
                                    v-for="(slice, index) in generatePieChartSlices(scientificAssetAllocation, pieChartSize)"
                                    :key="'scientific-slice-' + index" :d="slice.path" :fill="slice.color"></path>
                            </g>
                            <g transform="translate(50, 50)">
                                <template
                                    v-for="(slice, index) in generatePieChartSlices(scientificAssetAllocation, pieChartSize)"
                                    :key="'scientific-slice-group-' + index">
                                    <line :x1="slice.lineStartX" :y1="slice.lineStartY" :x2="slice.lineEndX"
                                        :y2="slice.lineEndY" stroke="#666" stroke-width="1" />
                                    <text :x="slice.labelX" :y="slice.labelY" text-anchor="start" font-size="10"
                                        fill="#333">
                                        {{ slice.type === 'fund' ? '基金' : slice.type === 'insurance' ? '保险' : '股票'
                                        }} ({{ slice.percentage }}%)
                                    </text>
                                </template>
                            </g>
                        </svg>
                        <div class="legend">
                            <div v-for="(item, index) in scientificAssetAllocation" :key="'scientific-legend-' + index"
                                class="legend-item">
                                <span class="legend-color" :style="{ backgroundColor: item.color }"></span>
                                {{ item.type === 'fund' ? '基金' : item.type === 'insurance' ? '保险' : '股票' }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <p v-else>No asset allocation data available for comparison.</p>
            <div class="mpt-suggestions">
                <h3>MPT 理论建议</h3>
                <div v-if="mptSuggestions.length > 0">
                    <ul>
                        <li v-for="(suggestion, index) in mptSuggestions" :key="'mpt-suggestion-' + index">
                            {{ suggestion.type === 'fund' ? '基金' : suggestion.type === 'insurance' ? '保险' : '股票' }}: {{
                                suggestion.action }} {{ suggestion.amount }}%
                        </li>
                    </ul>
                </div>
                <p v-else>No MPT suggestions available.</p>
            </div>
        </section>
    </div>
</template>

<script>
import { apiService } from '@/api';

export default {
    name: 'Dashboard',
    data() {
        return {
            purchaseRecords: [], // New data property for purchase records
            purchaseChartWidth: 600,
            purchaseChartHeight: 300,
            purchaseChartPadding: 40,
            pieChartSize: 200, // Define a size for the pie charts
            userProfile: null, // To store user profile data
            assetAllocationColors: ['#409EFF', '#67C23A', '#E6A23C'], // Colors for asset types (Funds, Insurance, Stocks)
            mptSuggestions: [], // New data property for MPT suggestions
        };
    },
    async created() {
        await this.fetchPurchaseRecords();
        await this.fetchUserProfile(); // Fetch user profile on creation
        await this.fetchMptSuggestions(); // Fetch MPT suggestions on creation
    },
    computed: {
        purchaseChartData() {
            const data = {};
            this.purchaseRecords.forEach(record => {
                const type = record.purchase_type;
                // Ensure data[type] is initialized as a number
                if (typeof data[type] !== 'number') {
                    data[type] = 0;
                }
                // Ensure record.amount is a number before adding
                const amount = parseFloat(record.amount);
                if (!isNaN(amount)) {
                    data[type] += amount;
                }
            });
            return Object.keys(data).map(type => ({
                type: type,
                amount: parseFloat(data[type].toFixed(2))
            }));
        },
        purchaseChartMaxAmount() {
            if (this.purchaseChartData.length === 0) return 0;
            return Math.max(...this.purchaseChartData.map(d => d.amount));
        },
        userAssetAllocation() {
            const allocation = {
                'fund': 0,
                'insurance': 0,
                'stock': 0,
            };
            this.purchaseRecords.forEach(record => {
                if (allocation.hasOwnProperty(record.purchase_type)) {
                    const amount = parseFloat(record.amount); // Parse amount here
                    if (!isNaN(amount)) { // Check if it's a valid number
                        allocation[record.purchase_type] += amount;
                    }
                }
            });
            const total = Object.values(allocation).reduce((sum, val) => sum + val, 0);
            if (total === 0) return [];
            return Object.keys(allocation).map((type, index) => ({
                type: type,
                amount: allocation[type],
                percentage: (allocation[type] / total * 100).toFixed(1),
                color: this.assetAllocationColors[index % this.assetAllocationColors.length],
            }));
        },
        scientificAssetAllocation() {
            if (!this.userProfile || !this.userProfile.risk_tolerance) {
                return [];
            }
            const riskTolerance = this.userProfile.risk_tolerance;
            let allocationPercentages = {};

            // Simplified scientific allocation model based on risk tolerance
            if (riskTolerance === 'low') {
                allocationPercentages = { 'fund': 0.5, 'insurance': 0.3, 'stock': 0.2 };
            } else if (riskTolerance === 'medium') {
                allocationPercentages = { 'fund': 0.4, 'insurance': 0.3, 'stock': 0.3 };
            } else if (riskTolerance === 'high') {
                allocationPercentages = { 'fund': 0.3, 'insurance': 0.2, 'stock': 0.5 };
            } else {
                // Default for unknown risk tolerance
                allocationPercentages = { 'fund': 0.4, 'insurance': 0.3, 'stock': 0.3 };
            }

            return Object.keys(allocationPercentages).map((type, index) => ({
                type: type,
                percentage: (allocationPercentages[type] * 100).toFixed(1),
                color: this.assetAllocationColors[index % this.assetAllocationColors.length],
            }));
        },
        purchaseChartXScale() {
            const labels = [];
            const chartInnerWidth = this.purchaseChartWidth - 2 * this.purchaseChartPadding;
            const barWidth = chartInnerWidth / this.purchaseChartData.length;

            this.purchaseChartData.forEach((data, index) => {
                labels.push({
                    x: this.purchaseChartPadding + index * barWidth + barWidth / 2,
                    text: data.type === 'fund' ? '基金' : data.type === 'insurance' ? '保险' : '股票'
                });
            });
            return labels;
        },
        purchaseChartYScale() {
            const labels = [];
            const numLabels = 5;
            const step = this.purchaseChartMaxAmount / (numLabels - 1);
            const chartInnerHeight = this.purchaseChartHeight - 2 * this.purchaseChartPadding;

            for (let i = 0; i < numLabels; i++) {
                const amount = i * step;
                const y = this.purchaseChartPadding + chartInnerHeight - (amount / this.purchaseChartMaxAmount) * chartInnerHeight;
                labels.push({
                    y: y,
                    text: amount.toFixed(0)
                });
            }
            return labels;
        },
    },
    methods: {
        async fetchUserProfile() {
            try {
                const response = await apiService.getProfile();
                if (response && response.user) {
                    this.userProfile = response.user;
                }
            } catch (error) {
                console.error('Error fetching user profile:', error);
            }
        },
        async fetchPurchaseRecords() {
            try {
                const response = await apiService.getPurchaseRecords();
                if (response && response.purchases) {
                    this.purchaseRecords = response.purchases;
                }
            } catch (error) {
                console.error('Error fetching purchase records:', error);
            }
        },
        async fetchMptSuggestions() {
            try {
                const response = await apiService.getMptSuggestions(); // Assuming this API call will be created
                if (response && response.suggestions) {
                    this.mptSuggestions = response.suggestions;
                }
            } catch (error) {
                console.error('Error fetching MPT suggestions:', error);
            }
        },
        generatePieChartSlices(data, chartSize) {
            let startAngle = 0;
            return data.map((item, index) => {
                const angle = parseFloat(item.percentage) / 100 * 360;
                const endAngle = startAngle + angle;

                const largeArcFlag = angle > 180 ? 1 : 0;

                const x1 = chartSize / 2 + chartSize / 2 * Math.sin(Math.PI * startAngle / 180);
                const y1 = chartSize / 2 - chartSize / 2 * Math.cos(Math.PI * startAngle / 180);

                const x2 = chartSize / 2 + chartSize / 2 * Math.sin(Math.PI * endAngle / 180);
                const y2 = chartSize / 2 - chartSize / 2 * Math.cos(Math.PI * endAngle / 180);

                const d = `M${chartSize / 2},${chartSize / 2} L${x1},${y1} A${chartSize / 2},${chartSize / 2} 0 ${largeArcFlag},1 ${x2},${y2} Z`;

                const midAngle = startAngle + angle / 2;
                const lineStartRadius = chartSize / 2;
                const lineEndRadius = chartSize / 2 + 20; // Extend line slightly outside

                const lineStartX = chartSize / 2 + lineStartRadius * Math.sin(Math.PI * midAngle / 180);
                const lineStartY = chartSize / 2 - lineStartRadius * Math.cos(Math.PI * midAngle / 180);

                const lineEndX = chartSize / 2 + lineEndRadius * Math.sin(Math.PI * midAngle / 180);
                const lineEndY = chartSize / 2 - lineEndRadius * Math.cos(Math.PI * midAngle / 180);

                const labelX = chartSize / 2 + (chartSize / 2 + 30) * Math.sin(Math.PI * midAngle / 180);
                const labelY = chartSize / 2 - (chartSize / 2 + 30) * Math.cos(Math.PI * midAngle / 180);

                startAngle = endAngle;

                return {
                    ...item,
                    path: d,
                    lineStartX,
                    lineStartY,
                    lineEndX,
                    lineEndY,
                    labelX,
                    labelY,
                    textAnchor: labelX > chartSize / 2 ? 'start' : 'end',
                };
            });
        },
    },
};
</script>

<style scoped>
.dashboard-container {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
    font-family: 'Arial', sans-serif;
}

.pie-chart-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 20px;
}

.legend {
    display: flex;
    flex-direction: column;
    margin-top: 10px;
}

.legend-item {
    display: flex;
    align-items: center;
    margin-bottom: 5px;
    font-size: 12px;
    color: #555;
}

.legend-color {
    width: 12px;
    height: 12px;
    border-radius: 3px;
    margin-right: 8px;
    display: inline-block;
}

h3 {
    text-align: center;
    color: #555;
    margin-bottom: 15px;
}

h1 {
    color: #333;
    text-align: center;
    margin-bottom: 30px;
}

.recommendation-section {
    background-color: #f9f9f9;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.recommendation-section h2 {
    color: #0056b3;
    margin-top: 0;
    margin-bottom: 15px;
    border-bottom: 2px solid #eee;
    padding-bottom: 10px;
}

.chart-container {
    display: flex;
    /* Use flexbox to arrange charts */
    justify-content: space-around;
    /* Distribute space around items */
    align-items: flex-start;
    /* Align items at the start of the cross axis */
    flex-wrap: wrap;
    /* Allow charts to wrap to the next line */
    margin-top: 20px;
}

.chart-wrapper {
    display: flex;
    gap: 40px;
    /* Space between charts */
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
}
</style>
