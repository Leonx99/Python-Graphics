from tkinter import *
from Controller import *



class MyCanvas:
    def __init__(self, rootWidget,parentView):
        self.CONST_INSIDE = 0 #0000
        self.CONST_LEFT = 1   #0001
        self.CONST_RIGHT = 2; #0010
        self.CONST_BOTTOM = 4 #0100
        self.CONST_TOP = 8    #1000







        self.parentView = parentView
        self.canvas = Canvas(rootWidget, width=640, height=640, bg="yellow", highlightthickness=0)
        
        #makes the object fill and resize to the size of the parent
        self.canvas.pack(fill=BOTH, expand=1)





        

        #resize funtion
        self.canvas.bind("<Configure>", self.on_resize)

    def on_resize(self,event):
        self.canvas.config(width=event.width,height=event.height)
        self.parentView.draw_model()





    '''
    #old draw function based around polygons with no clipping

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
    '''
    

    #New draw algorythm based around drawing lines and clipping
    def draw_Model(self,model):
        if(model is None):
            return
        self.canvas.delete("all")
        self.umin = model.normalized_coordinates[0]*int(self.canvas.cget("width"))
        self.vmin = model.normalized_coordinates[1]*int(self.canvas.cget("height"))
        self.umax = model.normalized_coordinates[2]*int(self.canvas.cget("width"))
        self.vmax = model.normalized_coordinates[3]*int(self.canvas.cget("height"))
        self.xmin = model.world_coordinates[0]
        self.ymax = model.world_coordinates[1]
        self.xmax = model.world_coordinates[2]
        self.ymin = model.world_coordinates[3]
        self.canvas.create_rectangle(self.umin,self.vmin,self.umax,self.vmax)
        for triangle in model.triangles:
            x1 = model.verticies[triangle[0]-1][0]
            y1 = model.verticies[triangle[0]-1][1]
            x2 = model.verticies[triangle[1]-1][0]
            y2 = model.verticies[triangle[1]-1][1]
            x3 = model.verticies[triangle[2]-1][0]
            y3 = model.verticies[triangle[2]-1][1]
            self._cohenSutherlandLineClipAndDraw(x1,y1,x2,y2)
            self._cohenSutherlandLineClipAndDraw(x2,y2,x3,y3)
            self._cohenSutherlandLineClipAndDraw(x3,y3,x1,y1)




    #START COHEND SUTHERLAND ALGO


    
    def _compute_Out_Code(self,x,y):
        #find where the point is in relation to world coordinates
        code = self.CONST_INSIDE

        if(x<self.xmin):
            code = code|self.CONST_LEFT
        elif(x>self.xmax):
            code = code|self.CONST_RIGHT
        if(y<self.ymax):
            code = code|self.CONST_BOTTOM
        elif(y>self.ymin):
            code = code|self.CONST_TOP
        return code

    def _cohenSutherlandLineClipAndDraw(self,x0,y0,x1,y1):
        #compute outcodes
        outcode0 = self._compute_Out_Code(x0,y0)
        outcode1 = self._compute_Out_Code(x1,y1)
        accept = False
        #both points are in the middle
        while(True):
            if(not (outcode0|outcode1)):
                accept = True
                break
            #both points are not in the middle & are in the same region
            elif(outcode0 & outcode1):
                break
            #need additional information to clip the line
            else:
                #find a point is not in the middle
                x = 0
                y = 0
                outOutCode = outcode0 if outcode0 else outcode1
                #use formulas y = y0 + slope * (x - x0), x = x0 + (1 / slope) * (y - y0)
                #top
                if (outOutCode & self.CONST_TOP):
                    if (not y1==y0):
                        x = x0 + (x1 - x0) * (self.ymin - y0) / (y1 - y0)
                    y = self.ymin
                #below
                elif (outOutCode & self.CONST_BOTTOM):
                    if (not y1==y0):
                        x = x0 + (x1 - x0) * (self.ymax - y0) / (y1 - y0)
                    y = self.ymax
                #right
                elif (outOutCode & self.CONST_RIGHT):
                    if (not x1==x0):
                        y = y0 + (y1 - y0) * (self.xmax - x0) / (x1 - x0)
                    x = self.xmax
                #left
                elif (outOutCode & self.CONST_LEFT):
                    if (not x1==x0):
                        y = y0 + (y1 - y0) * (self.xmin - x0) / (x1 - x0)
                    x = self.xmin
                #apply the new Variables
                if(outOutCode==outcode0):
                    x0=x
                    y0=y
                    outcode0 = self._compute_Out_Code(x0,y0)
                else:
                    x1=x
                    y1=y
                    outcode1 = self._compute_Out_Code(x1,y1)
        if (accept):
            finalX0 = (x0-self.xmin)*((self.umax-self.umin)/(self.xmax-self.xmin))+self.umin
            finalY0 = (y0-self.ymin)*((self.vmax-self.vmin)/(self.ymax-self.ymin))+self.vmin
            finalX1 = (x1-self.xmin)*((self.umax-self.umin)/(self.xmax-self.xmin))+self.umin
            finalY1 = (y1-self.ymin)*((self.vmax-self.vmin)/(self.ymax-self.ymin))+self.vmin
            self.canvas.create_line(finalX0,finalY0,finalX1,finalY1)
            self.canvas.update()