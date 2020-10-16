import random
from Coordinate import Coordinate
import General
from State import State
from LoggerClass import Logger

# LOGGING --
 
logger = Logger(module_name = __name__, class_name = 'Actuator')


class Actuator:
    #position, range_max, typ, emissivity_perception = 1, power = 100, resilience = 100, delta_t = 0.01, accuracy = 5, name = None, state = None 
    def __init__(self, position, range_max, class_, typ, power = 100,  resilience = 100, delta_t = 0.01, name = None  ):

        if not self.checkParam( position, class_, typ, range_max, power, resilience, delta_t ):
            raise Exception("Invalid parameters! Actuator not istantiate.")

        self._name = name
        self._id = General.setId('Actuator_ID', None) # Id generator automaticamente
        self._power = power# nota l'energia è gestita nello stato in quanto è variabile  
        self._range = range_max# è rappresentato da una tupla di distanze (x_d:int, y_d:int, z_d:int)
        self._state = State( run = True )
        self._resilience = resilience # resistenza ad uno SHOT in termini di power (se shot power > resilence --> danno al actuatore)
        self._delta_t = delta_t # Il tempo necessario per eseguire l'attuazione serve per calcolare il consumo energetico. Puotrà essere utilizzato per gestire eventuali detection che necessitano di più cicli
        self._type = typ # il tipo di attuazione (vedi General.ACTUATOR_TYPE)
        self._class = class_ # la classe dell'attuatore (vedi General.ACTUATOR_TYPE)
        self._position = position
      

        if not name:
            self._name = General.setName('Actuator_Name')
        else:
            self._name = name


    def checkParam(self, position, class_, typ, range_max,  power, resilience, delta_t):
        """Return True if conformity of the parameters is verified"""
        if not( range_max and range_max[0] >0 and range_max[1] >0 and range_max[2] >0 and delta_t and delta_t <= 1 and delta_t >= 0 and power and power <= 100 and power >= 0 and  resilience and  resilience <= 100 and resilience >= 0 ):
            return False
        
        if not typ or not class_ or not ( General.checkActuatorTypeAndClass( typ, class_ ) and General.checkPosition( position ) ):
            return False

        return True


    def isType( self, actuator_type):
        """Return True if actuator have self._type == actuator_type"""
        return self._type == actuator_type
                        
    

    def isClass( self, actuator_class):
        """Return True if actuator have self._class == actuator_class"""   
        return self._class == actuator_class
    

    def evalutateDamage(self, energy, power):
        """Evalutate the damage on actuator and update state"""
        if power > self._resilience:
            damage = power - self._resilience# in realtà il danno dovrebbe essere proporzionale all'energia
            return self._state.decrementHealth( damage )
        
        return self._state.getHealth()
    
    
    def exec_command(self, action_decription):
        # action description: 
        pass


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

    # test: ok
    def checkActuatorClass(self, actuator):
        """Return True if actuators is a actuator object otherwise False"""
        if not actuator or not isinstance(actuator, Actuator):
            return False
        
        return True

    def checkActuatorList(self, actuators):

        """Return True if actuators is a list of Actuator object otherwise False"""
        if actuators and isinstance(actuators, list) and all( isinstance(actuator, Actuator) for actuator in actuators ):
            return True

        return False

    def isOperative(self):
        """Return true if actuator state is running"""
        return self._state.isRunning()


    def evalutateSelfDamage(self, energy, power):
        """Evalutate the damage on sensor and update state"""
        if power > self._resilience:
            damage = power - self._resilience# in realtà il danno dovrebbe essere proporzionale all'energia
            return self._state.decrementHealth( damage )
        
        return self._state.getHealth()
