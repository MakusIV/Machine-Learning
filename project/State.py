
class State:

    def __init__(self, start = True, run = None  ): 

            self.__start = start
            self.__run = False                        
            self.__stop = True
            self.__destroy = False
            self.__remove = False
            
                
            
    def isStarted(self):
        return self.start            

    def isRunning(self):
        return self.run            

    def isDestroyed(self):
        return self.destroy

    def isStopped(self):
        return self.stop

    def isRemoved(self):
        return self.remove

    def checkState(self):
        """Check state and return true if correct state is verificated or raise Exception for state anomaly"""

        wrongState = ( self.__start and self.__remove ) or ( self.__run and ( self.__stop or self.__destroy ) ) or ( self.__remove and ( self.__run or self.__stop ) )

        if wrongState:
            raise Exception("Anomaly state!")

        return True
       
 
    def start(self):
        """Check state, set start state and return true. Raise Exception for state anomaly or return false for not correct conditions"""

        self.checkState()

        if self.__remove or self.__destroy:
            return False
            
        self.__start = True
        
        return True
        
        
    
    def stop(self):
        """Check state, set stop state and return true. Raise Exception for state anomaly or return false for not correct conditions"""

        self.checkState()

        if not self.__run:
            return False 

        self.__run = False
        self.__stop = True
        
        return True


    def run(self):
        """Check state, set run state and return true. Raise Exception for state anomaly or return false for not correct conditions"""

        self.checkState()

        if not self.__stop:
            return False 

        self.__run = True
        self.__stop = False
        
        return True



    def remove(self):
        """Check state, set stop state and return true. Raise Exception for state anomaly or return false for not correct conditions"""

        self.checkState()

        if not self.__stop:
            return False 

        self.__remove = True
        self.__active = False
        
        return True



    def destroy(self):
        """Check state, set destroy state and return true. Raise Exception for state anomaly or return false for not correct conditions"""

        self.checkState()

        if self.__remove:
            return False 

        self.__destroy = True
        self.__stop = True
        
        return True


    # le funzionalità specifiche le "inietti" o crei delle specializzazioni (classi derivate)