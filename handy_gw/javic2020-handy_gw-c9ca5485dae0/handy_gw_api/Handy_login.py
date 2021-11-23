# -*- coding: utf-8 -*-

from flask import Flask
import requests, xmltodict, json
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from flask_restful import Resource, Api
from flask_restful import reqparse
import redis

class Handy_login(Resource):
    def get(self):
        try:
            r = redis.StrictRedis(host="db", port=6379, db=0)
            parser = reqparse.RequestParser()
            
            parser.add_argument('name', type=str)
            parser.add_argument('passwd', type=str)
            args = parser.parse_args()

            _username= args['name']
            _userpasswd= args['passwd']
            parts = urlparse('http://123.212.190.148:8300/jsp/openapi/OpenApi.jsp?target=session&todo=login&name=사용자이름&passwd=로그인암호')   
            qs = dict(parse_qsl(parts.query))
            qs['name'] = _username
            qs['passwd'] = _userpasswd
            parts = parts._replace(query=urlencode(qs))
            url = urlunparse(parts)
            content = requests.get(url).content
            dicts = xmltodict.parse(content)

            if 'error' in dicts.keys():
                jsonString=json.dumps(dicts,ensure_ascii=False)
                jsonObj= json.loads(jsonString)
                return jsonObj['error']['code'], 404
            else:
                key=dicts['session']['key']
                jsonString=json.dumps(dicts,ensure_ascii=False)
                r.set(key,jsonString)
                response=json.loads(jsonString)
                return key,200
        except Exception as e:
            return {'error': str(e)}, 405



















