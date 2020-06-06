import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import joblib

import sklearn.feature_extraction.text as sktext
from sklearn.utils import shuffle
from sklearn.preprocessing import StandardScaler, OneHotEncoder

import pymorphy2
import nltk
from nltk.corpus import stopwords
from string import punctuation

from catboost import CatBoostClassifier

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
X_predict = pd.read_csv('data/predict.csv', encoding="cp1251", sep=";")
X_predict_prepared = X_predict.drop({'filename'}, axis=1)

def prepareSentence(morph, russian_stopwords, sentence):
    try:
        words = nltk.word_tokenize(sentence)
    except:
        try:
            words = sentence.split()
        except:
            return ''
    words = [morph.parse(word)[0].normal_form for word in words]
    words = [token for token in words if token not in russian_stopwords\
          and token != " " \
          and token.strip() not in punctuation]
    return ' '.join(words)

def one_hot_encode(df, col):
        df = df.copy()
        return df.drop(col, axis=1).join(pd.get_dummies(df[col], prefix=col))
    
def prepareData(data):
    morph = pymorphy2.MorphAnalyzer()
    russian_stopwords = stopwords.words("russian")
    data = one_hot_encode(data, 'section')
    data['text'] = data.apply(lambda row: prepareSentence(morph, russian_stopwords, row['text']), axis=1)
    return data

X_predict_prepared = prepareData(X_predict_prepared)

class DenseCountVectorizer(sktext.CountVectorizer):
    def transform(self, raw_documents, copy=True):
        X = super().transform(raw_documents)
        df = pd.DataFrame(X.toarray(), columns=self.get_feature_names())
        return df

    def fit_transform(self, raw_documents, y=None):
        X = super().fit_transform(raw_documents, y=y)
        df = pd.DataFrame(X.toarray(), columns=self.get_feature_names())
        return df

vectorizer = joblib.load("vectorizer-light.pkl")
X_predict_vectorized = vectorizer.transform(X_predict_prepared['text'])
X_predict_vectorized['section_common'] = X_predict_prepared.section_common
X_predict_vectorized['section_respons'] = X_predict_prepared.section_respons
X_predict_vectorized['section_rights'] = X_predict_prepared.section_rights
X_predict_vectorized['section_tasks'] = X_predict_prepared.section_tasks

from_file = CatBoostClassifier()

from_file.load_model("model-light.cbm")
predict = list(map(lambda x: round(x[1], 2), from_file.predict_proba(X_predict_vectorized)))
X_predict['light'] = predict
X_predict.to_csv('data/result.csv', sep = ';', encoding="cp1251")