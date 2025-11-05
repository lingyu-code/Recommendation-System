from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom user model with additional financial profile fields"""
    RISK_CHOICES = [
        ('low', '低风险'),
        ('medium', '中风险'), 
        ('high', '高风险'),
    ]
    
    phone = models.CharField(max_length=15, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    risk_tolerance = models.CharField(max_length=10, choices=RISK_CHOICES, default='medium')
    total_assets = models.DecimalField(max_digits=15, decimal_places=2, default=100000.00)
    investment_goal = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'auth_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return f"{self.username} ({self.get_risk_tolerance_display()})"

class Fund(models.Model):
    code = models.CharField(max_length=10)  # 基金代码
    name = models.CharField(max_length=100)  # 简称
    managers = models.CharField(max_length=100)  # 基金经理（可能多个）
    company = models.CharField(max_length=50)  # 基金公司
    star_count = models.IntegerField(null=True, blank=True)  # 5星评级家数

    rating_shanghai = models.IntegerField(null=True, blank=True)  # 上海证券
    rating_zhaoshang = models.IntegerField(null=True, blank=True)  # 招商证券
    rating_jianxin = models.IntegerField(null=True, blank=True)  # 济安金信
    rating_morningstar = models.IntegerField(null=True, blank=True)  # 晨星评级

    fee = models.FloatField(null=True, blank=True)  # 手续费
    fund_type = models.CharField(max_length=50)  # 类型
    def __str__(self):
        return f"{self.name} ({self.code})"

class InsuranceProduct(models.Model):
    category = models.CharField(max_length=50)  # 险种大类
    subcategory = models.CharField(max_length=100)  # 具体险种
    name = models.CharField(max_length=100)  # 产品名称（含公司）
    coverage_summary = models.TextField()  # 保障内容简述
    payout_limit = models.CharField(max_length=100)  # 赔付/保额上限
    deductible_and_ratio = models.CharField(max_length=100)  # 免赔&给付比例
    base_premium = models.CharField(max_length=200)  # 基准保费（含性别/年龄）
    tags = models.CharField(max_length=200)  # 关键词标签

    def __str__(self):
        return self.name


class StockDailyData(models.Model):
    ts_code = models.CharField(max_length=20)  # 股票代码
    trade_date = models.DateField()  # 交易日期

    open = models.FloatField()  # 开盘价
    high = models.FloatField()  # 最高价
    low = models.FloatField()  # 最低价
    close = models.FloatField()  # 收盘价
    pre_close = models.FloatField()  # 前一日收盘价

    change = models.FloatField()  # 涨跌额
    pct_chg = models.FloatField()  # 涨跌幅（%）

    vol = models.FloatField()  # 成交量（万股）
    amount = models.FloatField()  # 成交额（万元）

    class Meta:
        unique_together = ('ts_code', 'trade_date')  # 避免重复记录

    def __str__(self):
        return f"{self.ts_code} - {self.trade_date}"

class StockInfo(models.Model):
    ts_code = models.CharField(max_length=20, unique=True)  # Tushare代码
    symbol = models.CharField(max_length=10)  # 股票代码
    name = models.CharField(max_length=50)  # 股票名称
    area = models.CharField(max_length=50)  # 所在地区
    industry = models.CharField(max_length=50)  # 所属行业
    list_date = models.DateField()  # 上市日期

    def __str__(self):
        return f"{self.name} ({self.ts_code})"

class PurchaseRecord(models.Model):
    """用户购买记录"""
    PURCHASE_TYPES = [
        ('fund', '基金'),
        ('insurance', '保险'),
        ('stock', '股票'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    purchase_type = models.CharField(max_length=10, choices=PURCHASE_TYPES)
    product_id = models.IntegerField()  # 对应基金、保险或股票的ID
    product_name = models.CharField(max_length=200)  # 产品名称
    amount = models.DecimalField(max_digits=15, decimal_places=2)  # 购买金额
    quantity = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)  # 购买数量（股票/基金份额）
    purchase_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='completed')  # 交易状态
    
    class Meta:
        ordering = ['-purchase_date']
        verbose_name = '购买记录'
        verbose_name_plural = '购买记录'

    def __str__(self):
        return f"{self.user.username} - {self.product_name} - {self.amount}"
