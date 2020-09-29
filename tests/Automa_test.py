# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'project')

from State import State
from Automa import Automa




def testClassAutoma():

    result = True

    #name = 'Automa', dimension = [1, 1, 1], resilience = 10, state = State(run = True), ai = AI(), coord = None, sensors= None, actuators = None      
    automa = Automa()

    if automa._name != 'Automa' or automa._dimension != [1, 1, 1] or automa._resilience != 100 or automa._power != 100 or not automa._state or not State.checkStateClass(automa._state) or not automa._state.isRunning():
        print('Automa Failed!! ', automa._name, automa._dimension, automa._resilience, sensor._state)
        result = False 
    
    
    

    return result

print("Automa class test result:", testClassAutoma())