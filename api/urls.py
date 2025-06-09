from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.restaurant_views import RestaurantViewSet, RestaurantReviewViewSet, RestaurantFavoriteViewSet, Recommend_RestaurantViewSet
from .views.search_views import SearchAddressView, SearchLocationView
from .views.auth_views import UserLoginViewSet, UserRegisterViewSet, google_callback

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)       # `/api/restaurants/`
router.register(r'reviews', RestaurantReviewViewSet)     # `/api/reviews/`
router.register(r'favorites', RestaurantFavoriteViewSet) # `api/favorites/`

urlpatterns = [
    path('', include(router.urls)),
    # 查找地點經緯度
    path('search/location/', SearchLocationView.as_view(), name='search_location'),               # /api/search/location/
    # 搜尋提示
    path('search/address/', SearchAddressView.as_view(), name='search_address'),                 # /api/search/address/
    # 登入/註冊/Google登入
    path('auth/login/',UserLoginViewSet.as_view(), name='login'),                                # /api/auth/login/
    path('auth/register/',UserRegisterViewSet.as_view({'post': 'create'}), name='register'),     # /api/auth/register/
    path('google/callback', google_callback, name='google-login'),                               # /api/google/callback
    # 查找推薦餐廳
    path('recommend_restaurants/', Recommend_RestaurantViewSet.as_view({'get': 'list'}), name='recommend_restaurants'),       # /api/recommend
]