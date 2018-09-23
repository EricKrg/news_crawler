##################################################################################
# Name: sentiment analysis.py
# Author: Jonas Gütter
# Description: Perform sentiment analysis on data fetched by the News Crawler using 
# the bag-of-words model and the SentiWordNet lexicon 
##################################################################################

import pandas as pd
import numpy as np
import re
import scipy.stats as ss
import matplotlib.pyplot as plt
from collections import Counter
import plotly.plotly as py
import plotly.tools as tls

#%%Prepare lexicon
# downloaded September 2018 from http://sentiwordnet.isti.cnr.it/
# Load data
lexicon = pd.read_table('SentiWordNet_3.0.0_20130122.txt',sep='\t', header = 26)
lexicon = lexicon.iloc[0:117659,:]
# clean up words TODO: Instead of deleting surplus words in one row, create new rows for them
lexicon.SynsetTerms = [re.sub('#[abcdefghijklmnopqrstuvwxyz1234567890_ ]*','',word) for word in lexicon.SynsetTerms]
                
#%%  Get news articles

articles = pd.read_csv('example_articles.csv',sep='\t', header=None,names=['ID','source','title','content'], index_col = 0, skiprows = 1)                              
                              
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

#%% Sort data and calculate rank
articles['sentiment_score'] = sentiment_score
articles['sentiment_rank'] = ss.rankdata(sentiment_score * (-1))
articles = articles.sort_values(by = 'sentiment_rank')

#%% Visualize data 

articles_aj = articles[articles.source == 'AJ']
articles_bbc = articles[articles.source == 'BBC']
articles_rt = articles[articles.source == 'RT']


occurrences = Counter(articles.sentiment_score)
occurrences_aj_ref = Counter(articles_aj.sentiment_score)
occurrences_bbc_ref = Counter(articles_bbc.sentiment_score)
occurrences_rt_ref = Counter(articles_rt.sentiment_score)

occurrences_aj =  {}
occurrences_bbc = {}
occurrences_rt = {}

# Create dicts for each source. It's necessary that each dict has the same keys in the same order
for element in occurrences:
    if(element not in occurrences_aj_ref):
        occurrences_aj[element] = 0
    else:
        occurrences_aj[element] = occurrences_aj_ref[element]
    if(element not in occurrences_bbc_ref):
        occurrences_bbc[element] = 0
    else:
        occurrences_bbc[element] = occurrences_bbc_ref[element]
    if(element not in occurrences_rt_ref):
        occurrences_rt[element] = 0
    else:
        occurrences_rt[element] = occurrences_rt_ref[element]



width = 0.1
p1 = plt.bar(occurrences_aj.keys(), list(occurrences_aj.values()), width, color= 'blue')
p2 = plt.bar(occurrences_bbc.keys(), list(occurrences_bbc.values()), width, color="red", bottom = list(occurrences_aj.values()))
p3 = plt.bar(occurrences_rt.keys(), list(occurrences_rt.values()), width, color="green", bottom = [sum(x) for x in zip(list(occurrences_aj.values()), list(occurrences_bbc.values()))])

plt.ylabel('Frequencies')
plt.xlabel('Sentiment Scores')
plt.legend((p1[0], p2[0], p3[0]), ('Al Jazeera', 'BBC', 'Russia Today'))

plt.show()
#fig = plt.gcf()
#plotly_fig = tls.mpl_to_plotly(fig)
#py.iplot(plotly_fig, filename='basic-barchart')    