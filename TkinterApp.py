from tkinter import *
from TkinterMenuBar import *
from TkinterButtonGroup import *
from TkinterCanvas import *
from tkinter import messagebox
from Controller import *
from MyView import *



class App:

    def __init__(self,rootWidget):


        exitLambdaFunction = lambda: self.onExit(rootWidget)
        rootWidget.protocol("WM_DELETE_WINDOW", exitLambdaFunction)



        controllerReference = MyController(rootWidget)
        MyView(rootWidget,controllerReference)




    def onExit(self,rootWidget):
        #asks   OK? | CANCEL?
        if messagebox.askokcancel("Quit Dialog Title","Do you want to quit?"):
            rootWidget.destroy()