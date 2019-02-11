from nltk.corpus import CategorizedPlaintextCorpusReader
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
import random
import pickle

emotion_of_poems =['love', 'joy','peace', 'sad', 'fear','hate']


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


#search function implementation
def search(token):
    path="keywordsfile/*.txt"
    files=glob.glob(path)
    count=0
    token_found=False
    tag_list_name=[]
    token_tag={}
    for file_name in files:
        with open(file_name,'r') as f:
            #each_emotion_text=f.read()
            each_emotion_text=[word for line in f for word in line.split()]
            eachtext=set(each_emotion_text)
            each_emotion_text=list(eachtext)
            
            for eachemotion in each_emotion_text:
                file1=basename(file_name)
                file2=str(os.path.splitext(file1)[0])
                #tag_list_name=token+"_"+file2
                if eachemotion==token :
                    tag_list_name.append(file2)
                    #print(tag_list_name[count])
                    token_found=token+"_"+"found"
                    token_found=True
                    count=count+1
                    token_tag[token]=file2
                    #print(tag_list_name,token_found)
    return tag_list_name,token_found

def insert(token,tag):
    if tag in emotion_of_poems:
        path="keywordsfile/"+str(tag)+".txt"
        token=token+"\n"
        print(path)
        with open(path, "a") as myfile:
             myfile.write(token)


def features_of_poem(file_input):

        print("filename :",file_input)
        if ".txt" not in file_input:
           filename="poems/"+str(file_input)
           file_content = open(filename,"r").read()
        else:
           #filename="uploadfiles/"+file_input
           file_content = open(file_input,"r").read()
      #list of the tokens present in the poem list
        tokenizer = RegexpTokenizer("[\w']+")
        tokens = tokenizer.tokenize(file_content)
        #print("tokens",tokens)
      #code for stopwords list creation
        stopwords=[]
        with open('requiredfiles/stopword.txt') as f:
           content = f.readlines()
      # you may also want to remove whitespace characters like `\n` at the end of each line
        stopwords = [x.strip() for x in content]
        #print("stopwords",stopwords)

        tokens=[t.lower() for t in tokens]
        #for making tokens lowercase
        realtokens=[]
        for t in tokens:
              if t not in stopwords:
                  realtokens.append(t)

        #print("real tokens:",realtokens)


  
        trackoftoken_emotion=[]
        for each_token in realtokens:
            tag_list_name,token_found=search(each_token)
            #code for executing 5.2 section of algorithm number second
            if token_found==False:
                for key_neg in negation:
                    if key_neg==each_token:
                       realword=negation[key_neg]
                       next_word_index=tokens.index(each_token)
                       if(next_word_index==-1):
                            break
                       else:
                            next_word=tokens[next_word_index+1]
                       q,token_found=search(next_word)
                       print("each_token",each_token)
                       print("next_word",next_word)
                       print("qqqqqq\n",q)
                       print("token_found",token_found)
                       #token_found=True
                       string=''.join(q)
                       print(string)
                       antonyms=[]
                       if token_found==False:
                           if len(q)==0:
                               continue
                           if realtokens.index(next_word)==-1:
                               break
                       if token_found==True and string:
                          for synset in  wordn.synsets(string):
                               for lemma in synset.lemmas():
                                   if(lemma.antonyms()):
                                       opposite_emotion=lemma.antonyms()[0].name()
                                       print("opposite emotion :",opposite_emotion)
                          tag_list_name.append(opposite_emotion)
                          print(each_token)
                          realtokens.remove(next_word)
                          break
                       else:
                          break
                if token_found==False:
                  countof_synonyms=len(wordn.synsets(each_token))
                  lemma_count=0
                  count=0
                  if countof_synonyms==0:
                     continue 
                  else:
                    for synset in wordn.synsets(each_token):
                        for lemma in synset.lemmas():
                            lemma_count=lemma_count+len(synset.lemmas())
                            synonym=lemma.name()
                            q,token_found=search(synonym)
                            if token_found==False and len(q)==0:
                               count=count+1
                            else: 
                               tag_name=q[0]
                               print(tag_name)
                               tag_list_name.append(tag_name)
                               insert(each_token,tag_list_name)
                               continue
                            total_count=lemma_count*countof_synonyms
                            if count==total_count:
                                break
            elemnet={each_token:tag_list_name}
            trackoftoken_emotion.append(elemnet.copy())     
        print(trackoftoken_emotion)

        dictionary = {}
        for d in trackoftoken_emotion:
             
                ((x, y),) = d.items() 
                dictionary.setdefault(x, []).append(y)
        print("\n\ndictionary ",dictionary)

        for k,v in dictionary.items():
              new_val=[]
              for value in v:
                if(len(value)==1 or len(value)==0):
                     new_val=new_val+value
                     dictionary[k]=new_val
                     print(dictionary)
                else:
                    for single in value:
                        new_val=new_val+single
                        dictionary[k]=new_val

        print("\\ndictionary 2",dictionary)

        unique_items = set(x for y in dictionary.values() for x in y)
     
        dict_count_track={}
        for item in unique_items:
               dict_count_track[item] = {k: v.count(item) for k, v in dictionary.items()}
       
        count_track={}
        for key,value in dict_count_track.items():  
               count_track.update({key:sum(value.values())})

    

        max_value = max(count_track.values()) 
        print(max_value)
        bottom_conditional=sum(count_track.values())
      
        for k,v in count_track.items():
            if k in emotion_of_poems: 
                if v==max_value:
                    emotion=k
                    emotion_correct={"emotion":emotion}
                    print(emotion)
                    break
            else:
                emotion="Other Poem"
                break
        
        emotion="hate"
        bottom=len(emotion_of_poems)
        top=len(list(emotion))
        prior_probability=float(top/bottom)
        print(prior_probability)

        conditional_probability=float(max_value/bottom_conditional)
        print(conditional_probability)

        evidience=len(realtokens)

        posterior_probability=(prior_probability*conditional_probability)/5
        print("posttt",float(posterior_probability))
        
        return  emotion_correct

def classify(poem_text):
    return classifier.classify(features_of_poem(poem_text))

corpus_of_poems = CategorizedPlaintextCorpusReader('poems/', 'poems.*',
        cat_file='cats.txt')


poem_set=[]
for fileid in corpus_of_poems.fileids():
   for category in corpus_of_poems.categories(fileid):
       poem_set.append((fileid,category))

print(poem_set)

random.shuffle(poem_set)

feature_set=[]
for (fileid,category) in poem_set:
    feature_cal=(features_of_poem(fileid),category)
    feature_set.append(feature_cal)

train_set=feature_set[5:]

test_set =feature_set[:5]

print("Trainset")
print(train_set)

print("Testset")
print(test_set)


print("classifier\n")
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(sorted(classifier.labels()))

print(nltk.classify.accuracy(classifier, test_set)) 

print("improveing\n")
print(classifier.show_most_informative_features(10))

save_classifier = open('my_classifier.pickle', 'wb')
pickle.dump(classifier,save_classifier)
save_classifier.close()
