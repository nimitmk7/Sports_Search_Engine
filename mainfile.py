import os
import math
import time
import sys
import nltk
import glob
import errno
import natsort
import difflib
from PyQt5 import QtCore, QtGui, QtWidgets
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
#from collections import Ordered_Dict


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(892, 587)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.query_search = QtWidgets.QTextEdit(self.centralwidget)
        self.query_search.setGeometry(QtCore.QRect(120, 190, 591, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.query_search.setFont(font)
        self.query_search.setObjectName("query_search")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(710, 190, 71, 51))
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./download.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(40, 40))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(120, 250, 661, 251))
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(350, 10, 511, 161))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("./Mighty-sports-2019-new-logo.jpg"))
        self.label.setObjectName("label")
        self.close = QtWidgets.QPushButton(self.centralwidget)
        self.close.setGeometry(QtCore.QRect(340, 510, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.close.setFont(font)
        self.close.setStyleSheet("background-color: rgb(223, 223, 223);")
        self.close.setObjectName("close")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(630, 510, 112, 23))
        self.radioButton.setObjectName("radioButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.query_search.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\';\"><br /></p></body></html>"))
        self.close.setText(_translate("MainWindow", "Close"))
        self.radioButton.setText(_translate("MainWindow", "Autocorrect"))
        self.close.clicked.connect(self.ButtonExit)
        self.query_search.setText("<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; text-indent:9px; line-height: 40px;\">"'Enter the search query here...'"</p>")
        self.pushButton.clicked.connect(self.EvaluateQuery)
        self.constructIndex()

    def ButtonExit(self):
        exit();

    def EvaluateQuery(self):
        #self.textEdit.setText("Hello")
        #print(self.WordDict.keys())

        query = str(self.query_search.toPlainText())
        query = query.split(" ")
        print(query)

        strresponse=""
        content=""

        if(self.radioButton.isChecked()):
            strresponse+='Showing results for '
            for i in range(len(query)):
                closest=difflib.get_close_matches(query[i],self.WordDict.keys())
                print(closest)
                query[i]=closest[0]
                strresponse+=str(query[i])+' '
            strresponse+='\n\n\n\n#################################\n\n\n\n'

        for i in range(len(query)):
            query[i]=query[i].lower()
        
        response=self.search(query)
        
        count=0
        for val in response:
            count+=1
            newpath=''
            if(len(str(val[0]))==1):
                newpath='./sports-articles-for-objectivity-analysis/Raw data/Text000'+str(val[0]+1)+'.txt'
            elif(len(str(val[0]))==2):
                newpath='./sports-articles-for-objectivity-analysis/Raw data/Text00'+str(val[0]+1)+'.txt'
            elif(len(str(val[0]))==3):
                newpath='./sports-articles-for-objectivity-analysis/Raw data/Text0'+str(val[0]+1)+'.txt'
            elif(len(str(val[0]))==4):
                newpath='./sports-articles-for-objectivity-analysis/Raw data/Text'+str(val[0]+1)+'.txt'
            
            with open(newpath,'rb') as content_file:
                content =str(count)+') '+str(content_file.read().decode('utf-8','ignore'))
            strresponse+=content+'\n\n\n'+'******************End of Article********************'+'\n\n\n'
        if(strresponse==""):
            self.textEdit.setText("No Results Found")    
        else:
            self.textEdit.setText(strresponse)

    def constructIndex(self):
        cwd = os.getcwd()

        #Directory for files
        self.files=[]
        # Defining a Regular Expression for importing files
        path = 'sports-articles-for-objectivity-analysis/Raw data/*.txt'
        # Using glob to import files from a path having given regular expression in their name
        self.files = glob.glob(path)
        # Sorting files on the basis of their names
        self.files = natsort.natsorted(self.files)
        # Creating the Documents Corpus
        docs=[]
        # Writing the the content of files into documents corpus
        for i in range(0,1000):
            f = open(self.files[i],'r+',encoding="unicode_escape")
            g = f.read()
            docs.append(g)
        # Initializing the processed corpus    
        self.filtered_docs=[]
        tokenizer = RegexpTokenizer(r'\w+')
        stop = set(stopwords.words('english'))
        # Removing stopwords, punctuation and unnecessary elements using NLTK and converting documents into tokens of words
        for i in range(1000):
            text = docs[i]
            text1=[]
            words = nltk.word_tokenize(text)
            words = [word.lower() for word in words if word.isalpha()]
            for word in words:
                if word not in stop:
                    text1.append(word)
            self.filtered_docs.append(text1)
        # Initializing the dictionary used for calculating document frequency     
        self.WordDict = {}
        for i in range(1000):
            for j in self.filtered_docs[i]:
                if(j not in self.WordDict):
                    self.WordDict[j]=1
        # Initializing the array of dictionaries, each dictionary to be used for computing term frequency for a document            
        self.freq_table=[]
        # Calculating term frequency of each word in every document
        for i in range(1000):
            freq={}
            for j in self.filtered_docs[i]:
                if j in freq:
                    freq[j]=freq[j]+1;
                else:
                    freq[j]=1;
            self.freq_table.append(freq)
        # Calculating Document Frequency of each unique word in the corpus    
        for key in self.WordDict:
            for i in range(1000):
                if(key in self.freq_table[i]):
                    self.WordDict[key]=self.WordDict[key]+1
        # Calculating inverse document Frequency of each unique word in the corpus
        for key in self.WordDict:
            self.WordDict[key]=math.log(1000/float(self.WordDict[key]),10)

    # Modified(Normalized) term frequency        
    def tf(self,word,freq):
        if word in freq:
            return math.log(freq[word],10)+1;
        else:
            return 0;
    # Computing TF-IDF score for a term with respect to a document       
    def tf_idf(self,term,doc_id):
        if term not in self.WordDict.keys() or term not in self.freq_table[doc_id].keys():
            return 0
        return self.tf(term,self.freq_table[doc_id])*(self.WordDict[term])

    # Computing TF-IDF scores for a query with respect to a document     
    def query_tf_idf(self,query,doc_id):
        value=0;
        for i in query:
            value=value+self.tf_idf(i,doc_id)
        return value

    # Ranking the documents given a query on the basis of TF-IDF scores 
    def search(self,query):
        rank={}
        for i in range(1000):
            r=(self.query_tf_idf(query,i))
            if(r>0):
                rank[i]=r
        print(sorted(rank.items(), reverse = True, key = lambda x : (x[1],x[0])))
        return sorted(rank.items(), reverse=True, key = lambda x : (x[1],x[0]))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
