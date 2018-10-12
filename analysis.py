from bs4 import BeautifulSoup
import urllib3
import certifi
import requests
import pandas as pd
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
import time
import numpy as np
from matplotlib import pyplot as plt
import re
import statsmodels.api as sm
import seaborn as sns
from sklearn import preprocessing
from statsmodels.graphics.mosaicplot import mosaic
import matplotlib.colors as colors
from mpl_toolkits.mplot3d import Axes3D
from sklearn.manifold import TSNE
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.metrics import accuracy_score, f1_score
import warnings
warnings.filterwarnings('ignore')

%matplotlib inline
import seaborn as sns

import plotly
import plotly.graph_objs as go
plotly.offline.init_notebook_mode(connected=True)

import matplotlib.pyplot as plt
%matplotlib inline


from sklearn.model_selection import train_test_split
#pd.options.display.max_rows = len(df)

import nltk
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
nltk.download('punkt')
punc = ['.', ',', '"', "'", '?', '!','+', ':', ';', '(', ')', '[', ']', '{', '}',"%", '-', '✔', '™', '1','2','3','4','5','6','7','8', '9', '0', 'which', 1234567890]
stop_words = ENGLISH_STOP_WORDS.union(punc)
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from nltk import word_tokenize,sent_tokenize


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from imblearn.over_sampling import RandomOverSampler
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn import ensemble
import xgboost
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from pandas_ml import ConfusionMatrix
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn import naive_bayes
from sklearn import svm
from sklearn import neighbors
from sklearn import decomposition
from sklearn.metrics.pairwise import cosine_similarity
from matplotlib import cm
from sklearn import model_selection
from sklearn.metrics import mean_squared_error
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from imblearn.over_sampling import SMOTE
import patsy as pt
import pymc3 as pm
from keras.models import Sequential
from keras import initializers
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn import preprocessing
from keras import optimizers

def column_count(dataframe ,column):
    """count the number of unique items in each column"""
    count=[]
    column_types= [i for i in column.unique()]
    for c in column_types:
        count.append((c, len(dataframe[column==c])))
    return dict(count)
def clean_id_col(row_num, digit):
    """clean up id column """
    df['ID'].iloc[row_num]=df['Link'].iloc[row_num][digit:]
    print (df['ID'].iloc[row_num])
def normalize(col):
    minimum = col.min()
    maximum = col.max()
    return (col-minimum)/(maximum-minimum)
def reports_classification(clf,X_train,X_test,y_train,y_test ):
    predict = clf.predict(X_test)
    cm=confusion_matrix(y_test, predict)
    cr=classification_report(y_test, predict)
    score_train=clf.score(X_train, y_train)
    score_test=clf.score(X_test, y_test)
    return print (cm, cr, score_train, score_test)


def highrating_count_perc(dataframe):
    """map catagorical labels for generalized by % of 5 star ratings in reviews as well, aveg and  poor as specified by the keys below
    0=above_average, 1=average, 2=below_average, 3= poor"""
    dataframe['4&5StarCount%_rounded']=dataframe['4&5StarCount%'].round(1).astype('str')
    percentile_mapping={'1.0': 0,
                 '0.9':0,
                 '0.8':1,
                 '0.7':2,
                 '0.6':2,
                 '0.5':3,
                 '0.4':3,
                 '0.3':3,
                 '0.2':3,
                 '0.1':3,
                 '0.0':3}
    dataframe['4&5StarCount%_tile']=dataframe['4&5StarCount%_rounded'].map(percentile_mapping)


from nltk.tokenize import word_tokenize
def text_processor(dialogue):
    dialogue = word_tokenize(dialogue)
    nopunc=[word.lower() for word in dialogue if word not in stop_words]
    nopunc=' '.join(nopunc)
    return [word for word in nopunc.split()]
def text_process(text):
    nopunc=[word.lower() for word in text if word not in stop_words]
    nopunc=''.join(nopunc)
    return [word for word in nopunc.split()]


def plot_feature_importances(clf):
    n_features = X_train.shape[1]
    plt.figure(figsize=(10,10))
    plt.barh(range(n_features), clf.feature_importances_, align='center')
    plt.yticks(np.arange(n_features), X_train.columns.values)
    plt.xlabel("Feature importance")
    plt.ylabel("Feature")
    plt.title ('Feature Importance')
    plt.show()

def regression_performance_analysis (clf):
    plt.figure(figsize=(8,5))
    plt.scatter(y_train, clf.predict(X_train), label='Model')
    plt.scatter(y_test, clf.predict(X_test), label='Actual' )
    plt.title('Model vs Data for Training Set')
    plt.legend()
    plt.show()
    print('Base Scores:')
    base_train= (mean_squared_error(y_train, clf.predict(X_train))*100).round(2)
    base_test=(mean_squared_error(y_test, clf.predict(X_test))*100).round(2)
    print('train set:', base_train, '%', 'test set:', base_test, '%')
    train_score=(clf.score(X_train, y_train)*100).round(2)
    test_score=(clf.score(X_test, y_test)*100).round(2)
    print('Model Performance:')
    print('train score:',train_score ,'%', 'test score:',test_score , '%')
