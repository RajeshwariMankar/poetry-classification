# poetry-classification
This project tries to give the emotion category associated with the poem. It is based on automatic emotion recognition from poems written in English using Natural Language Processing (NLP) where the poem is given as input and the result is emotion associated with the given poem. Here, we try to categorize poems only in 6 emotions: Joy, Peace, Love, Sad, Hate and Fear.

## Requirements:
  - Python 3.x
  - NLTK
  - Beautiful Soup(bs4)
  - Flask
  - SKLearn

## Dataset:
We have created our own corpus by fetching data from https://www.poemhunter.com/ using web scraping.

## Execution:

Run app.py file which is responsible for training of a poem dataset and also runs flask application. After training of dataset,open localhost: 5000 in browser.Now give an input either by inserting a title of a poem and content of a poem or by uploading a file having a poem. After submitting,the emotion category of poem is displayed.The below figure represents the uploaded text file of poem.<br><br>


<p align="center">
  <img width="750" height="380" src="https://github.com/keshab97/poetry-classification/blob/master/Images/Test%20result%20of%20joy.png" title='Test result of poem category (Joy)'>
<p align="center">Test result of poem category (Joy)</p>
 
##### The following is a process executed when we input a poem for extracting emotion category of poem :
- True casing is implemented on poem to determine the proper capitalization of words.After that , tokenization is done as shown  below.
<p align="center">
  <img width="750" height="280" src="https://github.com/keshab97/poetry-classification/blob/master/Images/Tokenization.png" title='Tokenization'<br>
<p align="center">Tokenization</p><br>
<p Here, a stream of text is broken up into tokens/words. These tokens are stored in a list.</p></p>
 
- Each token is then assigned with one particular parts of speech tag.Tagging before stopwords removal is useful in getting actual meaning of the word. Thus, first, part of speech tag of each token is found and that tags are maintained in list having same index as that of their corresponding token. The below figure shows tag of corresponding tokens.
<p align="center">
  <img width="750" height="280" src="https://github.com/keshab97/poetry-classification/blob/master/Images/Tagging.png" title='Tagging'>
<p align="center">Tagging</p><br>

- A list of dictionaries is maintained as a key value part , where tokens are termed as key and value is list containing a part   of speech associated with that particular token.A list is maintained to store these dictionaries. Unique dictionary is created
because poem may contain same word repetitively and postag associated with each token can be different for the same word. Thus, dictionary for each token is created. <p align="center">
  <img width="750" height="280" src="https://github.com/keshab97/poetry-classification/blob/master/Images/POS%20tag%20tracking%20list.png" title='POS Tag tracking list'><p align="center">POS Tag tracking list</p><br>
 
- After tokenization, tokens present in stopwords list are removed. Thus, a list of tokens free from stopwords are obtained as shown in given figure.<p align="center">
  <img width="750" height="280" src="https://github.com/keshab97/poetry-classification/blob/master/Images/Pure%20Tokens.png"  title='Pure tokens'><p align="center">Pure tokens</p><br>

- After removing stopwords from token list, dictionaries whose key is present as an element in stopwords list are removed. Thus,     a list is obtained having a key having no stopwords as shown in given below figure. A list of dictionaries are maintained as a key value part, where token sare termed as key and value is updated as first value, the parts of speech and second, the index value of a token.If a poem has any past tense word then the following process is executed:<br>
The antonyms of that word is found and that antonyms are searched in all keyword files.If that antonym present in any keywords file, its emotion is return as the original tokens emotion.<p align="center">
  <img width="750" height="280" src="https://github.com/keshab97/poetry-classification/blob/master/Images/Pos%20Tag%20tracking%20list%20(not%20contain%20stopwords%20as%20key).png"  title='Pos Tag tracking list (not contain stopwords as key)'><p align="center">Pos Tag tracking list (not contain stopwords as key)</p><br>
  
- The word may have more than one emotion category so track of each emotion category of word/token is kept in a list of
  dictionary as shown.<p align="center">
  <img width="750" height="280" src="https://github.com/keshab97/poetry-classification/blob/master/Images/Track%20Emotion.png"  title='Track Emotion'><p align="center">Track Emotion</p><br>
  
 - A list is maintained which keep track of the emotion category that occur in a poem.<p align="center">
  <img width="750" height="280" src="https://github.com/keshab97/poetry-classification/blob/master/Images/Unique%20Emotion.png"  title='Unique Emotion'><p align="center">Unique Emotion</p><br>
  
 - Finally,a dictionary is maintained which keep track of the number of words each emotion category occur in a poem. An emotion  category which has maximum number of words is a preferable emotion category of that poem. And is used as a feature for training a
poem.<p align="center">
  <img width="750" height="280" src="https://github.com/keshab97/poetry-classification/blob/master/Images/Each%20Emotion%20Category%20Number.png"  title='Each Emotion Category Number'><p align="center">Each Emotion Category Number</p><br>
Thus, the emotion category obtained for the above inputted poem is categorized as joy.

## Model and Accuracy Measure :

Scikit learn module and SKlearn classifier are used to train the model.In total nine classifiers, are used. Two Nave Bayes classifiers: MultinominalNB and BernoulliNB two linear model classifiers Logistic Regression and SGDclassifier and three Support Vector Machine(SVM) classifiers: SVC, Linear SVC, Mu SVC.

To calculate the accuracy,the voting system is created in which each algorithm gets one vote and the classifier that has more votes is chosen. And gives the emotion of the poem.
The below figure shows the accuracy of all the classifiers that we have used.<p align="center">
  <img width="750" height="280" src="https://github.com/keshab97/poetry-classification/blob/master/Images/Accuracy%20of%20classifiers.png"  title='Accuracy of classifiers'><p align="center">Accuracy of classifiers</p><br>
