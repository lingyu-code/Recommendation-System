import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from collections import defaultdict
import math
from .models import Insurance, Fund, Stock, UserProfile, ClickHistory, UserHolding

class RecommendationEngine:
    """推荐算法引擎"""
    
    def __init__(self):
        self.scaler = StandardScaler()
    
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
        all_insurances = list(Insurance.objects.all())
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
                    'type': insurance.insurance_type,
                    'premium': float(insurance.premium),
                    'description': insurance.description,
                    'score': 1.0 / (distances[0][idx] + 1e-6),
                    'algorithm': 'KNN'
                })
            return recommendations
        return []
    
    def _cosine_insurance_recommendation(self, user_profile, limit):
        """余弦相似度保险推荐"""
        all_insurances = list(Insurance.objects.all())
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
                'type': insurance.insurance_type,
                'premium': float(insurance.premium),
                'description': insurance.description,
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
                'net_value': float(fund.net_value),
                'daily_change': float(fund.daily_change),
                'score': similarity,
                'algorithm': 'Collaborative Filtering'
            })
        
        return recommendations
    
    def _risk_based_fund_recommendation(self, user_profile, limit):
        """基于风险偏好的基金推荐"""
        risk_mapping = {
            'low': ['low'],
            'medium': ['low', 'medium'],
            'high': ['low', 'medium', 'high']
        }
        
        allowed_risk_levels = risk_mapping.get(user_profile.risk_tolerance, ['low'])
        suitable_funds = Fund.objects.filter(risk_level__in=allowed_risk_levels)
        
        # 按收益率排序
        sorted_funds = sorted(suitable_funds, 
                            key=lambda x: abs(float(x.daily_change)), 
                            reverse=True)
        
        recommendations = []
        for fund in sorted_funds[:limit]:
            recommendations.append({
                'id': fund.id,
                'code': fund.code,
                'name': fund.name,
                'type': fund.fund_type,
                'net_value': float(fund.net_value),
                'daily_change': float(fund.daily_change),
                'score': 0.8,  # 基础分数
                'algorithm': 'Risk-Based'
            })
        
        return recommendations
    
    def _popular_fund_recommendation(self, limit):
        """热度基金推荐"""
        # 按点击量或收益率排序
        popular_funds = Fund.objects.all().order_by('-daily_change')[:limit]
        
        recommendations = []
        for fund in popular_funds:
            recommendations.append({
                'id': fund.id,
                'code': fund.code,
                'name': fund.name,
                'type': fund.fund_type,
                'net_value': float(fund.net_value),
                'daily_change': float(fund.daily_change),
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
        # 获取用户持有的股票行业
        user_holdings = UserHolding.objects.filter(user=user_profile.user, stock__isnull=False)
        user_industries = set(holding.stock.industry for holding in user_holdings if holding.stock)
        
        all_stocks = list(Stock.objects.all())
        
        recommendations = []
        for stock in all_stocks:
            # 计算行业相关性分数
            industry_score = 1.0 if stock.industry in user_industries else 0.3
            
            # 综合分数（行业相关性 + 涨跌幅）
            trend_score = min(1.0, max(0.1, abs(float(stock.change_rate)) / 10.0))
            total_score = industry_score * 0.6 + trend_score * 0.4
            
            recommendations.append({
                'code': stock.code,
                'name': stock.name,
                'industry': stock.industry,
                'current_price': float(stock.current_price),
                'change_rate': float(stock.change_rate),
                'score': total_score,
                'algorithm': 'Industry Correlation'
            })
        
        # 按分数排序
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:limit]
    
    def _trend_based_stock_recommendation(self, limit):
        """基于趋势分析的股票推荐"""
        # 按涨跌幅排序
        trending_stocks = Stock.objects.all().order_by('-change_rate')[:limit*2]
        
        recommendations = []
        for stock in trending_stocks:
            # 计算趋势分数
            trend_score = min(1.0, max(0.1, float(stock.change_rate) / 10.0 + 0.5))
            
            recommendations.append({
                'code': stock.code,
                'name': stock.name,
                'industry': stock.industry,
                'current_price': float(stock.current_price),
                'change_rate': float(stock.change_rate),
                'score': trend_score,
                'algorithm': 'Trend Analysis'
            })
        
        return recommendations[:limit]
    
    def _build_user_features(self, user_profile):
        """构建用户特征向量"""
        # 年龄归一化
        age_norm = min(user_profile.age / 80.0, 1.0)
        
        # 风险偏好编码
        risk_mapping = {'low': 0.2, 'medium': 0.5, 'high': 0.8}
        risk_score = risk_mapping.get(user_profile.risk_tolerance, 0.5)
        
        # 资产归一化（假设最大资产1000万）
        assets_norm = min(float(user_profile.total_assets) / 10000000.0, 1.0)
        
        return [age_norm, risk_score, assets_norm]
    
    def _build_insurance_features(self, insurance, user_profile):
        """构建保险特征向量"""
        # 保费归一化（假设最大保费10000）
        premium_norm = min(float(insurance.premium) / 10000.0, 1.0)
        
        # 年龄匹配度
        age_range = insurance.suitable_ages.split('-')
        if len(age_range) == 2:
            min_age, max_age = int(age_range[0]), int(age_range[1])
            age_match = 1.0 if min_age <= user_profile.age <= max_age else 0.3
        else:
            age_match = 0.5
        
        # 保险类型编码
        type_mapping = {
            '意外险': 0.2, '医疗险': 0.4, '寿险': 0.6, 
            '重疾险': 0.8, '养老险': 0.7, '财产险': 0.3
        }
        type_score = type_mapping.get(insurance.insurance_type, 0.5)
        
        return [premium_norm, age_match, type_score]
    
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
        type_mapping = {
            '意外险': [1, 0, 0, 0, 0],
            '医疗险': [0, 1, 0, 0, 0],
            '寿险': [0, 0, 1, 0, 0],
            '重疾险': [0, 0, 0, 1, 0],
            '养老险': [0, 0, 0, 0, 1]
        }
        return type_mapping.get(insurance.insurance_type, [0.2, 0.2, 0.2, 0.2, 0.2])
    
    def _build_fund_features(self, fund):
        """构建基金特征向量"""
        # 风险等级编码
        risk_mapping = {'low': 0.2, 'medium': 0.5, 'high': 0.8}
        risk_score = risk_mapping.get(fund.risk_level, 0.5)
        
        # 收益率归一化
        return_norm = min(abs(float(fund.daily_change)) / 10.0, 1.0)
        
        # 基金类型编码
        type_mapping = {
            '货币型': 0.1, '债券型': 0.3, '混合型': 0.6, '股票型': 0.8
        }
        type_score = type_mapping.get(fund.fund_type, 0.5)
        
        return [risk_score, return_norm, type_score]
