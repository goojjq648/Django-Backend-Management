from django.contrib.sites.models import Site
from restaurant_app.models import Category
from Backend_Manager.elasticsearch_client import es
from sentence_transformers import SentenceTransformer
from django.core.management import call_command

from . import es_category_index
from . import enrich_coord

import os


def setup_site():
    Site.objects.update_or_create(
        id=1,
        defaults={"domain": "127.0.0.1:8000", "name": "Localhost Site"}
    )
    print("Site 資料已建立/更新")

# 重建 DSL 索引


def rebuild_dsl_indexes():
    try:
        call_command("search_index", "--rebuild", "--parallel", "--noinput")
        print("DSL 索引已重建 (restaurants, streets 等)")
    except Exception as e:
        print(f"重建 DSL 索引失敗: {e}")

# 建立 Elasticsearch Category 資料


def setup_category():
    es_category_index.build_category_index()
    print("Elasticsearch Category 資料已建立")


def setup_enrich_coord():
    enrich_coord.enrich_coord()
    print("街道資料已匯入")


def import_streets():
    try:
        call_command("import_streets")  # 你自定義的 command
        print("街道資料已匯入")
    except Exception as e:
        print(f"匯入街道資料失敗: {e}")


def process_scraped_data():
    try:
        call_command("process_scraped_files", "--filelist", "set1")
        print("爬蟲資料已處理完畢")
    except Exception as e:
        print(f"處理爬蟲資料失敗: {e}")


def run():
    setup_site()            # 建立 Site 資料
    # setup_enrich_coord()  # 建立街道經緯度資料 (會跑很久，不需要測試快取的話可以關掉)
    import_streets()        # 匯入街道資料
    process_scraped_data()  # 處理爬蟲資料
    rebuild_dsl_indexes()   # 建立 Elasticsearch 對應document資料來建立索引
    setup_category()        # 建立 Elasticsearch Category 資料


if __name__ == "__main__":
    run()
