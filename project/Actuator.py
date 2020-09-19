import random
from Coordinate import Coordinate
import General
from State import State

class Actuator:
    
    def __init__(self, coord = None, name = None, dimension = None,  state = None  ):


            self.name = None
            self.id = self.setId(None)            
            self.state = None
                        
            if not(self.setName(name) or not self.setState(state):
                raise Exception("Invalid parameters! Object not istantiate.")


    def setId(self, id = None):

        self.id = General.setId('Actuator', id)
            
        return True


    def setName(self, name):

        self.name = General.setName('Actuator')

        return True

    def eval_command(self, request_action):
        # Valuta quali attuatori attivare e come attivarli in base alle info contenute in request_action (class Action)
        # Restituisce le informazioni sulle azioni effettuate quali stato, posizione degli attuatori
        action_info = None
        return action_info