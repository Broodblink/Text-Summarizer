import os
import time
import hashlib
import docx
import textrank as tr
#import tfidf.py
#import seq2seq.py
#import gui
class Test1:
    def __init__(self):
        print("Init compilted Test1")
    def get_summary(self):
        return "Here summarized text from Test1"
class Test2:
    def __init__(self):
        print("Init compilted Test2")
    def get_summary(self):
        return "Here summarized text from Test2"
class Test3:
    def __init__(self):
        print("Init compilted Test3")
    def get_summary(self):
        return "Here summarized text from Test3"

class Controller():
    def  __init__(self):
        self.__SavePath = "C:\\Users\\Roman2\\Documents\\Autominutes"
        if not os.path.exists(self.__SavePath):
            os.makedirs(self.__SavePath)
        print("initializate controller")
        self.__file_max_size = 1024*1024*200
        self.__error_status = 0
        self.__massege = ''
        
        #self.__default_mode = 'TFIDF'
        #self.__modes = ('TF-IDF','TextRank','SentEmb','Topic Modeling')

        self.__model = None
        self.__default_mode = 'TextRank'
        self.__modes = ('TextRank',)
        self.__model_dict = {'TextRank':tr.TextRank}
        self.__mode = self.setMode()
        

        self.__text_input = ''
        self.__text_out = ''
        self.__input_path = ''


    def resetTextBuffer(self):
        self.clearTextInputBuffer()
        self.clearTextOutBuffer()
    
    def generateFileName(self, name = None):
        data_time = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
        name = "File" + data_time
        return name

    def clearTextInputBuffer(self):
        self.__text_input = ''
    def clearTextOutBuffer(self):
        self.__text_out = ''

    def readData(self,path):
        extention = path.split('.')[-1]
        if not os.path.exists(path):
            self.__massege = "Error, this path not  exist"
        if extention not in ("txt","docx"):
            self.__massege = "Error, uncorrect type of input file"
            return
        file_size = os.path.getsize(path)
        self.__input_path = path
        #print(file_size)
        if extention == "txt":
            f = open(path,"r")
            self.__text_input = f.readlines()
            #print("self.text_input {0}".format(self.__text_input))
            f.close()
            return
        if extention == "docx":
            self.__text_input = "function in developing "
            return

    def getInputText(self):
        return self.__text_input
    def getOutText(self):
        return self.__text_out
    
    def getMassege(self):
        return self.__massege
    def resetMassege(self):
        self.__massege = ''

    def getInputPath(self):
        return self.__input_path

    def setMode(self,mode=None):
        if mode in self.__modes:
            self.__mode = mode
        else:
            print( "Set Default mode")
            #self.__massege = "Set Default mode"
            self.__mode = self.__default_mode
        self.loadMode()

    def loadMode(self):
        self.__model = self.__model_dict[self.__mode]()
        #print("Model loaded")

    def getMode(self):
        return self.__mode
    def getSummary(self, parameters=None):
        """take input text and return summary in string format
        mode used algorithm option
        TF-IDF - 0
        Topic modeling - 1
        TR(TextRank) - 2
        DPL(deep learning) - 3
        SentEmb - 4
        parameteers - additional parameters for summmarization model"""
        if self.__text_input=='':
            self.__massege = 'Error, empty input text'
            print(self.__massege)
            self.__text_out = ''
            return
            
        if self.__model == None:
            self.__massege = 'Error? have not choose algorithm'
            print(self.__massege)
            self.__text_out = ''
            return
        text = ''.join([line.split('\n')[0]+' ' for line  in self.__text_input])
        summary = self.__model.getSummary(text)
        #print(summary)
        self.__text_out = summary

    def clearAll(self):
        self.resetMassege()
        self.resetTextBuffer()

    def save(self , name = None):
        if self.__text_out is None or self.__text_out == '':
            self.__massege="Error, Empty output text"
            return
        if name is None or name == '':
            name = self.generateFileName()+".txt"
        else:
            name+='.txt'
        full_file_name =os.path.join(self.__SavePath , name)
        file = open(full_file_name,'w')
        file.write(self.__text_out)
        file.close()
        print(full_file_name)

    def saveDocx(self,name=None):
        print("save_docx")
        if isinstance(self.__text_out, str):
            texts = [self.__text_out]
        elif isinstance(self.__text_out, list):
            texts = self.__text_out
        else:
            raise TypeError('Unsupported type of text varariable')
        if name is None or name ==  '':
            name = self.generateFileName()
        full_file_name =os.path.join(self.__SavePath, name)
        document = docx.Document()
        #texts = [self.text_out]
        for line in texts:
            document.add_paragraph(line)
        document.save(full_file_name + '.docx')
        print(full_file_name + '.docx')
        return document


def TestController():
    controller = Controller()
    controller.readData( "C:\\Users\\Roman2\\Desktop\\PMP\\text_test\\example.txt")
    controller.getSummary()
    controller.saveDocx()
    #print(controller.getOutText())
if __name__ == "__main__":
    TestController()