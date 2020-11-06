from tkinter import *
from tkinter import filedialog as fd
import controller as cr
class MainController():
    def __init__(self):
        self.gui = Gui(self.insertText,self.saveText,self.saveDocx,self.Summary)
        self.control = cr.Controller()
    
    def start(self):
        self.gui.mainloop()
    def clearAllGui(self):
        self.gui.input_file_path.delete(0 , END)
        self.gui.out_file_path.delete(0 , END)
        self.gui.text_input.delete(1.0 , END)
        self.gui.text_output.delete(1.0, END)

    def clearAll(self):
        self.clearAllGui()
        self.control.clearAll()

    def insertText(self):
        file_name = fd.askopenfilename()
        #self.control.clearAll()
        self.clearAll()
        #self.control.resetTextBuffer()
        #print(type(file_name))
        self.control.readData(file_name)
        self.gui.input_file_path.delete(0,END)
        self.gui.input_file_path.insert(0,file_name)
        text = ''.join(self.control.getInputText())
        if len(text) > 100000:
            text = text[:100000]
        self.gui.text_input.delete(1.0, END)
        self.gui.text_input.insert(1.0,text)

    def saveText(self):
        name = self.gui.out_file_path.get()
        #print(name , type(name))
        self.control.save(name)
        error_massege = self.control.getMassege()
        if error_massege!='':
            print(error_massege)
            self.clearAll()
        return

    def saveDocx(self):
        name = self.gui.out_file_path.get()
        print("asadassadas")
        self.control.saveDocx(name)
        error_massege = self.control.getMassege()
        if error_massege!='':
            print(error_massege)
            self.clearAll()
        return

    def Summary(self):
        self.control.getSummary()
        error_massege = self.control.getMassege()
        if error_massege!= '':
            print(error_massege)
            return
        summary = self.control.getOutText()
        x = 40
        summary = ''.join([summary[y-x:y]+'\n' for y in range(x, len(summary)+x,x)])
        self.gui.text_output.insert(1.0, summary)
        return

    def setModel(self,mode):
        self.control.setMode(mode)
        self.a.destroy()

    def chooseModel(self):
        self.a = Toplevel()
        self.a.geometry('200x150')
        a['bg'] = 'grey'
        self.a.overrideredirect(True)
        Label(self.a, text="About this").pack(expand=1)
        Buttom(self.a,text="Test1",command = self.setModel("Test1")).pack()
        Buttom(self.a,text="Test2",command = self.setModel("Test2")).pack()
        Buttom(self.a,text="Test3",command = self.setModel("Test3")).pack()

class Gui():
    def __init__(self,insertText,SaveText,saveDocx,Summary):
        self.root = Tk()
        self.name_label = Label(text = "Text to Sum", width = 40)#,bg ='#000000',fg = 'black')
        self.name_label.grid(row=0, column=0, columnspan=5)

        self.input_file_path = Entry(width=60 , bg ='white',fg = 'black')
        self.input_file_path.grid(row=1, column=0, columnspan=3)

        self.out_file_path = Entry(width=60)
        self.out_file_path.grid(row=3, column=0, columnspan=3)

        self.button_open =  Button(text="Open",command = insertText)
        self.button_open.grid(row=1,column = 4)

        self.button_save =  Button(text="Save",command = SaveText)
        self.button_save.grid(row=3,column = 4)

        self.button_summarize = Button(text="Summarize", command = Summary)
        self.button_summarize.grid(row=1,column = 5)

        self.button_save_docx =  Button(text="Save Docx",command = saveDocx)
        self.button_save_docx.grid(row = 3,column = 5)

        self.text_input = Text(width=40, height=30)
        self.text_input.grid(row = 4,column = 0, columnspan = 2)
        self.text_output = Text(width=40, height=30)
        self.text_output.grid(row = 4, column = 3, columnspan = 2)

    def mainloop(self):
        self.root.mainloop()


def main():
    mc = MainController()
    mc.start()


if __name__=='__main__':
    main()