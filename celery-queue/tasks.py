import os
import time
from celery import Celery
import requests
import re
from pymongo import MongoClient

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

client = MongoClient("db:27017")
db = client.wordsdb

@celery.task(name='tasks.add')
def add(url: str) -> int:
    response = requests.get(url)
    words = re.findall(r"[\w']+", response.text)
    
    for w in words:
        insert = False
        doc = db.wordsdb.find_one({'word': w})
        if not doc:
            insert = True
            doc = {
                'word': w, 'count': 0, 'url': url
            }
        
        doc['count'] = doc['count'] + 1

        if insert is False:
            db.wordsdb.update({'_id': doc['_id']}, doc, upsert=True)
        else:
            db.wordsdb.insert_one(doc)

    return 0