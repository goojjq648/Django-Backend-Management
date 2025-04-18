from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from restaurant_app.models import Restaurant, Restaurantcategory, Businesshours, Category
from admin_app.admin_form import sub_restaurant_form as restaurant_form
import json


def edit_restaurant_data(request):
    response_data = {'action': 0, 'message': ''}

    if request.method != 'POST':
        return JsonResponse({'action': 0, 'message': '無效的請求方法'})

    id = request.POST.get('restaurant_id')
    print(f'id: {id}')
    action = request.POST.get('restaurant_action')

    if action != 'create' and action != 'edit':
        return JsonResponse({'action': 0, 'message': '無效的處理動作'})

    name = request.POST.get('name')
    print(f'name: {name}')

    if name == '':
        return JsonResponse({'action': 0, 'message': '餐廳名稱不能為空！'})

    rating = request.POST.get('rating')
    review_count = request.POST.get('review_count')
    address = request.POST.get('address')
    phone_number = request.POST.get('phone_number')
    average_spending = request.POST.get('average_spending')

    opening_hours = request.POST.get('opening_hours')
    if not opening_hours and opening_hours != '':
        try:
            opening_hours = json.loads(opening_hours)
        except:
            return JsonResponse({'action': 0, 'message': '營業時間是無效的JSON格式'})

    service = request.POST.get('services')
    if not service and service != '':
        try:
            services = json.loads(service)
        except:
            return JsonResponse({'action': 0, 'message': '服務資訊是無效的JSON格式'})

    latitude = request.POST.get('latitude')
    print(type(latitude))

    if latitude == '':
        return JsonResponse({'action': 0, 'message': '緯度不能為空！'})

    if float(latitude) > 90 or float(latitude) < -90:
        return JsonResponse({'action': 0, 'message': '緯度必須在-90到90之間！'})

    longitude = request.POST.get('longitude')

    if longitude == '':
        return JsonResponse({'action': 0, 'message': '經度不能為空！'})

    image_url = request.POST.get('image_url')
    google_url = request.POST.get('google_url')

    real_hash_value = Restaurant.generateHashValue(name, address)

    if action == 'create':
        if Restaurant.objects.filter(hash_value=real_hash_value).exists():
            return HttpResponse('餐廳名稱重複！請確認')

        try:
            # print('create restaurant')
            Restaurant.objects.create(
                name=name,
                hash_value=real_hash_value,
                rating=rating,
                review_count=review_count,
                address=address,
                phone_number=phone_number,
                average_spending=average_spending,
                opening_hours=opening_hours,
                services=service,
                latitude=latitude,
                longitude=longitude,
                image_url=image_url,
                google_url=google_url
            )
        except Exception as e:
            print(e)
            return JsonResponse({'action': 0, 'message': '新增失敗'})
    elif action == 'edit':
        try:
            # print('edit restaurant')
            Restaurant.objects.filter(id=id).update(
                name=name,
                hash_value=real_hash_value,
                rating=rating,
                review_count=review_count,
                address=address,
                phone_number=phone_number,
                average_spending=average_spending,
                opening_hours=opening_hours,
                services=service,
                latitude=latitude,
                longitude=longitude,
                image_url=image_url,
                google_url=google_url
            )
        except Exception as e:
            print(e)
            return JsonResponse({'action': 0, 'message': '修改失敗'})

    return JsonResponse({'action': 1, 'message': 'OK'})


def check_restaurantdata(request):
    response_data = {'action': 0, 'message': ''}

    if request.method != 'GET':
        return JsonResponse({'action': 0, 'message': '無效的請求方法'})

    action = request.GET.get('act')
    print(f'action: {action}')

    # 檢查餐廳名稱
    name = request.GET.get('restaurant_name')
    if name is not None:
        if name == '':
            return JsonResponse({'action': 0, 'message': '餐廳名稱不能為空！'})

        if action == 'create' and Restaurant.objects.filter(name=name).exists():
            return JsonResponse({'action': 0, 'message': '餐廳名稱重複！請確認'})

    # 檢查評分
    rating = request.GET.get('restaurant_rating')
    if rating is not None:
        if rating != '':
            if float(rating) > 5 or float(rating) < 0:
                return JsonResponse({'action': 0, 'message': '評分必須在0到5之間！'})

    # 檢查營業時間
    business_hours = request.GET.get('restaurant_business_hours')
    if business_hours is not None:
        try:
            business_hours = json.loads(business_hours)
        except:
            return JsonResponse({'action': 0, 'message': '營業時間是無效的JSON格式'})

    service = request.GET.get('services')
    if service is not None:
        try:
            services = json.loads(service)
        except:
            return JsonResponse({'action': 0, 'message': '服務資訊是無效的JSON格式'})

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

def del_restaurant(request):
    if request.method != 'POST':
        return JsonResponse({'action': 0, 'message': '無效的請求方法'})
    
    data = json.loads(request.body)

    restaurant_id = data.get('restaurant_id')

    if not restaurant_id:
        return JsonResponse({'action': 0, 'message': '餐廳編號為空，請確認'})

    Restaurant.objects.filter(id=restaurant_id).delete()

    return JsonResponse({'action': 1, 'message': '刪除成功'})


def restaurant(request):
    sub_title = '餐廳資料'
    field_names = [field.verbose_name for field in Restaurant._meta.fields]
    restaurant_data_list = [restaurant.as_dict()
                            for restaurant in Restaurant.objects.all()]

    # 新增欄位用
    field_names.append('選項')

    form = restaurant_form.RestaurantForm()
    render_form = form.render_all_fields()

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
    fields = ['編號', '餐廳名稱', '營業時間(JSON)', '星期幾', '開始時間', '結束時間']
    restaurantDatas = Businesshours.objects.select_related('restaurant').all()
    return render(request, 'admin_app/restaurant/sub_business_hours.html', locals())
