from django.contrib.auth import views as auth_views
from django.urls import path
from . import views 

from .type_views import restaurant_views
from .type_views import system_setting_views as system_setting
from .type_views import admin_user_views as admin_user

app_name = 'admin_app'
urlpatterns = [
    # 登入/登出
    path('admin_login/', auth_views.LoginView.as_view(
        template_name='admin_app/base/sign_in.html'), name='adminlogin'),
    path('admin_logout/', auth_views.LogoutView.as_view(), name='adminlogout'),
    
    # 後台主頁面
    path('dashboard/', views.admin_mainPage, name='admin_dashboard'),
    path('loadscript/', views.check_dyamic_jsfile, name='loadscript'),
    
    # 後台右側頁面
    path('getpagedata/', views.getpagedata, name='getpagedata'),
    
    # 系統設定 - 類別設定 
    path('get_admin_setting/', system_setting.fetch_admin_setting_data, name='getadminsetting'),
    path('selectType/', system_setting.admin_select_type, name='selectType'),
    path('confirm_editSetting/', system_setting.confirm_editSetting, name='confirmeditSetting'),
    path('confirm_deleteSetting/', system_setting.confirm_delete_mainType, name='confirmdeleteSetting'),

    # 後臺會員
    path('create_admin_member/', admin_user.create_admin_member, name='create_user'),

    # 餐廳
    path('edit_restaurant/', restaurant_views.edit_restaurant_data, name='editrestaurant'),
    path('check_restaurantdata/', restaurant_views.check_restaurantdata, name='checkrestaurantdata'),
    path('del_restaurant/', restaurant_views.del_restaurant, name='delrestaurantdata'),
]
