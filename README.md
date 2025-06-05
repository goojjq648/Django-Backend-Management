# Django-Backend-Management
Django + Bootstrap 5 Backend Management

# 餐廳探索網站後端

這是餐廳探索平台的後端專案，提供前端使用者進行地點搜尋、餐廳分類推薦、地圖定位與資料查詢的 RESTful API。  
後端以 **Django + MySQL + Elasticsearch** 為基礎架構，並整合 Google 登入與語意向量搜尋。

# 專案前後端架構說明

本專案為前後端分離架構，後端為 Django + MySQL API，前端為 Vue 3 實作的 SPA。

👉 前端 GitHub 專案位置：[restaurant-frontend](https://github.com/goojjq648/Restaurant-frontend)

# 功能
1. 會員註冊、第三方登入(Google)
2. 搜尋不同地區的餐廳資料
3. 會員評論

# 使用技術
- Python 3.x
- Django 5.0.6
- Django REST Framework
- MySQL
- Elasticsearch 8.17.2（語意搜尋分類、地區建議）
- SentenceTransformers（產生 embedding 向量）
  
# 套件安裝

### 建立虛擬環境

```bash
python -m venv venv
source venv/bin/activate  # Windows 用 venv\Scripts\activate

# 安裝依賴套件
pip install -r requirements.txt
```

# 設定檔設定
### authSetting.env：
此為 Elasticsearch、Google 登入金鑰設定、Django Secret Key的設定檔案。

```
ELASTICSEARCH_HOST=
ELASTICSEARCH_USER=
ELASTICSEARCH_PASSWORD=

GOOGLE_CLIENT_ID=
SECRET_KEY=
```

### databaseSetting.env：
資料庫設定 :

```env
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

# 資料庫設計（簡要）
1. 建立 MySQL 資料庫（名稱建議為 restaurant)
2. 匯入初始資料（可參考init_schema.sql，並匯入)

主要資料表：
- `Restaurant`：餐廳基本資訊
- `Category`：餐廳分類（支援多對多）
- `RestaurantCategory`：關聯表
- `BusinessHours`：營業時間
- `RestaurantImage`：圖片儲存
- `Street`：街道資料庫（for Elasticsearch 補字）

匯入資料庫
請先建立 MySQL 資料庫，並修改 settings.py 中的資料庫連線設定。

## 資料來源：餐廳爬蟲與資料導入

本專案餐廳資料非人工建立，而是透過自動化爬蟲工具蒐集自 Google Map（或其他平台）。  
👉 爬蟲工具可以參考這個repo: [google_map_restaurant_scraping](https://github.com/goojjq648/google_map_restaurant_scraping)
- 爬蟲資料儲存為 JSON 格式  
- 使用自定義 Python 工具將 JSON 轉換並寫入資料庫（MySQL） 

### 主要檔案說明：

- 爬蟲輸出資料：[restaurant_data](https://github.com/goojjq648/Django-Backend-Management/tree/main/restaurant_app/static/restaurant_data)   
- 導入工具程式：[process_scraped_files.py](https://github.com/goojjq648/Django-Backend-Management/blob/main/restaurant_app/management/commands/process_scraped_files.py)  
支援多種處理模式與參數，可控制要處理的日期、檔案集與是否更新資料。  

### 工具設定說明
工具內可定義多組檔案清單，例如：  

```python
# process_scraped_files.py 中的設定片段  
JSON_FILE_LIST = {
    'set1': ['restaurant_台北市中正區韓國料理_2024-09-20.json', 'restaurant_台北市中正區小吃_2024-09-20.json'],
    'set2': ['restaurant_台北市中正區韓國料理_2024-09-20.json']
}
```

#### 匯入所有預設檔案集
```bash
python manage.py process_scraped_files
```

#### 匯入特定檔案集（set2）
```bash
python manage.py process_scraped_files --filelist set2
```

#### 匯入今天的檔案（檔名含今日日期）
```bash
python manage.py process_scraped_files --today
```

#### 匯入今天的檔案，並允許更新資料庫中已存在的餐廳資料
```bash
python manage.py process_scraped_files --today --update
```

#### 匯入特定檔案集，並允許更新已存在資料
```bash
python manage.py process_scraped_files --filelist set2 --update
```

## Street 資料表資料來源與匯入
為了提供地點模糊搜尋（autocomplete），本專案建立了 `Street` 資料表，包含台灣所有縣市 / 區 / 路段的資料。

### 資料來源
- CSV 檔案路徑：`restaurant_app/static/csv/opendata-road.csv`
- 資料來源：台灣政府開放資料（OpenData）

### 匯入工具
使用 Django 的自定義管理指令 `import_tw_city_csv_data.py` 將 CSV 匯入 MySQL：

```bash
python manage.py import_tw_city_csv_data
```

# Elasticsearch 設定
請確認本機已啟動 Elasticsearch（port: 9200）

### 索引建置方式
以下為目前已建立於本機的 Elasticsearch 索引：  
`restaurants`:餐廳基本資料查詢索引  

`streets`:補字搜尋用地點資料（市/區/街道)  

`category_semantic`: 餐廳分類語意搜尋（語意相似推薦）  

1. `restaurants` 與 `streets`：  
先創建索引  
```bash
python manage.py search_index --create
```
如需重新建立這些索引，請依下方方式操作:  
```bash
python manage.py search_index --rebuild
```

2. category_semantic：  
`\restaurant_app\script\es_category_index.py`  
可以使用  
```bash
python manage.py shell
```
```
from restaurant_app.utils.es_category_index import build_category_index
build_category_index()
```

# 運行專案
```bash
python manage.py runserver
```

### 測試
在瀏覽器網址列輸入以下即可看到畫面
```
http://127.0.0.1:8000/
```

