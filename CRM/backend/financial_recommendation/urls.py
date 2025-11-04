from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views import View

class APIRootView(View):
    def get(self, request):
        api_endpoints = {
            "message": "金融智能推荐系统API",
            "endpoints": {
                "admin": "/admin/",
                "api_root": "/api/",
                "user_profiles": "/api/user-profiles/",
                "insurances": "/api/insurances/",
                "funds": "/api/funds/",
                "stocks": "/api/stocks/",
                "user_holdings": "/api/user-holdings/",
                "click_history": "/api/click-history/",
                "insurance_recommendations": "/api/insurance/recommended/?user_id=1",
                "fund_recommendations": "/api/fund/recommended/?user_id=1",
                "stock_recommendations": "/api/stock/recommended/?user_id=1",
                "financial_diagnosis": "/api/financial-diagnosis/"
            },
            "frontend": "请启动前端开发服务器访问完整界面"
        }
        return JsonResponse(api_endpoints)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('recommendation.urls')),
    path('', APIRootView.as_view(), name='api-root'),
]
