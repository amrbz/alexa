import os
from sanic import Blueprint
from sanic.views import HTTPMethodView
from sanic.response import json, text
import psycopg2
import configparser
from .threads import get_threads
from .cdms import get_cdms
import pywaves as pw
from .ipfs import create_ipfs_file, read_ipfs_file

import redis
# from redis.connection import ConnectionPool

config = configparser.ConfigParser()
config.read('config.ini')

alexa = Blueprint('alexa_v1', url_prefix='/alexa')


dsn = {
    "user": os.environ['POSTGRES_USER'],
    "password": os.environ['POSTGRES_PASSWORD'],
    "database": os.environ['POSTGRES_DB'],
    "host": config['DB']['host'],
    "port": config['DB']['port'],
    "sslmode": config['DB']['sslmode'],
    "target_session_attrs": config['DB']['target_session_attrs']
}


class Alexa(HTTPMethodView):
    @staticmethod
    def post(request):
        
        cdm = '''<?xml version="1.0"?>
        \r\n<cdm>
        \r\n<version>{cdmv}</version>
        \r\n<blockchain>Waves</blockchain>
        \r\n<network>Testnet</network>
        \r\n<opcodes>
        \r\n<opcode>
        \r\n<trafficlight>1234567</trafficlight>
        \r\n<value>GODMODE</value>
        \r\n</opcode>
        \r\n</opcodes>
        \r\n</cdm>
        '''.format(
            cdmv=os.environ['CDM_VERSION']
        )
        # pw.setChain('testnet')
        # pw.setNode(node=os.environ['NODE_URL'], chain='testnet')
        pw.setNode('https://testnode1.wavesnodes.com','testnet')
        sponsor = pw.Address(seed=os.environ['SPONSOR_SEED'])
        attachment = create_ipfs_file(cdm)
        asset = pw.Asset(os.environ['ASSET_ID'])
        feeAsset = pw.Asset(os.environ['ASSET_ID'])

        print('NODE_URL', os.environ['NODE_URL'])
        print('sponsor', sponsor)
        print('asset', asset)
        print('attachment', attachment['Hash'])

        tx = sponsor.sendAsset(
            recipient = sponsor,
            asset = asset,
            feeAsset = feeAsset,
            amount = 1,
            attachment = attachment['Hash'])

        print('TX: {}'.format(tx))
        return json({'tx': tx})


    @staticmethod
    def get(request):
        conn = psycopg2.connect(**dsn)
        try:
            with conn:
                with conn.cursor() as cur:
                    tr_id = '1234567'
                    sql = """
                        SELECT COUNT(*) FROM records
                        WHERE id='{tr_id}'
                    """.format(
                        tr_id=tr_id
                    )
                    cur.execute(sql)
                    count = cur.fetchone()[0]
        except Exception as error:
            pass
        res = 1 if count > 0 else 0
        return text(count)
        

alexa.add_route(Alexa.as_view(), '/')
