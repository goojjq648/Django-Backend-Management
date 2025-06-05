from django.conf import settings
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from restaurant_app.models import Category
from Backend_Manager.elasticsearch_client import es

# es = Elasticsearch("http://localhost:9200")
model = SentenceTransformer('all-MiniLM-L6-v2')
index_name = 'category_semantic' # Elasticsearch index (category)

# 建立語意索引
def build_category_index():
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)

    # 建立語意索引跟mapping
    mapping = {
        "mappings": {
            "properties": {
                "name": {"type": "text"},
                "embedding": {
                    "type": "dense_vector", # 一個 dense vector（密集向量），長度為 384，這與 all-MiniLM-L6-v2 輸出的向量維度一致。
                    "dims": 384,
                    "index": True,
                    "similarity": "cosine" # 餘弦相似度，適合語意比較
                }
            }
        }
    }
    es.indices.create(index=index_name, body=mapping)

    for cat in Category.objects.all():
        embedding = model.encode(cat.name).tolist() # 將文本轉換為語意向量
        es.index(index=index_name, body={
            "name": cat.name,
            "embedding": embedding
        })
    

def update_new_categories():
    existing_ids = set()  # 可從 ES 查一次已有的分類名或 ID
    res = es.search(index=index_name, body={"query": {"match_all": {}}}, size=1000)
    for hit in res['hits']['hits']:
        existing_ids.add(hit['_source']['name'])  # 或用你定義的唯一 key

    # 處理新分類
    for cat in Category.objects.all():
        if cat.name not in existing_ids:
            embedding = model.encode(cat.name).tolist()
            es.index(index=index_name, body={
                "name": cat.name,
                "embedding": embedding
            })