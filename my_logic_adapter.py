from chatterbot.logic import LogicAdapter
from datetime import datetime
import nltk
import nltk.classify.util
from konlpy.tag import Okt
import yaml
import pickle
import os
import random
import json 
from lines_summarizer import TextRank # New Summarizer
from datetime import datetime

from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import ne_chunk
import re
import common_api_frame as api_frame

from naive_bayes_model import *

import google_auth
from flask import jsonify

import requests
from flask import Response, session

import nltk
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('punkt')

from nltk.tokenize import sent_tokenize

API_HOST_HANDY_PORT = "http://10.30.7.19.nip.io:7000"
API_HOST_OAUTH_PORT = "http://10.30.7.19.nip.io:7040"

def extractNumber(string):
    regex = re.compile(r'([0-9]*)')
    tokens = word_tokenize(string)
    pos = pos_tag(tokens)
    namedEnt = ne_chunk(pos, binary=True)
    first = True
    for i in namedEnt:
        if(first==True and i[1]=='CD'):
            num = regex.search(i[0])
            return num.group()
            first = False
    return None


def Draft_Vacation(s_date,e_date):
        params = {
            'draft_sdate' : s_date,
            'draft_edate' : e_date,
            'key' : session['userKey']
        }        
        url = API_HOST_HANDY_PORT + '/draftvacation'
        response = requests.get(url, params=params)
        if response.status_code == 200: # 성공
            resp = api_frame.wrapContent(" "+s_date+"부터 "+e_date+"까지 휴가를 신청했습니다.")
            return resp
        elif response.status_code == 404:
            resp = api_frame.wrapContent("휴가신청을 실패했습니다. 다시 시도해주세요.") #휴가신청실패
            return resp
        else:
            resp = api_frame.wrapContent("휴가신청 중에 에러가 발생했습니다. 다시 시도해주세요.") #휴가신청실패
            return resp


def switch_case(user_input):
    service = {
        '휴가신청' : 'draft_vacation',
        '메일확인' : 'mail_check',
        '메일요약' : 'mail_summery',
        '로그아웃' : 'do_logout',
        '핸디로그아웃' : 'handy_logout',
        '구글로그아웃' : 'google_logout',
        '구글로그인' : 'google_login',
        '취소' : 'cancel',
        '긍정' : 'yes',
        '부정' : 'no',
        'no_service' : 'no_service'
    }
    print("user intent :",service[user_input])
    return service[user_input]    


# INYEONG
def getAllMailList(token, mail_type):
    params = {
        'token': token,
        'type': mail_type
    }
    url = API_HOST_OAUTH_PORT + '/all-mails'
    resp = requests.get(url, params=params)

    if resp.status_code == 201:
        mail_json = json.loads(resp.text) # return json
        raw_content = mail_json['body']
        msgid_content = []
        snippet_content = []
        for data in raw_content:
            msgid_content.append(str(list(data.keys())[0]))
            snippet_content.append(str(list(data.values())[0]))
        return msgid_content, snippet_content

    elif resp.status_code == 404:
        mail_json = json.loads(resp.text)
        content = mail_json['error'] # return error msg
        return content, None
    else:
        content = "ERROR"
        return content, None

def getSpecificMailById(token, msgid, opt):
    params = {
        'token' : token,
        'msgid' : msgid,
        'opt' : opt
    }
    url = API_HOST_OAUTH_PORT + '/specific-mail'
    resp = requests.get(url, params=params)

    if resp.status_code == 201:
        mail_json = json.loads(resp.text)
        content = mail_json['Data'] 
    elif resp.status_code == 404:
        mail_json = json.loads(resp.text)
        content = mail_json['error'] # return error msg
    else:
        content = "ERROR"
    return content
######

class MyLogicAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.__classifier = NB_classifier_interface() # 나이브 베이즈 모델
        self._request_box = RequestBox() # 서비스
        self.mail_summary = False

        # for gmail
        self.tmp_queue = []
        ####

        """
        request_box에 실행중인 서비스가 있는 경우,
        사용자 의도분석 결과가 서비스목록(labels)에 있을 경우
        True를 반환하여 my_service_logic_adapter의 process 함수가 실행된다.
        """
    def can_process(self,statement):
        # 서비스 중
        if(self._request_box.hasOngoingRequest()):
            print("service is ongoing")
            return True
        # 사용자 입력의 의도가 서비스 목록에 있을 경우 실행
        intent = self.__classifier.getPredict(statement.text)
        print("intent : ",intent)
        print("labels : ",self.__classifier.getLabels())
        if intent in self.__classifier.getLabels():
            print("predict in :",intent)
            print("CanProcess : true")
            return True
        else:
            return False

    def Do_Handy_Logout(self):
        if 'userKey' in session:
            params={
                'key' : session['userKey']
            }
            url = API_HOST_HANDY_PORT + '/logout'
            resp = requests.get(url, params=params)
            if resp.status_code == 200:
                session.pop('userKey',None)
                
                if google_auth.is_logged_in():
                    google_token = google_auth.get_google_access_token()
                    after = {"recommended_delay_ms":1000,"actions":[{"behavior":"logout","logout_link":f'./google/logout/{google_token}'}]}
                    resp = api_frame.wrapContent("[핸디+구글로그아웃] 동시 로그아웃을 진행합니다", after, type="logout_message")
                else:
                    # Origin
                    after = {"recommended_delay_ms":750,"actions":[{"behavior":"logout","logout_link":'/'}]}
                    resp = api_frame.wrapContent("[핸디로그아웃] 핸디로그아웃을 실행합니다", after, type="logout_message")

            elif resp.status_code != 200:
                after = {"recommended_delay_ms":750,"actions":[{"behavior":"logout","logout_link":"./"}]} # not redirecting now
                resp= api_frame.wrapContent("[핸디로그아웃] 핸디로그아웃에 실패하였습니다 다시 시도해주세요.", after, type="logout_message")

            else:
                after = {"recommended_delay_ms":750,"actions":[{"behavior":"logout","logout_link":"./"}]} # not redirecting now
                resp= api_frame.wrapContent("[핸디로그아웃] 오류가 발생하였습니다. 다시 시도해주세요.", after, type="logout_message")

        else:
            after = {"recommended_delay_ms":750,"actions":[{"behavior":"logout","logout_link":"./"}]} # not redirecting now
            resp= api_frame.wrapContent("[핸디로그아웃] 현재 로그인이 되어있지 않습니다.", after, type="logout_message")
            
        return resp

    # INYEONG
    def doGoogleLogout(self):
        if google_auth.is_logged_in():
            google_token = google_auth.get_google_access_token()
            after = {"recommended_delay_ms":1000,"actions":[{"behavior":"logout","logout_link":f'./google/logout/{google_token}'}]}
            resp= api_frame.wrapContent("[구글로그아웃] 구글로그아웃을 실행합니다", after, type="logout_message")
        else:
            after = {"recommended_delay_ms":1000,"actions":[{"behavior":"logout","logout_link":"./"}]} # not redirecting now
            resp= api_frame.wrapContent("[구글로그아웃] 현재 로그인이 되어있지 않습니다.", after, type="logout_message")
        return resp

    def doGoogleLogin(self):
        after = {"recommended_delay_ms":750,"actions":[{"behavior":"logout","logout_link":"./google/login"}]}
        resp= api_frame.wrapContent("[구글로그인] 로그인 페이지로 이동합니다.", after, type="logout_message")
        return resp
    ############
    
    def debugStatement(self,statement):
        print("--------debugStatement--------")
        print("---id:",statement.id,"\ntext:",statement.text,"\nsearch_text:",statement.search_text,"\nconversation:",statement.conversation,"\npersona:",statement.persona,"\ntags:",statement.tags,"\nin_response_to:",statement.in_response_to,"\nsearch_in_response_to:",statement.search_in_response_to)
        print("------------------------------")
        print()

    def process(self, input_statement, additional_response_selection_parameters):
        """

        """
        print("---additional_response_selection_parameters : ",additional_response_selection_parameters)
        statement = input_statement
        selected_statement = input_statement
        selected_statement.confidence = 1 #confidence

        if self._request_box.hasOngoingRequest(): # 서비스가 실행중인 경우

            intent = switch_case(self.__classifier.getPredict(statement.text)) # intent를 분류 
            request_packet = self._request_box.getOngoing() # 현재 서비스를 알아냄
            now_service = request_packet.getServiceName() # 현재 서비스의 이름 /휴가신청, 메일확인
            print("---intent : ",intent)
            print("---request_packet 현재 서비스: ",request_packet)
            print("---now_service 현재 서비스 이름: ",now_service)

            if(intent =='cancel'): # 취소
                print("---intent : ",intent)
                selected_statement.text = api_frame.wrapContent(now_service+" 서비스를 취소했습니다.") # 취소 메시지 전송
                # selected_statement.text = api_frame.wrapContent("서비스를 취소합니다") # 취소 메시지 전송
                self._request_box.removeOngoing()# 현재 서비즈 중단
                return selected_statement
            
            if intent != "no_service": # intent가 숫자가 아닌 경우
                print("intent가 숫자가 아닌 경우")
                if intent != switch_case(now_service): #현재 서비스와 다른 경우
                    print("현재 서비스와 다른 경우")
                    if intent == 'yes': #확인
                        print("---intent == yes")
                        request_packet.setAgreement(True)
                        request_packet.doSequence(self,selected_statement)
                    else:
                        print("----다른 서비스 요청")
                        self._request_box.removeOngoing() #현재 서비스를 취소
                        # 요청한 서비스 실행
                        self.process(input_statement,{})
                else: # 현재 서비스 재요청하는 경우
                    print("현재 서비스 재요청")
                    print("---request_packet : ",request_packet)
                    request_packet.doSequence(self,selected_statement)
            else: # intent(no_service)가 사용자 입력(숫자 등..)인 경우
                print("---request_packet : ",request_packet)
                request_packet.doSequence(self,selected_statement) # 현재 서비스의 .doSequence()실행

        else: # 실행중인 서비스가 없는 경우
            print("---empty service case")
            service_name = self.__classifier.getPredict(statement.text)
            intent = switch_case(service_name) # intent를 분류 
            # intent = switch_case(self.__classifier.getPredict(statement.text)) # intent를 분류 
            if (intent == 'draft_vacation'): # 휴가신청
                # 로그인서버에서 bool값으로 로그인 확인
                rr = RestRequest() # 휴가신청 클래스 생성
                self._request_box.putOngoing(rr) # 현재 서비스로 등록
                rr.setServiceName(service_name) # 서비스 이름 설정
                if (rr.hasNext()): # 시작일 종료일 중 어떤 것 이라도 none(입력을 받지 않으면) True 둘다 입력받으면 false
                    selected_statement.text = api_frame.wrapContent(rr.getNext()) # 시작일 종료일 입력받기
                else:
                    ###
                    selected_statement.text = Draft_Vacation(rr.getData())
                    ###
                    self._request_box.removeOngoing() #현재 서비스에서 제거

            elif (intent == 'google_login'):
                selected_statement.text = self.doGoogleLogin()

            elif (intent == 'google_logout'):
                selected_statement.text = self.doGoogleLogout()

            elif (intent == 'handy_logout'):
                selected_statement.text = self.Do_Handy_Logout()
            
            elif (intent == 'cancel'):
                selected_statement.text = api_frame.wrapContent("현재 진행중인 서비스가 존재하지 않습니다.")

            elif ( (intent == 'mail_check') or (intent == 'mail_summery') ):
                if google_auth.is_logged_in():
                    
                    google_token = google_auth.get_google_access_token()
                    
                    msgid_content, snippet_content = getAllMailList(token=google_token, mail_type='unread')
                    mr = MailRequest(token=google_token, msgid_content=msgid_content, snippet_content=snippet_content)
                    self._request_box.putOngoing(mr)

                    ###
                    if intent == 'mail_summery':
                        self.mail_summary = True
                    else:
                        self.mail_summary = False

                    mr.setServiceName(service_name)
                    ###

                    if mr.hasNext():
                        selected_statement.text= api_frame.wrapContent(mr.getNext(), type="latest mails")
                    
                    else:
                        if self.mail_summary == True:
                            selected_statement.text = api_frame.wrapContent(mr.summarize(), type="summarized")
                        else:
                            selected_statement.text = api_frame.wrapContent(mr.getContent())
                        self.tmp_queue.append(mr)
                        self._request_box.removeOngoing()
                else:
                    selected_statement.text = self.doGoogleLogin()
            else: 
                print("other intent:", intent)
                selected_statement.text = api_frame.wrapContent("문의하신 내용에 대해 다음에는 안내드릴 수 있도록 열심히 학습하겠습니다.")

        self.debugStatement(selected_statement)
        return selected_statement


