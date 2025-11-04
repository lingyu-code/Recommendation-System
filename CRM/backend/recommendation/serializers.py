from rest_framework import serializers
from .models import UserProfile, Insurance, Fund, Stock, UserHolding, ClickHistory

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = '__all__'

class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class UserHoldingSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)
    fund = FundSerializer(read_only=True)
    insurance = InsuranceSerializer(read_only=True)

    class Meta:
        model = UserHolding
        fields = '__all__'

class ClickHistorySerializer(serializers.ModelSerializer):
    insurance = InsuranceSerializer(read_only=True)
    fund = FundSerializer(read_only=True)
    stock = StockSerializer(read_only=True)

    class Meta:
        model = ClickHistory
        fields = '__all__'
