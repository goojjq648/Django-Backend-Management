from django.contrib.auth import views as auth_views
from django.urls import path
from . import views 

from .type_views import restaurant_views
from .type_views import system_setting_views as system_setting

app_name = 'admin_app'
urlpatterns = [
    # 登入/登出
    path('admin_login/', auth_views.LoginView.as_view(
        template_name='admin_app/base/sign_in.html'), name='adminlogin'),
    path('admin_logout/', auth_views.LogoutView.as_view(), name='adminlogout'),
    
    # 後台主頁面
    path('dashboard/', views.admin_mainPage, name='admin_dashboard'),
    path('get_admin_setting/', system_setting.fetch_admin_setting_data, name='getadminsetting'),
    path('confirm_editSetting/', system_setting.confirm_editSetting,
         name='confirmeditSetting'),
    
    # 後台右側頁面
    path('getpagedata/', views.getpagedata, name='getpagedata'),
    
    # 後台其他功能類頁面
    path('edit_restaurant/', restaurant_views.edit_restaurant_data, name='editrestaurant'),
    path('selectType/', system_setting.admin_select_type, name='selectType')
]
