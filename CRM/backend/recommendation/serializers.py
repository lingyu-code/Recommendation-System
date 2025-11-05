from rest_framework import serializers
from .models import Fund, InsuranceProduct, StockInfo, StockDailyData, User, PurchaseRecord

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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                 'phone', 'age', 'risk_tolerance', 'total_assets', 'investment_goal')
        read_only_fields = ('id',)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 
                 'first_name', 'last_name', 'phone', 'age', 'risk_tolerance', 
                 'total_assets', 'investment_goal')

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError('密码不匹配')
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class PurchaseRecordSerializer(serializers.ModelSerializer):
    purchase_type_display = serializers.CharField(source='get_purchase_type_display', read_only=True)
    
    class Meta:
        model = PurchaseRecord
        fields = ('id', 'purchase_type', 'purchase_type_display', 'product_id', 'product_name', 
                 'amount', 'quantity', 'purchase_date', 'status')
        read_only_fields = ('id', 'purchase_date')

class PurchaseRequestSerializer(serializers.Serializer):
    product_type = serializers.ChoiceField(choices=['fund', 'insurance', 'stock'])
    product_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=15, decimal_places=2, min_value=0.01)
    quantity = serializers.IntegerField(required=False, allow_null=True)

class StockPurchaseRequestSerializer(serializers.Serializer):
    """股票购买请求序列化器"""
    policyholder_name = serializers.CharField(max_length=100, required=True)
    quantity = serializers.IntegerField(min_value=100)
    direction = serializers.ChoiceField(choices=['buy', 'sell'])
    stock_id = serializers.IntegerField()
