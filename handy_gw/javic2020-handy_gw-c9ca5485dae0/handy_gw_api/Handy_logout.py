# -*- coding: utf-8 -*-

from flask import Flask
import requests, xmltodict, json
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from flask_restful import Resource, Api
from flask_restful import reqparse
import redis

class Handy_logout(Resource):
    def get(self):
        try:
            r = redis.StrictRedis(host="db", port=6379, db=0)
            parser = reqparse.RequestParser()
            parser.add_argument('key', type=str)
            args = parser.parse_args()
           
            _userkey= args['key']
            parts = urlparse('http://123.212.190.148:8300/jsp/openapi/OpenApi.jsp?target=session&todo=logout&K=요청키값')   
            qs = dict(parse_qsl(parts.query))
            qs['K'] = _userkey

            parts = parts._replace(query=urlencode(qs))
            url = urlunparse(parts)
            content = requests.get(url).content
            dicts = xmltodict.parse(content)
            
            if 'error' in dicts.keys():
                return 'error: 인증 오류가 발생하였습니다. ', 404
            else:
                r.delete(_userkey)
                return 'OK', 200
        except Exception as e:
            return {'error': str(e)},404





