from http import client
from pickle import OBJ
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from datetime import date
import argparse
import configparser
import json
import re
import sys, os
import logging
#from django.contrib.postgres.search import SearchVector
#from catalog.models import Document
#from BookReaders.read_book import *


##CONSTANTS
NEED_CODE_REQUEST = -1
NEED_PASSWORD = -2
BAD_SESSION_FILE = -3
NEED_AUTH = -4
IS_BUSSY = -5
SUCCESS = 0



# получаем параметры для запуска клиента
def parse_config(path):
    config = configparser.ConfigParser()
    config.read(path)
    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']
    try:
        phone = config['Telegram']['phone']
    except KeyError:
        phone = None
    session_name = config['Telegram']['session']
    return session_name, api_id, api_hash, phone


class TG_client(TelegramClient):
    def __init__(self, session_name, api_id, api_hash):
        super().__init__(session_name, api_id, api_hash)
        self.session_name = session_name

    def __del__(self):
        self._disconnect_session()
        

    def _connect_sesion(self):
        if not self.is_connected():
            self.connect()

    def _disconnect_session(self):
        if self.is_connected():
            self.disconnect()

    def auth(self,phone,code=None,password=None):
        self._connect_sesion()
        self.sign_in(phone=int(phone))
        if code:
            self.sign_in(code=int(code),password=password)
        if self.is_user_authorized():
            return True
        return False
    


    @staticmethod
    def save_message(message, types, message_json):
        try:
            if message.file and message.file.name and message.file.ext in types:
                message_json[message.file.id] = message
        except:
            return 0
        return 1

    @staticmethod
    def get_message_meta_data(message):
        data={}
        data['hash_key']=message.file.id
        data['name']=message.file.name
        data['size']=message.file.size
        data['ext']=message.file.ext
        data['description']=message.message
        print(data)
        return data

    def get_media(self, path, channels, types, period):
        logger = logging.getLogger("get_documents.get_media")
        channels_entities = ['https://t.me/'+x.replace('https://t.me/','') for x in channels]
        channels_count = 0
        message_json = dict()
        if types == 'all':
            types = ['.pdf', '.epub', '.fb2', '.djvu', '.txt']
        for channel in channels_entities:
            
                msg_count = 0
                for message in self.iter_messages(channel):
                    if period != "all":
                        # за один конкретный день
                        if period[0] == period[1]: 
                            if message.date.strftime("%Y-%m-%d") == period[0].strftime("%Y-%m-%d"):
                                if self.save_message(message, types, message_json) != 0:
                                    msg_count += 1
                        # диапазон
                        elif message.date.strftime("%Y-%m-%d") <= period[1].strftime("%Y-%m-%d") and message.date.strftime("%Y-%m-%d") >= period[0].strftime("%Y-%m-%d"):
                            if self.save_message(message, types, message_json) != 0:
                                msg_count += 1
                    else:
                        if self.save_message(message, types, message_json) != 0:
                            msg_count += 1
                #нужные сообщения сохранены в json-словаре, забираем ключи и выбираем только те, hash_key которых нет в базе
                #из базы забираем только hash_keys, которые есть в message_json
                tg_hash_keys = [tg_hash_key[0] for tg_hash_key in Document.objects.filter(tg_hash_key__in=message_json.keys()).values_list('tg_hash_key')] #1 обращение к базе
                keys_to_insert = list(set(message_json.keys()) - set(tg_hash_keys))
                objects_ = []
                for key in keys_to_insert:
                    path_to_object = message_json[key].download_media(file=path + '/documents/').replace(path,'')
                    ext_=message_json[key].file.ext
                    local_hash_key_, book_text_, image_, title_, _, author_ = take_additional_features(path+str(path_to_object), ext_)
                    objects_.append(
                        Document(
                            tg_hash_key=message_json[key].file.id,
                            local_hash_key=local_hash_key_,
                            name=message_json[key].file.name,
                            ext=ext_,
                            size=message_json[key].file.size,
                            path=path_to_object,
                            description=message_json[key].message,
                            book_text=book_text_,
                            image=image_,
                            title=title_,
                            author=author_
                        )
                    )
                if objects_:
                    Document.objects.bulk_create(objects_) #1 обращение к базе
                    Document.objects.update(search_vector=SearchVector("book_text"))
                channels_count += 1
                if msg_count == 0:
                    print("Книг за указанный период в канале {0} не обнаружено".format(channels[channels_count-1]))
                else:
                    print("Все книги, найденные за указанный период в канале {0}, загружены".format(channels[channels_count-1]))
            



if __name__ == "__main__":
    pass