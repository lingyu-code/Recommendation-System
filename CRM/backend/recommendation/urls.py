from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'funds', views.FundViewSet)
router.register(r'insurance', views.InsuranceProductViewSet)
router.register(r'stocks', views.StockInfoViewSet)
router.register(r'stock-data', views.StockDailyDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('recommendations/', views.get_recommendations, name='get_recommendations'),
    path('dashboard/', views.get_dashboard_data, name='dashboard_data'),
    path('health/', views.health_check, name='health_check'),
]
