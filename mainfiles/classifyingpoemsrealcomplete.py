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
from nltk.tokenize import RegexpTokenizer
import random
import pickle
from nltk import word_tokenize, pos_tag

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

def determine_tense_input(sentance):
    text = word_tokenize(sentance)
    tagged = pos_tag(text)

    tense = {}
    tense["future"] = len([word for word in tagged if word[1] == "MD"])
    tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
    tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]]) 
    return(tense)

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


#insertion of the token in the list
def insert(token,tag):
    if tag in emotion_of_poems:
        path="keywordsfile/"+str(tag)+".txt"
        print(token)
        token="\n"+token
        with open(path, 'a') as file:
              file.write(token)

def remove(l):
    tuple(filter(lambda x:not isinstance(x, (str, list, tuple)) or x, (remove(x) if isinstance(x, (tuple, list)) else x for x in l)))


#feature extraction from poem
def features_of_poem(file_input):
    print("filename :",file_input)
    if ".txt" not in file_input:
        filename="poems/"+str(file_input)
        file_content = open(filename,"r").read()
    else:
        file_content = open(file_input,"r").read()  


    tokenizer = RegexpTokenizer("[\w']+")
    tokens = tokenizer.tokenize(file_content)  

    stopwords=[]
    with open('requiredfiles/stopword.txt') as f: 
        content = f.readlines()

    stopwords = [x.strip() for x in content]

    tokens=[t.lower() for t in tokens]


#code for extracting real tokens which not contain any stopwords
    realtokens=[]
    for t in tokens:
        if t not in stopwords:
            realtokens.append(t)
    print(realtokens)
#code for keeping tract of each word and its emotion
    trackoftoken_emotion=[]
    length_realtokens=len(realtokens)
    for each_token in realtokens:
        tag_list_name,token_found=search(each_token)
        if token_found==False:
            tense=""
            tense_check=value=determine_tense_input(each_token)
            print(determine_tense_input(each_token))
            for key,value in tense_check.items():
	            if value==1:
	                tense=key
	                print(key)

            if tense=="past":
                    for synset in wordn.synsets(each_token):
                        for lemma in synset.lemmas():
                            if(lemma.antonyms()):
                                opposite_em=lemma.antonyms()[0].name()
                                print(opposite_em)
                                tag_list_name.append(opposite_em)

            for key_neg in negation:
                if key_neg==each_token:
                    next_word_index=realtokens.index(each_token)
                    next_position=length_realtokens-1
                    #if(next_word_index==-1 or next_word_index==next_position):
                    if(next_word_index==-1 or next_word_index==next_position or realtokens[-1]==each_token):
                        break
                    else:
                        next_word=realtokens[next_word_index+1]
                        position=realtokens.index(next_word)
                    q,token_found=search(next_word)
                    string=''.join(q)
                    if token_found==False:
                        if len(q)==0:
                            continue
                    
                    if token_found==True:
                        for synset in  wordn.synsets(string):
                            for lemma in synset.lemmas():
                                if(lemma.antonyms()):
                                    opposite_emotion=lemma.antonyms()[0].name()
                                    tag_list_name.append(opposite_emotion)
                        print(next_word)            
                        if(next_word):
                            print("next_word :",realtokens[position])
                            word_to_remove=realtokens[position]
                            realtokens.remove(word_to_remove)
                            break

                    else:
                        break
            
            if token_found==False:
                countof_synonyms=len(wordn.synsets(each_token))
                if countof_synonyms==0:
                    continue
                else:
                    synonyms=[]
                    for synset in wordn.synsets(each_token):
                        for lemma in synset.lemmas():
                            each_lemma=lemma.name()
                            synonyms.append(each_lemma)
                    
                    lengthofsynset=len(synonyms)
                    count=0
                    for each_syn in synonyms:
                        q,token_found=search(each_syn)
                        if token_found==False and len(q)==0:
                            count=count+1
                        else:
                            tag_name=''.join(q[0])
                            path="keywordsfile/"+str(tag_name)+".txt"
                            if each_token not in open(path,'r').read():
                                if tag_name in emotion_of_poems:
                                    tag_list_name.append(tag_name)
                                    insert(each_token,tag_name)
                                
                            else:
                                continue

                        if count==lengthofsynset:
                            break

        element={each_token:tag_list_name}
        trackoftoken_emotion.append(element.copy())  
    print(trackoftoken_emotion)
    dictionary = {}
    for d in trackoftoken_emotion:
        ((x, y),) = d.items()  
        dictionary.setdefault(x, []).append(y)
        
    print(dictionary)

    #for removing empty list
    for key,value in dictionary.items():
        each_value=dictionary[key]
        remove(each_value)


    for k,v in dictionary.items():
        new_val=[]
        for value in v:
            new_val=new_val+value
            dictionary[k]=new_val

    unique_items = set(x for y in dictionary.values() for x in y)

    dict_count_track={}
    for item in unique_items:
        dict_count_track[item] = {k: v.count(item) for k, v in dictionary.items()}

    print(dict_count_track)

    
    count_track={}
    for key,value in dict_count_track.items(): 
        count_track.update({key:sum(value.values())})
    
    print("counter track",count_track)

    max_value = max(count_track.values()) 
    print(max_value)
    bottom_conditional=sum(count_track.values())

    for k,v in count_track.items():
        if k in emotion_of_poems and v==max_value: 
            emotion=k
            print(emotion)
            emotion_correct={"emotion":emotion}
            return  emotion_correct
            break
       
    return emotion_correct
    


def classify(poem_text):
    return classifier.classify(features_of_poem(poem_text))

corpus_of_poems = CategorizedPlaintextCorpusReader('poems/', 'poems.*',
        cat_file='cats.txt')


#code for generating errors
# Return errors in order to improve algorithm
def errors_em(poem_set):
    errors = []
    for (fileid, category) in poem_set:
        poem = corpus_of_poems.words(fileids=[fileid])
        emotion_correct = features_of_poem(poem)
        guess = classifier.classify(features_of_poem(poem))

        if guess != category:
            errors.append((category, guess, poem,emotion_correct['emotions']))

    return errors

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

train_set=feature_set[25:]

test_set =feature_set[:25]

print("Trainset")
print(train_set)

print("Testset")
print(test_set)


print("classifier\n")
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(sorted(classifier.labels()))

print(nltk.classify.accuracy(classifier, test_set)) 

print("improveing\n")
print(classifier.show_most_informative_features(20))

save_classifier = open('my_classifier.pickle', 'wb')
pickle.dump(classifier,save_classifier)
save_classifier.close()

