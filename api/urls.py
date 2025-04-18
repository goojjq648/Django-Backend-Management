from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.restaurant_views import RestaurantViewSet
from .views.search_views import SearchAddressView
from .views.auth_views import google_callback

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)  # 讓 `/api/restaurants/` 成為 API 端點

urlpatterns = [
    path('', include(router.urls)),
    path('search/address/', SearchAddressView.as_view(), name='search_address'),  # /api/search/address/
    path('google/callback', google_callback, name='google-login'),                # /api/google/callback
]