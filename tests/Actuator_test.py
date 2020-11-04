
# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'project')
from Actuator import Actuator
import General
from LoggerClass import Logger
from Automa import Automa
from Position_manager import Position_manager
from Sensor import Sensor
from Object import Object
from Coordinate import Coordinate


# LOGGING --
 
logger = Logger(module_name = __name__, class_name = 'Actuator_test')

def testClassActuator():

    result = True 

    #position, range_max, class_, typ, power = 100,  resilience = 100, delta_t = 0.01, name = None   
    actuator = Actuator( position = ( 0, 0, 0 ), range_max = ( 100, 100, 100 ), class_ = 'mover', typ = '2-legs' )


    if actuator._position != ( 0, 0, 0 ) or not actuator._name or actuator._power != 100 or actuator._resilience != 100 or not actuator._state or actuator._delta_t != 0.01 :
        print('Actuator Failed!! ', actuator._position, actuator._name, actuator._power, actuator._resilience, actuator._delta_t)
        result = False 
    
    

    try:
        actuator = Actuator( position = (0, 0, 0), range_max = 1, class_ = 'mover', typ = '2-legs' )

        
    except Exception:
        pass

    else:
        print('Actuator Failed!! Not launch exception for not valid range_max parameter 1', actuator._range, actuator._name, actuator._power, actuator._resilience, actuator._delta_t)
        result = False


    try:
        actuator = Actuator( position = (0, 0, 0), range_max = (1, 1, -1), class_ = 'mover', typ = '2-legs', power = 100 )
        
    except Exception:
        pass

    else:
        print('Actuator Failed!! Not launch exception for not valid range_max parameter (1, 1, -1)', actuator._range, actuator._name, actuator._power, actuator._resilience, actuator._delta_t)
        result = False


    try:
        actuator = Actuator( position = (0, 0, 0), range_max = (10, 10, 10), class_ = 'mover', typ = '2-foot', power = 100 )
        
    except Exception:
        pass

    else:
        print('Actuator Failed!! Not launch exception  for not valid typ parameter', actuator._class, actuator._type, actuator._name, actuator._power, actuator._resilience, actuator._delta_t)
        result = False




    try:
        actuator = Actuator( position = (0, 0, 0), range_max = (10, 10, 10), class_ = 'object_pusher', typ = '2-legs', power = 100 )
        
    except Exception:
        pass

    else:
        print('Actuator Failed!! Not launch exception  for not valid class parameter', actuator._class, actuator._type, actuator._name, actuator._power, actuator._resilience, actuator._delta_t)
        result = False

    
    try:
        actuator = Actuator( position = (0, 0, 0), range_max = (10, 10, 10), class_ = 'object_hitter', typ = '2-legs', power = 100 )
        
    except Exception:
        pass

    else:
        print('Actuator Failed!! Not launch exception  for not valid class parameter typ not in that class', actuator._class, actuator._type, actuator._name, actuator._power, actuator._resilience, actuator._delta_t)
        result = False


    # test Actuator.evalutateDamage( energy, power )

    actuator = Actuator( position = (0, 0, 0), range_max = (50, 50, 50), class_ = 'mover', typ = '2-legs', power = 50, resilience = 50 )
    actuator.evalutateSelfDamage(energy = 100, power = 60)

    if actuator._state._health != 90:
        print('Actuator.evalutatSelfDamage(energy = 100, power = 60) Failed!! ', actuator._power, actuator._resilience, actuator._name, actuator._state, actuator._state._health)
        result = False 
    

    if not actuator.isOperative():
        print('Actuator.isOperative() Failed!! ', actuator._state, actuator._state._run)
        result = False 
    

    # test checkActuatorClass()

    if not Actuator.checkActuatorClass(actuator, actuator):
        print('Actuator.checkActuatorClass(sensor) Failed!! ', actuator._state, actuator._state._health)
        result = False 
    
    # test checkActuatorList()

    actuators = [ Actuator( position = ( 0, 0, 0 ), range_max = ( 100, 100, 100 ), class_ = 'mover', typ = '2-legs' ), Actuator( position = ( 0, 0, 0 ), range_max = ( 100, 100, 100 ), class_ = 'mover', typ = '2-legs' ), Actuator( position = ( 0, 0, 0 ), range_max = ( 100, 100, 100 ), class_ = 'mover', typ = '2-legs' ) ]

    if not Actuator.checkActuatorList(actuator, actuators): 
        print('Actuator.checkSensorList(sensors) Failed!! ', actuators[0]._id, actuators[0]._state, actuators[0]._state._health)
        result = False

    

    actuators = [ Actuator( position = ( 0, 0, 0 ), range_max = ( 100, 100, 100 ), class_ = 'mover', typ = '2-legs' ), Actuator( position = ( 0, 0, 0 ), range_max = ( 100, 100, 100 ), class_ = 'mover', typ = '2-legs' ), list(), Actuator( position = ( 0, 0, 0 ), range_max = ( 100, 100, 100 ), class_ = 'mover', typ = '2-legs' ) ]

    if Actuator.checkActuatorList(actuator, actuators): 
        print('Actuator.checkSensorList(sensors) Failed!! ', actuators[0]._id, actuators[0]._state, actuators[0]._state._health)
        result = False  
    

    # test moving()

    actuator = Actuator( position = ( 0, 0, 0 ), range_max = ( 100, 100, 100 ), class_ = 'mover', typ = '2-legs', delta_t = 0.1)
    sensors = [ Sensor( typ = "radio", position = ( 0, 0, 0 ), range_max = (100, 100, 100) ) ]
    automa = Automa( actuators = [ actuator ], sensors = sensors )
    posMng = Position_manager()
    posMng.insertObject( ( 0, 0, 0 ), automa )
    target_position = (5, 5, 3)
    moved, energy_actuator, position_rached = actuator.moving( automa, posMng, [ target_position, 0.6 ]  )

    if not moved or energy_actuator != actuator._state.getEnergy() or automa.getPosition() != (3, 3, 3) or not position_rached: 
        print('Actuator.moving() Failed!! A', moved, energy_actuator, position_rached, actuator._state.getEnergy(), automa.getPosition(), target_position )
        result = False     


    actuator = Actuator( position = ( 0, 0, 0 ), range_max = ( 100, 100, 100 ), class_ = 'mover', typ = '2-legs', delta_t = 0.1)
    sensors = [ Sensor( typ = "radio", position = ( 0, 0, 0 ), range_max = (100, 100, 100) ) ]
    automa = Automa( actuators = [ actuator ], sensors = sensors )
    posMng = Position_manager()
    posMng.insertObject( ( 0, 0, 0 ), automa )
    target_position = (5, 5, 3)
    moved, energy_actuator, position_rached = actuator.moving( automa, posMng, [ target_position, 0.2 ]  )

    if not moved or energy_actuator != actuator._state.getEnergy() or automa.getPosition() != (2, 2, 2) or position_rached: 
        print('Actuator.moving() Failed!! B', moved, energy_actuator, actuator._state.getEnergy(), automa.getPosition(), target_position )
        result = False     


    # test exec_command()

    actuator = Actuator( position = ( 0, 0, 0 ), range_max = ( 100, 100, 100 ), class_ = 'mover', typ = '2-legs', delta_t = 0.1)
    sensors = [ Sensor( typ = "radio", position = ( 0, 0, 0 ), range_max = (100, 100, 100) ) ]
    automa = Automa( actuators = [ actuator ], sensors = sensors )
    posMng = Position_manager()
    posMng.insertObject( ( 0, 0, 0 ), automa )
    target_position = (5, 5, 3)

    action_info = actuator.exec_command( automa, posMng, [ target_position, 0.2 ] )
    moved = action_info[ 0 ]
    energy_actuator = action_info[ 1 ]
    actuation_terminated = action_info[ 2 ]

    if not moved or energy_actuator != actuator._state.getEnergy() or automa.getPosition() != (2, 2, 2): 
        print('Actuator.exc_command() - move - Failed!! ', moved, energy_actuator, actuator._state.getEnergy(), automa.getPosition(), target_position )
        result = False     



    actuator = Actuator( position = ( 0, 0, 0 ), range_max = ( 10, 10, 10 ), class_ = 'object_manipulator', typ = 'hand', delta_t = 0.1)
    sensors = [ Sensor( typ = "radio", position = ( 0, 0, 0 ), range_max = (100, 100, 100) ) ]
    automa = Automa( actuators = [ actuator ], sensors = sensors )
    posMng = Position_manager()
    posMng.insertObject( ( 0, 0, 0 ), automa )    
    obj = Object( coord = Coordinate( 5, 5, 5 ) )
    posMng.insertObject( ( 5, 5, 5 ), obj )

    action_info = actuator.exec_command( automa, posMng, [ obj, (9, 9, 9) ] )
    manipulate = action_info[ 0 ]
    energy_actuator = action_info[ 1 ]
    actuation_terminated = action_info[ 2 ]

    if not manipulate or energy_actuator != actuator._state.getEnergy() or obj.getPosition() != (9, 9, 9): 
        print('Actuator.exc_command() - translate - Failed!! ', moved, energy_actuator, actuator._state.getEnergy(), obj.getPosition(), target_position )
        result = False 


    actuator = Actuator( position = ( 0, 0, 0 ), range_max = ( 10, 10, 10 ), class_ = 'object_manipulator', typ = 'hand', delta_t = 0.1)
    sensors = [ Sensor( typ = "radio", position = ( 0, 0, 0 ), range_max = (100, 100, 100) ) ]
    automa = Automa( actuators = [ actuator ], sensors = sensors )
    posMng = Position_manager()
    posMng.insertObject( ( 0, 0, 0 ), automa )    
    obj = Object( coord = Coordinate( 5, 5, 5 ) )
    posMng.insertObject( ( 5, 5, 5 ), obj )

    action_info = actuator.exec_command( automa, posMng, [ obj, (11, 11, 11) ] )
    manipulate = action_info[ 0 ]
    energy_actuator = action_info[ 1 ]
    actuation_terminated = action_info[ 2 ]

    if manipulate: 
        print('Actuator.exc_command() - translate - Failed!! ', manipulate, energy_actuator, actuator._state.getEnergy(), obj.getPosition(), target_position )
        result = False 


    actuator = Actuator( position = ( 0, 0, 0 ), range_max = ( 10, 10, 10 ), class_ = 'object_catcher', typ = 'clamp', delta_t = 0.1)
    sensors = [ Sensor( typ = "radio", position = ( 0, 0, 0 ), range_max = (100, 100, 100) ) ]
    automa = Automa( actuators = [ actuator ], sensors = sensors )
    posMng = Position_manager()
    posMng.insertObject( ( 0, 0, 0 ), automa )    
    obj = Object( coord = Coordinate( 5, 5, 5 ) )
    posMng.insertObject( ( 5, 5, 5 ), obj )

    action_info = actuator.exec_command( automa, posMng, [ obj ] )
    catch = action_info[ 0 ]
    energy_actuator = action_info[ 1 ]
    actuation_terminated = action_info[ 2 ]

    if not catch or energy_actuator != actuator._state.getEnergy() or obj.getCaught_from() != automa.getId() or not automa.checkCaught( obj ): 
        print('Actuator.exc_command() - translate - Failed!! ', catch, energy_actuator, actuator._state.getEnergy(), obj.getCaught_from() )
        result = False 


    return result

print("Actuator class test result:", testClassActuator())
