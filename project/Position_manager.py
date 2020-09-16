### The Manager of object position in the World
#import numpy as np
import General
import random
from Coordinate import Coordinate

class Position_manager:

    """ Manager of objects position
        Nota: usa un dictionary con key = Coordinate object quindi per utilizzare un elemento del dizionario
        mediante la Key devi utilizzare lo stesso oggetto non istanziare un altro oggetto con gli stessi valori
        """
    def __init__( self, name = 'Fuffy', limits = [ [-50, -50, -50], [50, 50, 50] ] ):
        self.name = name
        self.limits = limits 
        self.pos = {} ### key:coord, value:obj
        self.pos_ = [] #[    [ obj000, obj001, obj002 ], [  obj  pos_[1][1][1]= 

    def getName(self):
        return self.name

    def setName(self, name):

        if not name:
            return False

        self.name = name
        return True

    def getLimits(self):
        return self.limits

    def setLimits(self, limits):
        self.limits = limits
        return True

        
    def insertObject( self, index, obj ):
        """ Insert [obj, coord] in position dictionary and return true. If coord is out of limits or obj is None or exist an object in coord then return False"""        
        
        if not index or not obj:
            return False

        res, _ = self.inLimits(index, self.limits)

        if not res:
            return False

        if self.pos.get(index):
            return False

        obj.coord.setPosition(index)
        
        self.pos[index] = obj
        return True

    
    
    def removeObject( self, obj ):
        """ Remove [obj] in position dictionary and return index position. If obj not exists return False"""
        
        if not obj:
            return False
        
        index = self.searchObject(obj)

        if not index:
            return False

        self.pos.pop( index ) 
        return index


    def removeObjectAtCoord( self, index ):
        """ Remove if exist obj in index position and return index. If obj not exists return False"""
        
        if not index:
            return False
                
        obj = self.pos.pop( index, None)

        if not obj:
            return False

        self.pos[ index ] = None        
        return obj


    def changeObject(self, index, new_obj):
        """ Update obj, in index position dictionary and return old object if exists. If index or obj is None or index is out of limits return False"""
        
        if not index or not new_obj or not self.inLimits(index, self.limits):
            return False

        result = self.pos.get( index )

        if not result:
            return False

        self.pos[ index ] = new_obj
        return result 

    
    def getObjectAtCoord( self, index ):
        """ Return obj at coord index. Return false if obj not presents"""

        if not index:
            return False
        
        obj = self.pos.get( index )

        if not obj:
            return False

        return obj


    def getObject( self, obj ):
        """ Return obj at coord index. Return false if obj not presents"""

        if not obj:
            return False

        index = self.searchObject( obj )
        
        if not index:
            return False

        return self.pos.get( index )


    def searchObject( self, obj ):
        """ Search [obj] in position dictionary and return coord position. If obj not exists return False"""

        try:
            index = list( self.pos.keys() )[ list( self.pos.values() ).index( obj ) ]

        except ValueError:
            return False

    
        return index


    def listObject( self ):
        """ Return a list of obj existents in position manager. If obj not exists return False"""

        try:
            index = list( self.pos.values() )

        except ValueError:
            return False

        if not index:
            return False

        return index


    def getObjectInVolume(self, volume, dimension = None):
        """ Return {  (x,y,z), obj } portion within volume. Return false if objects not presents within volume"""
        
        if not volume:
            return False

        if not dimension:
            dimension = [3, 3, 3]

        if len(self.pos) >= ( volume[1][0] - volume[0][0] + 1 ) * ( volume[1][1] - volume[0][1] + 1 ) * ( volume[1][2] - volume[0][2] + 1 ):
            return self._getObjectInVolumeFromObjectList(volume)
        else:
            return self._getObjectInVolumeFromVolumeIteration(volume, dimension)

        return False

    def _getObjectInVolumeFromObjectList(self, volume):
        """ Return {  (x,y,z), obj } portion within volume. Return false if objects not presents within volume"""
        # volume = ( (xl, yl, zl), (xh, yh, zh) )
        # si basa sulla lista degli oobject istanziati, quindi più efficente della getObectVolum() se il di ricerca  in termini di posizioni
        # è inferiore al numero di oggetti istanziati: lista di 1000 oggetti equivale ad un volume di ricerca di 10x10x10 posizioni
        # considera comunque che una ricerca planare x,y su livello 0 (z =0): volume = [ [0, 0, 0], [10, 5, 0] ] richiederebbe solo 50 iterazioni
        # mentre questa funzione itera sempre tutta la lista di oggetti.


        if not volume:
            return False

        objects = self.listObject()

        if not objects:
            return False

        detected = [ obj for obj in objects if obj.isCollision(volume)]

        if not detected or len(detected) == 0:
            return False

        return detected




    def _getObjectInVolumeFromVolumeIteration(self, volume, dimension):
        """ Return {  (x,y,z), obj } portion within volume. Return false if objects not presents within volume"""
        # volume = ( (xl, yl, zl), (xh, yh, zh) ), dimension = [ xd, yd, zd]
        # nota: valuta la presenza di un object solo con la coordinata di riferimento senza considerare le sue dimensioni
        # nota: devi modificare considerando il volume occupaodall'oggetto. Oneroso computazionalmente

        detected = {}

        self.normalizeVolume( volume )

        for z in range(volume[0][2], volume[1][2] + 1 + dimension[2]):
           
           for y in range(volume[0][1], volume[1][1] + 1 + dimension[1]):
              
              for x in range(volume[0][0], volume[1][0] + 1 + dimension[0]):
                    
                    obj = self.getObjectAtCoord( ( x, y, z) )
                    
                    if obj:
                        detected[ (x, y, z) ] = obj

        if len( detected ) == 0:
            return False

        return detected




    def normalizeVolume(self, limits):  

        result = False      

        if limits[0][0] < self.limits[0][0]:
            limits[0][0] = self.limits[0][0]
            result = True

        if limits[0][1] < self.limits[0][1]:
            limits[0][1] = self.limits[0][1]
            result = True

        if limits[0][2] < self.limits[0][2]:
            limits[0][2] = self.limits[0][2]
            result = True

        if limits[1][0] > self.limits[1][0]:
            limits[1][0] = self.limits[1][0]
            result = True

        if limits[1][1] > self.limits[1][1]:
            limits[1][1] = self.limits[1][1]
            result = True

        if limits[1][2] > self.limits[1][2]:
            limits[1][2] = self.limits[1][2]
            result = True

        return result



    
    def getObjectInRange(self, coord, range, dimension):

        """ Return {  (x,y,z), obj } portion within volume positionated in coord and range dimension. Return false if objects not presents within volume"""
        # range = [int] or [int, int, int]
        # volume = ( (coord.x, coord.y, coord.z), (coord.x + range, coord.y + range, coord.z + range) )

        if not range or not coord or not isinstance(range, list) or not isinstance(coord, Coordinate):
            return False

        lenRange = len(range)

        if not ( lenRange == 1 or lenRange == 3 ):
            return False
        
        
        if lenRange == 1 and isinstance(range[0], int):
            
            volume = [ [ coord.x, coord.y, coord.z ], [ coord.x + range[0], coord.y + range[0], coord.z + range[0] ] ]
            
        elif isinstance(range[0], int) and isinstance(range[1], int) and isinstance(range[2], int):

            volume = [ [ coord.x, coord.y, coord.z ], [ coord.x + range[0], coord.y + range[2], coord.z + range[2] ] ]
        
        else:
            return False
        
        return self.getObjectInVolume(volume, dimension)
        
        

    def getRandomCoord(self):
        """Return an instance of Coordinate with random position inbound limits"""
        x = random.randint(self.limits[0][0], self.limits[1][0])
        y = random.randint(self.limits[0][2], self.limits[1][2])
        z = random.randint(self.limits[0][2], self.limits[1][2])

        return Coordinate(x = x, y = y, z = z)



    def inLimits(self, index, limits):
        """
        return 2D-Array with state of corrispective coordinate:
        limits = [ [x-min, y_min, z_min], [x-max, y_max, z_max] ] and return true if
        presents a false in 2D array
        """
        
        out_limit = [ [False, False, False], [False, False, False] ]
        result = True

        if index[0] > limits[1][0]:
            out_limit[1][0] = True
            result = False
        
        if index[1] > limits[1][1]:
            out_limit[1][1] = True
            result = False
        
        if index[2] > limits[1][2]:
            out_limit[1][2] = True
            result = False

        if index[0] < limits[0][0]:
            out_limit[0][0] = True
            result = False
        
        if index[1] < limits[0][1]:
            out_limit[0][1] = True
            result = False
        
        if index[2] < limits[0][2]:
            out_limit[0][2] = True
            result = False
                
        return result, out_limit


    def clean(self):
        """Remove all object istantiate in enviroments"""
        self.pos.clear()
        return True



    def show(self):
        """print list of object instantiate in Enviroments"""        
        for k, v in self.pos.items():
            print('key: ( {0} )  -  value: ( {1} )'.format(k, v.to_string()))
        
        