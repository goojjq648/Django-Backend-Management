from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
from apscheduler.triggers.cron import CronTrigger

from . import file_paths as path_def
from datetime import datetime, timedelta
import os
import re


# def CheckAndCrawlRestaurantScraperData(filelist_key=None):
#     print('CheckAndCrawlRestaurantScraperData')
#     folder_path = path_def.getRestaurantScraperDataFolder()
#     today = datetime.today().strftime('%Y-%m-%d')

#     pattern = re.compile(r'restaurant_.*_(\d{4}-\d{2}-\d{2})\.json')

#     for filename in os.listdir(folder_path):
#         match = pattern.match(filename)
#         if match and match.group(1) == today:
#             print(f"find today's restaurant scraper data: {filename}")
#             # 如果有指定 filelist_key，則從 JSON_FILE_LIST 取得檔案清單
#             if filelist_key:
#                 call_command('process_scraped_files', filelist=filelist_key, update=True)
#             else:
#                 # 預設執行 Django 指令
#                 call_command('process_scraped_files')
#             break
#     else:
#         print(f"沒有找到今天的爬蟲資料")


def start():
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(CheckAndCrawlRestaurantScraperData, 'interval', days=1)  # 每天執行一次
    # scheduler.start()
    scheduler = BackgroundScheduler()

    # 立即執行一次任務，然後每隔一天執行一次
    scheduler.add_job(
        lambda: call_command('process_scraped_files', '--today', '--update'),
        CronTrigger(hour=3, minute=0),  # 每天凌晨 3 點執行
        id='daily_scraping'
    )

    scheduler.start()
