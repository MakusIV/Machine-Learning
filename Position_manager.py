### The Manager of object position in the World
import numpy as np

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


    
    def getObjectInVolume(self, limits):
        """ Return {  (x,y,z), obj } portion within limits. Return false if objects not presents within volume"""
        # volume = ( (xl, yl, zl), (xh, yh, zh) )

        detected = {}

        self.normalizeVolume(limits)

        for z in range(limits[0][2], limits[1][2] + 1):
           
           for y in range(limits[0][1], limits[1][1] + 1):
              
              for x in range(limits[0][0], limits[1][0] + 1):
                    
                    obj = self.getObjectAtCoord( ( x, y, z) )
                    
                    if obj:
                        detected[(x, y, z)] = obj

        if len( detected ) == 0:
            return False

        return detected


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


    def show(self):
        
        for k, v in self.pos.items():
            print('key: ( {0} )  -  value: ( {1} )'.format(k, v.to_string()))
        
        