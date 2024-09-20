from django.contrib.staticfiles import finders
import json
import os

ADMIN_SETTING_PATH = finders.find('data/admin_Setting.json')


def read_json_file(path):
    if not path:
        return {}
    else:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)  # 拿到的是 dict


def write_json_file(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# def generate_files(main_category, sub_categories):
#     base_template_dir = os.path.join(
#         'Backend_Manager', 'admin_app', 'templates', 'admin_app', main_category)
#     base_static_dir = os.path.join(
#         'Backend_Manager', 'admin_app', 'static', 'scripts', main_category)

#     # 創建對應資料夾
#     os.makedirs(base_template_dir, exist_ok=True)
#     os.makedirs(base_static_dir, exist_ok=True)

#     # 針對每個子類別生成 HTML 和 JS
#     for sub_category in sub_categories:
#         html_content = f"<h1>{sub_category} Page</h1>"
#         js_content = f"console.log('This is the {sub_category} script');"

#         # 生成 .html 檔案
#         with open(os.path.join(base_template_dir, f'{sub_category}.html'), 'w', encoding='utf-8') as html_file:
#             html_file.write(html_content)

#         # 生成 .js 檔案
#         with open(os.path.join(base_static_dir, f'{sub_category}.js'), 'w', encoding='utf-8') as js_file:
#             js_file.write(js_content)


class AdminSetting:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AdminSetting, cls).__new__(
                cls, *args, **kwargs)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        self.admin_setting_path = finders.find('data/admin_Setting.json')
        self.__admin_func_type_list = read_json_file(self.admin_setting_path)
        self.__initialized = True

    def reloadAdminFuncTypeList(self):
        self.__admin_func_type_list = read_json_file(self.admin_setting_path)

    def get_admin_func_type_list(self):
        return self.__admin_func_type_list

    def check_admin_func_type_list(self, main_type):
        return main_type in self.__admin_func_type_list

    # "SystemSetting": {
    #   "button_icon": "#grid",
    #   "sub_detail": {
    #     "sub_setting": "設定類別"
    #   }
    # }
    def edit_admin_func_type_list(self, orgin_main_type, main_type, button_icon, sub_datail_list):
        admin_list = self.__admin_func_type_list
        # 如果有改名稱，要檢查是否有重複的主類別
        if orgin_main_type != main_type:
            if self.check_admin_func_type_list(main_type):
                print('主類別名稱已經被使用，請重新輸入')
                return False
        
        print(f'edit_admin_func_type_list: {orgin_main_type} -> {main_type}')
        print(f'edit_admin_func_type_list: {admin_list}')
        # 如果沒有改名稱，要刪掉原本的主類別才能新增新的主類別
        if orgin_main_type in admin_list:
            del admin_list[orgin_main_type]
            admin_list[main_type] = {
                "button_icon": button_icon,
            }

            if sub_datail_list:
                admin_list[main_type]["sub_detail"] = sub_datail_list

            write_json_file(self.admin_setting_path, admin_list)
            return True

        return False
    
    def add_admin_func_type_list(self, main_type, button_icon, sub_datail_list):
        admin_list = self.__admin_func_type_list
        if main_type in admin_list:
            print('主類別名稱已經被使用，請重新輸入')
            return False

        admin_list[main_type] = {
            "button_icon": button_icon,
        }

        if sub_datail_list:
            admin_list[main_type]["sub_detail"] = sub_datail_list

        write_json_file(self.admin_setting_path, admin_list)
        return True

    def delete_admin_func_type_list(self, main_type):
        admin_list = self.__admin_func_type_list
        if main_type in admin_list:
            del admin_list[main_type]

        write_json_file(self.admin_setting_path, admin_list)
