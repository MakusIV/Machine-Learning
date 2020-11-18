# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'project')

from State import State
from Sensor import Sensor
from Sensibility import Sensibility
from Position_manager import Position_manager
from Object import Object
from LoggerClass import Logger


# LOGGING --
 
logger = Logger(module_name = __name__, class_name = 'Sensor_test')

def testClassSensor():

    result = True    
    sensor = Sensor( position = (0, 0, 0), range_max = (10, 10, 10), typ = "thermal" )


    if sensor._position != (0, 0, 0) or not sensor._sensibility or not isinstance(sensor._sensibility, Sensibility) or sensor._power != 100 or sensor._resilience != 100 or not sensor._name or not sensor._state or not sensor._type or sensor._type != 'thermal':
        print('Sensor Failed!! ', sensor._sensibility, sensor._power, sensor._resilience)
        result = False 
    
    sensor = Sensor( typ = "radio", position = (0, 0, 0), range_max = (100, 100, 100), accuracy=20, power=20, resilience=20, name='tullio' )

    if sensor._position != (0, 0, 0) or not sensor._sensibility or sensor._power != 20 or sensor._resilience != 20 or sensor._name != 'tullio' or not sensor._state or not sensor._type or sensor._type != 'radio':
        print('Sensor Failed!! ', sensor._sensibility, sensor._power, sensor._resilience, sensor._name, sensor._state)
        result = False 
    


    try:
        sensor = Sensor( position = (0, 0, 0), sensibility=-1, power=-1, resilience=-1, typ = "radio")
        
    except Exception:
        pass

    else:
        print( 'Sensor Failed!!  Not launch Exception', sensor._sensibility, sensor._power, sensor._resilience, sensor._name, sensor._state , sensor._type)
        result = False


    try:
        sensor = Sensor( position = (0, 0, 0), sensibility=10, power=1, resilience=101, typ = "radio")
        
    except Exception:
        pass

    else:
        print( 'Sensor Failed!!  Not launch Exception', sensor._sensibility, sensor._power, sensor._resilience, sensor._name, sensor._state, sensor._type )
        result = False


    
    # test Sensor.evalutateDamage( energy, power )
    sensor = Sensor( typ = "radio", position = (0, 0, 0), range_max=(50, 50, 50), power=50, resilience=50, accuracy=7)
    sensor.evalutateSelfDamage(power = 60)

    if sensor._state._health != 90:
        print('Sensor.evalutatSelfDamage(energy = 100, power = 60) Failed!! ', sensor._sensibility, sensor._power, sensor._resilience, sensor._name, sensor._state, sensor._state._health)
        result = False 
    

    # test checkSensorClass()

    if not Sensor.checkSensorClass(sensor, sensor):
        print('Sensor.checkSensorClass(sensor) Failed!! ', sensor._state, sensor._state._health)
        result = False 
    
    # test checkSensorList()

    sensors = [Sensor( typ = "radio", position = (0, 0, 0), range_max = (100, 100, 100) ), Sensor( typ = "radio", position = (0, 0, 0), range_max = (100, 100, 100)  ), Sensor( typ = "radio", position = (0, 0, 0), range_max = (100, 100, 100) ), Sensor( typ = "radio", position = (0, 0, 0), range_max = (100, 100, 100) )]

    if not Sensor.checkSensorList(sensor, sensors): 
        print('Sensor.checkSensorList(sensors) Failed!! ', sensors[0]._id, sensors[0]._state, sensors[0]._state._health)
        result = False

    
    sensors = [Sensor( typ = "radio", position = (0, 0, 0), range_max = (100, 100, 100) ), Sensor( typ = "radio", position = (0, 0, 0), range_max = (100, 100, 100) ), list(), Sensor( typ = "radio", position = (0, 0, 0), range_max = (100, 100, 100) )]

    if Sensor.checkSensorList(sensor, sensors):
        print('Sensor.checkSensorList(sensors) Failed!! ', sensors[0]._id, sensors[0]._state, sensors[0]._state._health)
        result = False  
    
    # test sensor.perception()-test with object emissivity > sensor emissivity_perception: sensor should be percept object
    num_objects = 100
    num_objects_for_linear = int( (num_objects)**(1/3) )    
    object_dimension = (3, 2, 1)
    separation_from_objects = 7
    incr = ( object_dimension[0] + separation_from_objects, object_dimension[2] + separation_from_objects, object_dimension[2] + separation_from_objects )
    dim_linear = ( num_objects_for_linear * incr[0], num_objects_for_linear * incr[2], num_objects_for_linear * incr[2] )
    bound = ( int( dim_linear[0]/2 ), int( dim_linear[1]/2 ), int( dim_linear[2]/2 ) )
    logger.logger.info("num_objects:{0},  num_objects_for_linear:{1},  object_dimension:{2},  separation_from_objects:{3},  incr:{4},  dim_linear:{5},  bound:{6}".format( num_objects,  num_objects_for_linear, object_dimension, separation_from_objects, incr, dim_linear, bound) )

    pm = Position_manager(name='position manager', limits = [ [ -bound[0] , -bound[1], -bound[2]], [ bound[0], bound[1], bound[2] ] ])

    for z in range(-bound[2], bound[2], incr[2]):
        for y in range(-bound[1], bound[1], incr[1]):
            for x in range(-bound[0], bound[0], incr[0]):
                pm.insertObject( position = (x, y, z), obj = Object(name = 'New_'+str( int(  ((bound[0] + x)%dim_linear[0])/incr[0] + num_objects_for_linear*((bound[1] + y)%dim_linear[1])/incr[1] + num_objects_for_linear*num_objects_for_linear*((bound[2] + z)%dim_linear[2])/incr[2] ) ), dimension = ( object_dimension[0], object_dimension[1], object_dimension[2]) , emissivity = {"radio": 5, "thermal": 0, "optical": 0, "nuclear": 0, "electric": 0, "acoustics": 0, "chemist": 0 } ) )
    
    sensor.perception( pm, sensor._position )

    # test sensor.perception()-test with object emissivity < sensor emissivity_perception: sensor not should be percept object
    num_objects = 100
    num_objects_for_linear = int( (num_objects)**(1/3) )    
    object_dimension = (3, 2, 1)
    separation_from_objects = 7
    incr = ( object_dimension[0] + separation_from_objects, object_dimension[2] + separation_from_objects, object_dimension[2] + separation_from_objects )
    dim_linear = ( num_objects_for_linear * incr[0], num_objects_for_linear * incr[2], num_objects_for_linear * incr[2] )
    bound = ( int( dim_linear[0]/2 ), int( dim_linear[1]/2 ), int( dim_linear[2]/2 ) )
    logger.logger.info("num_objects:{0},  num_objects_for_linear:{1},  object_dimension:{2},  separation_from_objects:{3},  incr:{4},  dim_linear:{5},  bound:{6}".format( num_objects,  num_objects_for_linear, object_dimension, separation_from_objects, incr, dim_linear, bound) )

    pm = Position_manager(name='position manager', limits = [ [ -bound[0] , -bound[1], -bound[2]], [ bound[0], bound[1], bound[2] ] ])

    for z in range(-bound[2], bound[2], incr[2]):
        for y in range(-bound[1], bound[1], incr[1]):
            for x in range(-bound[0], bound[0], incr[0]):
                pm.insertObject( position = (x, y, z), obj = Object(name = 'New_'+str( int(  ((bound[0] + x)%dim_linear[0])/incr[0] + num_objects_for_linear*((bound[1] + y)%dim_linear[1])/incr[1] + num_objects_for_linear*num_objects_for_linear*((bound[2] + z)%dim_linear[2])/incr[2] ) ), dimension = ( object_dimension[0], object_dimension[1], object_dimension[2]) , emissivity = {"radio": 0, "thermal": 0, "optical": 0, "nuclear": 0, "electric": 0, "acoustics": 0, "chemist": 0 } ) )
    
    sensor.perception( pm, sensor._position )


    return result

print("Sensor class test result:", testClassSensor())
