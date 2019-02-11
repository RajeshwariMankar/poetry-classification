#from mainfiles.classifyingpoems import classifier,classify,poem_set
import nltk
import os
from flask import Flask,abort,render_template,request,redirect,url_for
from werkzeug.utils import secure_filename
from mainfiles.classifyingpoems import classify
from mainfiles.classifyingpoems import *

# Flask initialization
app = Flask(__name__)

UPLOAD_FOLDER = 'uploadfiles/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = set(['txt', 'pdf'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/result_input',methods=['POST','GET'])
def input():
    if request.method == 'POST':
        if (request.form["submit"]):
            title=request.form['title']
            poemtext = request.form['poemtext']
            complete_text=title+"\n\n"+poemtext
            filename_upload=UPLOAD_FOLDER+"/"+"uploadedfile.txt"
            file_open=open(filename_upload,'w')
            file_open.write(complete_text)
            file_open.close()
            #filename_again,extension=os.path.splittext("uploadedfile.txt")
            #filename_o=filename_again+"."+extension
            emo=classify(filename_upload)
            return render_template('index.html',words=emo)
    else:
        render_template('index.html')

@app.route('/result_file',methods=['POST','GET'])
def uploadfiles():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        file_opening=UPLOAD_FOLDER+str(filename)
        file1 = open(file_opening,"r")
        print(file1)
        title=file1.readline()
        content_file=file1.read()
        file1.close()
        emo=classify(file_opening)
        #words=tokenization(content_file)
      
        return render_template('index.html',words=emo,title=title,readfile_content=content_file)
    else:
        return render_template('index.html')


@app.route('/learning')
def learning():
       #accuracy_of_emotions = str(nltk.classify.accuracy(classify,test_set))
       errors_of_emotions = errors_em(poem_set)
       accuracy=nltk.classify.accuracy(classifier, test_set)
       return render_template('learning.html',accuracy=accuracy,errors_of_emotions=errors_of_emotions)

if __name__ == '__main__':
    app.run(debug=True)
