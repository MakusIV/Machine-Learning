### General Methods

import random
from State import State
from Actuator import Actuator
from Sensor import Sensor
from AI import AI
from Obstacle import Obstacle

def checkState(state):

    if not state or not isinstance(state, State):
        return False
        
    return True

def checkEnvState(state):

    if not state or not isinstance(state, EnvState):
        return False
        
    return True

def checkSensor(sensor):

    if not sensor or not isinstance(sensor, Sensor):
        return False
        
    return True

def checkSensors(sensors):

    if not sensor or not isinstance(sensors, list) or any(not isinstance(item, Sensor), sensors):
        return False
        
    return True

def checkActuators(actuators):

    if not actuators or not isinstance(actuators, list) or any(not isinstance(item, Actuator), actuators):
        return False
        
    return True


def checkActuator(actuator):

    if not actuator or not isinstance(state, Actuator):
        return False
        
    return True


def checkObstacle(obstacle):

    if not obstacle or not isinstance(obstacle, Obstacle):
        return False
        
    return True

def checkObstacles(obstacles):

    if not obstacles or not isinstance(obstacles, list) or any(not isinstance(item, Obstacle), Obstacle):
        return False
        
    return True


def checkDimension(dimension):
    """ Return True if dimension is an list normalized as dimension:  dimension: [int dim_x, int dim_y, int dim_z]"""

    if not dimension or not isinstance(dimension, list) and not len(dimension) == 3 or not isinstance( dimension[0], int) or not  isinstance( dimension[1], int) or not  isinstance( dimension[2], int):
            return False
    
    return True


def checkVolume(volume):
    """ Return True if volume is an list normalized as volume:  volume: [ [ int x_low, int y_low, int z_low ], [ int x_high, int y_high, int z_high ] ]"""

    if not volume or not isinstance( volume, list ) or len(volume) != 2 or len(volume[0]) != 3  or len(volume[1]) != 3:
         return False
    
    elif not isinstance( volume[0][0], int ) or not isinstance( volume[0][1], int ) or not isinstance( volume[0][2], int ) or not isinstance( volume[1][0], int ) or not isinstance( volume[1][1], int ) or not isinstance( volume[1][2], int ):
             return False

    
    if volume[0][0] > volume[1][0] and volume[0][1] > volume[1][1] and volume[0][2] > volume[1][2]:
        return False
    
    return True


def setId(name, id):
            
    if not id or not isinstance(id, int):
        id = str(name) + '_#' + str( random.randint(1, 999999) )  # hashing or radInt
    else:
        id = str(name) + '_#' + str(id)
    
    return id


def setName(name):
            
        if not name or not isinstance(name, str):
            name = 'unamed_'+str(random.randint(1, 9999)) # hashing or radInt
        
        return name