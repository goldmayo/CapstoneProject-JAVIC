from konlpy.tag import Okt
import yaml
#import yaml

pos_tagger = Okt()

#test = input("Input : ")
train=[]
with open("data/korean/test/test2.yml", 'r',encoding='UTF8') as stream:
    data_loaded = yaml.safe_load(stream)    
    dt = data_loaded["conversations"]
    for i in dt:
        train.append((i[0],i[1]))
print("load data from yml file :",train)
print("__________________________________")

all_words = set( word.lower() for passage in train for word in pos_tagger.morphs( passage[0], stem=True,norm=False) )
print("all_words :", all_words)
print("__________________________________")

t = [
    (   
        { word: ( word in pos_tagger.morphs(x[0], stem=True,norm=False) )  for word in all_words }, 
        x[1]
        # { word: ( word in word_tokenize(x[0]) )  for word in all_words }, 
        # x[1]
    )
    for x in train
]
print("t :",t)
'약하다': False, '목록': False, '하고': False, '해': False, '핸디': False, '확인': False, '부탁': False,
 '하다': False, '싶다': False, '구글': False, '약': False, '요': False,
 '휴가': True, '신청': True, '요약': False, '해주다': False, '보여주다': False, '취소': False, '메일': False},
 '휴가신청')
- - 휴가신청
  - 휴가신청

  {'약하다': False, '목록': False, '하고': False, '해': False, '핸디': False, '확인': False, '부탁': False,
   '하다': False, '싶다': False, '구글': False, '약': False, '요': False, '휴가': False, '신청': False,
   '요약': False, '해주다': False, '보여주다': True, '취소': False, '메일': True},
    '메일확인')
- - 메일보여줘
  - 메일확인
#tokenized_words = tokenizer.morphs(test, norm=True, stem=False)
#print("tokenized_words : ",tokenized_words) # 휴가 가다 싶다