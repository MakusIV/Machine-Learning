# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'project')

from State import State
from Automa import Automa
from Sensor import Sensor
from Actuator import Actuator
from Coordinate import Coordinate




def testClassAutoma():

    result = True
    # actuator(position, range_max, typ, power = 100,  resilience = 100, delta_t = 0.01, name = None, state = None)
    #name = 'Automa', dimension = [1, 1, 1], resilience = 10, state = State(run = True), ai = AI(), coord = None, sensors= None, actuators = None      
    coord = Coordinate( 0, 0, 0 )
    sensors = [ Sensor( typ = "radio", position = coord.getPosition(), range_max = (100, 100, 100) ), Sensor( typ = "optical", position = coord.getPosition(), range_max = (100, 100, 100) ), Sensor( typ = "thermal", position = coord.getPosition(), range_max = (100, 100, 100) )]
    actuators = [ Actuator( position = coord.getPosition(), range_max = ( 10, 10, 10 ), typ = "move", power = 100,  resilience = 100, delta_t = 0.01 ), Actuator( position = coord.getPosition(), range_max = ( 10, 10, 10 ), typ = "move", power = 100,  resilience = 100, delta_t = 0.01 ) ]
    automa = Automa(coord = coord, sensors = sensors, actuators = actuators)

    if automa._name != 'Automa' or automa._dimension != [1, 1, 1] or automa._resilience != 100 or automa._power != 100 or not automa._state or not isinstance(automa._state, State) or not automa._state.isRunning():
        print('Automa Failed!! ', automa._name, automa._dimension, automa._resilience, automa._state)
        result = False 
    
    
    

    return result

print("Automa class test result:", testClassAutoma())