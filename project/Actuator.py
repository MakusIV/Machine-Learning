import random
from Coordinate import Coordinate
import General
from State import State
from LoggerClass import Logger

# LOGGING --
 
logger = Logger(module_name = __name__, class_name = 'Actuator')


class Actuator:
    
    def __init__(self, name = None, power = None,  state = None  ):

        if not(power and state ):
            raise Exception("Invalid parameters! Actuator not istantiate.")


        self._name = None
        self._id = None
        self._power = power     
        self._state = state

        if not name:
            self._name = General.setName('Actuator_Name')
        else:
            self._name = name

        if not id:
            self._id = General.setId('Actuator_ID')
        else:
            self._id = id
                        
        

    def setId(self, id = None):

        if not id:
            return False
        else:
            self._id = id        
            
        return True


    def setName(self, name):

        if not name:
            return False
        else:
            self._name = name

        return True

    def eval_command(self, request_action):
        # Valuta quali attuatori attivare e come attivarli in base alle info contenute in request_action (class Action)
        # Restituisce le informazioni sulle azioni effettuate quali stato, posizione degli attuatori
        action_info = None
        return action_info