import nltk
import nltk.classify.util
from konlpy.tag import Okt
import yaml
import pickle

pos_tagger = Okt()

train = []

with open("data/korean/test/my_train.yml", 'r',encoding='UTF8') as stream:
    data_loaded = yaml.safe_load(stream)
    # print("data_loaded : ",data_loaded)
    # data_loaded :  {'categories': ['휴가신청'], 'conversations': [['휴가 신청 해줘', '휴가신청'], ['휴가 신청', '휴가신청'], ['휴가신청', '휴가신청'], ['휴가 신청 부탁해', '휴가신청'], ['휴가신청해줘', '휴가신청'], ['휴가신청부탁해', '휴가신청'], ['휴가를 신청해', '휴가신청'], ['휴가를 신청해줘', '휴가신청'], ['휴가신청요청해', '휴가신청'], ['휴가신청을 희망해', '휴가신청'], ['휴가신청할께', '휴가신청'], ['휴가신청하고 싶어', '휴가신청'], ['휴가를 보내고 싶어', '휴가신청'], ['나는 휴가신청을 하고싶어', '휴가신청']]}
    # print('--------------------------')
    
    dt = data_loaded["conversations"]
    # print("dt : ",dt)
    #dt :  [['휴가 신청 해줘', '휴가신청'], ['휴가 신청', '휴가신청'], ['휴가신청', '휴가신청'], ['휴가 신청 부탁해', '휴가신청'], ['휴가신청해줘', '휴가신청'], ['휴가신청부탁해', '휴가신청'], ['휴가를 신청해', '휴가신청'], ['휴가를 신청해줘', '휴가신청'], ['휴가신청요청해', '휴가신청'], ['휴가신청을 희망해', '휴가신청'], ['휴가신청할께', '휴가신청'], ['휴가신청하고 싶어', '휴가신청'], ['휴가를 보내고 싶어', '휴가신청'], ['나는 휴가신청을 하고싶어', '휴가신청']]
    # print("-----------------------------")
    
    for i in dt:
        train.append((i[0],i[1]))
# #print("load data from yml file :",train)
# print("______________loaded____________________")
# # train = [
# #     #( '휴가신청','휴가신청' ),
# #     ( '휴가',' 휴가신청' ),
# #     ( '신청','휴가신청' ),

# #     #( '메일확인','메일확인' ),
# #     ( '메일','메일확인' ),
# #     ( '확인','메일확인' ),

# #     ( '요약','메일요약'),

# #     ( '취소','취소' ),

# #     ( '로그아웃','로그아웃'),

# # ]

# # test = [
# #     ( '휴가신청','휴가신청' ),
# #     ( '휴가 신청','휴가신청' ),
# #     ( '휴가 신청해줘',' 휴가신청' ),
# #     ( '휴가 신청할게','휴가신청' ),
# #     ( '휴가 신청하고 싶어','휴가신청' ),

# #     ( '메일목록','메일확인' ),
# #     ( '메일확인','메일확인' ),
# #     ( '메일 확인해줘','메일확인' ),
# #     ( '메일 확인','메일확인' ),
# #     ( '메일 확인 부탁해','메일확인' ),
# #     ( '메일 확인해','메일확인' ),

# #     ( '메일 요약해줘','메일요약' ),
# #     ( '메일 요약부탁해','메일요약' ),
# #     ( '메일 요약해','메일요약' ),
# #     ( '메일요약','메일요약' ),
# #     ( '메일 요약','메일요약' ),

# #     ( '로그아웃 해줘','로그아웃' ),
# #     ( '취소할래','취소' ),
# #     ( '구글 로그아웃해', '구글로그아웃' ),
# #     ( '핸디 로그아웃', '핸디 로그아웃'),
# #     ( '휴가 신청 부탁해','휴가신청' )
# # ]

all_words = set( word.lower() for passage in train for word in pos_tagger.nouns( passage[0]) )
# print("all_words :", all_words)
# print("__________________________________")

# t = [
#     (   
#         { word: ( word in pos_tagger.nouns(x[0]) )  for word in all_words }, 
#         x[1]
#         # { word: ( word in word_tokenize(x[0]) )  for word in all_words }, 
#         # x[1]
#     )
#     for x in train
# ]
# #print("t :",t)

