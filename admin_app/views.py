from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, FileResponse
from .admin_setting import AdminSetting
from django.shortcuts import render, get_object_or_404, redirect
from restaurant_app.models import Restaurant, Restaurantcategory, Businesshours, Category

# Create your views here.

def admin_login(request):
    return render(request, 'admin_app/base/sign_in.html')


def get_admin_setting():
    return AdminSetting()


def get_admin_setting_data(request):
    data = get_admin_setting().get_admin_func_type_list()

    return JsonResponse(data)


def confirm_editSetting(request):
    select_action = request.POST.get('admin_setting_action')
    main_type = request.POST.get('name')
    if not main_type:
        return HttpResponse('沒有填寫主類別名稱') 
    
    button_icon = request.POST.get('selected_main_Icon')
    if not button_icon:
        return HttpResponse('沒有設定主類別圖標') 

    sub_idx = request.POST.get('subcategory_Idx')
    sublist = {}
    
    for i in range(int(sub_idx)+1):
        # 子類別ID
        sub_id = request.POST.get('subcategories[' + str(i) + '][id]')
        # 子類別名稱
        sub_name = request.POST.get('subcategories[' + str(i) + '][name]')
        print(sub_id, sub_name)
        if not sub_id:
            return HttpResponse('沒有填寫子類別ID')
        if not sub_name:
            return HttpResponse('沒有填寫子類別名稱')
        
        sublist[sub_id] = sub_name
    
    # 處理設定檔
    get_admin_setting().edit_admin_func_type_list(main_type, button_icon, sublist)
    
    if select_action == 'addMainType':
        return HttpResponse('新增成功')
    else:
        return HttpResponse('修改成功')


@login_required(login_url = 'admin_app:adminlogin')
def admin_mainPage(request):
    admin_setting = get_admin_setting()
    admin_func_type_list = admin_setting.get_admin_func_type_list()
    return render(request, 'admin_app/base/admin_main_page.html', locals())


def getpagedata(request):
    pageID = request.GET.get('page_id')

    match pageID:
        case 'Home':
            return render(request, 'admin_app/base/home.html')
        case 'sub_restaurant':
            return restaurant(request)
        case 'sub_type':
            return sub_type(request)
        case 'sub_business_hours':
            return restaurant_business_hours(request)
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


def restaurant(request):
    title = '餐廳資料'
    fields = ['編號', '餐廳名稱', '評分', '評論數', '地址',
              '平均消費', '營業時間', '緯度', '經度', '圖片網址', '選項']

    restaurantDatas = Restaurant.objects.all()

    return render(request, 'admin_app/restaurant/sub_restaurant.html', locals())


def sub_type(request):
    title = '餐廳類型'
    fields = ['編號', '類型名稱']
    restaurantDatas = Category.objects.all()
    return render(request, 'admin_app/restaurant/sub_type.html', locals())


def restaurant_business_hours(request):
    title = '餐廳營業時間'
    fields = ['編號', '星期幾', '開始時間', '結束時間']
    restaurantDatas = Businesshours.objects.all()
    return render(request, 'admin_app/restaurant/sub_business_hours.html', locals())


def sub_setting(request, admin_list, mainType):
    return render(request, 'admin_app/SystemSetting/sub_setting.html', {'admin_list': admin_list, 'mainType': mainType})


def admin_select_type(request):
    mainType = request.GET.get('mainType')

    admin_setting = get_admin_setting()
    admin_list = admin_setting.get_admin_func_type_list()

    if mainType is None:
        return JsonResponse({})
    elif mainType == 'addMainType':
        return JsonResponse({})
    else:
        if admin_list[mainType] is not None:
            return JsonResponse(admin_list[mainType])

    # print(admin_list[mainType].items())

    return JsonResponse(admin_list[mainType])
