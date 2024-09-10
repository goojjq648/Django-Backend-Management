from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render, get_object_or_404, redirect
# 後台會員管理功能
from .type_views import admin_user_views as admin_user
# 類別設定
from .type_views import system_setting_views as system_setting
# 餐廳功能
from .type_views import restaurant_views

# Create your views here.

def admin_login(request):
    return render(request, 'admin_app/base/sign_in.html')


@login_required(login_url = 'admin_app:adminlogin')
def admin_mainPage(request):
    admin_func_type_list = system_setting.retrieve_admin_setting_data()
    return render(request, 'admin_app/base/admin_main_page.html', locals())

@login_required(login_url = 'admin_app:adminlogin')
def getpagedata(request):
    pageID = request.GET.get('page_id')

    match pageID:
        case 'Home':
            return render(request, 'admin_app/base/home.html')
        case 'sub_restaurant':
            return restaurant_views.restaurant(request)
        case 'sub_type':
            return restaurant_views.sub_type(request)
        case 'sub_business_hours':
            return restaurant_views.restaurant_business_hours(request)
        case 'sub_setting':
            admin_list = system_setting.retrieve_admin_setting_data()
            return system_setting.sub_setting(request, admin_list, None)
        case 'sub_admin_member':
            return admin_user.sub_admin_member(request)

    return render(request, 'admin_app/other/404.html')

