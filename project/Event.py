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

        self._type = None # type: HIT, PUSH, POP, ASSIMILATE, MOVE
        self._id = General.setId(self._type, None) # l'id viene generato automaticamente nel runtime per ogni istanza creata
        self._volume = volume
        self._time2go = time2go
        self._duration = duration
        self._energy = energy
        self._power = power
        self._mass = mass
   

    def decrTime2Go(self):
        self._time2go = self._time2go -1
        return self._time2go

    def decrDuration(self):
        self._duration = self._duration - 1
        return self._duration

    def isActivable(self):
        return self._time2go == 0 and self._duration > 0

    def isAwaiting(self):
        return self._time2go > 0

    def isPush(self):
        return self._type == 'PUSH'

    def isPop(self):
        return self._type == 'POP'

    def isHit(self):
        return self._type == 'HIT'

    def isAssimilate(self):
        return self._type == 'ASSIMILATE'

    def isMove(self):
        return self._type == 'MOVE'

    
    

    def checkParam(self, typ, volume,  time2go, duration, energy, power, mass):

        if not General.checkEventType( typ ):
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