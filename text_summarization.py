
# coding: utf-8

# In[202]:

import nltk
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest


# In[203]:

class TextSummary:
    def __init__(self, min_freq = 0.2, max_freq = 0.8):
        self.min_freq = min_freq
        self.max_freq = max_freq
        self._stopwords = set(stopwords.words('english') + list(punctuation))
        
    def find_frequency(self,wordlist):
        freq_words = nltk.FreqDist(wordlist)
        my_new_dict = {}
        maximum_freq = max(freq_words.values())
        for key,value in freq_words.items():
            freq_ratio = value/maximum_freq
            if(freq_ratio > self.min_freq or freq_ratio < self.max_freq):
                my_new_dict[key] = freq_ratio
        return my_new_dict
       
    def summarize(self, document, n):
        share_sent = 'Share this with Email Facebook Messenger Messenger Twitter Pinterest WhatsApp LinkedIn Copy this link These are external links and will open in a new window'
        document = document.replace(share_sent, '')
        sent_tokens = sent_tokenize(document)
        word_sent = [word_tokenize(s.lower()) for s in sent_tokens]
        word_sent = sum(word_sent, [])
        #print(word_sent)
        frequencies_dict = self.find_frequency(word_sent)
        sentence_ranks = {}
        for i, sent in enumerate(sent_tokens):
            word_tokens = word_tokenize(sent.lower())
            freq_count = 0
            for word in word_tokens:
                freq = frequencies_dict[word]
                freq_count+=freq
            sentence_ranks[sent]=freq_count
        # Logic to select the best 2 sentence
        return nlargest(n, sentence_ranks, key=sentence_ranks.get)
        
  
    
    


# In[204]:

import requests
from bs4 import BeautifulSoup


# In[205]:

response = requests.get('http://feeds.bbci.co.uk/news/rss.xml')
soup = BeautifulSoup(response.content, 'lxml')


# In[206]:

soup.findAll('guid')


# In[207]:

to_summarize = list(map(lambda p: p.text, feed.find_all('guid')))


# In[208]:

print("Please enter the number of articles ")
n = int(input())


# In[209]:

# Fetch 5 articles

summarize_n = to_summarize[:n]

summarize_n


# In[210]:

def get_only_text(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'lxml')
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return soup.title.text, text


# In[211]:

ts = TextSummary()


# In[212]:


for article_url in summarize_n:
    title, text = get_only_text(article_url)
    print(title)
    print(ts.summarize(text, 3))


# In[ ]:

get_ipython().system('jupyter nbconve')


# In[ ]:



