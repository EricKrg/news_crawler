##################################################################################
# Name: sentiment analysis.py
# Author: Jonas Gütter
# Description: Perform sentiment analysis on data fetched by the News Crawler using 
# the bag-of-words model and the SentiWordNet lexicon 
##################################################################################

import pandas as pd
import numpy as np
import re


#%%Prepare lexicon
# downloaded September 2018 from http://sentiwordnet.isti.cnr.it/
# Load data
lexicon = pd.read_table('SentiWordNet_3.0.0_20130122.txt',sep='\t', header = 26)
lexicon = lexicon.iloc[0:117659,:]
# clean up words TODO: Instead of deleting surplus words in one row, create new rows for them
lexicon.SynsetTerms = [re.sub('#[abcdefghijklmnopqrstuvwxyz1234567890_ ]*','',word) for word in lexicon.SynsetTerms]
                
#%%  Get news articles

articles = pd.read_csv('news_articles.csv',sep=',', header=None,names=['ID','source','content'], index_col = 0, skiprows = 1)                              
                              
#%% Create corpus

# base corpus consists of al words in the lexicon
corpus = lexicon.iloc[:,2:5]
corpus.columns = ['PosScore', 'NegScore','Term']
# if a word in an article does not appear in the corpus, append it to the corpus 
# and assume that PosScore and NegScore are 0
for article in articles.content:
    word_count = 0
    word_count_not_in_corpus = 0
    for word in article.split():
        word_count += 1
        if not (word in corpus.Term.unique()):
            corpus = corpus.append({'PosScore':0, 'NegScore':0, 'Term':word}, ignore_index=True)
            word_count_not_in_corpus += 1
    print('ratio of unknown words: ',word_count_not_in_corpus/word_count)


#%% Encode articles in bag-of-words-model
    
articles_encoded = np.zeros((len(corpus),len(articles)))

for column,article in enumerate(articles.content):
    for word in article.split():
        word_position_in_corpus = corpus.Term[corpus.Term == word].index[0]
        articles_encoded[word_position_in_corpus,column] += 1

#%% Calculate sentiment by summing all negative and positive scores of an article
        
sentiment_score = np.inner(np.transpose(articles_encoded),corpus.PosScore)   -  np.inner(np.transpose(articles_encoded),corpus.NegScore)

#%%

# TODO: Titel dazunehmen
# Rang bestimmen
# Balkendiagramm erstellen    