
from Coordinate import Coordinate
import General
from State import State

class Sensor:
    
    def __init__(self, name = None, sensibility = None,  state = None  ):


            self.name = None
            self.id = self.setId(None)
            self.state = None
            self.power = None
            self,ì.sensibility = None
                        
            if not(self.setName(name) or not self.setState(state):
                raise Exception("Invalid parameters! Object not istantiate.")


    def setId(self, id = None):

        self.id = General.setId('Sensor', id)
            
        return True


    def setName(self, name):

        self.name = General.setName('Sensor')

        return True

    def perception(self, posMng, request_perception):
        # Valuta quali sensori attivare e come attivarli in base alle info contenute in request_perception (Class Perception)
        # Restituisce le informazioni sulle azioni effettuate quali stato, posizione degli attuatori
        percept_info = None
        return percept_info