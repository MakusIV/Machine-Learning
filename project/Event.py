import random
from Coordinate import Coordinate
import General
from State import State

class Event:
    
    def __init__(self, coord = None, name = None, dimension = None,  state = None  ):


            self.name = None
            self.id = self.setId(None)
            self.dimension = None
            self.coord = None
            self.state = None
                        
            if not(self.setName(name) and self.setDimension(dimension) and self.setCoord(coord)) or not self.setState(state):
                raise Exception("Invalid parameters! Object not istantiate.")

