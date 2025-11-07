import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from collections import defaultdict
import math
from .models import InsuranceProduct, Fund, StockInfo, StockDailyData, User, PurchaseRecord

class RecommendationEngine:
    """推荐算法引擎"""
    
    def __init__(self):
        self.scaler = StandardScaler()

    def get_mpt_suggestions(self, user_id):
        """
        根据Modern Portfolio Theory (MPT) 为用户提供资产配置建议。
        比较用户当前资产配置与基于风险偏好的科学配置，给出买入或卖出建议。
        """
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return []

        # 1. 获取用户当前资产配置
        user_allocation_data = self._get_user_current_asset_allocation(user_id)
        if not user_allocation_data:
            return []

        user_total_assets = user_allocation_data['total_amount']
        user_current_percentages = user_allocation_data['percentages']

        # 2. 获取科学资产配置（基于风险偏好）
        scientific_allocation_percentages = self._get_scientific_asset_allocation(user.risk_tolerance)

        suggestions = []
        for asset_type in ['fund', 'insurance', 'stock']:
            current_percentage = user_current_percentages.get(asset_type, 0)
            target_percentage = scientific_allocation_percentages.get(asset_type, 0)

            difference_percentage = target_percentage - current_percentage

            if abs(difference_percentage) > 0.01:  # Only suggest if there's a significant difference
                amount_to_adjust = user_total_assets * abs(difference_percentage) / 100
                
                if difference_percentage > 0:
                    suggestions.append({
                        'type': asset_type,
                        'action': '增加', # Increase
                        'amount': round(amount_to_adjust, 2),
                        'percentage': round(abs(difference_percentage), 1)
                    })
                else:
                    suggestions.append({
                        'type': asset_type,
                        'action': '减少', # Decrease
                        'amount': round(amount_to_adjust, 2),
                        'percentage': round(abs(difference_percentage), 1)
                    })
        return suggestions

    def _get_user_current_asset_allocation(self, user_id):
        """计算用户当前的资产配置比例和总金额"""
        purchase_records = PurchaseRecord.objects.filter(user_id=user_id)
        
        allocation = {
            'fund': 0,
            'insurance': 0,
            'stock': 0,
        }
        total_amount = 0

        for record in purchase_records:
            if record.purchase_type in allocation:
                amount = float(record.amount)
                allocation[record.purchase_type] += amount
                total_amount += amount
        
        if total_amount == 0:
            return None

        percentages = {
            'fund': (allocation['fund'] / total_amount) * 100,
            'insurance': (allocation['insurance'] / total_amount) * 100,
            'stock': (allocation['stock'] / total_amount) * 100,
        }
        return {'total_amount': total_amount, 'percentages': percentages}

    def _get_scientific_asset_allocation(self, risk_tolerance):
        """根据风险偏好返回科学的资产配置比例"""
        allocation_percentages = {}
        if risk_tolerance == 'low':
            allocation_percentages = { 'fund': 50, 'insurance': 30, 'stock': 20 }
        elif risk_tolerance == 'medium':
            allocation_percentages = { 'fund': 40, 'insurance': 30, 'stock': 30 }
        elif risk_tolerance == 'high':
            allocation_percentages = { 'fund': 30, 'insurance': 20, 'stock': 50 }
        else:
            # Default for unknown risk tolerance
            allocation_percentages = { 'fund': 40, 'insurance': 30, 'stock': 30 }
        return allocation_percentages

    def insurance_recommendation(self, user_profile, limit=5):
        """保险推荐算法 - 使用KNN和余弦相似度"""
        recommendations = []
        
        # 方法1: KNN基于用户画像
        knn_recommendations = self._knn_insurance_recommendation(user_profile, limit)
        recommendations.extend(knn_recommendations)
        
        # 方法2: 余弦相似度基于保险特征
        cosine_recommendations = self._cosine_insurance_recommendation(user_profile, limit)
        recommendations.extend(cosine_recommendations)
        
        # 去重并排序
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec['id'] not in seen:
                seen.add(rec['id'])
                unique_recommendations.append(rec)
        
        return unique_recommendations[:limit]
    
    def _knn_insurance_recommendation(self, user_profile, limit):
        """KNN保险推荐"""
        # 获取所有保险产品
        all_insurances = list(InsuranceProduct.objects.all())
        if not all_insurances:
            return []
        
        # 构建用户特征向量
        user_features = self._build_user_features(user_profile)
        
        # 构建保险特征矩阵
        insurance_features = []
        for insurance in all_insurances:
            features = self._build_insurance_features(insurance, user_profile)
            insurance_features.append(features)
        
        # 使用KNN找到最相似的保险
        if len(insurance_features) > 1:
            knn = NearestNeighbors(n_neighbors=min(limit, len(insurance_features)), metric='euclidean')
            knn.fit(insurance_features)
            distances, indices = knn.kneighbors([user_features])
            
            recommendations = []
            for idx in indices[0]:
                insurance = all_insurances[idx]
                recommendations.append({
                    'id': insurance.id,
                    'name': insurance.name,
                    'category': insurance.category,
                    'subcategory': insurance.subcategory,
                    'coverage_summary': insurance.coverage_summary,
                    'payout_limit': insurance.payout_limit,
                    'base_premium': insurance.base_premium,
                    'score': 1.0 / (distances[0][idx] + 1e-6),
                    'algorithm': 'KNN'
                })
            return recommendations
        return []
    
    def _cosine_insurance_recommendation(self, user_profile, limit):
        """余弦相似度保险推荐"""
        all_insurances = list(InsuranceProduct.objects.all())
        if not all_insurances:
            return []
        
        # 构建用户偏好向量
        user_vector = self._build_user_preference_vector(user_profile)
        
        # 计算每个保险的相似度
        similarities = []
        for insurance in all_insurances:
            insurance_vector = self._build_insurance_vector(insurance)
            similarity = cosine_similarity([user_vector], [insurance_vector])[0][0]
            similarities.append((insurance, similarity))
        
        # 按相似度排序
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        recommendations = []
        for insurance, similarity in similarities[:limit]:
            recommendations.append({
                'id': insurance.id,
                'name': insurance.name,
                'category': insurance.category,
                'subcategory': insurance.subcategory,
                'coverage_summary': insurance.coverage_summary,
                'payout_limit': insurance.payout_limit,
                'base_premium': insurance.base_premium,
                'score': similarity,
                'algorithm': 'Cosine Similarity'
            })
        
        return recommendations
    
    def fund_recommendation(self, user_profile, clicked_fund_id=None, limit=5):
        """基金推荐算法 - 使用协同过滤和FP-Growth思想"""
        recommendations = []
        
        # 方法1: 基于点击历史的协同过滤
        if clicked_fund_id:
            cf_recommendations = self._collaborative_filtering_fund(user_profile, clicked_fund_id, limit)
            recommendations.extend(cf_recommendations)
        
        # 方法2: 基于用户风险偏好的推荐
        risk_recommendations = self._risk_based_fund_recommendation(user_profile, limit)
        recommendations.extend(risk_recommendations)
        
        # 方法3: 热度推荐（新用户）
        if not recommendations:
            popularity_recommendations = self._popular_fund_recommendation(limit)
            recommendations.extend(popularity_recommendations)
        
        # 去重并排序
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec['id'] not in seen:
                seen.add(rec['id'])
                unique_recommendations.append(rec)
        
        return unique_recommendations[:limit]
    
    def _collaborative_filtering_fund(self, user_profile, clicked_fund_id, limit):
        """基于协同过滤的基金推荐"""
        try:
            clicked_fund = Fund.objects.get(id=clicked_fund_id)
        except Fund.DoesNotExist:
            return []
        
        # 获取所有基金
        all_funds = list(Fund.objects.exclude(id=clicked_fund_id))
        
        # 基于基金特征的相似度计算
        clicked_features = self._build_fund_features(clicked_fund)
        
        similarities = []
        for fund in all_funds:
            fund_features = self._build_fund_features(fund)
            similarity = cosine_similarity([clicked_features], [fund_features])[0][0]
            similarities.append((fund, similarity))
        
        # 按相似度排序
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        recommendations = []
        for fund, similarity in similarities[:limit]:
            recommendations.append({
                'id': fund.id,
                'code': fund.code,
                'name': fund.name,
                'type': fund.fund_type,
                'managers': fund.managers,
                'company': fund.company,
                'star_count': fund.star_count,
                'score': similarity,
                'algorithm': 'Collaborative Filtering'
            })
        
        return recommendations
    
    def _risk_based_fund_recommendation(self, user_profile, limit):
        """基于风险偏好的基金推荐"""
        # 根据风险偏好映射到基金类型
        risk_mapping = {
            'low': ['货币型', '债券型'],
            'medium': ['货币型', '债券型', '混合型'],
            'high': ['货币型', '债券型', '混合型', '股票型']
        }
        
        allowed_fund_types = risk_mapping.get(user_profile.risk_tolerance, ['货币型', '债券型'])
        suitable_funds = Fund.objects.filter(fund_type__in=allowed_fund_types)
        
        # 按星级排序
        sorted_funds = sorted(suitable_funds, 
                            key=lambda x: x.star_count if x.star_count else 0, 
                            reverse=True)
        
        recommendations = []
        for fund in sorted_funds[:limit]:
            recommendations.append({
                'id': fund.id,
                'code': fund.code,
                'name': fund.name,
                'type': fund.fund_type,
                'managers': fund.managers,
                'company': fund.company,
                'star_count': fund.star_count,
                'score': 0.8,  # 基础分数
                'algorithm': 'Risk-Based'
            })
        
        return recommendations
    
    def _popular_fund_recommendation(self, limit):
        """热度基金推荐"""
        # 按星级排序
        popular_funds = Fund.objects.all().order_by('-star_count')[:limit]
        
        recommendations = []
        for fund in popular_funds:
            recommendations.append({
                'id': fund.id,
                'code': fund.code,
                'name': fund.name,
                'type': fund.fund_type,
                'managers': fund.managers,
                'company': fund.company,
                'star_count': fund.star_count,
                'score': 0.7,  # 基础分数
                'algorithm': 'Popularity'
            })
        
        return recommendations
    
    def stock_recommendation(self, user_profile, limit=5):
        """股票推荐算法 - 使用行业相关性和趋势分析"""
        recommendations = []
        
        # 方法1: 行业相关性推荐
        industry_recommendations = self._industry_based_stock_recommendation(user_profile, limit)
        recommendations.extend(industry_recommendations)
        
        # 方法2: 趋势分析推荐
        trend_recommendations = self._trend_based_stock_recommendation(limit)
        recommendations.extend(trend_recommendations)
        
        # 去重并排序
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec['code'] not in seen:
                seen.add(rec['code'])
                unique_recommendations.append(rec)
        
        return unique_recommendations[:limit]
    
    def _industry_based_stock_recommendation(self, user_profile, limit):
        """基于行业相关性的股票推荐"""
        # 获取所有股票
        all_stocks = list(StockInfo.objects.all())
        
        recommendations = []
        for stock in all_stocks:
            # 基于风险偏好选择行业
            risk_industry_mapping = {
                'low': ['银行', '公用事业', '食品饮料'],
                'medium': ['银行', '公用事业', '食品饮料', '医药生物', '电子'],
                'high': ['计算机', '传媒', '通信', '电子', '医药生物']
            }
            
            preferred_industries = risk_industry_mapping.get(user_profile.risk_tolerance, ['银行', '公用事业'])
            industry_score = 1.0 if stock.industry in preferred_industries else 0.3
            
            # 综合分数（行业相关性 + 随机因素）
            import random
            random_score = random.uniform(0.5, 0.9)
            total_score = industry_score * 0.6 + random_score * 0.4
            
            recommendations.append({
                'code': stock.ts_code,
                'symbol': stock.symbol,
                'name': stock.name,
                'industry': stock.industry,
                'area': stock.area,
                'score': total_score,
                'algorithm': 'Industry Correlation'
            })
        
        # 按分数排序
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:limit]
    
    def _trend_based_stock_recommendation(self, limit):
        """基于趋势分析的股票推荐"""
        # 获取最新的股票数据（按交易日期排序）
        from django.db.models import Max
        latest_date = StockDailyData.objects.aggregate(Max('trade_date'))['trade_date__max']
        
        if latest_date:
            # 获取最新日期的股票数据
            latest_stocks = StockDailyData.objects.filter(trade_date=latest_date)
            
            recommendations = []
            for stock_data in latest_stocks:
                try:
                    stock_info = StockInfo.objects.get(ts_code=stock_data.ts_code)
                    
                    # 计算趋势分数（基于涨跌幅）
                    pct_chg_value = stock_data.pct_chg if stock_data.pct_chg is not None else 0.0
                    trend_score = min(1.0, max(0.1, abs(pct_chg_value) / 10.0 + 0.5))
                    
                    recommendations.append({
                        'code': stock_info.ts_code,
                        'symbol': stock_info.symbol,
                        'name': stock_info.name,
                        'industry': stock_info.industry,
                        'current_price': stock_data.close,
                        'change_rate': stock_data.pct_chg,
                        'score': trend_score,
                        'algorithm': 'Trend Analysis'
                    })
                except StockInfo.DoesNotExist:
                    continue
            
            # 按分数排序
            recommendations.sort(key=lambda x: x['score'], reverse=True)
            return recommendations[:limit]
        
        return []
    
    def _build_user_features(self, user_profile):
        """构建用户特征向量"""
        # 年龄归一化
        age = user_profile.age if user_profile.age is not None else 25 # Default age to 25 if None
        age_norm = min(age / 80.0, 1.0)
        
        # 风险偏好编码
        risk_mapping = {'low': 0.2, 'medium': 0.5, 'high': 0.8}
        risk_score = risk_mapping.get(user_profile.risk_tolerance, 0.5)
        
        # 资产归一化（假设最大资产1000万）
        total_assets = float(user_profile.total_assets) if user_profile.total_assets is not None else 100000.00 # Default assets if None
        assets_norm = min(total_assets / 10000000.0, 1.0)
        
        return [age_norm, risk_score, assets_norm]
    
    def _build_insurance_features(self, insurance, user_profile):
        """构建保险特征向量"""
        # 保费估算（从base_premium中提取数字）
        import re
        premium_match = re.search(r'(\d+)', insurance.base_premium)
        premium_value = float(premium_match.group(1)) if premium_match else 5000
        premium_norm = min(premium_value / 10000.0, 1.0)
        
        # 保险类型编码
        category_mapping = {
            '意外险': 0.2, '医疗险': 0.4, '寿险': 0.6, 
            '重疾险': 0.8, '养老险': 0.7, '财产险': 0.3
        }
        category_score = category_mapping.get(insurance.category, 0.5)
        
        # 标签匹配度（简单实现）
        tags = insurance.tags.lower() if insurance.tags else ''
        tag_score = 0.5
        
        # Handle user_profile.age being None
        user_age = user_profile.age if user_profile.age is not None else 25 

        if user_age < 30 and '年轻人' in tags:
            tag_score = 0.9
        elif user_age >= 30 and user_age < 50 and '家庭' in tags:
            tag_score = 0.9
        elif user_age >= 50 and '养老' in tags:
            tag_score = 0.9
        
        return [premium_norm, category_score, tag_score]
    
    def _build_user_preference_vector(self, user_profile):
        """构建用户偏好向量"""
        # 基于用户画像的偏好
        if user_profile.age < 30:
            return [0.8, 0.6, 0.3, 0.2, 0.1]  # 年轻人偏好意外险、医疗险
        elif user_profile.age < 50:
            return [0.6, 0.8, 0.7, 0.5, 0.3]  # 中年人偏好医疗险、重疾险、寿险
        else:
            return [0.4, 0.7, 0.8, 0.9, 0.6]  # 年长者偏好养老险、重疾险
    
    def _build_insurance_vector(self, insurance):
        """构建保险产品向量"""
        category_mapping = {
            '意外险': [1, 0, 0, 0, 0],
            '医疗险': [0, 1, 0, 0, 0],
            '寿险': [0, 0, 1, 0, 0],
            '重疾险': [0, 0, 0, 1, 0],
            '养老险': [0, 0, 0, 0, 1]
        }
        return category_mapping.get(insurance.category, [0.2, 0.2, 0.2, 0.2, 0.2])
    
    def _build_fund_features(self, fund):
        """构建基金特征向量"""
        # 基金类型风险编码
        type_risk_mapping = {
            '货币型': 0.1, '债券型': 0.3, '混合型': 0.6, '股票型': 0.8
        }
        risk_score = type_risk_mapping.get(fund.fund_type, 0.5)
        
        # 星级归一化
        star_norm = min(fund.star_count / 5.0, 1.0) if fund.star_count else 0.5
        
        # 手续费归一化
        fee_norm = min(fund.fee / 3.0, 1.0) if fund.fee else 0.5
        
        return [risk_score, star_norm, fee_norm]
