import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import joblib

import sklearn.feature_extraction.text as sktext
from sklearn.utils import shuffle
from sklearn.preprocessing import StandardScaler, OneHotEncoder

import pymorphy2
from string import punctuation
import nltk
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

from catboost import CatBoostClassifier

class DenseCountVectorizer(sktext.CountVectorizer):
    def transform(self, raw_documents, copy=True):
        X = super().transform(raw_documents)
        df = pd.DataFrame(X.toarray(), columns=self.get_feature_names())
        return df

    def fit_transform(self, raw_documents, y=None):
        X = super().fit_transform(raw_documents, y=y)
        df = pd.DataFrame(X.toarray(), columns=self.get_feature_names())
        return df

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

def main(params):
	input_file = 'data/predict.csv' if len(params) < 2 else params[1]
	output_file = 'data/result.csv' if len(params) < 3 else params[2]
	personification_techie = 0.5 if len(params) < 4 else float(params[3])
	print(f'\nInput file: {input_file}')
	print(f'Output file: {output_file}\n')
	X_predict = pd.read_csv(input_file, encoding="cp1251", sep=";")
	X_predict_prepared = X_predict.drop({'filename'}, axis=1)
	X_predict_prepared = prepareData(X_predict_prepared)

	vectorizer = joblib.load("vectorizer-light-person.pkl")
	X_predict_vectorized = vectorizer.transform(X_predict_prepared['text'])
	X_predict_vectorized['section_common'] = X_predict_prepared.section_common
	X_predict_vectorized['section_respons'] = X_predict_prepared.section_respons
	X_predict_vectorized['section_rights'] = X_predict_prepared.section_rights
	X_predict_vectorized['section_tasks'] = X_predict_prepared.section_tasks
	X_predict_vectorized['techie'] = personification_techie

	from_file = CatBoostClassifier()
	from_file.load_model("model-light-person.cbm")
	predict = list(map(lambda x: round(x[1], 2), from_file.predict_proba(X_predict_vectorized)))
	X_predict['light'] = predict
	X_predict.to_csv(output_file, sep = ';', encoding="cp1251")

if __name__ == "__main__":
	import sys
	params = sys.argv
	main(params)
