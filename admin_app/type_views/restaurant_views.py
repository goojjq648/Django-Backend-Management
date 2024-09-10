from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from restaurant_app.models import Restaurant, Restaurantcategory, Businesshours, Category

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