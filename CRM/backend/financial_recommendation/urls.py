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
                "funds": "/api/funds/",
                "insurance": "/api/insurance/",
                "stocks": "/api/stocks/",
                "stock_data": "/api/stock-data/",
                "recommendations": "/api/recommendations/",
                "dashboard": "/api/dashboard/",
                "health_check": "/api/health/"
            },
            "frontend": "请启动前端开发服务器访问完整界面"
        }
        return JsonResponse(api_endpoints)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('recommendation.urls')),
    path('', APIRootView.as_view(), name='api-root'),
]