class RequestBox(object):
    def __init__(self):
        self.__ongoing_request = False
        self.ongoing_packet = None

    def putOngoing(self,packet):# 서비스 추가
        self.ongoing_packet = packet
    def hasOngoingRequest(self): # 서비스 유무 확인
        return self.ongoing_packet is not None
    def getOngoing(self): #서비스 가져오기
        return self.ongoing_packet
    def removeOngoing(self): # 서비스 삭제
        if self.hasOngoingRequest():
            tmp = self.ongoing_packet
            self.ongoing_packet = None
            return tmp
        else:
            pass
    
class OngoingPacket(object):
    def __init__(self):
        pass
    def hasNext(self):
        raise NotImplementedError()
    def getNext(self):
        raise NotImplementedError()
    def putCurrentResponse(self,resp):
        raise NotImplementedError()
    def getData(self):
        raise NotImplementedError()
    def getServiceName(self):
        raise NotImplementedError()    
    def doSequence(self,uppercls,selected_statement):
        return NotImplementedError()


# INYEONG
class MailRequest(OngoingPacket):
    def __init__(self, token, msgid_content, snippet_content):
        super().__init__()
        self.__dict = {1:"메일을 선택해주세요.",-1:"알 수 없음"}
        self.token = token
        self.__mfilelist = list(snippet_content)
        self.__mfilelist_thread = list(msgid_content)
        self.__mail_thread_id = None
    
        ###
        self.__service_name = None
        ###
    def hasNext(self):
        return self.__mail_thread_id is None
    
    def getNextAsNumber(self):
        if self.__mail_thread_id is None:
            return 1
        else:
            return None
    
    def putCurrentResponse(self, resp):
        resp = extractNumber(resp)
        if (not resp is None) and type(resp) is str and resp.isdigit():
            index = int(resp)-1
            if 0 <= index < len(self.__mfilelist_thread):
                self.__mail_thread_id = self.__mfilelist_thread[index]                
                return True
        return False
    ###    
    def getServiceName(self):
        return self.__service_name

    def setServiceName(self, name):
            self.__service_name = name
    ###

    def getNext(self):
        nn = self.getNextAsNumber()
        if nn is None:
            return None
        elif nn==1:
            return self.__mfilelist
        else:
            return self.__dict[nn]

    def getData(self):
        mail_thread_id = self.__mail_thread_id
        if not mail_thread_id is None:
            api_resp = getSpecificMailById(token=self.token, msgid=mail_thread_id, opt='plain')
            return api_resp
        else:
            return None

    def summarize(self):
        content = self.getData()
        if content is None:
            return None
        else:
            # INYEONG
            textrank = TextRank(content)
            
            res = []
            for row in textrank.summarize(3):
                res.append(row)
            return res
            
    def getContent(self):
        return self.getData()

    def doSequence(self,uppercls,selected_statement):
        if self.hasNext():
            succ = self.putCurrentResponse(selected_statement.text) # bool
            if succ:
                if self.hasNext():
                    selected_statement.text = api_frame.wrapContent(self.getNext(), type="latest mails")
                else:
                    if uppercls.mail_summary==True:
                        selected_statement.text = api_frame.wrapContent(self.summarize(), type="summarized")
                    else:
                        selected_statement.text = api_frame.wrapContent(self.getContent())
                    uppercls.tmp_queue.append(self)
                    uppercls._request_box.removeOngoing()
            else:
                selected_statement.text = api_frame.wrapContent("잘못된 입력.\t\n"+self.getNext())

        else:
            if uppercls.mail_summary == True:
                selected_statement.text = api_frame.wrapContent(self.summarize(), type="summarized")
            else:
                selected_statement.text = api_frame.wrapContent(self.getContent())
            uppercls.tmp_queue.append(self)
            uppercls._request_box.removeOngoing()

