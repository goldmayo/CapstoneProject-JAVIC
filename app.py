# -*- coding: utf-8 -*-
from flask import Flask, render_template, send_from_directory, session, request, redirect, url_for
import flask

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

import os
import json
import random
import functools
import requests

from konlpy.tag import Okt
import redis

#local module
import common_api_frame as api_frame

# add now : local module
import google_auth
from authlib.client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery
from googleapiclient.discovery import build
#####

app = Flask(__name__)

app.register_blueprint(google_auth.app)
app.secret_key = os.environ["FN_CLIENT_SECRET"]

API_HOST_HANDY_PORT = "http://10.30.7.19.nip.io:7000"

#---create bot
bot = ChatBot(
    'Terminal',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        #'chatterbot.logic.MathematicalEvaluation',
        #'chatterbot.logic.TimeLogicAdapter',
        {
            'import_path':'my_logic_adapter.MyLogicAdapter'
        },
        {
            'import_path':'chatterbot.logic.BestMatch',
            'default_response': '질문의 의도를 모르겠어요.',
            'maximum_similarity_threshold': 0.90
        },

    ],
    database_uri='sqlite:///database.sqlite3'
)
trainer = ChatterBotCorpusTrainer(bot)
trainer.train("./data/korean/chatterbot_corpus")


@app.route('/',methods=['GET','POST'])
def show_login():
    # session.pop('userKey',None)
    if 'userKey' in session:
#        print("session key :",session['userKey'])
        return redirect(url_for('chatbot'))
    else:
#        print("no session")
        return render_template("login.html")


@app.route('/chatbot',methods=['GET', 'POST'])
def chatbot():
    if 'userKey' in session:
        print("session key :",session['userKey'])
        return render_template('chatbot.html')
    else:
        return redirect(url_for('show_login'))

@app.route('/ajax_login',methods=['POST'])
def test_ajax():
    if request.method == "POST":
        req = request.get_json()
        print("req :",req)
        params = {
            'name' : req['name'],
            'passwd' : req['passwd']
        }
        print("params :", params)
        url = API_HOST_HANDY_PORT + '/login'
        api_resp = requests.get(url, params=params)
        print("api_resp :",api_resp)

        if api_resp.status_code == 200:
            received_key = json.loads(api_resp.text)
            print("received key:",received_key)
            
            session['userKey'] = received_key
            print("session['userKey']:",session['userKey'])

            to_client = "200"
            resp = json.dumps(to_client, ensure_ascii=False)

            return resp
            # return redirect(url_for('chatbot'))
        
        elif api_resp.status_code == 404:
            received_data = json.loads(api_resp.text)

            error_res = json.dumps(str(received_data), ensure_ascii=False)

            return error_res
        
        else:
            error = "500"
            resp = json.dumps(error)
            return resp
    

@app.route("/req",methods=['POST'])
def procReq():
    if 'userKey' not in session:
        after = {"recommended_delay_ms":2000,"actions":[{"behavior":"logout","logout_link":"./"}]}
        resp = api_frame.wrapContent("현재 로그인이 되어있지 않습니다. 2초 후 로그인 페이지로 이동합니다.", after, type="logout_message")
        return resp

    global okt
    req = flask.request.get_json()
    print("req:",req)
    txt = req["text"]
    rst = txt
    response = bot.get_response(txt)
    rst = response.text
    dict = rst
    try:
        tmp = json.loads(dict)
        temp_resp =dict 
        del tmp
    except:
        temp_resp = api_frame.wrapContent(dict)
    
    resp = app.make_response(temp_resp)
    resp.mimetype="application/json"
    print("resp :",resp)

    return resp

if __name__ == '__main__':
    app.run(debug=True, port=7070)
