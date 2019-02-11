import sys
import nltk
import glob
from nltk.corpus import stopwords
import os
from os.path import basename
from nltk.corpus import wordnet as wordn
import os.path
import sys
import re
from nltk.tokenize import RegexpTokenizer
import operator
from collections import Counter
from itertools import chain
from collections import defaultdict
from collections import OrderedDict
from nltk.tokenize import RegexpTokenizer


#search function implementation
def search(token):
    path="../keywordsfile/*.txt"
    files=glob.glob(path)
    count=0
    token_found=False
    tag_list_name=[]
    token_tag={}
    for file_name in files:
        with open(file_name,'r') as f:
            #each_emotion_text=f.read()
            each_emotion_text=[word for line in f for word in line.split()]
            for eachemotion in each_emotion_text:
                file1=basename(file_name)
                file2=str(os.path.splitext(file1)[0])
                #tag_list_name=token+"_"+file2
                if eachemotion==token :
                    tag_list_name.append(file2)
                    # print(tag_list_name[count])
                    #token_found=token+"_"+"found"
                    token_found=True
                    count=count+1
                    token_tag[token]=file2

    return tag_list_name,token_found 

#alogrithm for insertion of elements which are not present in the corpus to add it to the corpus
def insert(token,tag):
    print("inside of the insert function")
    emotion_list =['love', 'joy','peace', 'sad','fear','hate']
    if(tag in emotion_list):
        path="../keywordsfile/"+str(tag)+".txt"
        print(path)
        with open(path, "a") as myfile:
             string=token+"\n"
             print("string",string)
             myfile.write(string)
             
        
#algorithm second which is the main algorithm of this project
#code for finding tokens in the given poem
emotion_list =['love', 'joy','peace', 'sad','fear','hate']

file_content = open("poem.txt").read()
#list of the tokens present in the poem list
tokenizer = RegexpTokenizer("[\w']+")
tokens = tokenizer.tokenize(file_content)
print(tokens)

#negative words list
negation={"aren't":"are not",
"can't":"cannot",
"can't":"can not",
"couldn't":"could not",
"daren't":"dare not",
"didn't":"did not",
"doesn't":"does not",
"don't":"do not",
"hasn't":"has not",
"haven't":"have not",
"hadn't":"had not",
"isn't":"is not",
"mayn't":"may not",
"mightn't":"might not",
"mustn't":"must not",
"needn't":"need not",
"oughtn't":"ought not",
"shan't":"shall not",
"shouldn't":"should not",
"wasn't":"was not",
"weren't":"were not",
"won't":"will not",
"wouldn't":"would not"}


#code for stopwords list creation
stopwords=[]
with open('../requiredfiles/stopword.txt') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
stopwords = [x.strip() for x in content] 
print(stopwords)

tokens=[t.lower() for t in tokens]
#for making tokens lowercase
realtokens=[]
for t in tokens:
        if t not in stopwords:
            realtokens.append(t)

print(realtokens)



trackoftoken_emotion=[]
for each_token in realtokens:
    tag_list_name,token_found=search(each_token)
    #code for executing 5.2 section of algorithm number second
    if token_found==False:
        for key_neg in negation:
            if key_neg==each_token:
                realword=negation[key_neg]
                next_word_index=tokens.index(each_token)
                next_word=tokens[next_word_index+1]
                q,token_found=search(next_word)
                token_found=True
                antonyms=[]
                for synset in wordn.synsets(q[0]):
                    for lemma in synset.lemmas():
                        if(lemma.antonyms()):
                            opposite_emotion=lemma.antonyms()[0].name()
                tag_list_name.append(opposite_emotion)
                realtokens.remove(each_token)
                break

        if token_found==False:
                    #synonym=[]
                countof_synonyms=len(wordn.synsets(each_token))
                print(countof_synonyms)
                lemma_count=0
                count=0
                if countof_synonyms==0:
                        print("cccc")
                        break
                else:        
                    for synset in wordn.synsets(each_token):
                        print("entry in synset")
                        for lemma in synset.lemmas():
                            print("entry in lemma")
                            lemma_count=lemma_count+len(synset.lemmas())
                            synonym=lemma.name()
                            print("ssss ",synonym)
                            q,token_found=search(synonym)
                            print("q ",q)
                            print("token_found ",token_found)
                            if token_found==False and len(q)==0:
                               count=count+1
                               print("count ",count)
                            else: 
                               tag_name=''.join(q)
                               print("else tag_list_name",tag_name)   
                               insert(each_token,tag_name)
                               tag_list_name.append(tag_name)
                               
                            total_count=lemma_count*countof_synonyms
                            if count==total_count:
                                break
                elemnet={each_token:tag_list_name}
                trackoftoken_emotion.append(elemnet.copy())     

##algorithm for addding 6 to 9 lines present int he algorithm
#execution of line number from  6 to 9
#{
#for key_1 in trackoftoken_emotion:
 #  for em in trackoftoken_emotion[key_1]:
       #P(word/t.tag)
       #likehood probability
 #      word=len(key_1)
  #     tag_length=len(trackoftoken_emotion[key_1])
   #    likehood_Prob=float(word/tag_length)

       #class prior probablity
    #   class_prior_prob=float(len(em)/tag_length)

       #predictor prior probability
     #  predictor_prior=float(word/len(trackoftoken_emotion))

       #prob[tag/word]
       #Prob_tag_word=
      # Prob_tag_word=(likehood_Prob*class_prior_prob)/predictor_prior
# }

##dict_count_track={}
##for keys in list(trackoftoken_emotion.keys()):
  ##  if trackoftoken_emotion[keys] == []:
    ##    del trackoftoken_emotion[keys]




print(trackoftoken_emotion)

dictionary = {}
for d in trackoftoken_emotion:
    # (assumes just one key/value per dict)
    ((x, y),) = d.items() 
    dictionary.setdefault(x, []).append(y)

print(dictionary)


for key,value in dictionary.items():
    length_val=len(dictionary[key])
    if len(length_val)==0:
        removable=dictionary[key]
        del removable
print("dictionary11111",dictionary)
for k,v in dictionary.items():
    new_val=[]
    for value in v:
        new_val=new_val+value
        dictionary[k]=new_val

print(dictionary)


dict_count_track={}
for keys in list(dictionary.keys()):
    if dictionary[keys] == []:
        del dictionary[keys]

print(dictionary)
#code for each token present in T
for k,v in dictionary.items():
    new_val=[]
    for value in v:
        new_val=new_val+value
        dictionary[k]=new_val

print(dictionary)

unique_items = set(x for y in dictionary.values() for x in y)
print(unique_items)
dict_count_track={}
for item in unique_items:
    dict_count_track[item] = {k: v.count(item) for k, v in dictionary.items()}

print(dict_count_track)

count_track={}
for key,value in dict_count_track.items():  
    print(key," ", sum(value.values()))
    count_track.update({key:sum(value.values())})

print(count_track)


max_emotion=max(int(d['countALL']) for d in dict_count_track.values())
#maximum=max(dict_count_track.items(), key=operator.itemgetter(1))[0]
#max_emotion=dict_count_track[maximum]

print("SO MAXIMUM EMOTION IS  "+str(max_emotion))
#print(max((dict_count_track[k] for k in dict_count_track) ,key=dict_count_track.get))
for k,v in dict_count_track.items():
    for key in v :
        if(v["countALL"]==max_emotion):
            if k in emotion_list:
               print(k)
               break
            else:
                print("Other emotion")
                break
        else:
            break
    
