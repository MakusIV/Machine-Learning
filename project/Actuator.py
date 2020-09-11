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