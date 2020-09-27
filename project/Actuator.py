import random
from Coordinate import Coordinate
import General
from State import State
from LoggerClass import Logger

# LOGGING --
 
logger = Logger(module_name = __name__, class_name = 'Actuator')


class Actuator:
    
    def __init__(self, name = None, power = None,  resilience = None, state = None  ):

        if not(power and state ):
            raise Exception("Invalid parameters! Actuator not istantiate.")


        self._name = None
        self._id = None
        self._power = power# nota l'energia è gestita nello stato in quanto è variabile  
        self._state = state
        self._resilence = resilience # resistenza ad uno SHOT in termini di power (se shot power > resilence --> danno al sensore)

        if not name:
            self._name = General.setName('Actuator_Name')
        else:
            self._name = name

        if not id:
            self._id = General.setId('Actuator_ID')
        else:
            self._id = id
                        
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

    def eval_command(self, request_action):
        # Valuta quali attuatori attivare e come attivarli in base alle info contenute in request_action (class Action)
        # Restituisce le informazioni sulle azioni effettuate quali stato, posizione degli attuatori
        action_info = None
        return action_info