class RestRequest(OngoingPacket):    
    def __init__(self):
        super().__init__()
        self.__service_name = None
        self.__start_date = None
        self.__end_date = None
        self.__agreement = False 
        self.__system_date_format = '%Y%m%d'
        self.__today = datetime.today().strftime(self.__system_date_format) #yyyymmdd
        self.__dict =  {1:"시작 날짜를 입력해주세요.(YYYYMMDD)",2:"종료 날짜를 입력해주세요(YYYYMMDD)",3:str(self.__start_date)+"부터 "+str(self.__end_date)+"까지 휴가를 신청하시겠습니까?",-1:"알 수 없음"} # 3번은 잘 안됨
        self.__invalid_msg = {1:"날짜형식 혹은 시작일이 올바르지 않습니다. 다시 입력해주세요.",2:"날짜형식 혹은 종료일이 올바르지 않습니다. 다시 입력해주세요.",3:"확인과 취소를 선택해주세요.",-1:"날짜형식이 올바르지 않습니다. 다시 입력해주세요."}

    def getData(self):
        return (self.__start_date, self.__end_date, self.__request_status)
    
    def getServiceName(self):
            return self.__service_name
    
    def setServiceName(self,name):
            self.__service_name = name
    
    def hasNext(self):
        return self.__start_date is None or self.__end_date is None or self.__agreement is False
    
    def getNextAsNumber(self):
        if self.hasNext():
            if self.__start_date is None:
                return 1
            elif self.__end_date is None:
                return 2
            elif self.__agreement is False:
                return 3
            else:
                return False
        else:
            return None
            
    def getNext(self):
        n = self.getNextAsNumber()
        if n is None:
            return None
        else:
            return self.__dict[n]

    def request_MSG(self): #재전송 MSG
        n = self.getNextAsNumber()
        if n is None:
            return None
        else:
            return self.__invalid_msg[n]
            
    def check_format(self,dates):
        try:
            input_date = datetime.strptime(str(dates),self.__system_date_format) # 날짜 형식체크 
            del(input_date)
            return True
        except ValueError:
            return False
    
    def check_invalid(self,resp):
        num = self.getNextAsNumber()
        if num is None:
            pass
        elif num==1:
            if self.check_format(resp):
                if  int(resp) > int(self.__today):
                    return True
                else:
                    return False # 지난 날짜 __start_date = None > getNextAsNumber = 1
            else:
                return False # 날짜형식이 올바르지 않음
        elif num==2:
            if self.check_format(resp):
                if int(resp) > int(self.__start_date):
                    return True
                else:
                    return False # 휴가 시작일이 종료일보다 더 뒤의 날짜 __end_date = None > getNextAsNumber = 2
            else:
                return False # 날짜형식이 올바르지 않음
        elif num==3: # y/n
            if self.__agreement == True: # yes 취소는 아예 doSequence가 실행이 되지 않음
                return True
            else: # yes말고 내려올 건 숫자 밖에 없음
                return False # 에러 예 아니오 
        else:
            return False


    def putCurrentResponse(self,resp):
        num = self.getNextAsNumber()
        if num is None:
            pass
        elif num==1:
            self.__start_date = resp
        elif num==2:
            self.__end_date = resp
        elif num==3:
            pass

    def setAgreement(self,agree):
        self.__agreement = agree
    
    def doSequence(self,uppercls,selected_statement):
        if self.hasNext(): #<__start_date, __end_date 둘 중 하나라도 none이면 true>
            if self.check_invalid(selected_statement.text): # bool
                self.putCurrentResponse(selected_statement.text)
                if self.hasNext(): #실행구역
                    if self.getNextAsNumber() == 3: #유저가 네 라고하면 
                        selected_statement.text = api_frame.wrapContent(str(self.__start_date)+"부터 "+str(self.__end_date)+"까지 휴가를 신청하시겠습니까?",type="confirm") # 다음 입력 메세지
                    else:
                        selected_statement.text = api_frame.wrapContent(self.getNext()) # 다음 입력 메세지
                else:

                    # ###
                    #     """
                    #     확인/취소            
                    #     취소누르면 process에서 입력받자마자 컷 해줌
                    #     예스하면 self.__agreement = True 
                    #     yes > setAgreement > self.__agreement = True > hasNext() #실행구역 = False
                        
                    #     내일할것 :
                          #네/ 아니오   타입 컨펌 말풍선 구현해 놓음 프론트 구현해야한다.
                          #로그인 철저히 검사
                    #     메일서비스
                            
                    #     """
                    if self.__agreement == True:
                        selected_statement.text = Draft_Vacation(self.__start_date,self.__end_date)
                        
                        uppercls._request_box.removeOngoing()
                    else:
                        selected_statement.text = common_api_frame.wrapContent("휴가신청을 취소합니다.")
                        uppercls._request_box.removeOngoing()
            else:
                selected_statement.text = api_frame.wrapContent(self.request_MSG())           
        else: # <__start_date, __end_date, confirm(y/n) 모두 충족>
            if self.__agreement:
                selected_statement.text = Draft_Vacation(self.__start_date,self.__end_date)
                uppercls._request_box.removeOngoing()
            else:
                selected_statement.text = common_api_frame.wrapContent("휴가신청을 취소합니다.")
                uppercls._request_box.removeOngoing()
