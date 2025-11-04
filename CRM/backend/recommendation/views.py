from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import UserProfile, Insurance, Fund, Stock, UserHolding, ClickHistory
from .serializers import (
    UserProfileSerializer, InsuranceSerializer, FundSerializer, 
    StockSerializer, UserHoldingSerializer, ClickHistorySerializer
)
from .recommendation_algorithms import RecommendationEngine
import json

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class InsuranceViewSet(viewsets.ModelViewSet):
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerializer

    @action(detail=False, methods=['get'])
    def recommended(self, request):
        user_id = request.query_params.get('user_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                user_profile = UserProfile.objects.get(user=user)
                engine = RecommendationEngine()
                recommended_insurances_data = engine.insurance_recommendation(user_profile)
                # 获取实际的保险对象
                insurance_ids = [rec['id'] for rec in recommended_insurances_data]
                recommended_insurances = Insurance.objects.filter(id__in=insurance_ids)
                serializer = self.get_serializer(recommended_insurances, many=True)
                return Response(serializer.data)
            except (User.DoesNotExist, UserProfile.DoesNotExist):
                return Response({"error": "User or user profile not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "user_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

class FundViewSet(viewsets.ModelViewSet):
    queryset = Fund.objects.all()
    serializer_class = FundSerializer

    @action(detail=False, methods=['get'])
    def recommended(self, request):
        user_id = request.query_params.get('user_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                user_profile = UserProfile.objects.get(user=user)
                engine = RecommendationEngine()
                recommended_funds_data = engine.fund_recommendation(user_profile)
                # 获取实际的基金对象
                fund_ids = [rec['id'] for rec in recommended_funds_data]
                recommended_funds = Fund.objects.filter(id__in=fund_ids)
                serializer = self.get_serializer(recommended_funds, many=True)
                return Response(serializer.data)
            except (User.DoesNotExist, UserProfile.DoesNotExist):
                return Response({"error": "User or user profile not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "user_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    @action(detail=False, methods=['get'])
    def recommended(self, request):
        user_id = request.query_params.get('user_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                user_profile = UserProfile.objects.get(user=user)
                engine = RecommendationEngine()
                recommended_stocks_data = engine.stock_recommendation(user_profile)
                # 获取实际的股票对象
                stock_codes = [rec['code'] for rec in recommended_stocks_data]
                recommended_stocks = Stock.objects.filter(code__in=stock_codes)
                serializer = self.get_serializer(recommended_stocks, many=True)
                return Response(serializer.data)
            except (User.DoesNotExist, UserProfile.DoesNotExist):
                return Response({"error": "User or user profile not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "user_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

class UserHoldingViewSet(viewsets.ModelViewSet):
    queryset = UserHolding.objects.all()
    serializer_class = UserHoldingSerializer

    def get_queryset(self):
        queryset = UserHolding.objects.all()
        user_id = self.request.query_params.get('user_id')
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        return queryset

class ClickHistoryViewSet(viewsets.ModelViewSet):
    queryset = ClickHistory.objects.all()
    serializer_class = ClickHistorySerializer

    def create(self, request):
        user_id = request.data.get('user_id')
        insurance_id = request.data.get('insurance_id')
        fund_id = request.data.get('fund_id')
        stock_id = request.data.get('stock_id')

        try:
            user = User.objects.get(id=user_id)
            click_history = ClickHistory.objects.create(
                user=user,
                insurance_id=insurance_id if insurance_id else None,
                fund_id=fund_id if fund_id else None,
                stock_id=stock_id if stock_id else None
            )
            serializer = self.get_serializer(click_history)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class InsuranceRecommendedView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                user_profile = UserProfile.objects.get(user=user)
                engine = RecommendationEngine()
                recommended_insurances_data = engine.insurance_recommendation(user_profile)
                # 获取实际的保险对象
                insurance_ids = [rec['id'] for rec in recommended_insurances_data]
                recommended_insurances = Insurance.objects.filter(id__in=insurance_ids)
                serializer = InsuranceSerializer(recommended_insurances, many=True)
                return Response(serializer.data)
            except (User.DoesNotExist, UserProfile.DoesNotExist):
                return Response({"error": "User or user profile not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "user_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)


class FundRecommendedView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                user_profile = UserProfile.objects.get(user=user)
                engine = RecommendationEngine()
                recommended_funds_data = engine.fund_recommendation(user_profile)
                # 获取实际的基金对象
                fund_ids = [rec['id'] for rec in recommended_funds_data]
                recommended_funds = Fund.objects.filter(id__in=fund_ids)
                serializer = FundSerializer(recommended_funds, many=True)
                return Response(serializer.data)
            except (User.DoesNotExist, UserProfile.DoesNotExist):
                return Response({"error": "User or user profile not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "user_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)


class StockRecommendedView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                user_profile = UserProfile.objects.get(user=user)
                engine = RecommendationEngine()
                recommended_stocks_data = engine.stock_recommendation(user_profile)
                # 获取实际的股票对象
                stock_codes = [rec['code'] for rec in recommended_stocks_data]
                recommended_stocks = Stock.objects.filter(code__in=stock_codes)
                serializer = StockSerializer(recommended_stocks, many=True)
                return Response(serializer.data)
            except (User.DoesNotExist, UserProfile.DoesNotExist):
                return Response({"error": "User or user profile not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "user_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)


class FinancialDiagnosisView(APIView):
    def post(self, request):
        try:
            data = request.data
            user_id = data.get('user_id')
            income = data.get('income')
            expenses = data.get('expenses')
            savings = data.get('savings')
            risk_tolerance = data.get('risk_tolerance')
            investment_goal = data.get('investment_goal')
            
            if not all([user_id, income, expenses, savings, risk_tolerance, investment_goal]):
                return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
            
            # 简单的理财诊断逻辑
            savings_ratio = savings / income if income > 0 else 0
            expense_ratio = expenses / income if income > 0 else 0
            
            diagnosis_result = {
                "savings_health": "良好" if savings_ratio >= 0.2 else "需要改善",
                "expense_control": "良好" if expense_ratio <= 0.6 else "需要控制",
                "recommended_actions": [],
                "risk_assessment": risk_tolerance,
                "investment_suggestions": []
            }
            
            if savings_ratio < 0.2:
                diagnosis_result["recommended_actions"].append("建议增加储蓄比例至收入的20%以上")
            
            if expense_ratio > 0.6:
                diagnosis_result["recommended_actions"].append("建议控制支出在收入的60%以内")
            
            # 根据风险承受能力和投资目标给出建议
            if risk_tolerance == "保守":
                diagnosis_result["investment_suggestions"].append("建议配置货币基金、定期存款等低风险产品")
            elif risk_tolerance == "稳健":
                diagnosis_result["investment_suggestions"].append("建议配置债券基金、混合基金等中等风险产品")
            else:
                diagnosis_result["investment_suggestions"].append("建议配置股票基金、指数基金等高风险高收益产品")
            
            return Response(diagnosis_result)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
