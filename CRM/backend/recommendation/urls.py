from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'funds', views.FundViewSet)
router.register(r'insurance', views.InsuranceProductViewSet)
router.register(r'stocks', views.StockInfoViewSet)
router.register(r'stock-data', views.StockDailyDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', views.user_register, name='user_register'),
    path('auth/profile/', views.user_profile, name='user_profile'),
    path('purchase/', views.purchase_product, name='purchase_product'),
    path('purchase/records/', views.get_purchase_records, name='purchase_records'),
    path('purchase/stock/', views.purchase_stock, name='purchase_stock'),
    path('mpt-suggestions/', views.get_mpt_suggestions, name='mpt_suggestions'),
]
