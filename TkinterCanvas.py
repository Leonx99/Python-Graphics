from tkinter import *
from Controller import *



class MyCanvas:
    def __init__(self, rootWidget,parentView):
        self.parentView = parentView
        self.canvas = Canvas(rootWidget, width=640, height=640, bg="yellow", highlightthickness=0)
        
        #makes the object fill and resize to the size of the parent
        self.canvas.pack(fill=BOTH, expand=1)

        #resize funtion
        self.canvas.bind("<Configure>", self.on_resize)

    def on_resize(self,event):
        self.canvas.config(width=event.width,height=event.height)
        self.parentView.draw()






    def draw_Model(self, model):
        if(model is None):
            return
        #Called when draw key pressed
        self.canvas.delete("all")
        #draw the normalized_coordinates
        umin = model.normalized_coordinates[0]*int(self.canvas.cget("width"))
        vmin = model.normalized_coordinates[1]*int(self.canvas.cget("height"))
        umax = model.normalized_coordinates[2]*int(self.canvas.cget("width"))
        vmax = model.normalized_coordinates[3]*int(self.canvas.cget("height"))
        xmin = model.world_coordinates[0]
        ymax = model.world_coordinates[1]
        xmax = model.world_coordinates[2]
        ymin = model.world_coordinates[3]
        self.canvas.create_rectangle(umin,vmin,umax,vmax)
        for triangle in model.triangles:
            x1 = (model.verticies[triangle[0]-1][0]-xmin)*((umax-umin)/(xmax-xmin))+umin
            y1 = (model.verticies[triangle[0]-1][1]-ymin)*((vmax-vmin)/(ymax-ymin))+vmin
            x2 = (model.verticies[triangle[1]-1][0]-xmin)*((umax-umin)/(xmax-xmin))+umin
            y2 = (model.verticies[triangle[1]-1][1]-ymin)*((vmax-vmin)/(ymax-ymin))+vmin
            x3 = (model.verticies[triangle[2]-1][0]-xmin)*((umax-umin)/(xmax-xmin))+umin
            y3 = (model.verticies[triangle[2]-1][1]-ymin)*((vmax-vmin)/(ymax-ymin))+vmin
            self.canvas.create_polygon([x1,y1,x2,y2,x3,y3],outline='black',fill='red',width=1)