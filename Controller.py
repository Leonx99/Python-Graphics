from ModelClass import *



class MyController:
    def __init__(self):
        self.model = None



    def loadModel(self,modelFileLocation):
        self.model= Model(modelFileLocation)
        return self.model