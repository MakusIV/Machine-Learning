# Automa
import Object


class Automa(Object):

    def __init__(self, name = None, id = None, dimension = None, coord = None, state = None  ):

        Object.__init__(self, name = name, id = id, dimension = dimension, coord = coord, state = state)

        self.ai = None #AI Engine
        self env_state = None #Enviroment state
        self current_action = None
                         
        if not self.setAi(ai):
            raise Exception("Invalid parameters! Automata not istantiate.")

        def percept(posMng):
            """Run an perception action and set the current env_state percepted """
            self.env_state = self.ai.percept(posMng, self.state)

        def evalutate(state):
            self.current_action  = self.ai.evalutate(self.env_state)

        # vedi il libro
        
    