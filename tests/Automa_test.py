# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'project')

from State import State
from Automa import Automa
from Sensor import Sensor
from Actuator import Actuator
from Coordinate import Coordinate
from Position_manager import Position_manager
from Object import Object

from LoggerClass import Logger


# LOGGING --
 
logger = Logger(module_name = __name__, class_name = 'Automa_test')




def testClassAutoma():

    result = True
    # actuator(position, range_max, typ, power = 100,  resilience = 100, delta_t = 0.01, name = None, state = None)
    #name = 'Automa', dimension = [1, 1, 1], resilience = 10, state = State(run = True), ai = AI(), coord = None, sensors= None, actuators = None      
    coord = Coordinate( 0, 0, 0 )
    sensors = [ Sensor( typ = "radio", position = coord.getPosition(), range_max = (100, 100, 100) ), Sensor( typ = "optical", position = coord.getPosition(), range_max = (100, 100, 100) ), Sensor( typ = "thermal", position = coord.getPosition(), range_max = (100, 100, 100) )]
    actuators = [ Actuator( position = coord.getPosition(), range_max = ( 10, 10, 10 ), class_ = "mover", typ = "crawler", power = 100,  resilience = 100, delta_t = 0.01 ), Actuator( position = coord.getPosition(), range_max = ( 10, 10, 10 ), class_ = "mover", typ = "crawler", power = 100,  resilience = 100, delta_t = 0.01 ) ]
    automa = Automa(coord = coord, sensors = sensors, actuators = actuators)
    
    
    if automa._name != 'Automa' or automa._dimension != [1, 1, 1] or automa._resilience != 100 or automa._power != 100 or not automa._state or not isinstance(automa._state, State) or not automa._state.isRunning():
        print('Automa Failed!! ', automa._name, automa._dimension, automa._resilience, automa._state)
        result = False 
    

    # test: automa.eval_actuators_activation( action )
    #
    action = [ 'move', (10, 10, 10) ] #(action_type, position or object) 
    actuators_activation = automa.eval_actuators_activation( action )

    if not actuators_activation or not isinstance(actuators_activation, list) or not actuators[0].checkActuatorList( actuators_activation[0] ) or actuators_activation[1] != 'move' or actuators_activation[2] != ( 10, 10, 10 ):
        print('Automa.eval_actuators_activation( action ) Failed!!', actuators_activation[0], actuators_activation[1])
        result = False 
    

    action(self, request_action)
    #"""Activates Actuators for execution of Action. Return action informations."""
    #action_info: le informazioni dopo l'attivazione degli attuatori e lo stato degli stessi( classe)
    # actions_info = [] # (action_type, position, object)
    


    # test: automa.percept( pm )
    #     
    # create positione manager for manage enviroments, create object and populate pm
    num_objects = 100
    num_objects_for_linear = int( (num_objects)**(1/3) )    
    object_dimension = (3, 2, 1)
    separation_from_objects = 7
    incr = ( object_dimension[0] + separation_from_objects, object_dimension[2] + separation_from_objects, object_dimension[2] + separation_from_objects )
    dim_linear = ( num_objects_for_linear * incr[0], num_objects_for_linear * incr[2], num_objects_for_linear * incr[2] )
    bound = ( int( dim_linear[0]/2 ), int( dim_linear[1]/2 ), int( dim_linear[2]/2 ) )
    logger.logger.info( "num_objects:{0},  num_objects_for_linear:{1},  object_dimension:{2},  separation_from_objects:{3},  incr:{4},  dim_linear:{5},  bound:{6}".format( num_objects,  num_objects_for_linear, object_dimension, separation_from_objects, incr, dim_linear, bound ) )

    pm = Position_manager( name ='position manager', limits = [ [ -bound[0] , -bound[1], -bound[2]], [ bound[0], bound[1], bound[2] ] ] )

    for z in range(-bound[2], bound[2], incr[2]):
        for y in range(-bound[1], bound[1], incr[1]):
            for x in range(-bound[0], bound[0], incr[0]):
                
                if z == -bound[2] and y == -bound[1] and x == -bound[0]:
                    pm.insertObject( position = (x, y, z), obj = automa )    
                else:
                    pm.insertObject( position = (x, y, z), obj = Object(name = 'New_'+str( int(  ((bound[0] + x)%dim_linear[0])/incr[0] + num_objects_for_linear*((bound[1] + y)%dim_linear[1])/incr[1] + num_objects_for_linear*num_objects_for_linear*((bound[2] + z)%dim_linear[2])/incr[2] ) ), dimension = ( object_dimension[0], object_dimension[1], object_dimension[2]) , emissivity = {"radio": 5, "thermal": 0, "optical": 5, "nuclear": 0, "electric": 0, "acoustics": 0, "chemist": 0 } ) )
    
    
    obj_list = automa.percept( pm )

    if len( obj_list ) == 0 or not isinstance( obj_list, list) or any( False for obj in obj_list if not isinstance( obj, Object ) ):
        print('Automa.percept() Failed len(object_list) = 0 !! ', automa._id, obj_list)
        result = False 
    





    return result

print("Automa class test result:", testClassAutoma())