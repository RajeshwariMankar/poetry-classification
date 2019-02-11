#declaration of beautifulsoup
from bs4 import BeautifulSoup
#taking function stopwords ,wordnet and CategorizedPlaintextcorpusReader declaration
from nltk.corpus import wordnet, CategorizedPlaintextCorpusReader, stopwords
#import of nltk,request,os.path,sys,re
import requests
import nltk
import os.path
import sys,re

#nine types of emotions represent poems emotion
emotion_of_poems =['love', 'joy','peace', 'sad', 'fear','hate']

#base directory name
basepath = os.path.dirname(os.path.realpath(__file__))
print(basepath)
directory="poems"
poemdirectory="../"+directory
if not os.path.exists(poemdirectory):
    os.makedirs(poemdirectory)


url = 'http://www.poemhunter.com'
topic_directory = '/poem-topics/'
topic_complete_url=url+topic_directory
print(topic_complete_url)
topic_page_request=requests.get(topic_complete_url)
print(topic_page_request)
#code for searching poems_topic page
search_topic_page=BeautifulSoup(topic_page_request.content,'html.parser')
    
#finding of the list of all poems topics
topic_elements_second=search_topic_page.find('ul',class_= 'subjectsMain-list')
count=0
#code for finding out the topic_element list elements
poem_topic_list=[]
for list_ele in  topic_elements_second.find_all('li'):
    #poems_topic=list_ele.a.get_text().strip().encode('utf-8')
    poems_topic=list_ele.a.get_text().strip()
    poem_topic_list.append(poems_topic)
    print(poems_topic)    
    
print(poem_topic_list)
    
#code for removing elements not present in the poems topic
emotions=[]
for e in emotion_of_poems:
    for synset in wordnet.synsets(e):
        for lemma in synset.lemmas():
            #if lemma.name() in poem_topic_list:
            emotions.append((lemma.name(),e))
    

print("BEFORE")
print(emotions)
print(len(emotions))
emotions_perfect=set(emotions)
emotion_poems=list(emotions_perfect)
print("AFTER")
print(emotion_poems)
print(len(emotion_poems))
after_union=set().union(emotion_of_poems,emotion_poems)
print(after_union)
