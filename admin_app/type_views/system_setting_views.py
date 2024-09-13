from admin_app.admin_setting import AdminSetting
from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render
import json

def fetch_admin_setting_data(request):
    data = get_admin_setting().get_admin_func_type_list()

    return JsonResponse(data)

def get_admin_setting():
    return AdminSetting()

def retrieve_admin_setting_data():
    return get_admin_setting().get_admin_func_type_list()

def sub_setting(request, admin_list, mainType):
    return render(request, 'admin_app/SystemSetting/sub_setting.html', {'admin_list': admin_list, 'mainType': mainType})

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
        return HttpResponse('新增成功，請重新整理頁面')
    else:
        return HttpResponse('修改成功，請重新整理頁面')
    

def confirm_delete_mainType(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8') 
        body_data = json.loads(body_unicode)
        
        mainType = body_data.get('mainType')

        get_admin_setting().delete_admin_func_type_list(mainType)

    return HttpResponse('刪除成功，請重新整理頁面')

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

    return JsonResponse(admin_list[mainType])