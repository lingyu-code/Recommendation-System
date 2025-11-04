from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Fund, InsuranceProduct, StockInfo, StockDailyData
from .serializers import (
    FundSerializer, InsuranceProductSerializer, 
    StockInfoSerializer, StockDailyDataSerializer,
    RecommendationRequestSerializer, UserProfileSerializer
)
from .recommendation_algorithms import RecommendationEngine

class FundViewSet(viewsets.ModelViewSet):
    queryset = Fund.objects.all()
    serializer_class = FundSerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """搜索基金"""
        query = request.query_params.get('q', '')
        if query:
            funds = Fund.objects.filter(name__icontains=query) | Fund.objects.filter(code__icontains=query)
            serializer = self.get_serializer(funds, many=True)
            return Response(serializer.data)
        return Response([])
    
    @action(detail=False, methods=['get'])
    def top_performers(self, request):
        """获取表现最好的基金"""
        funds = Fund.objects.all().order_by('-star_count')[:10]
        serializer = self.get_serializer(funds, many=True)
        return Response(serializer.data)

class InsuranceProductViewSet(viewsets.ModelViewSet):
    queryset = InsuranceProduct.objects.all()
    serializer_class = InsuranceProductSerializer
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """按类别获取保险产品"""
        category = request.query_params.get('category', '')
        if category:
            products = InsuranceProduct.objects.filter(category=category)
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        return Response([])
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """搜索保险产品"""
        query = request.query_params.get('q', '')
        if query:
            products = InsuranceProduct.objects.filter(name__icontains=query) | InsuranceProduct.objects.filter(tags__icontains=query)
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        return Response([])

class StockInfoViewSet(viewsets.ModelViewSet):
    queryset = StockInfo.objects.all()
    serializer_class = StockInfoSerializer
    
    @action(detail=False, methods=['get'])
    def by_industry(self, request):
        """按行业获取股票"""
        industry = request.query_params.get('industry', '')
        if industry:
            stocks = StockInfo.objects.filter(industry=industry)
            serializer = self.get_serializer(stocks, many=True)
            return Response(serializer.data)
        return Response([])
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """搜索股票"""
        query = request.query_params.get('q', '')
        if query:
            stocks = StockInfo.objects.filter(name__icontains=query) | StockInfo.objects.filter(symbol__icontains=query)
            serializer = self.get_serializer(stocks, many=True)
            return Response(serializer.data)
        return Response([])

class StockDailyDataViewSet(viewsets.ModelViewSet):
    queryset = StockDailyData.objects.all()
    serializer_class = StockDailyDataSerializer
    
    @action(detail=False, methods=['get'])
    def by_stock(self, request):
        """获取特定股票的日线数据"""
        ts_code = request.query_params.get('ts_code', '')
        if ts_code:
            data = StockDailyData.objects.filter(ts_code=ts_code).order_by('-trade_date')[:30]
            serializer = self.get_serializer(data, many=True)
            return Response(serializer.data)
        return Response([])

@api_view(['POST'])
def get_recommendations(request):
    """获取个性化推荐"""
    serializer = RecommendationRequestSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        
        # 创建推荐引擎
        engine = RecommendationEngine()
        
        # 创建用户档案对象（模拟）
        class UserProfile:
            def __init__(self, data):
                self.age = data.get('age', 30)
                self.risk_tolerance = data.get('risk_tolerance', 'medium')
                self.total_assets = data.get('total_assets', 100000)
                self.investment_goal = data.get('investment_goal', '')
                self.user = None
        
        user_profile = UserProfile(data)
        limit = data.get('limit', 5)
        
        # 获取各类推荐
        try:
            fund_recommendations = engine.fund_recommendation(user_profile, limit=limit)
            insurance_recommendations = engine.insurance_recommendation(user_profile, limit=limit)
            stock_recommendations = engine.stock_recommendation(user_profile, limit=limit)
            
            response_data = {
                'funds': fund_recommendations,
                'insurance': insurance_recommendations,
                'stocks': stock_recommendations,
                'user_profile': {
                    'age': user_profile.age,
                    'risk_tolerance': user_profile.risk_tolerance,
                    'total_assets': user_profile.total_assets,
                    'investment_goal': user_profile.investment_goal
                }
            }
            
            return Response(response_data)
            
        except Exception as e:
            return Response(
                {'error': f'推荐算法执行错误: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_dashboard_data(request):
    """获取仪表板数据"""
    try:
        # 统计数据
        total_funds = Fund.objects.count()
        total_insurance = InsuranceProduct.objects.count()
        total_stocks = StockInfo.objects.count()
        
        # 热门基金（按星级）
        popular_funds = Fund.objects.all().order_by('-star_count')[:5]
        fund_serializer = FundSerializer(popular_funds, many=True)
        
        # 热门股票（按行业分布）
        trending_stocks = StockInfo.objects.all()[:5]
        stock_serializer = StockInfoSerializer(trending_stocks, many=True)
        
        # 保险类别统计
        insurance_categories = InsuranceProduct.objects.values('category').distinct()
        
        dashboard_data = {
            'stats': {
                'total_funds': total_funds,
                'total_insurance': total_insurance,
                'total_stocks': total_stocks
            },
            'popular_funds': fund_serializer.data,
            'trending_stocks': stock_serializer.data,
            'insurance_categories': [cat['category'] for cat in insurance_categories]
        }
        
        return Response(dashboard_data)
        
    except Exception as e:
        return Response(
            {'error': f'获取仪表板数据错误: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def health_check(request):
    """健康检查端点"""
    return Response({'status': 'healthy', 'service': 'recommendation-backend'})
