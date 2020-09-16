
import Object

class Resource(Object):

    def __init__(self, type = 'FOOD', name = 'Food', dimension = [1, 1, 1], coord = None, state = None  ):

            Object.__init__(self, name = name, dimension = dimension, coord = coord, state = State(run = True))

            self._type = type #FOOD, WATER, ENERGY, ....
            self env_state = None #Enviroment state
            self current_action = None
                            
            if not self.setAi(ai):
                raise Exception("Invalid parameters! Automata not istantiate.")
    