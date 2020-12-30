import nltk
from nltk import NaiveBayesClassifier
import nltk.classify.util
from konlpy.tag import *
import yaml
import pickle
import os

class NB_classifier_interface():
    def __init__(self):
        self.classifier = NaiveBayesClassifier
        self.__tokenizer = Okt()
        self.train_data = []
        self._isTrain = False
        saved_model = 'naivebayes.pickle'
        if(os.path.exists(saved_model)):
            self.load_model(saved_model)
            self._isTrain = True
        else:
            self.train()

    def is_trained(self):
        return self._isTrain

    def load_data(self,path):
        with open(path, 'r',encoding='UTF8') as stream:
            data_loaded = yaml.safe_load(stream)
            dt = data_loaded["conversations"]
            for i in dt:
                self.train_data.append((i[0],i[1]))
        #print("load data from yml file :",train)
        #print("--- train data loaded ---")
        return self.train_data
    
    def save_model(self,classifier):
        save_classifier = open("naivebayes.pickle","wb")
        pickle.dump(classifier, save_classifier)
        save_classifier.close()
        #print("--- classifier saved ---","\n") 
    
    def load_model(self,file_name):
        classifier_f = open(file_name, "rb")
        self.classifier = pickle.load(classifier_f)
        classifier_f.close()

    def preprocess(self,data):
        features = set( word for passage in data for word in self.__tokenizer.morphs( passage[0],stem=True,norm=False,) )
        #print("--- extracted features :", features ---)
        preprocessed_data = [
            (   
                { word: ( word in self.__tokenizer.morphs(x[0],stem=True,norm=False) )  for word in features }, 
                x[1]
            )
            for x in data
        ]
        #print("t :",t)
        return preprocessed_data
    
    def train(self):
        # 처음 train하는 경우
        # print("is_trained??",self._isTrain)
        # print("--- train data load ---")
        train_data = self.load_data("data/korean/test/my_train.yml")
        # print(" --- preprocess ---")
        preprocessed_data = self.preprocess(train_data)
        # print("--- train ---")
        classifier = self.classifier.train(preprocessed_data)
        # print("--- save model ---")
        self.save_model(classifier)
        self._isTrain = True
        # print("---after train isTrain :",self._isTrain)
        return

    def getFeatures(self):
        # classifier = load_model()
        features = set( word[0] for word in self.classifier.most_informative_features())
        # del(classifier)
        return features
    
    def getLabels(self):
        # classifier = load_model()
        labels = self.classifier.labels()
        # del(classifier)
        return labels      

    def getPredict(self,sentence):
        print("--- sentence :",sentence)
        userinput = self.__tokenizer.morphs(sentence,stem=True,norm=False)
        print("--- userinput :",userinput)
        preprocessed_sentence = { word : ( word in userinput ) for word in self.getFeatures() }
        print("---prep_sentence: ",preprocessed_sentence, type(preprocessed_sentence))
        print("---prep_sentence: ",preprocessed_sentence.keys(), type(preprocessed_sentence))

        if any(x in userinput for x in preprocessed_sentence.keys()):
            intents = self.classifier.classify(preprocessed_sentence)
        else:
            intents = "no_service"
        print("predict :", intents)
        return intents
 