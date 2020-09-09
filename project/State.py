
class State:

    def __init__(self, start = True, run = None  ): 

            self._start = start
            self._run = run                       
            self._stop = True
            self._destroy = False
            self._remove = False

            if not run:
                self. _run = False
            
            elif not start and run:
                self._run = False

    def toString(self):
        return "start: " + str(self._start) + ", run: " + str(self._run) + ", stop: " + str(self._stop) + ", remove: " + str(self._remove) + ", destroy: " + str(self._destroy)
            
    def isStarted(self):
        return self._start            

    def isRunning(self):
        return self._run            

    def isDestroyed(self):
        return self._destroy

    def isStopped(self):
        return self._stop

    def isRemoved(self):
        return self._remove

    def checkState(self):
        """Check state and return true if correct state is verificated or raise Exception for state anomaly"""

        wrongState = ( self._start and self._remove ) or ( self._run and ( not self._start or self._stop or self._destroy ) ) or ( self._remove and ( self._run or not self._stop ) )

        if wrongState:
            raise Exception("Anomaly state!")

        return True
       
 
    def start(self):
        """Check state, set start state and return true. Raise Exception for state anomaly or return false for not correct conditions"""

        self.checkState()

        if self._remove or self._destroy:
            return False
            
        self._start = True
        
        return True
        
        
    
    def stop(self):
        """Check state, set stop state and return true. Raise Exception for state anomaly or return false for not correct conditions"""

        self.checkState()

        if not self._run:
            return False 

        self._run = False
        self._stop = True
        
        return True


    def run(self):
        """Check state, set run state and return true. Raise Exception for state anomaly or return false for not correct conditions"""

        self.checkState()

        if not self._stop:
            return False 

        self._run = True
        self._stop = False
        
        return True



    def remove(self):
        """Check state, set remove state and return true. Raise Exception for state anomaly or return false for not correct conditions"""

        self.checkState()

        if not self._stop:
            return False 

        self._remove = True
        self._active = False
        
        return True



    def destroy(self):
        """Check state, set destroy state and return true. Raise Exception for state anomaly or return false for not correct conditions"""

        self.checkState()

        if self._remove:
            return False 

        self._destroy = True
        self._stop = True
        
        return True


    # le funzionalità specifiche le "inietti" o crei delle specializzazioni (classi derivate)