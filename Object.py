import random
from Coordinate import Coordinate

class Object:

    def __init__(self, name = None, id = None, dimension = None, coord = None  ):

            self.name = None
            self.id = None
            self.dimension = None
            self.coord = None
                        
            if not(self.setName(name) and self.setId(id) and self.setDimension(dimension) and self.setCoord(coord)):
                raise Exception("Invalid parameters! Object not istantiate.")
            


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
            
        if not dimension or not isinstance(dimension, list) and not len(dimension) == 3 or not isinstance( dimension[0], int) or not  isinstance( dimension[1], int) or not  isinstance( dimension[2], int) :
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


    def isCollision(volume):
        """Return True if object is within volume"""
        pass

    def getDistance(pos):
        """Return distance (d, xd, yd, zd) from object to pos:(x, y, z)"""
        pass

    def getId(self):
        return self.id


    def getName(self):
        return self.name

    
    def getPosition(self):
        return self.coord.getPosition()



    def to_string(self):
        return 'Name: {0}  -  Id: {1}'.format(self.getName(), str(self.id))