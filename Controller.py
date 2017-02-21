from ModelClass import *
import time



class MyController:
    def __init__(self,rootWidget):
        self.model = None
        self.rootWidget = rootWidget



    def loadModel(self,modelFileLocation):
        self.model= Model(modelFileLocation)
        return self.model

    def draw(self):
        return self.model
        
    def rotationCall(self,rotationType,canvas,rotationSteps,rotationTheta):
        #Don't do anything on last call
        if rotationSteps==0:return

        thetaPerStep = rotationTheta/int(rotationSteps)
        #rotation type is 1,2,3:x,y,z
        if rotationType ==1:
            self.model.rotate_X(thetaPerStep)
        if rotationType ==2:
            self.model.rotate_Y(thetaPerStep)
        if rotationType ==3:
            self.model.rotate_Z(thetaPerStep)
        canvas.draw_Model(self.model)
        self.rootWidget.after(300,lambda: self.rotationCall(rotationType,canvas,rotationSteps-1,rotationTheta-thetaPerStep))
            
