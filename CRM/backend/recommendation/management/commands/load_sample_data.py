from django.core.management.base import BaseCommand
from recommendation.models import Insurance, Fund, Stock, StockHistory, User, UserProfile
import json
import os
from datetime import datetime

class Command(BaseCommand):
    help = 'Load sample data into the database'

    def handle(self, *args, **options):
        # 加载保险数据
        self.load_insurance_data()
        # 加载基金数据
        self.load_fund_data()
        # 加载股票数据
        self.load_stock_data()
        # 创建演示用户
        self.create_demo_users()
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded sample data'))

    def load_insurance_data(self):
        """加载保险数据"""
        insurance_file = os.path.join(os.path.dirname(__file__), '../../../../data_example/保险.json')
        
        with open(insurance_file, 'r', encoding='utf-8') as f:
            insurance_data = json.load(f)
        
        for item in insurance_data:
            Insurance.objects.get_or_create(
                id=item['id'],
                defaults={
                    'name': item['name'],
                    'insurance_type': item['type'],
                    'suitable_ages': item['suitable_ages'],
                    'premium': item['premium'],
                    'coverage': item['coverage'],
                    'description': item['description'],
                    'tags': item['tags'],
                    'features': item['features']
                }
            )
        
        self.stdout.write(f'Loaded {len(insurance_data)} insurance records')

    def load_fund_data(self):
        """加载基金数据"""
        fund_file = os.path.join(os.path.dirname(__file__), '../../../../data_example/基金.json')
        
        with open(fund_file, 'r', encoding='utf-8') as f:
            fund_data = json.load(f)
        
        for item in fund_data:
            # 处理涨跌幅字符串，去掉百分号并转换为小数
            daily_change = float(item['daily_change'].strip('%+'))
            week_change = float(item['week_change'].strip('%+'))
            month_change = float(item['month_change'].strip('%+'))
            
            Fund.objects.get_or_create(
                code=item['code'],
                defaults={
                    'name': item['name'],
                    'fund_type': item['type'],
                    'risk_level': 'high' if '高风险' in item['risk_level'] else 'medium' if '中风险' in item['risk_level'] else 'low',
                    'net_value': item['net_value'],
                    'daily_change': daily_change,
                    'week_change': week_change,
                    'month_change': month_change,
                    'manager': item['manager'],
                    'establish_date': datetime.strptime(item['establish_date'], '%Y-%m-%d').date(),
                    'scale': item['scale'],
                    'description': item['description'],
                    'tags': item['tags'],
                    'features': item.get('features', [])
                }
            )
        
        self.stdout.write(f'Loaded {len(fund_data)} fund records')

    def load_stock_data(self):
        """加载股票数据"""
        stock_file = os.path.join(os.path.dirname(__file__), '../../../../data_example/股票.json')
        
        with open(stock_file, 'r', encoding='utf-8') as f:
            stock_data = json.load(f)
        
        for item in stock_data:
            # 处理涨跌幅字符串，去掉百分号并转换为小数
            change_rate = float(item['change_rate'].strip('%+'))
            change_amount = float(item['change_amount'])
            
            # 处理市值字符串，去掉"亿元"并转换为数值
            market_cap_str = item['market_cap'].replace('亿元', '').strip()
            market_cap = float(market_cap_str) * 100000000  # 转换为元
            
            # 处理股息率字符串
            dividend_yield = float(item['dividend_yield'].strip('%')) if item['dividend_yield'] else None
            
            stock, created = Stock.objects.get_or_create(
                code=item['code'],
                defaults={
                    'name': item['name'],
                    'industry': item['industry'],
                    'current_price': item['current_price'],
                    'change_rate': change_rate,
                    'change_amount': change_amount,
                    'market_cap': market_cap,
                    'pe_ratio': item['pe_ratio'],
                    'pb_ratio': item['pb_ratio'],
                    'dividend_yield': dividend_yield,
                    'description': item['description']
                }
            )
            
            # 加载历史数据
            if created and 'history_data' in item:
                for history_item in item['history_data']:
                    StockHistory.objects.get_or_create(
                        stock=stock,
                        date=datetime.strptime(history_item['date'], '%Y-%m-%d').date(),
                        defaults={
                            'open_price': history_item['open'],
                            'close_price': history_item['close'],
                            'high_price': history_item['high'],
                            'low_price': history_item['low'],
                            'volume': history_item['volume']
                        }
                    )
        
        self.stdout.write(f'Loaded {len(stock_data)} stock records with history data')

    def create_demo_users(self):
        """创建演示用户"""
        demo_users = [
            {
                'username': 'demo1',
                'password': '123456',
                'age': 25,
                'occupation': '工程师',
                'family_status': '单身',
                'risk_tolerance': 'low',
                'total_assets': 500000
            },
            {
                'username': 'demo2',
                'password': '123456',
                'age': 35,
                'occupation': '经理',
                'family_status': '已婚',
                'risk_tolerance': 'medium',
                'total_assets': 1000000
            },
            {
                'username': 'demo3',
                'password': '123456',
                'age': 45,
                'occupation': '企业家',
                'family_status': '已婚有子女',
                'risk_tolerance': 'high',
                'total_assets': 3000000
            }
        ]
        
        for user_data in demo_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={'is_active': True}
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                
                UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'age': user_data['age'],
                        'occupation': user_data['occupation'],
                        'family_status': user_data['family_status'],
                        'risk_tolerance': user_data['risk_tolerance'],
                        'total_assets': user_data['total_assets']
                    }
                )
        
        self.stdout.write(f'Created {len(demo_users)} demo users')
