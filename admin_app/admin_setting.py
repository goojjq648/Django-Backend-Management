from django.contrib.staticfiles import finders
import json

ADMIN_SETTING_PATH = finders.find('data/admin_Setting.json')

def read_json_file(path):
    if not path:
        return {}
    else :
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f) # 拿到的是 dict

class AdminSetting:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AdminSetting, cls).__new__(cls, *args, **kwargs)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        self.admin_setting_path = finders.find('data/admin_Setting.json')
        self.__admin_func_type_list = read_json_file(self.admin_setting_path )
        self.__initialized = True

    def reloadAdminFuncTypeList(self):
        self.__admin_func_type_list = read_json_file(self.admin_setting_path)
        
    def setAdminFuncTypeList(self, admin_func_type_list):
        pass
        
    def get_admin_func_type_list(self):
        return self.__admin_func_type_list