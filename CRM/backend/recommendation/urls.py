from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'user-profiles', views.UserProfileViewSet)
router.register(r'insurances', views.InsuranceViewSet)
router.register(r'funds', views.FundViewSet)
router.register(r'stocks', views.StockViewSet)
router.register(r'user-holdings', views.UserHoldingViewSet)
router.register(r'click-history', views.ClickHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('insurance/recommended/', views.InsuranceRecommendedView.as_view(), name='insurance-recommended'),
    path('fund/recommended/', views.FundRecommendedView.as_view(), name='fund-recommended'),
    path('stock/recommended/', views.StockRecommendedView.as_view(), name='stock-recommended'),
    path('financial-diagnosis/', views.FinancialDiagnosisView.as_view(), name='financial-diagnosis'),
]
