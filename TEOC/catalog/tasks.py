import logging
import os
import json
from datetime import datetime

from django.urls import reverse

from TEOC.celery import app
from TEOC.settings import MEDIA_ROOT
from catalog.models import Document

@app.task
def load_documents_in_catalog():
    for filename in os.listdir(MEDIA_ROOT+'/jsons/'):
        doc = json.load(open(MEDIA_ROOT+'/jsons/'+filename,'r'))
        #1 взять из базы все доки  select hash_key from tbl where hash_key in doc.keys()
        hash_keys = [hash_key[0] for hash_key in Document.objects.filter(hash_key__in=doc.keys()).values_list('hash_key')]
        keys_to_insert = list(set(doc.keys()) - set(hash_keys))
        objects_ = [
            Document(
                hash_key=doc[key]['hash_key'],
                name=doc[key]['name'],
                ext=doc[key]['ext'],
                size=doc[key]['size'],
                path=doc[key]['path'],
                description=doc[key]['description']) for key in keys_to_insert
            ]
        if objects_:
            Document.objects.bulk_create(objects_)




        # doc_cat,created = Document.objects.get_or_create(hash_key=doc['hash_key'],
        #                                             name=doc['name'],
        #                                             ext=doc['ext'],
        #                                             size=doc['size'])
        # if  created:
        #     doc_cat.path = doc['path']
        #     doc_cat.description =  doc['description']
        #     doc_cat.save()
