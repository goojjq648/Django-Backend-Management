from admin_app.admin_user import Admin_Users_Manager
from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render


def get_admin_users_manager():
    return Admin_Users_Manager()


def sub_admin_member(request):
    title = '使用者資料'
    fields = ['編號', '帳號', '電子郵件', '是否為後台員工', '是否為超級管理員', '帳號是否啟動']
    user_manager = get_admin_users_manager()
    users = user_manager.get_all_users()
    return render(request, 'admin_app/SystemSetting/sub_admin_member.html', locals())


def create_admin_member(request):
    response = {'status': 0, 'message': ''}
    status = 0
    message = ''
    
    if request.method != 'POST':
        status, message = False, '無效的請求方法'

        username = request.POST.get('admin_member_name')
        email = request.POST.get('admin_member_email')
        password = request.POST.get('admin_member_password')
        password_confirm = request.POST.get('admin_member_password_confirm')

        if password != password_confirm:
            status, message = False, '密碼不一致，請重新輸入'
        
        if not username or not email or not password or not password_confirm:
            status, message = False, '欄位不得為空'

        if status == True:
            user_manager = get_admin_users_manager()
            response['status'], response['message'] = user_manager.create_user(username, email, password)

    return JsonResponse(response)

def delete_admin_member(request):
    response = {'status': 0, 'message': ''}
    if request.method == 'POST':
        username = request.POST.get('admin_member_name')
        user_manager = get_admin_users_manager()
        response['status'], response['message'] = user_manager.delete_user(username)
