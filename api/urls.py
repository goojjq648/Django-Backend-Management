from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)  # 讓 `/api/restaurants/` 成為 API 端點

urlpatterns = [
    path('', include(router.urls)),
]