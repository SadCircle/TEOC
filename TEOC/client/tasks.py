from django.urls import reverse
import datetime

import json

from TEOC.settings import MEDIA_ROOT

from catalog.tasks import load_documents_in_catalog
from TEOC.celery import app
from client.tg_client import *
from client.models import *
import logging


# данные для авторизации


@app.task
def auth_telegram(parser_id, code=None, password=None):
    '''Авторизация телеграмм аккаунта для парсера parser_id'''
    try:
        logger = logging.getLogger("auth_telegram")
        parser = Parser.objects.get(id=parser_id)
        session = TG_client(parser.session, parser.api_id, parser.api_hash)
        session.connect()
        if session.is_connected():
            if not session.is_user_authorized():
                session.sign_in(phone=str(parser.phone))
                if code:
                    try:
                        session.sign_in(code=int(code))
                    except SessionPasswordNeededError:
                        if password:
                            session.sign_in(password=str(password))
                            logger.info(f"Sign in with session {parser.session}")
                        else:
                            logger.error("Need password!")
                            return NEED_PASSWORD
                else:
                    logger.error("Need code request!")
                    return NEED_CODE_REQUEST
            parser.auth = True
            parser.save()
            return SUCCESS
        else:
            logger.error("Bad session file!")
            return BAD_SESSION_FILE
    finally:
        if session.is_user_authorized():
            del session


@app.task
def get_documents(parser_id,channels):
    '''Загрузка документов из телеграмм каналов channels с помощью парсеров parser_id'''
    try:
        logger = logging.getLogger("get_documents")
        parser = Parser.objects.get(id=parser_id)
        last_time = datetime.datetime.date(parser.time_update)
        session = TG_client(parser.session, parser.api_id, parser.api_hash)
        if parser.in_progress:
            logger.error("Parser is busy!")
            return IS_BUSSY
            
        session.connect()
        if session.is_connected():
            if not session.is_user_authorized():
                logger.error("Need authorization!")
                return NEED_AUTH
        else:
            logger.error("Bad session file!")
            return BAD_SESSION_FILE

        parser.in_progress = True
        parser.save()
        logger.info(f"Session {parser.session} created")

        session.get_media(  
            path=MEDIA_ROOT ,
            channels=channels,
            types='all',
            period=[last_time,datetime.datetime.date(datetime.datetime.now())]
                        )
        logger.info(f"Session {parser.session} disconnected")
        return SUCCESS
    finally:
        parser.in_progress = False
        parser.save()
        del session


@app.task
def get_auto():
    parsers = Parser.objects.filter(auth=True)
    channels = [channel.url for channel in Tg_Channels.objects.all()]
    for parser in parsers:
        get_documents(parser.id,channels)