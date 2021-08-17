from State import State
from Threat import Threat
from Resource import Resource
from Obstacle import Obstacle
from Action import Action
import General
from LoggerClass import Logger

# LOGGING --
 
logger = Logger(module_name = __name__, class_name = 'AI')


class AI:

    # La AI è deputata esclusivamente alla valutazione delle informazioni ricevute dai sensori per 
    # l'aggiornamento dello stato dell'automa e del enviroment conosciuto dall'automa (env_state)
    # e per definire l'azione da compiere in base a queste informazioni
    

    def __init__(self, state = State(run = True), env_state = None  ):
        
        self._state = state #Class State 
        self._env_state = env_state

        if not self.checkProperty():
            raise Exception("Invalid parameters! Object not istantiate.")

        logger.logger.debug('AI Instantiate')

    # Methods

    def checkProperty(self):

        if not self._state or not isinstance(self._state, State):
            return False
            
        return True

    def evalutate(self, percept_info, state):
        """Evalutate the info of the enviroments knows (percept_info), update internal and 
        enviroment state property of ai and return the action to execute. Raise an Generic Exception"""
        
        # updateInternalState --> updateEnvState --> evalutation --> Action

        if not self.updateInternalState( percept_info ): 
            raise Exception("evalutate method failed! updateInternalState Failed")

        if not self.updateEnvState( percept_info ): 
            raise Exception("evalutate method failed! updateEnvState Failed")

        return self.evalutation(  state )


    def updateInternalState( self, perception_info ):
        """update the internal_state property"""
        # nota: l'internal state serve solo per valutare il livello di efficenza dell'ai nell'esecuzione delle sue funzioni
        return True

    def updateEnvState( self, perception_info ):
        """update the env_state object property"""
        # nota l'env_state è la porzione dell'intero enviroments (contesto) conosciuto dalla AI       

        return True


    def evalutation( self, state ):
        """Evalutate the Action to Automa execute. Return an istance of Action"""
        
        # eval_threat --> eval_resource --> eval_space --> eval_action
        
        threats = self._ev_threat( self._state, self._env_state, state )
        resources = self._ev_resource( self._state, self._env_state, state )
        obstacles = self._ev_obstacle( self._state, self._env_state, state )
        action = self._ev_action(threats, resources, obstacles, state) #action = Action(...) una classe
     
        return action
        

    def _ev_threat( self, internal_state, env_state, state ):
        """Evalutate Threats with level of threath and position. Return an istance of Threat.
        Rise an Invalid Parameters Exception"""
        threats = Threat()
        return threats        

    def _ev_resource( self, internal_state, env_state, state ):
        """Evalutate Resource with level of resource and position. Return an istance of Resource.
        Rise an Invalid Parameters Exception"""
        resources = Resource()
        return resources

    def _ev_obstacle( self, internal_state, env_state, state ):
        """Evalutate Space enviroments with Obstacles. Return an istance of Obstacle.
        Rise an Invalid Parameters Exception"""
        obstacles = Obstacle()
        return obstacles

    def _ev_action(self, threaths, resources, space_env, state):
        """Evalutate action to execute considering threats, resources, space_env and state.
        Return an instance of Action. Rise an Invalid Parameters Exception"""
        action = Action()
        return action



        