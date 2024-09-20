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
    sub_title = '設定類別'
    return render(request, 'admin_app/SystemSetting/sub_setting.html', {'sub_title': sub_title, 'admin_list': admin_list, 'mainType': mainType})


def confirm_editSetting(request):
    select_action = request.POST.get('admin_setting_action')
    main_type = request.POST.get('name')
    orgin_main_type = request.POST.get('OrgInputMainTypeName')

    # 如果主類別有變更，要檢查是否有重複的主類別
    if orgin_main_type != main_type:
        if get_admin_setting().check_admin_func_type_list(main_type):
            return HttpResponse('主類別名稱已經被使用，請重新輸入')

    if not main_type:
        return HttpResponse('沒有填寫主類別名稱')

    button_icon = request.POST.get('selected_main_Icon')
    if not button_icon:
        return HttpResponse('沒有設定主類別圖標')

    sub_idx = request.POST.get('subcategory_Idx')
    # print(sub_idx)
    sublist = {}

    for i in range(int(sub_idx)):
        # 子類別ID
        sub_id = request.POST.get('subcategories[' + str(i) + '][id]')
        # 子類別名稱
        sub_name = request.POST.get('subcategories[' + str(i) + '][name]')
        # print(sub_id, sub_name)

        if not sub_id:
            return HttpResponse('沒有填寫子類別ID')
        if not sub_name:
            return HttpResponse('沒有填寫子類別名稱')

        sublist[sub_id] = sub_name


    # 處理設定檔
    if  select_action == 'addMainType':
        if get_admin_setting().add_admin_func_type_list(main_type, button_icon, sublist) is False:
            return HttpResponse('新增資料失敗，請重新確認資料是否有誤')
    else:
        if get_admin_setting().edit_admin_func_type_list(orgin_main_type, main_type, button_icon, sublist) is False:
            return HttpResponse('更新資料失敗，請重新確認資料是否有誤')

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
