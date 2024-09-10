from django.contrib.auth.models import User

class Admin_Users_Manager:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Admin_Users_Manager, cls).__new__(cls, *args, **kwargs)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        self.__initialized = True

    def get_all_users(self):
        users = User.objects.all()
        return users

    def create_user(self, request):
        if request.method != 'POST':
            return 
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not email or not password:
            return
        
        user = User.objects.create_user(username, email, password)
        user.save()