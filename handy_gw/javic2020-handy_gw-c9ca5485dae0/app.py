from flask import render_template,Flask
import requests, xmltodict, json
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from flask_restful import Resource, Api
from flask_restful import reqparse

from handy_gw_api.Handy_login import Handy_login
from handy_gw_api.Handy_logout import Handy_logout
from handy_gw_api.Draft_vacation import Draft_vacation
import redis

app = Flask(__name__)
api = Api(app)

api.add_resource(Handy_login, '/login')
api.add_resource(Handy_logout, '/logout')
api.add_resource(Draft_vacation, '/draftvacation')

@app.route('/')
def index():
    return render_template("/index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)
