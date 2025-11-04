from rest_framework import serializers
from .models import Fund, InsuranceProduct, StockInfo, StockDailyData

class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = '__all__'

class InsuranceProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceProduct
        fields = '__all__'

class StockInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockInfo
        fields = '__all__'

class StockDailyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockDailyData
        fields = '__all__'

class RecommendationRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
    age = serializers.IntegerField(default=30)
    risk_tolerance = serializers.ChoiceField(
        choices=['low', 'medium', 'high'], 
        default='medium'
    )
    total_assets = serializers.FloatField(default=100000)
    investment_goal = serializers.CharField(max_length=100, required=False)
    limit = serializers.IntegerField(default=5)

class UserProfileSerializer(serializers.Serializer):
    age = serializers.IntegerField()
    risk_tolerance = serializers.ChoiceField(choices=['low', 'medium', 'high'])
    total_assets = serializers.FloatField()
    investment_goal = serializers.CharField(max_length=100, required=False)
