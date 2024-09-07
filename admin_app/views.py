from django.http import HttpResponse, JsonResponse, FileResponse
from .admin_setting import AdminSetting
from django.shortcuts import render, get_object_or_404, redirect
# from food_app.models import Restaurant, Restaurantcategory, Businesshours, Category

# Create your views here.

def get_admin_setting():
    return AdminSetting()

def get_admin_setting_data(request):
    data = get_admin_setting().get_admin_func_type_list()

    return JsonResponse(data)

def admin_mainPage(request):
    # 對應後台可以點選的 key = type, value = 子選單list(id : sub_name) (可以複數，沒有子選單就不處理給空值)
    admin_setting = get_admin_setting()
    admin_func_type_list = admin_setting.get_admin_func_type_list()
    return render(request, 'admin_app/base/admin_main_page.html', locals())


def getpagedata(request):
    pageID = request.GET.get('page_id')

    match pageID:
        case 'Home':
            return render(request, 'admin_app/base/home.html')
        case 'sub_restaurant':
            pass
            # return restaurant(request)
        case 'sub_type':
            pass
            # return sub_type(request)
        case 'sub_business_hours':
            pass
            # return restaurant_business_hours(request)
        case 'sub_setting':
            admin_setting = get_admin_setting()
            admin_list = admin_setting.get_admin_func_type_list()
            return sub_setting(request, admin_list, None)

    return render(request, 'admin_app/other/404.html')


def edit_restaurant_data(request):
    id = request.POST.get('restaurant_id')
    name = request.POST.get('restaurant_name')
    print(f'{id} {name} 更新成功')

    return render(request, 'admin_app/restaurant/sub_restaurant.html', locals())


# def restaurant(request):
#     title = '餐廳資料'
#     fields = ['編號', '餐廳名稱', '評分', '評論數', '地址',
#               '平均消費', '營業時間', '緯度', '經度', '圖片網址', '選項']

#     restaurantDatas = Restaurant.objects.all()

#     print(restaurantDatas)

#     return render(request, 'admin_app/restaurant/sub_restaurant.html', locals())


# def sub_type(request):
#     title = '餐廳類型'
#     fields = ['編號', '類型名稱']
#     restaurantDatas = Category.objects.all()
#     return render(request, 'admin_app/restaurant/sub_type.html', locals())


# def restaurant_business_hours(request):
#     title = '餐廳營業時間'
#     fields = ['編號', '星期幾', '開始時間', '結束時間']
#     restaurantDatas = Businesshours.objects.all()
#     return render(request, 'admin_app/restaurant/sub_business_hours.html', locals())


def sub_setting(request, admin_list, mainType):
    return render(request, 'admin_app/SystemSetting/sub_setting.html', {'admin_list': admin_list, 'mainType': mainType})

def admin_select_type(request):
    mainType = request.GET.get('mainType')
    
    admin_setting = get_admin_setting()
    admin_list = admin_setting.get_admin_func_type_list()

    print(admin_list[mainType])

    return sub_setting(request, admin_list, mainType)