# # train_data에서 중복을 허용하지 않고 label를 추출.
# intent_keys = set(x[1] for x in train)

# print("intent_keys : ",intent_keys)
# # len(test_keys)만큼 숫자 인덱스 생성.
# intent_values = [x for x in range(len(intent_keys))]
# print("intent_values :",intent_values)

# # intents가 dict형식이므로 key와 value의 수정과 추가 삭제가 용이.
# intents = dict(zip(intent_keys, intent_values))
# print("intents : ", intents)

# #print("intent['휴가신청'] :",intents['휴가신청'])

# classifier = nltk.NaiveBayesClassifier.train(t)
# classifier.show_most_informative_features()
#__________________________________
# test_sentence = '로그아웃'
# print("input :",test_sentence)
#__________________________________
#nouns_words = pos_tagger.nouns(test_sentence)
#print("nouns_words : ",nouns_words, type(nouns_words))

# extracted_word = " ".join(nouns_words)
# print("extracted_word : ",extracted_word) # str
#______________________________________________________
# test_sent_features = { word : ( word in pos_tagger.nouns(test_sentence) ) for word in all_words }
# print("test_sent_features :",test_sent_features)

# print(classifier.classify(test_sent_features))
#_______________________________________________________
# save_classifier = open("naivebayes.pickle","wb")
# pickle.dump(classifier, save_classifier)
# save_classifier.close()
# print("--- classifier saved ---","\n") 
# -- Load classifier from pickle
# classifier_f = open("naivebayes.pickle", "rb")
# classifier_new = pickle.load(classifier_f)
# classifier_f.close()
# print("--- classifier loaded ---","\n")  
# print(type(classifier_new))
# classifier_new.show_most_informative_features()
# print("_________ Classifier type", "_" * 30, "\n")

# print("most_informative_features :",classifier_new.most_informative_features()[0])
# #print(classifier_new.most_informative_features()[0])


#features = set( word[0] for word in classifier_new.most_informative_features())
# print("features :",features)

# print("________________________________")
# print("labels :",classifier_new.labels())




test = []

with open("data/korean/test/my_test.yml", 'r',encoding='UTF8') as stream:
    data_loaded = yaml.safe_load(stream)
    # print("data_loaded : ",data_loaded)
    # data_loaded :  {'categories': ['휴가신청'], 'conversations': [['휴가 신청 해줘', '휴가신청'], ['휴가 신청', '휴가신청'], ['휴가신청', '휴가신청'], ['휴가 신청 부탁해', '휴가신청'], ['휴가신청해줘', '휴가신청'], ['휴가신청부탁해', '휴가신청'], ['휴가를 신청해', '휴가신청'], ['휴가를 신청해줘', '휴가신청'], ['휴가신청요청해', '휴가신청'], ['휴가신청을 희망해', '휴가신청'], ['휴가신청할께', '휴가신청'], ['휴가신청하고 싶어', '휴가신청'], ['휴가를 보내고 싶어', '휴가신청'], ['나는 휴가신청을 하고싶어', '휴가신청']]}
    # print('--------------------------')
    
    dt = data_loaded["conversations"]
    # print("dt : ",dt)
    #dt :  [['휴가 신청 해줘', '휴가신청'], ['휴가 신청', '휴가신청'], ['휴가신청', '휴가신청'], ['휴가 신청 부탁해', '휴가신청'], ['휴가신청해줘', '휴가신청'], ['휴가신청부탁해', '휴가신청'], ['휴가를 신청해', '휴가신청'], ['휴가를 신청해줘', '휴가신청'], ['휴가신청요청해', '휴가신청'], ['휴가신청을 희망해', '휴가신청'], ['휴가신청할께', '휴가신청'], ['휴가신청하고 싶어', '휴가신청'], ['휴가를 보내고 싶어', '휴가신청'], ['나는 휴가신청을 하고싶어', '휴가신청']]
    # print("-----------------------------")
    
    for i in dt:
        test.append((i[0],i[1]))

#preprocessing
testing = [
    (   
        { word: ( word in pos_tagger.nouns(x[0]) )  for word in all_words },
        x[1]
        # { word: ( word in word_tokenize(x[0]) )  for word in all_words }, 
        # x[1]
    )
    for x in test
]

