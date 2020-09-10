
class State:

    def __init__(self, active = True, run = None  ): 

            self._active = active
            self._run = run # True only with active True                      
            self._destroy = False # True only with run False
            self._remove = False # True only with start and run False
            self._anomaly = False # True only with active true
            self._critical = False # True only with active true
            self._efficiency = 10 #full
            self._energy = 10 #full 
            self._health = 10 #full

            if not run:
                self. _run = False
            
            elif not active and run:
                self._run = False



    def evalutateEfficiency(self):
        """Update efficiency from energy and health levels ad return efficiency level"""
        self._efficiency = energy * health / 100
        return self._efficiency

    
    def evalutateAnomaly(self):
        """Update anomaly state from efficiency level and return it"""

        if (efficiency < 3):
            self.setAnomaly(True)
        
        return self._anomaly
        

    def evalutateCritical(self):
        """Upgrade critical state from health level and return it"""

        if (health < 3):
            self.setCritical(True)
        
        return self._critical


    def setCritical(self, value):

        if not self._active or self._destroy or self._remove:
            return False

        self._critical = value
        self.checkState()

        return True


    def setAnomaly(self, value):

        if not self._active or self._destroy or self._remove:
            return False

        self._critical = value
        self.checkState()

        return True




    def toString(self):
        return "active: " + str(self._active) + ", run: " + str(self._run) + ", remove: " + str(self._remove) + ", destroy: " + str(self._destroy) + ", anomaly: " + str(self._anomaly) + ", critical: " + str(self._critical) 
            
    def isActive(self):
        return self._active            

    def isRunning(self):
        return self._run            

    def isDestroyed(self):
        return self._destroy


    def isRemoved(self):
        return self._remove

    def isAnomaly(self):
        return self._anomaly
    
    def isCritical(self):
        return self._critical


    def checkState(self):
        """Check state and return true if correct state is verificated or raise Exception for state anomaly"""

        wrongState = ( self._active and self._remove ) or ( self._run and ( not self._active or self._destroy or self._remove) or ( self._anomaly or self._critical ) and not self._active )

        if wrongState:
            raise Exception("Anomaly state!")

        return True
       
 
    def active(self):
        """Check state, set active state and return true. Raise Exception for state anomaly or return false for not correct conditions"""        

        if self._remove or self._destroy:
            return False
            
        self._active = True
        self.checkState()
        
        return True
        
        
    
    def stop(self):
        """Check state, set stop state and return true. Raise Exception for state anomaly or return false for not correct conditions"""       

        if not self._run:
            return False 

        self._run = False
        self.checkState()

        return True


    def run(self):
        """Check state, set run state and return true. Raise Exception for state anomaly or return false for not correct conditions"""

        if not active:
            return False

        self._run = True
        self.checkState()        

        return True



    def remove(self):
        """Check state, set remove state and return true. Raise Exception for state anomaly or return false for not correct conditions"""

        if self._run or not self._active:
            return False 

        self._remove = True
        self._active = False
        self.checkState()
        
        return True



    def destroy(self):
        """Check state, set destroy state and return true. Raise Exception for state anomaly or return false for not correct conditions"""        

        if self._remove or not self._active:
            return False 

        self._destroy = True
        self._run = False
        self.checkState()

        return True


    # le funzionalità specifiche le "inietti" o crei delle specializzazioni (classi derivate)