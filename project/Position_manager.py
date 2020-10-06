### The Manager of object position in the World
#import numpy as np
import General
import random
from Coordinate import Coordinate
from Automa import Automa
from LoggerClass import Logger
from Object import Object

# LOGGING --
 
logger = Logger(module_name = __name__, class_name = 'Position_manager')





class Position_manager:

    """ Manager of objects position
        Nota: usa un dictionary con key = Coordinate object quindi per utilizzare un elemento del dizionario
        mediante la Key devi utilizzare lo stesso oggetto non istanziare un altro oggetto con gli stessi valori
        """
    def __init__( self, name = 'Fuffy', limits = [ [-50, -50, -50], [50, 50, 50] ] ):
        self.name = name
        self.limits = limits 
        self.pos = {} # index:(x,y,z), value:obj
        self.map = {} # index:(x, y, z), value: id_obj 
        logger.logger.info("Position Manager created")

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
        
        dimension = obj.getDimension()
        mapped_cell = []

        for z in range( index[ 2 ], index[ 2 ] + dimension[ 2 ] ):
            for y in range( index[ 1 ], index[ 1 ] + dimension[ 1 ] ):
                for x in range( index[ 0 ], index[ 0 ] + dimension[ 0 ] ): 
                    
                    if self.map.get( ( x, y, z ) ):# verifica se la cella corrente è già mappata con un object id                   
                        
                        for i in mapped_cell:#  elimina le celle mappate
                            self.map.pop(i)

                        logger.logger.debug( "position_busy @:{0} exist obj: {1} ".format( index, self.map.get( ( x, y, z ) ) ) )
                        return False
                    
                    mapped_cell.append( (x, y, z) )
                    self.map[ ( x, y, z ) ] = obj.getId()
                    logger.logger.debug( "mapped obj: {0} at position: {1} ".format( obj.getId(), ( x, y, z ) ) )


        obj._coord.setPosition( index ) # aggiorna la coord dell'obj con la posizione d'inserimento      
        self.pos[ index ] = obj

        logger.logger.debug( "inserted obj: {0} at position: {1} ".format( obj.getName(), index ) )

        return True

    
    
    def removeObject( self, obj ):
        """ Remove [obj] in position dictionary and return index position. If obj not exists return False"""
        
        if not obj:
            return False
        
        obj_data = self.searchObject(obj)

        if not obj_data or obj_data[1] != obj:
            return False
        
        index = obj_data[0]

        self.pos.pop( obj_data[0] ) # rimuove l'obj dal position dict
        dimension = obj.getDimension()

        # rimuove gli id dell'obj dalla map dict
        for z in range( index[ 2 ], index[ 2 ] + dimension[ 2 ] ):
            for y in range( index[ 1 ], index[ 1 ] + dimension[ 1 ] ):
                for x in range( index[ 0 ], index[ 0 ] + dimension[ 0 ] ):
                    cell = self.map.get( ( x, y, z ) )
                    self.map.pop( (x, y, z) )
                    

                    if not cell or cell != obj.getId():
                        logger.logger.error( "exist obj: {0} not present at map position: {1} ".format( obj.getId(), index ) )
                        
                    
        logger.logger.debug( "removed obj: {0} @: {1}".format( obj.getId(), index ) )
        return index


    def removeObjectAtCoord( self, index ):
        """ Remove if exist obj in index position and return index. 
            If obj not exists return False"""
        
        if not index:
            return False
                
        obj_id = self.map.get( index )

        if not obj_id:
            return False
        
        obj_data = self.searchObject( obj_id )

        if obj_data and obj_data[0] and obj_data[1]:
            self.pos.pop( obj_data[0] ) # rimuove dal pos dict l'obj
            dimension = obj_data[ 1 ].getDimension()

            # rimuove gli id dell'obj dalla map dict
            for z in range( index[ 2 ], index[ 2 ] + dimension[ 2 ] ):
                for y in range( index[ 1 ], index[ 1 ] + dimension[ 1 ] ):
                    for x in range( index[ 0 ], index[ 0 ] + dimension[ 0 ] ):
                        cell = self.map.get( ( x, y, z ) )
                        
                        if not cell or cell != obj_data[ 1 ].getId():
                            logger.logger.error( "exist obj: {0} not present at map position: {1} ".format( obj_id, (x, y, z) ) )
                            
                        self.map.pop( (x, y, z) )

        logger.logger.debug( "removed obj: {0} @: {1}".format( obj_data[1].getId(), index ) )
        return obj_data[1]


        


    def changeObject(self, index, new_obj):
        """ Insert new_obj in index position of pos dictionary and remove a previous object. Return previous object. 
            If index or obj is None or index is out of limits or a previous object not existens return False"""
        
        if not index or not new_obj or not self.inLimits(index, self.limits):
            return False

        previous_obj = self.getObjectAtCoord( index )

        if previous_obj:
            self.removeObject( previous_obj )
            self.insertObject( index, new_obj)
            logger.logger.debug( "Changed obj: {0} with obj: {1} @: {2}".format( new_obj.getId(), previous_obj.getId(), index ) )
            return previous_obj 
        
        logger.logger.debug( "Not changed obj: {0} @: {1}, because not exists a previous object in that position".format( new_obj.getId(), index ) )
        return False


    def moveObject(self, index, obj):
        """ Move obj in index free position in pos dictionary and return True. 
            If index or obj is None or index is out of limits or a previous object existens return False"""
        
        if not index or not obj or not self.inLimits(index, self.limits):
            return False

        previous_obj = self.getObjectAtCoord( index )

        if not previous_obj:
            previous_pos = obj.getPosition()
            self.removeObject(obj)            
            self.insertObject( index, obj)
            logger.logger.debug( "Moved obj: {0} from: {1} to: {2}".format( obj.getId(), previous_pos, index ) )
            return True 
        
        logger.logger.debug( "Not moved obj: {0} from: {1} to: {2}, because exists an object in that position".format( obj.getId(), previous_pos, index ) )
        return False
    
    
    def getObjectAtCoord( self, index ):
        """ Return obj at index. Return false if obj not presents @ index"""

        if not index:
            return False
        
        obj = self.pos.get( index )

        if obj:
            logger.logger.debug( "detected @:{0} obj_id: {1} ".format( index, obj.getId() ) )
            return obj

        obj_id = self.map.get( index )

        if obj_id:
            logger.logger.debug( "detected @:{0} obj_id: {1} ".format( index, obj_id ) )
            return self.pos.get( index )
                                            
        logger.logger.debug( "obj not detected @ {0}".format( index ) )

        return False


    def getObject( self, obj ):
        """ Return obj if exists in pos dictionary. Return false if obj not presents
            param obj = obj, obj.id"""

        obj_searched = self.searchObject( obj )

        if not obj_searched:
            return False

        return obj_searched[1]
    
        


    def searchObject( self, obj ):
        """ Search obj in pos dictionary and return (obj position, obj). If obj not exists return False
            param obj = obj, obj.id"""

        if obj and isinstance(obj, Object):
            return self.getIndexWithObject( obj )            
            
        elif obj and isinstance(obj, str):
            return self.getObjectWithId( obj )
        
        return False


    def getIndexWithObject( self, obj ):
        """Return the (position, object) of the object"""
        
        if not obj:
            return False
        
        try:
            index = tuple( self.pos.keys() )[ list( self.pos.values() ).index( obj ) ]
            return ( index, obj )
        
        except ValueError:
            return False
    

    def listObject( self ):
        """ Return a list of obj existents in position manager. If obj not exists return False"""

        try:
            obj = list( self.pos.values() )

        except ValueError:
            return False

        if not obj:
            return False

        return obj

    
    def listAutoma( self ):
        """ Return a list of Automa existents in position manager. If Automa not exists return False"""
        # da testare
        objs = self.listObject()

        if not objs:
            return False
        
        automas = [obj for obj in objs if isinstance(obj, Automa)]

        if not automas or len(automas)==0:
            return False
        
        return automas




    def isNotMoreAutoma( self ):
        """ Return True if not lesser of one Automa exists in posMng"""        
        objs = self.listObject()        

        return any( isinstance(item, Automa) for item in objs)


    def getObjectInVolume(self, volume):
        """ Return {  (x,y,z), obj } portion within volume. Return false if objects not presents within volume"""
        
        if not volume:
            return False
        # se la dimensione della lista è inferiore al numero di iterazioni del loop che scandisce tutte le posizioni del volume        
        if len( self.pos ) >= ( volume[1][0] - volume[0][0] + 1 ) * ( volume[1][1] - volume[0][1] + 1 ) * ( volume[1][2] - volume[0][2] + 1 ):
            return self._getObjectInVolumeFromObjectList( volume ) # itera la pos dict

        else:
            return self._getObjectInVolumeFromVolumeIteration( volume ) # itera le posizioni del volume



    def _getObjectInVolumeFromObjectList(self, volume):
        """ Return {  (x,y,z), obj } portion within volume. Return false if objects not presents within volume"""
        # volume = ( (xl, yl, zl), (xh, yh, zh) )
        # si basa sulla lista degli oobject istanziati, quindi più efficente della getObectVolum() se il di ricerca  in termini di posizioni
        # è inferiore al numero di oggetti istanziati: lista di 1000 oggetti equivale ad un volume di ricerca di 10x10x10 posizioni
        # considera comunque che una ricerca planare x,y su livello 0 (z =0): volume = [ [0, 0, 0], [10, 5, 0] ] richiederebbe solo 50 iterazioni
        # mentre questa funzione itera sempre tutta la lista di oggetti.


        if not volume:
            return False

        detected = {}
        objects = self.listObject()

        if not objects:
            return False

        detected =  { obj.getPosition(): obj for obj in objects if obj.isCollision(volume) } 

        if len(detected) == 0:
            return False

        return detected




    def _getObjectInVolumeFromVolumeIteration(self, volume, dimension):
        """ Return {  (x,y,z), obj } portion within volume. Return false if objects not presents within volume"""
        # 
        # volume = ( (xl, yl, zl), (xh, yh, zh) ), dimension = [ xd, yd, zd]
        # nota: valuta la presenza di un object in un determinato volume considerando la dimensione presunta dell'oggetto.
        # In sostanza se la dimensione volumetrica dell'oggetto è più grande di quella stimata, questo metodo protrebbe non 
        # riscontrare la presenza di un oggetto in un volume dove una parte di esso è invece presente.
        
        detected = {}
        exclude_position = dict()

        self.isNormalizedVolume( volume )

        for z in range(volume[0][2], volume[1][2] + 1 + dimension[2]):           
           for y in range(volume[0][1], volume[1][1] + 1 + dimension[1]):              
              for x in range(volume[0][0], volume[1][0] + 1 + dimension[0]):

                    if not exclude_position[ ( x, y, z ) ]:
                        obj_id = self.map.get ( (x, y, z) )

                        if obj_id:
                            detected[ (x, y, z) ] = self.getObjectWithId( obj_id )
                            exclude_position = { **exclude_position, **detected[ (x, y, z) ][1].getVolumePosition() }

        if not detected or len( detected ) == 0:
            return False

        return detected


    def checkMap( self, index ):
        """Return id object if map(index) contains an id, otherwise False"""
        id_obj = self.map.get( index )

        if id_obj:
            return id_obj

        return False


    def getObjectWithId( self, id ):
        """Return (position, object) with object.id = id, otherwise False"""
        try:
            obj_searched = {  obj_.getId(): obj_ for obj_ in self.pos.values() }.get( id )
            index = obj_searched.getPosition()
            return (index, obj_searched)

        except ValueError:
            return False
        


    def isNormalizedVolume(self, limits):  

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
        
        