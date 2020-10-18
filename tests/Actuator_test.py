
# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'project')
from Actuator import Actuator
import General
from LoggerClass import Logger


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
    
    

    actuators = [ Actuator( position = ( 0, 0, 0 ), range_max = ( 100, 100, 100 ), class_ = 'mover', typ = '2-legs' ), Actuator( position = ( 0, 0, 0 ), range_max = ( 100, 100, 100 ), class_ = 'mover', typ = '2-legs' ), Actuator( position = ( 0, 0, 0 ), range_max = ( 100, 100, 100 ), class_ = 'mover', typ = '2-legs' ) ]

    if not Actuator.checkActuatorList(actuator, actuators): 
        print('Actuator.checkSensorList(sensors) Failed!! ', actuators[0]._id, actuators[0]._state, actuators[0]._state._health)
        result = False

    

    actuators = [ Actuator( position = ( 0, 0, 0 ), range_max = ( 100, 100, 100 ), class_ = 'mover', typ = '2-legs' ), Actuator( position = ( 0, 0, 0 ), range_max = ( 100, 100, 100 ), class_ = 'mover', typ = '2-legs' ), list(), Actuator( position = ( 0, 0, 0 ), range_max = ( 100, 100, 100 ), class_ = 'mover', typ = '2-legs' ) ]

    if Actuator.checkActuatorList(actuator, actuators): 
        print('Actuator.checkSensorList(sensors) Failed!! ', actuators[0]._id, actuators[0]._state, actuators[0]._state._health)
        result = False  
    
    

    return result

print("Actuator class test result:", testClassActuator())
