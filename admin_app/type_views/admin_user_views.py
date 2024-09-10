from admin_app.admin_user import Admin_Users_Manager
from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render

def get_admin_users_manager():
    return Admin_Users_Manager()

def sub_admin_member(request):
    user_manager = get_admin_users_manager()
    users = user_manager.get_all_users()
    return render(request, 'admin_app/SystemSetting/sub_admin_member.html', locals())