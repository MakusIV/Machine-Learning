
import Object

class Resource(Object):

    def __init__(self, type = 'FOOD', name = 'Food', dimension = [1, 1, 1], coord  ):

            Object.__init__(self, name = name, dimension = dimension, coord = coord, state = State(run = True))

            self._type = type #FOOD, WATER, ENERGY, ....
                            
           
    