# -- Reuse classifier
classifier_f = open("naivebayes.pickle", "rb")
classifier_new = pickle.load(classifier_f)
classifier_f.close()
print("--- classifier loaded ---","\n")  

print("--- loaded classifiter accuracy ---","\n")
print((nltk.classify.accuracy(classifier_new, testing))*100, '%')

# test_sentence = ''
# test_sentence = '구글로그아웃해줘'
# test_sentence = '메일목록보여줘'
# test_sentence = '메일목록보여줘'
# print("input :",test_sentence)

# test_morphs = pos_tagger.morphs(test_sentence,stem=True,norm=False) 
# print("morphs:",test_morphs)

# test_sent_features = { word : ( word in pos_tagger.nouns(test_sentence) ) for word in features }
# print("test_sent_features :",test_sent_features)
# print(classifier_new.classify(test_sent_features))

# print("_____________________________________________________")

# test_sent_features = { word : ( word in test_morphs ) for word in features }
# print("test_sent_features :",test_sent_features)

# print(classifier_new.classify(test_sent_features))


#############################################

# def intetnt_switch(x):
        
#         return {'휴가신청': lambda :,
#                 '메일확인': lambda :,
#                 '메일요약': lambda :,
#                 '로그아웃': lambda :,
#                 '취소': lambda :
#                 }.get(x, "No data")
# pos_tagger = Okt()
# # 학습할 데이터 로드
# def load_filter():
#     train = []
#     with open("data/korean/test/test.yml", 'r',encoding='UTF8') as stream:
#         data_loaded = yaml.safe_load(stream)
#         # print("data_loaded : ",data_loaded)
#         # data_loaded :  {'categories': ['휴가신청'], 'conversations': [['휴가 신청 해줘', '휴가신청'], ['휴가 신청', '휴가신청'], ['휴가신청', '휴가신청'], ['휴가 신청 부탁해', '휴가신청'], ['휴가신청해줘', '휴가신청'], ['휴가신청부탁해', '휴가신청'], ['휴가를 신청해', '휴가신청'], ['휴가를 신청해줘', '휴가신청'], ['휴가신청요청해', '휴가신청'], ['휴가신청을 희망해', '휴가신청'], ['휴가신청할께', '휴가신청'], ['휴가신청하고 싶어', '휴가신청'], ['휴가를 보내고 싶어', '휴가신청'], ['나는 휴가신청을 하고싶어', '휴가신청']]}
#         # print('--------------------------')
        
#         dt = data_loaded["conversations"]
#         # print("dt : ",dt)
#         #dt :  [['휴가 신청 해줘', '휴가신청'], ['휴가 신청', '휴가신청'], ['휴가신청', '휴가신청'], ['휴가 신청 부탁해', '휴가신청'], ['휴가신청해줘', '휴가신청'], ['휴가신청부탁해', '휴가신청'], ['휴가를 신청해', '휴가신청'], ['휴가를 신청해줘', '휴가신청'], ['휴가신청요청해', '휴가신청'], ['휴가신청을 희망해', '휴가신청'], ['휴가신청할께', '휴가신청'], ['휴가신청하고 싶어', '휴가신청'], ['휴가를 보내고 싶어', '휴가신청'], ['나는 휴가신청을 하고싶어', '휴가신청']]
#         # print("-----------------------------")
        
#         for i in dt:
#             train.append((i[0],i[1]))
#     return train
# train = lambda : load_filter()
# # 데이터 전처리를 위한 필터의 집합(set) 생성 한번만 로드하고 집합 생성후 로드된 train 삭제 
# all_words = set( word.lower() for passage in train for word in pos_tagger.nouns( passage[0]) )
# del(train)
# # 학습된 분류모델 로드
# classifier_f = open("naivebayes.pickle", "rb")
# classifier = pickle.load(classifier_f)
# classifier_f.close()

# user_input = input_statement.text
# # 입력 데이터 전처리
# preprocessed_user_input = { word : ( word in pos_tagger.nouns(test_sentence) ) for word in all_words }
# # 전처리된 입력 데이터를 분류 predict(classify)
# label = classifier.classify(preprocessed_user_input)
# # label = 
# intetnt_switch[label]


