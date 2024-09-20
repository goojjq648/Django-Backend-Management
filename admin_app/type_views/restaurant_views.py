from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from restaurant_app.models import Restaurant, Restaurantcategory, Businesshours, Category
import json

def edit_restaurant_data(request):
    if request.method != 'POST':
        return HttpResponse('請求錯誤')
    
    id = request.POST.get('restaurant_id')
    action = request.POST.get('restaurant_action')
    name = request.POST.get('restaurant_name')
    rating = request.POST.get('restaurant_rating')
    review_count = request.POST.get('restaurant_review_count')
    address = request.POST.get('restaurant_address')
    average_spending = request.POST.get('restaurant_average_spending')
    opening_hours = request.POST.get('restaurant_business_hours')
    latitude = request.POST.get('restaurant_latitude')
    longitude = request.POST.get('restaurant_longitude')
    image_url = request.POST.get('restaurant_image_url')

    if action == 'create':
        Restaurant.objects.create(
            name=name, 
            rating=rating, 
            review_count=review_count, 
            address=address, 
            average_spending=average_spending, 
            opening_hours=opening_hours, 
            latitude=latitude, 
            longitude=longitude, 
            image_url=image_url
        );
    elif action == 'edit':
        Restaurant.objects.filter(id=id).update(
        name=name, 
        rating=rating, 
        review_count=review_count, 
        address=address, 
        average_spending=average_spending, 
        opening_hours=opening_hours, 
        latitude=latitude, 
        longitude=longitude, 
        image_url=image_url
    )
        
    return restaurant(request)
    # return render(request, 'admin_app/restaurant/sub_restaurant.html', locals())

def check_restaurantdata(request):
    response_data = {'action': 0, 'message': ''}

    if request.method != 'GET':
        return JsonResponse({'action': 0, 'message': '無效的請求方法'})
    
    # 檢查餐廳名稱
    name = request.GET.get('restaurant_name')
    if name is not None:
        if name == '':
            return JsonResponse({'action': 0, 'message': '餐廳名稱不能為空！'})
        
        if Restaurant.objects.filter(name=name).exists():
            return JsonResponse({'action': 0, 'message': '餐廳名稱重複！請確認'})
    
    # 檢查評分
    rating = request.GET.get('restaurant_rating')
    if rating is not None:
        if rating != '':
            if float(rating) not in range(0, 6):
                return JsonResponse({'action': 0, 'message': '評分必須在0到5之間！'})

    # 檢查營業時間
    business_hours = request.GET.get('restaurant_business_hours')
    if business_hours is not None:
        try:
            json.loads(business_hours)  # 嘗試解析字串為 JSON
            print("JSON 解析成功")
        except json.JSONDecodeError:
            print("JSON 解析失敗")
            return JsonResponse({'action': 0, 'message': '營業時間必須為JSON格式！'})
    
    # 經度
    longitude = request.GET.get('restaurant_longitude')
    if longitude is not None:
        if longitude == '':
            return JsonResponse({'action': 0, 'message': '經度不能為空！'})
        
        if float(longitude) > 180 or float(longitude) < -180:
            return JsonResponse({'action': 0, 'message': '經度必須在-180到180之間！'})
    
    # 緯度
    latitude = request.GET.get('restaurant_latitude')
    if latitude is not None:
        if latitude == '':
            return JsonResponse({'action': 0, 'message': '緯度不能為空！'})

        if float(latitude) > 90 or float(latitude) < -90:
            return JsonResponse({'action': 0, 'message': '緯度必須在-90到90之間！'})

    
    response_data['action'] = 1
    response_data['message'] = "檢查完成"
    
    return JsonResponse(response_data)


def restaurant(request):
    sub_title = '餐廳資料'
    field_names = [field.verbose_name for field in Restaurant._meta.fields]
    restaurant_data_list = [restaurant.as_dict() for restaurant in Restaurant.objects.all()]

    # 新增選項
    field_names.append('選項')

    # fields = ['編號', '餐廳名稱','hash_value', '評分', '評論數', '地址','電話號碼',
    #           '平均消費', '營業時間','提供服務', '緯度', '經度', '圖片網址', 'google網址','選項']

    # restaurantDatas = Restaurant.objects.all()

    return render(request, 'admin_app/restaurant/sub_restaurant.html', locals())


def sub_type(request):
    title = '餐廳類型'
    fields = ['編號', '類型名稱']
    restaurantDatas = Category.objects.all()
    return render(request, 'admin_app/restaurant/sub_type.html', locals())

def sub_Restaurantcategory(request):
    title = '餐廳類型'
    fields = ['編號', '類型名稱']
    restaurantDatas = Restaurantcategory.objects.all()
    return render(request, 'admin_app/restaurant/sub_type.html', locals())


def restaurant_business_hours(request):
    title = '餐廳營業時間'
    fields = ['編號','餐廳名稱','營業時間(JSON)', '星期幾', '開始時間', '結束時間']
    restaurantDatas = Businesshours.objects.select_related('restaurant').all()
    return render(request, 'admin_app/restaurant/sub_business_hours.html', locals())