from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.db import models
from .models import Fund, InsuranceProduct, StockInfo, StockDailyData, User, PurchaseRecord
from .serializers import (
    FundSerializer, InsuranceProductSerializer, 
    StockInfoSerializer, StockDailyDataSerializer,
    UserSerializer, RegisterSerializer, PurchaseRecordSerializer, 
    PurchaseRequestSerializer, StockPurchaseRequestSerializer
)
from .recommendation_algorithms import RecommendationEngine

class FundViewSet(viewsets.ModelViewSet):
    queryset = Fund.objects.all()
    serializer_class = FundSerializer

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def recommendations(self, request):
        engine = RecommendationEngine()
        user_profile = request.user # Assuming request.user is the User object with profile info
        if not user_profile:
            return Response({"detail": "User profile not found."}, status=status.HTTP_400_BAD_REQUEST)
        
        # For fund recommendations, we might need a clicked_fund_id for collaborative filtering.
        # For now, we'll just use risk-based and popularity.
        recs = engine.fund_recommendation(user_profile)
        # The recommendations from the engine are already dicts, no need for serializer
        return Response(recs)
    

class InsuranceProductViewSet(viewsets.ModelViewSet):
    queryset = InsuranceProduct.objects.all()
    serializer_class = InsuranceProductSerializer

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def recommendations(self, request):
        engine = RecommendationEngine()
        user_profile = request.user # Assuming request.user is the User object with profile info
        if not user_profile:
            return Response({"detail": "User profile not found."}, status=status.HTTP_400_BAD_REQUEST)
        
        recs = engine.insurance_recommendation(user_profile)
        return Response(recs)
    

class StockInfoViewSet(viewsets.ModelViewSet):
    queryset = StockInfo.objects.all()
    serializer_class = StockInfoSerializer

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def recommendations(self, request):
        engine = RecommendationEngine()
        user_profile = request.user # Assuming request.user is the User object with profile info
        if not user_profile:
            return Response({"detail": "User profile not found."}, status=status.HTTP_400_BAD_REQUEST)
        
        recs = engine.stock_recommendation(user_profile)
        return Response(recs)
    

class StockDailyDataViewSet(viewsets.ModelViewSet):
    queryset = StockDailyData.objects.all()
    serializer_class = StockDailyDataSerializer


@api_view(['POST'])
def user_register(request):
    """用户注册"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        user_serializer = UserSerializer(user)
        return Response({
            'success': True,
            'message': '注册成功',
            'user': user_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def purchase_product(request):
    """购买产品（基金、保险、股票）"""
    if not request.user.is_authenticated:
        return Response({
            'success': False,
            'message': '用户未登录'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = PurchaseRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'success': False,
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    product_type = data['product_type']
    product_id = data['product_id']
    amount = data['amount']
    quantity = data.get('quantity')
    
    # 获取产品信息
    product_name = ""
    try:
        if product_type == 'fund':
            product = get_object_or_404(Fund, id=product_id)
            product_name = f"{product.name} ({product.code})"
        elif product_type == 'insurance':
            product = get_object_or_404(InsuranceProduct, id=product_id)
            product_name = product.name
        elif product_type == 'stock':
            product = get_object_or_404(StockInfo, id=product_id)
            product_name = f"{product.name} ({product.symbol})"
    except Exception as e:
        return Response({
            'success': False,
            'message': '产品不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # 创建购买记录
    purchase_record = PurchaseRecord.objects.create(
        user=request.user,
        purchase_type=product_type,
        product_id=product_id,
        product_name=product_name,
        amount=amount,
        quantity=quantity,
        status='completed'
    )
    
    # 更新用户总资产（这里简单处理，实际应该更复杂的逻辑）
    # request.user.total_assets -= amount
    # request.user.save()
    
    purchase_serializer = PurchaseRecordSerializer(purchase_record)
    
    return Response({
        'success': True,
        'message': '购买成功',
        'purchase': purchase_serializer.data
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_purchase_records(request):
    """获取用户的购买记录"""
    if not request.user.is_authenticated:
        return Response({
            'success': False,
            'message': '用户未登录'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    purchases = PurchaseRecord.objects.filter(user=request.user)
    serializer = PurchaseRecordSerializer(purchases, many=True)
    
    return Response({
        'success': True,
        'purchases': serializer.data
    })

@api_view(['POST'])
def purchase_stock(request):
    """股票交易（买入/卖出）"""
    if not request.user.is_authenticated:
        return Response({
            'message': '用户未登录'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = StockPurchaseRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'message': '参数验证失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    policyholder_name = data['policyholder_name']
    quantity = data['quantity']
    direction = data['direction']
    stock_id = data['stock_id']
    
    # 获取股票信息
    try:
        stock = get_object_or_404(StockInfo, id=stock_id)
    except Exception as e:
        return Response({
            'message': '股票不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # 获取最新股价（这里使用模拟数据，实际应该从数据库获取）
    # 在实际应用中，应该从 StockDailyData 获取最新价格
    current_price = 50.0  # 模拟价格，实际应该从数据库获取
    
    # 计算交易金额
    total_amount = quantity * current_price
    
    # 验证交易逻辑
    if direction == 'sell':
        # 检查用户是否持有足够的股票
        # 这里简化处理，实际应该检查用户的持仓
        user_holdings = PurchaseRecord.objects.filter(
            user=request.user,
            purchase_type='stock',
            product_id=stock_id,
            status='completed'
        ).aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
        
        if user_holdings < quantity:
            return Response({
                'message': f'持仓不足，当前持有{user_holdings}股，无法卖出{quantity}股'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    # 创建购买记录
    purchase_record = PurchaseRecord.objects.create(
        user=request.user,
        purchase_type='stock',
        product_id=stock_id,
        product_name=f"{stock.name} ({stock.symbol})",
        amount=total_amount,
        quantity=quantity,
        status='completed'
    )
    
    purchase_serializer = PurchaseRecordSerializer(purchase_record)
    
    return Response({
        'message': f'股票{direction == "buy" and "买入" or "卖出"}成功',
        'transaction': {
            'policyholder_name': policyholder_name,
            'stock_name': stock.name,
            'stock_code': stock.symbol,
            'direction': direction,
            'quantity': quantity,
            'price': current_price,
            'total_amount': total_amount,
            'transaction_time': purchase_record.purchase_date
        },
        'purchase_record': purchase_serializer.data
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_mpt_suggestions(request):
    """获取Modern Portfolio Theory (MPT) 资产配置建议"""
    if not request.user.is_authenticated:
        return Response({
            'success': False,
            'message': '用户未登录'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    engine = RecommendationEngine()
    user_profile_id = request.user.id # Assuming request.user is the User object
    
    suggestions = engine.get_mpt_suggestions(user_profile_id)
    
    return Response({
        'success': True,
        'suggestions': suggestions
    })

@api_view(['GET', 'PUT'])
def user_profile(request):
    """获取和更新用户个人信息"""
    if not request.user.is_authenticated:
        return Response({
            'success': False,
            'message': '用户未登录'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'GET':
        """获取用户信息"""
        serializer = UserSerializer(request.user)
        return Response({
            'success': True,
            'user': serializer.data
        })
    
    elif request.method == 'PUT':
        """更新用户信息"""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': '个人信息更新成功',
                'user': serializer.data
            })
        
        return Response({
            'success': False,
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
