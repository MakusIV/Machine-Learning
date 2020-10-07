import random
from Coordinate import Coordinate
import General
from State import State
from LoggerClass import Logger

# LOGGING --
 
logger = Logger(module_name = __name__, class_name = 'Object')

class Object:
    
    def __init__(self, dimension = (1, 1, 1), resilience = 100, coord = None, name = None, state = None ):


            self._name = None
            self._id = None
            self._dimension = dimension
            self._resilience = resilience # resistenza ad uno SHOT in termini di power (se shot power > resilence --> danno al sensore)            
            self._coord = coord
            self._state = None
            self.setState(state)

            if not name:
                self._name = General.setName('Object_Name')
                self._id = General.setId('Object_ID', None)
            else:
                self._name = name
                self._id = General.setId(name + '_ID', None)
                
            if not coord:
                self._coord = Coordinate(0, 0, 0)

    def evalutateDamage(self, energy, power):
        """Evalutate the damage on sensor and update state"""
        if power > self._resilience:
            damage = power - self._resilience# in realtà il danno dovrebbe essere proporzionale all'energia
            return self._state.decrementHealth( damage )
        
        return self.state.getHealth()


    def getVertex(self):

        llr = self.coord.getPosition()
        
        if len(self._dimension) == 3:
            dim_x = self._dimensione[0]
            dim_y = self._dimensione[1]
            dim_z = self._dimensione[2]
        
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
            self._state = State()
        else:
            self._state = state

        return True

    def getState(self):
        return self._state


    def setId(self, id):

        if not id:
            return False

        elif isinstance(id, str):
            self._id = id       
        
        else:
            self._id = str( id )       
            
        return True


    def setName(self, name):

        if not name:
            return False
        else:
            self._name = name

        return True
            

    
    def setDimension(self, dimension):
            
        if not General.checkDimension(dimension): # not dimension or not isinstance(dimension, list) and not len(dimension) == 3 or not isinstance( dimension[0], int) or not  isinstance( dimension[1], int) or not  isinstance( dimension[2], int) :
            return False
        else:
            self._dimension = dimension

        return True


    def setCoord(self, coord):
            
        if not coord or not isinstance(coord, Coordinate):
            return False
        else:
            self._coord = coord

        return True


    def isCollision(self, volume):
        """Return True if object's volume collide with volume"""
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

        pos = self._coord.getPosition()

        x_not_intersection =  pos[0] > volume[1][0] or pos[0] + self._dimension[0] < volume[0][0] 
        y_not_intersection =  pos[1] > volume[1][1] or pos[1] + self._dimension[1] < volume[0][1] 
        z_not_intersection =  pos[2] > volume[1][2] or pos[2] + self._dimension[2] < volume[0][2] 

        # not interection -> one or more axis not intersection
        if x_not_intersection or y_not_intersection or z_not_intersection:
            return False

        return True



    def getDistance(self, coord):
        """Return distance (d, xd, yd, zd) from object.coordinate to pos:[x, y, z]""" 

        if not coord or not isinstance(coord, Coordinate):
            return False       

        return self._coord.distance(coord)
        

    def getId(self):
        return self._id


    def getName(self):
        return self._name

    
    def getPosition(self):
        return self._coord.getPosition()

    def setPosition(self, position):
        self._coord.setPosition( position )


    def getDimension(self):
        return self._dimension

    def to_string(self):
        return 'Name: {0}  -  Id: {1}'.format(self.getName(), str(self._id))

    
    def checkObjectClass(self, object):
        """Return True if objects is a Object object otherwise False"""
        if not object or not isinstance(object, Object):
            return False
        
        return True

    def checkObjectList(self, objects):

        """Return True if objectsobject is a list of Object object otherwise False"""
        if objects and isinstance(objects, list) and all( isinstance(object, Object) for object in objects ):
            return True

        return False

     # vedi il libro
    def checkParam(self, name, dimension, resilience, state, coord ):
                
        # INSERISCI I TEST DI VERIFICA DELLE CLASSI NELLE CLASSI STESSE E ANCHE LA VERIFICA DELLE LISTE 

        if not name or not isinstance( name, str ) or not state or not isinstance( state, State ) or not coord or not isinstance( coord, Coordinate ) or not resilience or not isinstance( resilience, int )  or not( resilience <= 100 and resilience >= 0 ) or not General.checkDimension( dimension ):
            return False
            
        return True

    def getVolumePosition( self ):
        """Return the position of the object's volume"""
        
        position = self.getPosition()
        dimension = self.getDimension()
        volume_position = dict()

        for z in range( position[ 2 ], position[ 2 ] + dimension[ 2 ] ):           
           for y in range( position[ 1 ], position[ 1 ] + dimension[ 1 ] ):              
              for x in range( position[ 0 ], position[ 0 ] + dimension[ 0 ] ):
                  volume_position[ ( x, y, z ) ] = True

        return volume_position

    def getVolume( self ):
        """Return [ [ position ], [ position + dimensione ] ] """
        
        position = self.getPosition() 
        dimension = self.getDimension()

        return [ position, [ position[ 0 ] + dimension[ 0 ], position[ 1 ] + dimension[ 1 ], position[ 2 ] + dimension[ 2 ] ] ] 