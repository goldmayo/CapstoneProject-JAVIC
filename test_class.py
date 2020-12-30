import nltk
import nltk.classify.util
from konlpy.tag import *
import yaml
import pickle
import os
from naive_bayes_model import *
from datetime import datetime

NB = NB_classifier_interface()
#NB = IntentRecognizer()
# print("--- :",NB.getFeatures)
# # print("--- NB features :",NB.getFeatures())
# print("--- NB Type:",type(NB))
# # print("-- train start ---")
# # NB.getModel()
# # print("--- train finish ---")
# #print("-- train start ---")
# #NB.getModel()
# # print("--- train finish ---")
# print("--- NB features :",NB.getFeatures())
# print("--- NB Labels :",NB.getLabels())
# intent = NB.getPredict("야 로그아웃 해")
# print("--- NB predict :",intent)


# def Do_Cancel():
#     self._request_box.removeOngoing()# 현재 서비즈 중단
#     selected_statement.text = api_frame.wrapContent("서비스를 취소합니다") # 취소 메시지 전송
#     return selected_statement        
#     # return print("cancel")

# def Switch_Case(user_input):
#     service = {
#         '휴가신청' : Draft_Vacation,
#         # "메일확인" : mail_check,
#         # "메일요약" : mail_summerize,
#         # "로그아웃" : Do_logout
#         # "핸디로그아웃" : ,
#         # "구글로그아웃" : ,
#          "취소" : Do_Cancel
#     }
#     print("user_input :", user_input)
#     if user_input in service:
#         return service[user_input]()
#     else:
#         return print("no service.")

# inputstatement = '취소'
        
# statement = input_statement
# selected_statement = input_statement
# selected_statement.confidence = 1 #confidence

# if self._request_box.hasOngoingRequest():# 서비스 실행중
#     intent = self.__classifier.getPredict(statement.text) # intent를 분류
#     Switch_Case(intent) # 취소
#     request_packet = self._request_box.getOngoing() #현재 서비스를 알아냄
#     # 현재 실행중인 서비를 수행, 수행 후 .doSequence 메소드에서 현재 서비스를 request_box에서 제거.
#     request_packet.doSequence(self,selected_statement)

#  else:# 서비스를 실행하지 않고있는 경우
#     intent = self.__classifier.getPredict(statement.text)
#     print("intent value:",intent,self.__intent_recognizer.getTagFromIndex(intent))
    
#     Switch_Case(intent)

# self.debugStatement(input_statement)
# self.debugStatement(selected_statement)
# return selected_statement

class RestRequest():    
    def __init__(self):
        super().__init__()
        self.__start_date = "2020228"
        self.__end_date = "20200222"
        self.__dict =  {1: self.__start_date+"부터 "+self.__end_date+"까지"}
        self.__system_date_format = '%Y%m%d'

    def show(self):
        return self.__dict[1]
# today = datetime.today().strftime("%Y%m%d")
rr = RestRequest()
# print(rr.getData()) #(20200921, 20200931)
# print(type(rr.getData()[0])) # int
#print(type(rr.getData())) #<class 'tuple'>
# print(today) # 20200311
# print(type(today)) # str
# selected_statement.text = Draft_Vacation(rr.getData())
result = rr.show()
print(result)
    # def doSequence(self,uppercls,selected_statement):
    #     if self.hasNext():#<__start_date, __end_date 둘 중 하나라도 none이면 true>
    #         print("if(request_packet.hasNext()):")
    #         self.putCurrentResponse(selected_statement.text)
    #         if self.hasNext():
    #             print("    if(request_packet.hasNext()):")
    #             selected_statement.text = api_frame.wrapContent(self.getNext())
    #         else:
    #             print("    if(request_packet.hasNext())->else")
    #             selected_statement.text = Draft_Vacation(self.getData())
    #             uppercls.tmp_queue.append(self)
    #             uppercls._request_box.removeOngoing()
    #     else: # <__start_date, __end_date 모두 충족>
    #         print("if(request_packet.hasNext())->else")
    #         selected_statement.text = Draft_Vacation(self.getData())
    #         uppercls.tmp_queue.append(self)
    #         uppercls._request_box.removeOngoing()
