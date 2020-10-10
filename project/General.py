### General Methods

import random
import logging
import os
import math

# LOGGING --
# non èpossibile usare la classe Logger per evitare le circular dependencies: Logger importa General e Geneal imprta Logger

logging.basicConfig( level = logging.DEBUG )
# Create a custom logger
logger = logging.getLogger( __name__ )

log_dir = os.path.join(os.path.normpath(os.getcwd()), 'logs')
log_fname = os.path.join(log_dir, 'log_General.log')


# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler( log_fname )
c_handler.setLevel( logging.DEBUG )
f_handler.setLevel( logging.ERROR )

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(funcName)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)


# VALUES

SENSOR_TYPE = ("radio", "infrared", "optical", "nuclear", "electric", "acoustics", "chemist")


# METHODS

def checkSensorType(type):
    
    if not type or not isinstance(type, str):
        return False

    for val in SENSOR_TYPE:

        if val == type:
            return True
    
    return False

def checkDimension(dimension):
    """ Return True if dimension is an list normalized as dimension:  dimension: [int dim_x, int dim_y, int dim_z]"""

    if not dimension or not ( isinstance(dimension, list) or isinstance(dimension, tuple) ) and not len(dimension) == 3 or not isinstance( dimension[0], int) or not  isinstance( dimension[1], int) or not  isinstance( dimension[2], int):
            return False
    
    return True


def checkVolume(volume):
    """ Return True if volume is an list normalized as volume:  volume: [ [ int x_low, int y_low, int z_low ], [ int x_high, int y_high, int z_high ] ]"""

    if not volume or not isinstance( volume, list ) or len(volume) != 2 or len(volume[0]) != 3  or len(volume[1]) != 3:
         return False
    
    elif not isinstance( volume[0][0], int ) or not isinstance( volume[0][1], int ) or not isinstance( volume[0][2], int ) or not isinstance( volume[1][0], int ) or not isinstance( volume[1][1], int ) or not isinstance( volume[1][2], int ):
             return False

    # LO ESCLUDO DAL TEST IN QUANTO IN UN CONTESTO RELATIVO CON COOORDINATE NEGATIVE I LIMITI SUPERIORI E INFERIORI DEL VOLUME SI INVERTONO ANCHE UTILIZZANDO ABS NON E' POSSIBILE GARANTIRE COERENZA (VEDI Sensibility.get_probability_of_perception)
    #if abs( volume[0][0] ) > abs( volume[1][0] ) and abs( volume[0][1] ) > abs( volume[1][1] ) and abs( volume[0][2] ) > abs( volume[1][2] ):
    #    return False
    
    return True


def setId(name, id):
            
    if not id or not isinstance(id, int):
        id = str( name ) + '_#' + str( random.randint( 1, 999999 ) )  # hashing or radInt

    else:
        id = str( name ) + '_#' + str( id )
    
    return id


def setName(name):

            
        if not name or not isinstance( name, str ):
            name = 'unamed_#' + str( random.randint( 1, 9999 ) ) # hashing or radInt

        else:
            name = name + '_#' + str( random.randint( 1, 9999 ) ) # hashing or radInt
        
        return name