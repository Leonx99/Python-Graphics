from TkinterMenuBar import *
from TkinterButtonGroup import *
from TkinterCanvas import *
from Controller import *
import math


class MyView:
    def __init__(self,rootWidget,controllerReference):



        self.controllerReference = controllerReference


        #Add Top Menu Bar | Not used in this project
        #MyTkinterMenuBar(rootWidget)

        #add a button group
        self.buttonGroupReference = MyButtonGroup(rootWidget,self)

        #Add the canvas
        self.canvasReference = MyCanvas(rootWidget,self)


    def loadFile(self, fileLocation):
        model = self.controllerReference.loadModel(fileLocation)
        self.canvasReference.draw_Model(model)

    def draw(self):
        print("in draw statement")
        self.canvasReference.draw_Model(self.controllerReference.draw())

    def rotate_call(self,rotationType,rotationSteps,rotationTheta):
        self.controllerReference.rotationCall(rotationType,self.canvasReference,int(rotationSteps),math.radians(int(rotationTheta)))

    
