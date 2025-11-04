from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    occupation = models.CharField(max_length=100)
    family_status = models.CharField(max_length=50)  # 例如：单身、已婚、有子女
    risk_tolerance = models.CharField(max_length=20, choices=[
        ('low', '低风险'),
        ('medium', '中风险'),
        ('high', '高风险')
    ])
    total_assets = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class Insurance(models.Model):
    name = models.CharField(max_length=200)
    insurance_type = models.CharField(max_length=50)
    suitable_ages = models.CharField(max_length=50)
    premium = models.DecimalField(max_digits=10, decimal_places=2)
    coverage = models.TextField()
    description = models.TextField()
    tags = models.JSONField(default=list)  # 存储标签列表
    features = models.JSONField(default=list)  # 存储特性列表

    def __str__(self):
        return self.name

class Fund(models.Model):
    code = models.CharField(max_length=10)  # 基金代码
    name = models.CharField(max_length=200)
    fund_type = models.CharField(max_length=50)
    risk_level = models.CharField(max_length=20, choices=[
        ('low', '低风险'),
        ('medium', '中风险'),
        ('high', '高风险')
    ])
    net_value = models.DecimalField(max_digits=10, decimal_places=4)  # 净值
    daily_change = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # 日涨跌幅%
    week_change = models.DecimalField(max_digits=5, decimal_places=2)  # 周涨跌幅%
    month_change = models.DecimalField(max_digits=5, decimal_places=2)  # 月涨跌幅%
    manager = models.CharField(max_length=100)  # 基金经理
    establish_date = models.DateField()  # 成立日期
    scale = models.CharField(max_length=50)  # 规模
    description = models.TextField()
    tags = models.JSONField(default=list)
    features = models.JSONField(default=list)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Stock(models.Model):
    code = models.CharField(max_length=10)  # 股票代码
    name = models.CharField(max_length=100)
    industry = models.CharField(max_length=50)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    change_rate = models.DecimalField(max_digits=5, decimal_places=2)  # 涨跌幅%
    change_amount = models.DecimalField(max_digits=10, decimal_places=2)  # 涨跌额
    market_cap = models.DecimalField(max_digits=15, decimal_places=2)  # 市值
    pe_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # 市盈率
    pb_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # 市净率
    dividend_yield = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # 股息率%
    description = models.TextField()

    def __str__(self):
        return f"{self.code} - {self.name}"

class StockHistory(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='history_data')
    date = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.stock.code} - {self.date}"

class UserHolding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True, blank=True)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE, null=True, blank=True)
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.stock:
            return f"{self.user.username} - {self.stock.name}"
        elif self.fund:
            return f"{self.user.username} - {self.fund.name}"
        elif self.insurance:
            return f"{self.user.username} - {self.insurance.name}"
        return f"{self.user.username} - Holding"

class ClickHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE, null=True, blank=True)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE, null=True, blank=True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True, blank=True)
    clicked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.insurance:
            return f"{self.user.username} clicked insurance {self.insurance.name}"
        elif self.fund:
            return f"{self.user.username} clicked fund {self.fund.name}"
        elif self.stock:
            return f"{self.user.username} clicked stock {self.stock.name}"
        return f"{self.user.username} clicked item"
