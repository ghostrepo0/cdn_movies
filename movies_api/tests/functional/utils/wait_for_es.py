import time

from elasticsearch import Elasticsearch
from functional.settings import settings

es = Elasticsearch(settings.es_host)

while not es.ping():
    print('could not connect to elastic')
    time.sleep(1)
