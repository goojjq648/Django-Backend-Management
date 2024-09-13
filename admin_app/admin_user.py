from django.contrib.auth.models import User


class Admin_Users_Manager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Admin_Users_Manager, cls).__new__(
                cls, *args, **kwargs)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        self.__initialized = True

    def get_all_users(self):
        users = User.objects.all()
        return users
    
    def get_user_by_name(self, user_name):
        try:
            user = User.objects.get(username=user_name)
            return user
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            print("Multiple users found")
            return None
    
    def check_user_exist(self, user_name):        
        if User.objects.filter(username= user_name).exists():
            return True
        else:
            return False

    def create_user(self, user_name, email, password):        
        if self.check_user_exist(user_name):
            return False, '帳號已存在'

        user = User.objects.create_user(user_name, email, password)
        user.save()

        return True, '新增成功'
    
    def delete_user(self, user_name):
        if not self.check_user_exist(user_name):
            return False, '帳號不存在'

        user = self.get_user_by_name(user_name)
        if not user:
            return False, '刪除帳號失敗，有異常發生'
        else:
            user.delete()
            return True, '刪除成功'
        
