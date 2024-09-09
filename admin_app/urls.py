from django.urls import path
from . import views

app_name = 'admin_app'
urlpatterns = [
    path('dashboard/', views.admin_mainPage, name='admin_dashboard'),
    path('get_admin_setting/', views.get_admin_setting_data, name='getadminsetting'),
    path('confirm_editSetting/', views.confirm_editSetting, name='confirmeditSetting'),

    path('getpagedata/', views.getpagedata, name='getpagedata'),
    
    path('edit_restaurant/', views.edit_restaurant_data, name='editrestaurant'),
    path('selectType/', views.admin_select_type, name='selectType')
]