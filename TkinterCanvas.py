from tkinter import *
from Controller import *
import numpy as np
import math



class MyCanvas:
    def __init__(self, rootWidget,parentView):
        self.CONST_INSIDE = 0 #000000
        self.CONST_LEFT = 1   #000001
        self.CONST_RIGHT = 2; #000010
        self.CONST_BOTTOM = 4 #000100
        self.CONST_TOP = 8    #001000
        self.CONST_NEAR = 16  #010000  
        self.CONST_FAR = 32   #100000
        self.unitXmin=0
        self.unitXmax=1
        self.unitYmin=0
        self.unitYmax=1
        self.unitZmin=0
        self.unitZmax=1







        self.parentView = parentView
        self.canvas = Canvas(rootWidget, width=640, height=640, bg="yellow", highlightthickness=0)
        
        #makes the object fill and resize to the size of the parent
        self.canvas.pack(fill=BOTH, expand=1)





        

        #resize funtion
        self.canvas.bind("<Configure>", self.on_resize)

    def on_resize(self,event):
        self.canvas.config(width=event.width,height=event.height)
        self.parentView.draw_model()



    

    #New draw algorythm based around drawing lines and clipping
    def draw_Model(self,model,cameras):
        if(model is None):
            return
        if(cameras is None):
            return
        self.canvas.delete("all")
        for camera in cameras:
            self.umin = camera.viewPort[0]*int(self.canvas.cget("width"))
            self.vmin = camera.viewPort[1]*int(self.canvas.cget("height"))
            self.umax = camera.viewPort[2]*int(self.canvas.cget("width"))
            self.vmax = camera.viewPort[3]*int(self.canvas.cget("height"))
            self.xmin = camera.vrc[0]
            self.xmax = camera.vrc[1]
            self.ymin = camera.vrc[2]
            self.ymax = camera.vrc[3]
            self.zmin = camera.vrc[4]
            self.zmax = camera.vrc[5]
            self.canvas.create_rectangle(self.umin,self.vmin,self.umax,self.vmax,fill='#fff')
            windowText = self.canvas.create_text(self.umin,self.vmin,anchor='nw',text=" "+camera.cameraName)

            
            #generate matrix that should be used on verticies
            #translate VRP to origin
            #step 1
            vrp_translate = np.matrix([[1,0,0,-camera.vrp[0]],
                                    [0,1,0,-camera.vrp[1]],
                                    [0,0,1,-camera.vrp[2]],
                                    [0,0,0,1]])
            print("step 1\n",vrp_translate)
            #abc here refers to vpn
            matrix_vpn = np.matrix([[camera.vpn[0]],
                                    [camera.vpn[1]],
                                    [camera.vpn[2]],
                                    [1]])
            matrix_vup = np.matrix([[camera.vup[0]],
                                    [camera.vup[1]],
                                    [camera.vup[2]],
                                    [1]])
            #translation vpn to xz plane
            #abc here refers to vpn
            #step 2
            a = matrix_vpn[0,0]
            b = matrix_vpn[1,0]
            c = matrix_vpn[2,0]
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
            matrix_vpn = vpn_to_x * matrix_vpn
            matrix_vup = vpn_to_x * matrix_vup
            print("step 2\n",vpn_to_x)
            #step 3
            a = matrix_vpn[0,0]
            b = matrix_vpn[1,0]
            c = matrix_vpn[2,0]
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
            matrix_vpn = vpn_to_y * matrix_vpn
            matrix_vup = vpn_to_y * matrix_vup
            print("step 3\n",vpn_to_y)


            #step 4
            #abc here refers to vup
            a = matrix_vup[0,0]
            b = matrix_vup[1,0]
            c = matrix_vup[2,0]
            a_square_b_square = math.sqrt(math.pow(a,2)+math.pow(b,2))
            if(a_square_b_square==0):
                vup_rotation = np.matrix([[-1,0,0,0],
                                        [0,-1,0,0],
                                        [0,0,1,0],
                                        [0,0,0,1]])
            else:
                cos_theta_answer = b/a_square_b_square
                sin_theta_answer = a/(math.sqrt(math.pow(a,2)+math.pow(b,2)))
                vup_rotation = np.matrix([[cos_theta_answer,-sin_theta_answer,0,0],
                                        [sin_theta_answer,cos_theta_answer,0,0],
                                        [0,0,1,0],
                                        [0,0,0,1]])

            print("step 4\n",vup_rotation)
            if(camera.type==CameraType.PARALLEL):
                #step 5
                #shear along the z axis?
                #stretch the model so the center point of the window matches the center ???

                matrix_shear = np.matrix([[1,0,-(camera.prp[0]-((self.xmin+self.xmax)/2))/camera.prp[2],0],
                                            [0,1,-(camera.prp[1]-((self.ymin+self.ymax)/2))/camera.prp[2],0],
                                            [0,0,1,0],
                                            [0,0,0,1]])
                print("step 5\n",matrix_shear)
                
                #step 6
                #TODO: fix this?
                #we dont' have a zmin?
                
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
                print("step 6\n",matrix_T)

                #step 7
                #there is no nmin?
                matrix_S = np.matrix([[1/(U_T2-U_T1),0,0,0],
                                    [0,1/(V_T2-V_T1),0,0],
                                    [0,0,1/(N_T2-N_T1),0],
                                    [0,0,0,1]])
                print("step 7\n",matrix_S)
                matrix_final_Transform = matrix_S * matrix_T * matrix_shear * vup_rotation * vpn_to_y * vpn_to_x * vrp_translate


            #perpective steps 5-7    
            else:
                #step 5
                #translate the center of projection to the cneter of of the view reference

                matrix_cop = np.matrix([[1,0,0,-camera.prp[0]],
                                        [0,1,0,-camera.prp[1]],
                                        [0,0,1,-camera.prp[2]],
                                        [0,0,0,1]])
                print("step 5\n",matrix_cop)

                #step 6
                #same as parallel step 5
                #center window - prp
                matrix_shear = np.matrix([[1,0,-(camera.prp[0]-((self.xmin+self.xmax)/2))/camera.prp[2],0],
                                            [0,1,-(camera.prp[1]-((self.ymin+self.ymax)/2))/camera.prp[2],0],
                                            [0,0,1,0],
                                            [0,0,0,1]])
                print("step 6\n",matrix_shear)


                #step 7
                #vrp after transform...
                currentMatrix=matrix_shear *matrix_cop* vup_rotation * vpn_to_y * vpn_to_x * vrp_translate

                

                startingVRP =np.matrix( [[camera.vrp[0]],
                               [camera.vrp[1]],
                               [camera.vrp[2]],
                               [1]])
                currentVRP = currentMatrix*startingVRP
                scaleFactorU = currentVRP[2,0] / ((camera.vrc[0] - camera.vrc[1])/2)
                scaleFactorV = currentVRP[2,0] / ((camera.vrc[2] - camera.vrc[3])/2)

                #TODO B and F are the front and back clipping plane. I'm not sure where these numbers actually come from
                if(math.fabs(currentVRP[2,0]+self.zmax) > math.fabs(currentVRP[2,0]+self.zmin)):
                    subSet = 1/(currentVRP[2,0]+self.zmax) 
                else:
                    subSet = 1/(currentVRP[2,0]+self.zmin)

                scaleStep = np.matrix([[scaleFactorU*subSet,0,0,0],
                                        [0,scaleFactorV*subSet,0,0],
                                        [0,0,subSet,0],
                                        [0,0,0,1]])

                print("step 7\n",scaleStep)
                matrix_final_Transform = scaleStep * currentMatrix






            #Final matrix

            print('Final Matrix \n',matrix_final_Transform)
            print("umin/max...",self.umin,self.umax,self.umin,self.umax)
            print("vrp",camera.vrp)
            print("vpn",camera.vpn)
            print("vup",camera.vup)
            print("prp",camera.prp)
            print("vrc",camera.vrc)
            print("camera: ",camera.cameraName)

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
                #TODO debug print("a triangle\n",matrix_triangle)

                if(camera.type==CameraType.PARALLEL):
                    self._cohenSutherlandLineClipAndDraw(matrix_triangle[0,0],matrix_triangle[1,0],matrix_triangle[0,1],matrix_triangle[1,1])
                    self._cohenSutherlandLineClipAndDraw(matrix_triangle[0,1],matrix_triangle[1,1],matrix_triangle[0,2],matrix_triangle[1,2])
                    self._cohenSutherlandLineClipAndDraw(matrix_triangle[0,2],matrix_triangle[1,2],matrix_triangle[0,0],matrix_triangle[1,0])
                
                else:
                    self._cohenSutherlandLineClipAndDraw_P(matrix_triangle[0,0],matrix_triangle[1,0],matrix_triangle[2,0],matrix_triangle[0,1],matrix_triangle[1,1],matrix_triangle[2,1])
                    self._cohenSutherlandLineClipAndDraw_P(matrix_triangle[0,1],matrix_triangle[1,1],matrix_triangle[2,1],matrix_triangle[0,2],matrix_triangle[1,2],matrix_triangle[2,2])
                    self._cohenSutherlandLineClipAndDraw_P(matrix_triangle[0,2],matrix_triangle[1,2],matrix_triangle[2,2],matrix_triangle[0,0],matrix_triangle[1,0],matrix_triangle[2,0])
                




    #START COHEND SUTHERLAND ALGO



    def _compute_Out_Code(self,x,y):
        #find where the point is in relation to world coordinates
        code = self.CONST_INSIDE

        if(x<self.unitXmin):
            code = code|self.CONST_LEFT
        elif(x>self.unitXmax):
            code = code|self.CONST_RIGHT
        if(y<self.unitYmin):
            code = code|self.CONST_BOTTOM
        elif(y>self.unitYmax):
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
                    x = x0 + (x1 - x0) * (self.unitYmin - y0) / (y1 - y0)
                    y = self.unitYmin
                #below
                elif (outOutCode & self.CONST_BOTTOM):
                    x = x0 + (x1 - x0) * (self.unitYmax - y0) / (y1 - y0)
                    y = self.unitYmax
                #right
                elif (outOutCode & self.CONST_RIGHT):
                    y = y0 + (y1 - y0) * (self.unitXmax - x0) / (x1 - x0)
                    x = self.unitXmax
                #left
                elif (outOutCode & self.CONST_LEFT):
                    y = y0 + (y1 - y0) * (self.unitXmin - x0) / (x1 - x0)
                    x = self.unitXmin
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
            finalX0 = (x0-self.unitXmin)*((self.umax-self.umin)/(self.unitXmax-self.unitXmin))+self.umin
            finalY0 = (self.unitYmin-y0)*((self.vmax-self.vmin)/(self.unitYmax-self.unitYmin))+self.vmax
            finalX1 = (x1-self.unitXmin)*((self.umax-self.umin)/(self.unitXmax-self.unitXmin))+self.umin
            finalY1 = (self.unitYmin-y1)*((self.vmax-self.vmin)/(self.unitYmax-self.unitYmin))+self.vmax
            self.canvas.create_line(finalX0,finalY0,finalX1,finalY1)




