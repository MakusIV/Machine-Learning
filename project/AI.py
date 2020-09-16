

class AI:

    def __init__(self, sensor = None, actuator = None, internal_state = None, env_state = None  ):

            self._sensor # Class Sensor
            self._actuator #Class Actuators
            self._internal_state #Class State
            self._env_state #Class State 
                    
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
        """Evalutate the Action to Automa execute. Return an istance of Action"""
        threaths = self._ev_threath( internal_state, env_state )
        resources = self._ev_resource( internal_state, env_state )
        space_env = self._ev_space_env( internal_state, env_state )
        action = self._ev_action(threaths, resources, space_env) #action = Action(...) una classe
     
        return action
        
    def _ev_threath( internal_state, env_state ):
        """Evalutate Threats with level of threath and position. Return an istance of Threat.
        Rise an Invalid Parameters Exception"""
        pass

    def _ev_resource( internal_state, env_state ):
        """Evalutate Resource with level of resource and position. Return an istance of Resource.
        Rise an Invalid Parameters Exception"""
        pass

    def _ev_space_env( internal_state, env_state ):
        """Evalutate Space enviroments with Obstacles. Return an istance of SpaceEnv.
        Rise an Invalid Parameters Exception"""
        pass

    def _ev_action(threaths, resources, space_env):
        pass

    def execAction( self, action ):
        #use _actuators
        pass
        