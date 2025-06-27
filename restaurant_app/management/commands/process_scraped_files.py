from django.core.management.base import BaseCommand
import logging
from restaurant_app.models import Restaurant, Category, Businesshours, Restaurantimage
from django.db import IntegrityError
from django.conf import settings
from datetime import datetime
from restaurant_app.file_paths import getRestaurantScraperDataFolder
import os
import re
import json


# 設定 logger
# logger = logging.getLogger(
#     'food_app.management.commands.process_scraped_files')

def setup_dynamic_logger():
    log_filename = f"my_command_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    handler = logging.FileHandler(log_filename, encoding='utf-8')
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger


logger = setup_dynamic_logger()

# 處理讀json檔案


class Command(BaseCommand):
    help = '處理餐廳爬蟲數據的指令'

    JSON_FILE_LIST = {
        'set1': ['restaurant_台北市中正區韓國料理_2024-09-20.json', 'restaurant_台北市中正區小吃_2024-09-20.json'],
        'set2': ['restaurant_台北市中正區韓國料理_2024-09-20.json']
    }

    
    def add_arguments(self, parser):
        # 新增參數 --today 來處理今天的爬蟲資料
        parser.add_argument(
            '--today',
            action='store_true',  # 如果指定此參數，值為 True，否則為 False
            help='處理今天的爬蟲資料'
        )
        # 新增參數 --filelist 來選擇特定檔案list
        parser.add_argument(
            '--filelist',
            type=str,
            help='選擇要處理的檔案集，例如：set1 或 set2'
        )
        # 新增參數 --update-existing 來決定是否允許更新已存在的資料
        parser.add_argument(
            '--update',
            action='store_true',  # 如果指定此參數，值為 True，否則為 False
            help='允許更新已存在的餐廳資料'
        )

    def get_today_files(self):
        folder_path = getRestaurantScraperDataFolder()
        today = datetime.today().strftime('%Y-%m-%d')
        pattern = re.compile(r'restaurant_.*_(\d{4}-\d{2}-\d{2})\.json')

        today_files = [filename for filename in os.listdir(
            folder_path) if pattern.match(filename) and today in filename]
        logger.debug(f"找到今天的檔案: {today_files}")
        return today_files

    def handle(self, *args, **options):
        # 取得今天的爬蟲檔案
        today = options.get('today')
        if today:
            filelist = self.get_today_files()
            if not filelist:
                logger.warning(f"今天沒有找到爬蟲資料")
                return
        else:
            # 如果沒有指定 --today 才取得 --filelist
            # 取得選擇的檔案list
            filelist_key = options.get('filelist')
            filelist = None

            if filelist_key:
                filelist = self.JSON_FILE_LIST.get(filelist_key)
                logger.debug(f'filelist: {filelist}')

        update_existing = options.get('update')  # 判斷是否修正資料
        logger.debug(f'update_existing: {update_existing}')

        self.loadJsonFile(filelist, update_existing)

    def loadJsonFile(self, filelist=None, update_existing=False):
        jsonFilePath = getRestaurantScraperDataFolder()

        # 有指定檔案list就用指定的檔案list
        if filelist:
            for filename in filelist:
                if filename.endswith('.json'):
                    logger.debug(f'讀取檔案: {filename}')
                    file_path = os.path.join(jsonFilePath, filename)
                    # 讀取 JSON 檔案
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)  # 拿到的是 dict
                        self.WriteDataToDatabase(data, update_existing)
        # 沒有指定檔案list就讀所有檔案
        else:
            for filename in os.listdir(jsonFilePath):
                if filename.endswith('.json'):
                    logger.debug(f'讀取檔案: {filename}')
                    file_path = os.path.join(jsonFilePath, filename)

                    # 讀取 JSON 檔案
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)  # 拿到的是 dict
                        self.WriteDataToDatabase(data, update_existing)
                        # print(data['restaurants'][0])
                        # print(data['restaurants'][0]['name'])
                        # print(len(data['restaurants']))

        logger.debug('讀取結束')

    def checkJsonData(self, data):
        json_data = None
        if data == "null" or data == "[]" or data == "" or data == None or data == {}:
            json_data = None
        elif isinstance(data, (dict, list)) and data:
            #    json_data = json.dumps(data, ensure_ascii=False)
            json_data = data

        return json_data

    # 儲存至資料庫
    def WriteDataToDatabase(self, data, update_existing=False):
        size = len(data['restaurants'])

        for i in range(size):
            res_data = data['restaurants'][i]
            logger.debug(f'處理第 {i+1}-{res_data['id']} 餐廳')

            # 檢查餐廳是否已重覆
            restaurantData = None
            hash_code = Restaurant.generateHashValue(
                res_data['name'], res_data['address'])
            if not hash_code:
                logger.error(
                    f'第{i+1}-{res_data["id"]}資料 無 hash_value，不加入資料庫，請做確認')
                continue
            else:
                restaurantData = Restaurant.objects.filter(
                    hash_value=hash_code)

            restaurantData = Restaurant.objects.filter(name=res_data['name'])

            json_data = self.checkJsonData(res_data["businessHours"])
            services_data = self.checkJsonData(res_data["services"])
            # logger.debug(f'services_data: {res_data["services"]}')
            # logger.debug(f'services_data: {services_data}')

            #
            if (restaurantData.exists()):
                if update_existing:
                    try:
                        logger.debug(
                            f'{i+1}-{res_data["id"]}-{res_data["name"]} 比對hash {hash_code} 已存在於資料庫中，開始更新資料')
                        restaurant_exist = restaurantData.first()
                        # 更新
                        # restaurant_exist.name = res_data['name']
                        restaurant_exist.rating = None if res_data['rating'] == 'null' else float(
                            res_data['rating'])
                        restaurant_exist.review_count = 0
                        # restaurant_exist.address = res_data['address']
                        restaurant_exist.phone_number = None if res_data[
                            'phone_number'] == 'null' else res_data['phone_number']
                        restaurant_exist.average_spending = None if res_data[
                            'avg_pay'] == 'null' else res_data['avg_pay']
                        restaurant_exist.opening_hours = json_data
                        restaurant_exist.services = services_data
                        restaurant_exist.latitude = float(res_data['latitude'])
                        restaurant_exist.longitude = float(
                            res_data['longitude'])
                        restaurant_exist.image_url = None if res_data[
                            'image_url'] == 'null' else res_data['image_url']
                        restaurant_exist.google_url = None if res_data[
                            'google_url'] == 'null' else res_data['google_url']

                        restaurant_exist.save()
                        logger.debug(f'更新餐廳 {res_data["name"]} 成功')

                        if res_data['type']:
                            restaurant_exist.addCategories(res_data['type'])

                    except Exception as e:
                        logger.error(f'更新餐廳 {res_data["name"]} 失敗' + str(e))
                else:
                    logger.error(
                        f'{i+1}-{res_data["id"]}-{res_data["name"]} 比對hash {hash_code} 已存在於資料庫中，不加入資料庫，請做確認')
                continue

            #
            if not res_data['name']:
                logger.error(f'第{i+1}資料 無名稱，不加入資料庫，請做確認')
                continue

            # 新增餐廳類型
            logger.debug(f'新增類型: {res_data['type']}')
            if not res_data['type']:
                continue
            else:
                categoryData = Category.objects.filter(name=res_data['type'])
                if (categoryData.exists()):
                    logger.debug(f'{res_data["type"]} 已存在於資料庫中，不加入此種類')
                else:
                    Category.objects.create(name=res_data['type'])

            # 新增餐廳資訊
            logger.debug(f'新增餐廳資訊: {res_data["name"]}')
            restaurant_instance = None

            try:
                restaurant_instance = Restaurant.objects.create(
                    name=res_data['name'],
                    rating=None if res_data['rating'] == 'null' else float(
                        res_data['rating']),
                    review_count=0,
                    address=res_data['address'],
                    phone_number=None if res_data['phone_number'] == 'null' else res_data['phone_number'],
                    average_spending=None if res_data['avg_pay'] == 'null' else res_data['avg_pay'],
                    opening_hours=json_data,
                    services=services_data,
                    latitude=float(res_data['latitude']),
                    longitude=float(res_data['longitude']),
                    image_url=None if res_data['image_url'] == 'null' else res_data['image_url'],
                    google_url=None if res_data['google_url'] == 'null' else res_data['google_url']
                )

                logger.debug(f'新增餐廳資訊 {res_data["name"]} 成功')

            except IntegrityError as e:
                logger.error(f'新增餐廳資訊 {res_data["name"]} 失敗，原因: {e}')
            except Exception as e:
                logger.error(
                    "=====================================================")
                logger.error("ERROR")
                logger.error("name:", res_data['name'])
                logger.error("rating:", res_data['rating'])
                logger.error("address:", res_data['address'])
                logger.error("phone_number:", res_data['phone_number'])
                logger.error("average_spending:", res_data['avg_pay'])
                logger.error("opening_hours:", res_data['businessHours'])
                logger.error("services:", res_data['services'])
                logger.error("latitude:", res_data['latitude'])
                logger.error("longitude:", res_data['longitude'])
                logger.error("image_url:", res_data['image_url'])
                logger.error("google_url:", res_data['google_url'])
                logger.error(f'新增餐廳資訊 {res_data["name"]} 失敗，原因: {e}')
                logger.error(
                    "=====================================================")

            try:
                if not restaurant_instance:
                    continue

                if not res_data['type']:
                    logger.debug(f'餐廳種類 {res_data["name"]} 目前無資料')
                    continue
                else:
                    restaurant_instance.addCategories(res_data['type'])
            except Exception as e:
                logger.error(f'新增餐廳種類 {res_data["name"]} 失敗，原因: {e}')
