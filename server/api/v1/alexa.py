import os
from sanic import Blueprint
from sanic.views import HTTPMethodView
from sanic.response import json, text
import psycopg2
import configparser
from .threads import get_threads
from .cdms import get_cdms

import redis
# from redis.connection import ConnectionPool

config = configparser.ConfigParser()
config.read('config.ini')

alexa = Blueprint('alexa_v1', url_prefix='/alexa')


class Alexa(HTTPMethodView):
    @staticmethod
    def post(request):
        res = '1'
        return text(res)
        

alexa.add_route(Alexa.as_view(), '/')
