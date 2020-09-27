from Coordinate import Coordinate
import General
from State import State
from LoggerClass import Logger

# LOGGING --
 
logger = Logger(module_name = __name__, class_name = 'Event')


class Event:
    
    def __init__(self, typ, volume,  time2go = 1, duration = 1, energy = None, power = None, mass = None  ):

        if not self.checkParam(typ, volume,  time2go, duration, energy, power, mass):
            raise Exception("Invalid parameters! Event not istantiate.")        

        self._type = None # type: SHOT, PUSH, POP, EAT
        self._id = General.setId(self._type, None) # l'id vieene generato automaticamente nel runtime per ogni istanza creata
        self._volume = None
        self._time2go = None
        self._duration = None
        self._energy = None
        self._power = None
        self._mass = None
   

    def decrTime2Go(self):
        self._time2go = self._time2go -1
        return self._time2go

    def decrDuration(self):
        self._duration = self._duration - 1
        return self._duration

    def isActivable(self):
        return self._time2go == 1 and self._duration > 1

    def isAwaiting(self):
        return self._time2go > 1

    def isPush(self):
        return self._type == 'PUSH'

    def isPop(self):
        return self._type == 'POP'

    def isShot(self):
        return self._type == 'SHOT'

    def isEat(self):
        return self._type == 'EAT'


    
    

    def checkParam(self, typ, volume,  time2go, duration, energy, power, mass):

        if not ( type == 'SHOT' or self._type == 'PUSH' orself._type == 'POP' ):
            return False

        if not General.checkVolume(volume) or not isinstance(time2go, int) or not isinstance(duration, int):
            return False

        if energy and not isinstance(energy, int):
            return False

        if power and not isinstance(power, int):
            return False

        if mass and not isinstance(mass, int):
            return False

        return True