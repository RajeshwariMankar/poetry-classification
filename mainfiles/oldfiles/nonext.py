#declaration of beautifulsoup
from bs4 import BeautifulSoup

#taking function stopwords ,wordnet and CategorizedPlaintextcorpusReader declaration
from nltk.corpus import wordnet, CategorizedPlaintextCorpusReader, stopwords

#import of nltk,request,os.path,sys,re
import requests
import nltk
import os.path
import sys,re
from urllib.parse import urlparse



#nine types of emotions represent poems emotion
emotion_of_poems =['love', 'joy','peace', 'sad', 'fear','hate']

#emotion_of_poems = ['joy']

#base directory name
basepath = os.path.dirname(os.path.realpath(__file__))
print(basepath)
directory="poems"
poemdirectory="../"+directory
if not os.path.exists(poemdirectory):
    os.makedirs(poemdirectory)
   

#emotions list
emotions=[]
#Search in direct synonyms as well as the words themselves
for e in emotion_of_poems:
    for synset in wordnet.synsets(e):
        for lemma in synset.lemmas():
           emotions.append((lemma.name(),e))

print("BEFORE")
print(emotions)
print(len(emotions))
emotions_perfect=set(emotions)
emotion_of_poems=list(emotions_perfect)
print("AFTER")
print(emotion_of_poems)
print(len(emotion_of_poems))

#Use of poemhunter website for scrayping a poems data using requests and beautifulsoup for Creation of files for making dataset/corpus of poems
def create_poem_entry():
    url = 'http://www.poemhunter.com'
    searchdir = '/poems/'
    id_of_poem= 0
    category_file = open('../poems/cats.txt', 'a')
    # Search for each emotion
    for (sentiment, emotion) in emotion_of_poems:
        sent=sentiment+"/"
        #request for obtaining url
        complete_url=url+searchdir+sent
        page_request=requests.get(complete_url)
        first_url=str(complete_url)
        checking=str(page_request.url)
        print(first_url)
        print(checking) 
        a_url = urlparse(first_url)
        b_url = urlparse(checking) 
        match = a_url.netloc == b_url.netloc
        print(match)
        if match:
            print("true")
            #page_request=requests.get(complete_url)
            #request for obtaining html page of requested url using beautifulsoup
            search_page=BeautifulSoup(page_request.content,'html.parser')
            
            # Main scraping loop
            #finding of a list of poems on a perticular emotion page
            elements=search_page.find('ol',class_='rpoems-list')

                # Find of individual poem of perticular emotion
            for lise_ele in  elements.find_all('li'):
                    #for accessing title of the poem
                    title_of_poem = lise_ele.a.get_text().strip()
                    #for accessing link of the poem text 
                    link = lise_ele.a['href']
                    print(link)

                    #for accessing a url of a perticular poem
                    secondlink=requests.get(url + link)

                    #request for obtaining html page of requested url using beautifulsoup
                    poem_page = BeautifulSoup(secondlink.content,'html.parser')

                    #for finding poem text
                    poem_body = poem_page.find('div', class_='KonaBody').find('p')

                    #poemid for identifying perticular poem
                    filename = 'poems_' + str(id_of_poem)
                    print(filename)

                    #for storing that file into nltk_data and in corpus
                    poemfile_name = open('../poems/' + filename, 'a')
                    print(title_of_poem.upper())

                    #for writing poem text into the perticular file of poem id
                    poemfile_name.write(title_of_poem.upper() + str('\n\n'))

                    #for each string present in the poem body text
                    for s in poem_body.strings:

                        #for removing repeatable or <br> text in the poem text if any present
                        s = re.sub('(.*)<\s*br\s*>(.*)', '\1\2', s)

                        #for removing the "copyright" named text and also year if any present with copyright symbol
                        #ignore_line = r'(?:^|\W)(?:[Cc]opyright|\\xa9|[0-9]+)(?:\W|$)'
                        ignore_line = r'(?:^|\W)(?:[Cc]opyright|\\xa9)(?:\W|$)'
                        if re.sub(ignore_line, '', s) != s:
                            continue

                        # for removing any duplicate words present at the bottom of the poem text 
                        duplicate_line_removing = r'(?: |^)([^ ]*)( \1){2,}(?= |$)'
                        if re.sub(duplicate_line_removing, '', s) != s:
                            continue
                        print(s.strip())

                        #after removing all above writing the poem text in a file of perticular poem id
                        poemfile_name.write(s.strip() + '\n')

                    #for storing poemid and its emotion category in catagory file
                    category_file.write(filename + ' ' + emotion + '\n')

                    #closing of the file of perticular id
                    poemfile_name.close()

                    id_of_poem+= 1

            #if there any next page present on the html page 
            #nextpage1=search_page.find('div',class_='paginationANP')
            #if nextpage1:     
                #next_page = nextpage1.find('li',class_= 'next')
                #if next_page:
                        #request for obtaining url
                    #linkthird=requests.get(url+next_page.a['href'])
               
                        #request for obtaining html page of requested url using beautifulsoup
                    #search_page = BeautifulSoup(linkthird.content,'html.parser')
                #else:
                    #break

        #close category_file after completion of its work
    category_file.close()
    print(id_of_poem)


# create vocabularies for each emotion
def create_corpus():
    poem_corpus = CategorizedPlaintextCorpusReader('../poems/', 
    'poems_.*',cat_file='cats.txt') 

if __name__ == '__main__':
    create_poem_entry()
    create_corpus()