

class AI:

    def __init__(self, sensor = None, actuator = None, internal_state = None, env_state = None  ):

            self._sensor # Class Sensor
            self._actuator #Class Actuators
            self._internal_state
            self._env_state            
                    
            if not(self.setSensor(sensor) and self.setActuator(actuator) and self.setInternalState(internal_state) and self.setEnvState(env_state)):
                raise Exception("Invalid parameters! Object not istantiate.")



    def execPerception( self ):
        pass
        # use _sensors
        env_info  = None
        return env_info, internal_state_info

    def updateInternalState( self, internal_state_info ):
        pass

    def updateEnvState( self, env_info ):
        pass

    def evalutation( self, internal_state, env_state ):
        action = None  #action = Action(...) una classe
        return action
        
    def execAction( self, action ):
        #use _actuators
    
        