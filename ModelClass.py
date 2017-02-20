





class Model:

    def __init__(self,filePath):
        #read the file and put information into correct places
        self.verticies = []
        self.triangles = []
        self.world_coordinates = []
        self.normalized_coordinates = []
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
                if splitLine[0]== "w":
                    self.world_coordinates = [float(splitLine[1]),float(splitLine[2]),float(splitLine[3]),float(splitLine[4])]
                if splitLine[0]== "s":
                    self.normalized_coordinates = [float(splitLine[1]),float(splitLine[2]),float(splitLine[3]),float(splitLine[4])]
        except IOError as e:
            print ("could not read file error")
        finally:
            f.close()



