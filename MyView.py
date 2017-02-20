from TkinterMenuBar import *
from TkinterButtonGroup import *
from TkinterCanvas import *
from Controller import *


class MyView:
    def __init__(self,rootWidget,controllerReference):



        self.controllerReference = controllerReference


        #Add Top Menu Bar | Not used in this project
        #MyTkinterMenuBar(rootWidget)

        #add a button group
        self.buttonGroupReference = MyButtonGroup(rootWidget,self)

        #Add the canvas
        self.canvasReference = MyCanvas(rootWidget)


    def loadFile(self, fileLocation):
        model = self.controllerReference.loadModel(fileLocation)
        self.canvasReference.draw_Model(model)


    
