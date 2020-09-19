import Object

class Obstacle(Object):

    def __init__(self, type = 'WATER_STONE', name = 'Stone', dimension = [1, 1, 1], coord  ):

            Object.__init__(self, name = name, dimension = dimension, coord = coord, state = State(run = True))

            self._type = type #WATER_STONE, ENERGY_FIELD, ......
            # La water stone rappresenta un volume d'acqua fermo o mobile che non può essere attraversato                 
           