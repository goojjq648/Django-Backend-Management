from django.contrib.staticfiles import finders
import json

ADMIN_SETTING_PATH = finders.find('data/admin_Setting.json')

def read_json_file(path):
    if not path:
        return {}
    else :
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f) # 拿到的是 dict

def write_json_file(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
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
        
    def get_admin_func_type_list(self):
        return self.__admin_func_type_list

    # "SystemSetting": {
    #   "button_icon": "#grid",
    #   "sub_detail": {
    #     "sub_setting": "設定類別"
    #   }
    # }
    def edit_admin_func_type_list(self, main_type, button_icon, sub_datail_list):
        admin_list = self.__admin_func_type_list
        admin_list[main_type] = {
                "button_icon": button_icon,
                "sub_detail": sub_datail_list
        }

        write_json_file(self.admin_setting_path, admin_list)

    def delete_admin_func_type_list(self, main_type):
        admin_list = self.__admin_func_type_list
        if main_type in admin_list:
            del admin_list[main_type]

        write_json_file(self.admin_setting_path, admin_list)