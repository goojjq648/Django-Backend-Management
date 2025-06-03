from elasticsearch import Elasticsearch
from django.conf import settings

es = Elasticsearch(
    settings.ELASTICSEARCH_DSL['default']['hosts'],
    basic_auth=settings.ELASTICSEARCH_DSL['default']['http_auth'],
    ssl_context=settings.ELASTICSEARCH_DSL['default']['ssl_context'],
    verify_certs=settings.ELASTICSEARCH_DSL['default']['verify_certs'],
)
