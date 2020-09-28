
from Coordinate import Coordinate
import General
from State import State
from LoggerClass import Logger

# LOGGING --
 
logger = Logger(module_name = __name__, class_name = 'Sensor')

class Sensor:
    # Il sensore non è una specializzazione di Object

    def __init__(self, sensibility = 100,  power = 100, resilience = 100, name = None, state = None  ):

        if not self.checkParam( sensibility,  power, resilience ):
            raise Exception("Invalid parameters! Sensor not istantiate.")

        self._name = name
        self._id = General.setId('Sensor_ID', None) # Id generator automaticamente 
        self._state = state
        self._power = power# nota l'energia è gestita nello stato in quanto è variabile
        self._sensibility = sensibility
        self._resilience = resilience # resistenza ad uno SHOT in termini di power (se shot power > resilence --> danno al sensore)

        if not name or not isinstance(name, str):
            self._name = General.setName('Sensor_Name')
        else:
            self._name = name

        if not state or not isinstance(state, State):
            self._state = State()
        else:
            self.state = state


    def checkParam(self, sensibility,  power, resilience):
        return sensibility <= 100 and sensibility >= 0 and power <= 100 and power >= 0 and  resilience <= 100 and resilience >= 0


    def evalutateDamage(self, energy, power):
        """Evalutate the damage on sensor and update state"""
        if power > self._resilience:
            damage = power - self._resilience# in realtà il danno dovrebbe essere proporzionale all'energia
            return self._state.decrementHealth( damage )
        
        return self._state.getHealth()


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