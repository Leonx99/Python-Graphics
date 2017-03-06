import math





class Model:

    def __init__(self,filePath):
        #read the file and put information into correct places
        self.verticies = []
        self.triangles = []
        self.world_coordinates = []
        self.normalized_coordinates = []
        self.vrp = []
        self.vpn = []
        self.vup = []
        self.prp = []
        f = open(filePath, 'r')
        try:
            for line in f:
                splitLine = line.split()
                if splitLine == []:
                    break
                if splitLine[0]== "v":
                    self.verticies.append([float(splitLine[1]),float(splitLine[2]),float(splitLine[3])])
                if splitLine[0]== "f":
                    self.triangles.append([int(splitLine[1]),int(splitLine[2]),int(splitLine[3])])
                if splitLine[0]== "r":
                    self.vrp = [int(splitLine[1]),int(splitLine[2]),int(splitLine[3])]
                if splitLine[0]== "n":
                    self.vpn = [int(splitLine[1]),int(splitLine[2]),int(splitLine[3])]
                if splitLine[0]== "u":
                    self.vup = [int(splitLine[1]),int(splitLine[2]),int(splitLine[3])]
                if splitLine[0]== "p":
                    self.prp = [int(splitLine[1]),int(splitLine[2]),int(splitLine[3])]
                if splitLine[0]== "w":
                    self.world_coordinates = [float(splitLine[1]),float(splitLine[3]),float(splitLine[2]),float(splitLine[4]),float(splitLine[5]),float(splitLine[6])]
                if splitLine[0]== "s":
                    self.normalized_coordinates = [float(splitLine[1]),float(splitLine[2]),float(splitLine[3]),float(splitLine[4])]
        except IOError as e:
            print ("could not read file error")
        finally:
            f.close()


    def rotate_X(self,theta):
        for i in range(len(self.verticies)):
            self.verticies[i] = [self.verticies[i][0],self.verticies[i][1]*math.cos(theta)-self.verticies[i][2]*math.sin(theta),self.verticies[i][1]*math.sin(theta)+self.verticies[i][2]*math.cos(theta)]

    def rotate_Y(self,theta):
        for i in range(len(self.verticies)):
            self.verticies[i] = [self.verticies[i][0]*math.cos(theta)+self.verticies[i][2]*math.sin(theta),self.verticies[i][1],-self.verticies[i][0]*math.sin(theta)+self.verticies[i][2]*math.cos(theta)]


    def rotate_Z(self,theta):
        for i in range(len(self.verticies)):
            self.verticies[i] = [self.verticies[i][0]*math.cos(theta)-self.verticies[i][1]*math.sin(theta),self.verticies[i][0]*math.sin(theta)+self.verticies[i][1]*math.cos(theta),self.verticies[i][2]]


    def translate(self,x,y,z):
        for i in range(len(self.verticies)):
            self.verticies[i] = [self.verticies[i][0]+x,self.verticies[i][1]+y,self.verticies[i][2]+z]

    def nonuniform_scale(self,x_scale,y_scale,z_scale):
        for i in range(len(self.verticies)):
            self.verticies[i] = [self.verticies[i][0]*x_scale,self.verticies[i][1]*y_scale,self.verticies[i][2]*z_scale]