#START COHEND SUTHERLAND Perspective ALGO



    def _compute_Out_Code_P(self,x,y,z):
        #find where the point is in relation to world coordinates
        code = self.CONST_INSIDE

        if(x>z):
            code = code|self.CONST_LEFT
        elif(x<-z):
            code = code|self.CONST_RIGHT
        if(y<-z):
            code = code|self.CONST_BOTTOM
        elif(y>z):
            code = code|self.CONST_TOP
        if(z>self.unitZmax):
            code = code|self.CONST_FAR
        elif(z<self.unitZmin):
            code = code|self.CONST_NEAR
        return code

    def _cohenSutherlandLineClipAndDraw_P(self,x0,y0,z0,x1,y1,z1):
        #compute outcodes
        '''
        print("INPUT")
        print("X0 | Y0 | Z0")
        print(x0,y0,z0)
        print("X1 | Y1 | Z1")
        print(x1,y1,z1)
        '''
        outcode0 = self._compute_Out_Code_P(x0,y0,z0)
        outcode1 = self._compute_Out_Code_P(x1,y1,z1)
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
                z = 0
                outOutCode = outcode0 if outcode0 else outcode1
                #use formulas y = y0 + slope * (x - x0), x = x0 + (1 / slope) * (y - y0)
                #top
                if (outOutCode & self.CONST_TOP):
                    x = x0 + (x1 - x0) * (z0-y0) / ((y1 - y0) - (z1 - z0))
                    y = y0 + (y1 - y0) * (z0-y0) / ((y1 - y0) - (z1 - z0))
                    z = y
                #below
                elif (outOutCode & self.CONST_BOTTOM):
                    x = x0 + (x1 - x0) * (z0+y0) / ((y0 - y1) - (z1 - z0))
                    y = y0 + (y1 - y0) * (z0+y0) / ((y0 - y1) - (z1 - z0))
                    z = -y
                #right
                elif (outOutCode & self.CONST_RIGHT):
                    y = x0 + (x1 - x0) * (x0 + z0) / ((z0 - z1) - (x1 - x0))
                    x = y0 + (y1 - y0) * (x0 + z0) / ((z0 - z1) - (x1 - x0))
                    z = -x
                #left
                elif (outOutCode & self.CONST_LEFT):
                    y = x0 + (x1 - x0) * (x0 - z0) / ((z0 - z1) - (x1 - x0))
                    x = y0 + (y1 - y0) * (x0 - z0) / ((z0 - z1) - (x1 - x0))
                    z = x
                #near
                elif (outOutCode & self.CONST_NEAR):
                    z = self.unitZmin
                #far
                elif (outOutCode & self.CONST_FAR):
                    z = self.unitZmax
                #apply the new Variables
                if(outOutCode==outcode0):
                    x0=x
                    y0=y
                    z0 = z
                    outcode0 = self._compute_Out_Code_P(x0,y0,z0)
                else:
                    x1=x
                    y1=y
                    z1 = z
                    outcode1 = self._compute_Out_Code_P(x1,y1,z1)
        print("OUTPUT")
        print("X0 | Y0 | Z0")
        print(x0,y0,z0)
        print("X1 | Y1 | Z1")
        print(x1,y1,z1)
        
        if (accept):
            finalX0 = (x0-self.unitXmin)*((self.umax-self.umin)/(self.unitXmax-self.unitXmin))+self.umin
            finalY0 = (self.unitYmin-y0)*((self.vmax-self.vmin)/(self.unitYmax-self.unitYmin))+self.vmax
            finalX1 = (x1-self.unitXmin)*((self.umax-self.umin)/(self.unitXmax-self.unitXmin))+self.umin
            finalY1 = (self.unitYmin-y1)*((self.vmax-self.vmin)/(self.unitYmax-self.unitYmin))+self.vmax


            print("FINAL X0| Y0| X1| Y1")
            print(finalX0,finalY0,finalX1,finalY1)
            print("\n\n")
            self.canvas.create_line(finalX0,finalY0,finalX1,finalY1)
        
