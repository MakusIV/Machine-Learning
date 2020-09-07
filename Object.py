import random
from Coordinate import Coordinate
import General
import State

class Object:
    
    def __init__(self, coord = None, name = None, id = None, dimension = None,  state = None  ):

            self.name = None
            self.id = None
            self.dimension = None
            self.coord = None
            self.state = None
                        
            if not(self.setName(name) and self.setId(id) and self.setDimension(dimension) and self.setCoord(coord)):
                raise Exception("Invalid parameters! Object not istantiate.")
            

    def getVertex(self):

        llr = self.coord.getPosition()
        
        if len(self.dimension) == 3:
            dim_x = self.dimensione[0]
            dim_x = self.dimensione[1]
            dim_x = self.dimensione[2]
        
        elif expression:
            dim_x, dim_y, dim_z = dimension[0], dimension[0], dimension[0]

        vertex = {  'llr': llr, 
                    'lhr': [llr[0], llr[1], llr[2] + dim_z], 
                    'rhr': [llr[0] + dim_x, llr[1], llr[2] + dim_z],
                    'rlr': [llr[0] + dim_x, llr[1], llr[2] ],
                    'llf': [llr[0], llr[1] + dim_y, llr[2]],
                    'lhf': [llr[0], llr[1] + dim_y, llr[2] + dim_z],
                    'rhf': [llr[0] + dim_x, llr[1] + dim_y, llr[2] + dim_z],
                    'rlf': [llr[0] + dim_x, llr[1] + dim_y, llr[2]]  }
        return vertex


    def setState(self, state):

        if not state or not isinstance(state, State):
            return False
        else:
            self.state = state

        return True

    def getState(self):
        return state

    def setName(self, name):
            
        if not name or not isinstance(name, str):
            self.name = 'object_'+str(random.randint(1, 9999)) # hashing or radInt
        else:
            self.name = name

        return True

    
    def setId(self, id):
            
        if not id or not isinstance(id, int):
            self.id = random.randint(1, 999999) # hashing or radInt
        else:
            self.id = id

        return True
            

    
    def setDimension(self, dimension):
            
        if not General.checkDimension(dimension): # not dimension or not isinstance(dimension, list) and not len(dimension) == 3 or not isinstance( dimension[0], int) or not  isinstance( dimension[1], int) or not  isinstance( dimension[2], int) :
            self.dimension = [random.randint(1, 3), random.randint(1, 3), random.randint(1, 3) ] # xdim, ydim, zdim
        else:
            self.dimension = dimension

        return True


    def setCoord(self, coord):
            
        if not coord or not isinstance(coord, Coordinate):
            self.coord = Coordinate( random.randint(1, 99), random.randint(1, 99), random.randint(1, 99) ) # senza limiti
        else:
            self.coord = coord

        return True


    def isCollision(self, volume):
        """Return True if object is within volume"""
        # xd = dimension[0], yd = dimension[1], zd =dimension[2]
        # xvol_low = volume[0][0], yvol_low = volume[0][1], zvol_low = volume[0][2]
        # xvol_high = volume[1][0], yvol_high = volume[1][1], zvol_high = volume[1][2]
        # not intersection in x axes: x > xvol_high and x + xd < xvol_low
        # not intersection in y axes: y > yvol_high and y + yd < yvol_low
        # not intersection in z axes: z > zvol_high and z + zd < zvol_low
        # not interection -> one or more axis not intersection

        ## NOTA: volume = [ [xl, yl, zl],  [xh, yh, zh] ] dove xl, yl, zl <= xh, yh, zh

        if not General.checkVolume(volume): #not volume or not isinstance( volume, list ):
            raise Exception('Invalid parameters')

        pos = self.coord.getPosition()

        x_not_intersection =  pos[0] > volume[1][0] or pos[0] + self.dimension[0] < volume[0][0] 
        y_not_intersection =  pos[1] > volume[1][1] or pos[1] + self.dimension[1] < volume[0][1] 
        z_not_intersection =  pos[2] > volume[1][2] or pos[2] + self.dimension[2] < volume[0][2] 

        # not interection -> one or more axis not intersection
        if x_not_intersection or y_not_intersection or z_not_intersection:
            return False

        return True



    def getDistance(self, coord):
        """Return distance (d, xd, yd, zd) from object.coordinate to pos:[x, y, z]""" 

        if not coord or not isinstance(coord, Coordinate):
            return False       

        return self.coord.distance(coord)
        

    def getId(self):
        return self.id


    def getName(self):
        return self.name

    
    def getPosition(self):
        return self.coord.getPosition()


    def getDimension(self):
        return self.dimension

    def to_string(self):
        return 'Name: {0}  -  Id: {1}'.format(self.getName(), str(self.id))