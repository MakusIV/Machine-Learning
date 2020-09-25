
from Coordinate import Coordinate
import General
from State import State
from LoggerClass import Logger

# LOGGING --
 
logger = Logger(module_name = __name__, class_name = 'Sensor')

class Sensor:
    # Il sensore non è una specializzazione di Object

    def __init__(self, name = None, sensibility = None,  power = None, state = None  ):

        if not( power and state and sensibility ):
            raise Exception("Invalid parameters! Sensor not istantiate.")

        self._name = None
        self._id = None
        self._state = state
        self._power = power
        self._sensibility = sensibility

        if not name:
            self._name = General.setName('Sensor_Name')
        else:
            self._name = name

        if not id:
            self._id = General.setId('Sensor_ID')
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

    def perception(self, posMng, request_perception):
        # Valuta quali sensori attivare e come attivarli in base alle info contenute in request_perception (Class Perception)
        # Restituisce le informazioni sulle azioni effettuate quali stato, posizione degli attuatori
        percept_info = None
        return percept_info