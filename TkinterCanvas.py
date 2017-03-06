from tkinter import *
from Controller import *
import numpy as np
import math



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
        self.zmin = model.world_coordinates[4]
        self.zmax = model.world_coordinates[5]
        self.canvas.create_rectangle(self.umin,self.vmin,self.umax,self.vmax)


        #generate matrix that should be used on verticies
        #translate VRP to origin
        #step 1
        vrp_translate = np.matrix([[1,0,0,-model.vrp[0]],
                                   [0,1,0,-model.vrp[1]],
                                   [0,0,1,-model.vrp[2]],
                                   [0,0,0,1]])


        #abc here refers to vpn

        #come back to this and work out how this math even works? IT's the angle between the vectors using dot(U,V)/(norm(U),norm(V))
        #translation vpn to xz plane
        #abc here refers to vpn
        #step 2
        a = model.vpn[0]
        b = model.vpn[1]
        c = model.vpn[2]
        b_square_c_square = math.sqrt(math.pow(b,2)+math.pow(c,2))

        if (b_square_c_square == 0):
            vpn_to_x = np.matrix([[1,0,0,0],
                            [0,1,0,0],
                            [0,0,1,0],
                            [0,0,0,1]])
        else:
            cos_theta_answer = c/b_square_c_square
            sin_theta_answer = b/b_square_c_square
            vpn_to_x = np.matrix([[1,0,0,0],
                                    [0,cos_theta_answer,-sin_theta_answer,0],
                                    [0,sin_theta_answer,cos_theta_answer,0],
                                    [0,0,0,1]])

        #step 3
        a_square_c_square = math.sqrt(math.pow(a,2)+math.pow(c,2))

        if(a_square_c_square==0):
            vpn_to_y = np.matrix([[1,0,0,0],
                                    [0,1,0,0],
                                    [0,0,1,0],
                                    [0,0,0,1]])
        else:
            cos_theta_answer = c/a_square_c_square
            sin_theta_answer = a/a_square_c_square
            vpn_to_y = np.matrix([[cos_theta_answer,0,-sin_theta_answer,0],
                                    [0,1,0,0],
                                    [sin_theta_answer,0,cos_theta_answer,0],
                                    [0,0,0,1]])



        #step 4
        #abc here refers to vup
        a = model.vup[0]
        b = model.vup[1]
        c = model.vup[2]
        a_square_b_square = math.sqrt(math.pow(a,2)+math.pow(b,2))
        if(a_square_b_square==0):
            vup_rotation = np.matrix([[1,0,0,0],
                                      [0,1,0,0],
                                      [0,0,1,0],
                                      [0,0,0,1]])
        else:
            cos_theta_answer = b/a_square_b_square
            sin_theta_answer = a/(math.sqrt(math.pow(a,2)+math.pow(b,2)))
            vup_rotation = np.matrix([[cos_theta_answer,-sin_theta_answer,0,0],
                                      [sin_theta_answer,cos_theta_answer,0,0],
                                      [0,0,1,0],
                                      [0,0,0,1]])



        #step 5
        #shear along the z axis?
        #stretch the model so the center point of the window matches the center ???

        matrix_shear = np.matrix([[1,0,-(model.prp[0]-((self.xmin+self.xmax)/2))/model.prp[2],0],
                                    [0,1,-(model.prp[1]-((self.ymin+self.ymax)/2))/model.prp[2],0],
                                    [0,0,1,0],
                                    [0,0,0,1]])
        matrix_final_Transform = matrix_shear * vup_rotation * vpn_to_y * vpn_to_x * vrp_translate

        
        #step 6
        #TODO: fix this?
        #we dont' have a zmin?
        '''
        #This is really how to do it
        U_T1 = self.xmin if self.xmin<self.xmax else self.xmax
        U_T2 = self.xmin if self.xmin>self.xmax else self.xmax
        V_T1 = self.ymin if self.ymin<self.ymax else self.ymax
        V_T2 = self.ymin if self.ymin>self.ymax else self.ymax
        N_T1 = self.zmin if self.zmin<self.zmax else self.zmax
        N_T2 = self.zmin if self.zmin>self.zmax else self.zmax
        

        
        
        matrix_T = np.matrix([[1,0,0,-U_T1],
                              [0,1,0,-V_T1],
                              [0,0,1,-N_T1],
                              [0,0,0,1]])


        #step 7
        #there is no nmin?
        matrix_S = np.matrix([[1/(U_T2-U_T1),0,0,0],
                              [0,1/(V_T2-V_T1),0,0],
                              [0,0,1/(N_T2-N_T1),0],
                              [0,0,0,1]])
        '''
        #for some reaosn this is how to do it for the assignment
        matrix_T = np.matrix([[1,0,0,0],
                              [0,1,0,0],
                              [0,0,1,0],
                              [0,0,0,1]])


        #step 7
        #there is no nmin?
        matrix_S = np.matrix([[1,0,0,0],
                              [0,1,0,0],
                              [0,0,1,0],
                              [0,0,0,1]])

        #Final matrix
        

        matrix_final_Transform = matrix_S*matrix_T * matrix_shear * vup_rotation * vpn_to_y * vpn_to_x * vrp_translate

        for triangle in model.triangles:
            x1 = model.verticies[triangle[0]-1][0]
            y1 = model.verticies[triangle[0]-1][1]
            z1 = model.verticies[triangle[0]-1][2]
            x2 = model.verticies[triangle[1]-1][0]
            y2 = model.verticies[triangle[1]-1][1]
            z2 = model.verticies[triangle[1]-1][2]
            x3 = model.verticies[triangle[2]-1][0]
            y3 = model.verticies[triangle[2]-1][1]
            z3 = model.verticies[triangle[2]-1][2]
            matrix_triangle = np.matrix([[x1,x2,x3],
                                         [y1,y2,y3],
                                         [z1,z2,z3],
                                         [1,1,1]])
            matrix_triangle = matrix_final_Transform * matrix_triangle
            
            self._cohenSutherlandLineClipAndDraw(matrix_triangle[0,0],matrix_triangle[1,0],matrix_triangle[0,1],matrix_triangle[1,1])
            self._cohenSutherlandLineClipAndDraw(matrix_triangle[0,1],matrix_triangle[1,1],matrix_triangle[0,2],matrix_triangle[1,2])
            self._cohenSutherlandLineClipAndDraw(matrix_triangle[0,2],matrix_triangle[1,2],matrix_triangle[0,0],matrix_triangle[1,0])




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
