from Coordinate import Coordinate
import General
from State import State
from LoggerClass import Logger

# LOGGING --
 
logger = Logger(module_name = __name__, class_name = 'Action')


class Action:
    
    def __init__(self, coord = None, name = None, dimension = None,  state = None  ):

        if not(self.setName(name) and self.setDimension(dimension) and self.setCoord(coord)) or not self.setState(state):
            raise Exception("Invalid parameters! Action not istantiate.")


        self._name = None
        self._id = None

        if not name:
            self._name = General.setName('Event_Name')
        else:
            self._name = name

        if not id:
            self._id = General.setId('Event_ID')
        else:
            self._id = id
        
        self.dimension = None
        self.coord = None
        self.state = None
                    
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
