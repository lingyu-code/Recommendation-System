# 金融智能推荐系统

基于Django后端和Vue前端的金融智能推荐系统，提供投资和理财规划服务。

## 系统架构

- **后端**: Django + MySQL
- **前端**: Vue.js
- **推荐算法**: KNN、Apriori、FP-Growth

## 功能模块

### 投资中心
- 投资仪表盘：数据可视化展示
- 基金推荐：产品展示、相似推荐、搜索功能
- 股票推荐：推荐列表、搜索功能

### 理财规划
- 理财诊断：个人资产分布可视化
- 保险推荐：个性化保险推荐

### 个人中心
- 用户登录
- 个人信息管理
- 风险偏好设置

## 项目结构

```
financial_recommendation_system/
├── backend/                 # Django后端
├── frontend/               # Vue前端
├── data/                   # 数据文件
└── README.md
```

## 安装和运行

### 后端设置
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 前端设置
```bash
cd frontend
npm install
npm run serve
```

## 数据说明

系统使用示例数据，包括：
- 保险数据 (20条)
- 基金数据 
- 股票数据
- 用户信息
