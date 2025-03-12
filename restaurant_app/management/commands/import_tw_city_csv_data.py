import csv
import os
import re
import unicodedata
import emoji
from django.core.management.base import BaseCommand
from restaurant_app.models import Streets
from restaurant_app.file_paths import getCSVDataFolder

class Command(BaseCommand):
    help = 'Import street names from CSV and log failed records'

    def clean_data(self, value):
        if value:
            # Unicode 正規化（解決異體字、擴展字符）
            value = unicodedata.normalize('NFC', value)
            # 刪除隱藏字符 (BOM, 零寬字符, 換行, tab)
            value = re.sub(r'[\ufeff\u200b\r\n\t]', '', value.strip())
            # 移除全形空格
            value = re.sub(r'\u3000', ' ', value)
            # 移除 emoji（可以選擇保留或刪除）
            value = emoji.replace_emoji(value, replace='') 
        return value

    def handle(self, *args, **kwargs):
        folder_path = getCSVDataFolder()

        # 確認資料夾存在
        if os.path.isdir(folder_path):
            # 列出所有檔案
            files = os.listdir(folder_path)

            # 選擇 CSV 檔案
            csv_files = [file for file in files if file.endswith('.csv')]
            if not csv_files:
                self.stdout.write(self.style.ERROR('No CSV files found in the folder.'))
                return

            # 建立錯誤記錄檔案
            error_log_path = os.path.join(folder_path, 'error_log.csv')
            with open(error_log_path, mode='w', newline='', encoding='utf-8-sig') as error_file:
                error_writer = csv.writer(error_file)
                # 設定標頭
                error_writer.writerow(['city', 'district', 'road', 'error'])

                total_count = 0
                failed_count = 0

                for file in csv_files:
                    file_path = os.path.join(folder_path, file)
                    self.stdout.write(self.style.NOTICE(f"Importing file: {file}"))
                    
                    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
                        reader = csv.DictReader(csvfile)
                        count = 0

                        for row in reader:
                            try:
                                # 資料清理 + 正規化處理
                                city = self.clean_data(row['city'])
                                district = self.clean_data(row['site_id'])
                                road = self.clean_data(row['road'])

                                # 匯入策略：使用 get_or_create 避免重複
                                obj, created = Streets.objects.get_or_create(
                                    city=city,
                                    district=district,
                                    road=road
                                )
                                if created:
                                    count += 1
                                    total_count += 1
                                else:
                                    # 如果已存在，但有些資料不完整 → 更新內容
                                    obj.city = city
                                    obj.district = district
                                    obj.road = road
                                    obj.save()

                            except Exception as e:
                                # 紀錄錯誤到錯誤記錄檔
                                error_writer.writerow([row.get('city'), row.get('site_id'), row.get('road'), str(e)])
                                failed_count += 1
                                # 顯示錯誤訊息
                                self.stdout.write(self.style.ERROR(f"⚠️ Error importing street: {row}"))
                                self.stdout.write(self.style.ERROR(f"⚠️ Error message: {e}"))

                        self.stdout.write(self.style.SUCCESS(f"✔️ Imported {count} streets from {file}."))

            self.stdout.write(self.style.SUCCESS(f"✅ Total imported streets: {total_count}"))
            if failed_count > 0:
                self.stdout.write(self.style.WARNING(f"❌ {failed_count} records failed to import."))
                self.stdout.write(self.style.WARNING(f"📁 Error log saved to: {error_log_path}"))
            else:
                self.stdout.write(self.style.SUCCESS("🎉 No errors during import!"))

        else:
            self.stdout.write(self.style.ERROR(f"❌ Folder not found: {folder_path}"))
