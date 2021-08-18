from logging import raiseExceptions
from typing import Dict
from State import State
from Threat import Threat
from Resource import Resource
from Obstacle import Obstacle
from Action import Action
from Object import Object
import General
from LoggerClass import Logger

# LOGGING --
 
logger = Logger(module_name = __name__, class_name = 'AI')


class AI:

    # La AI è deputata esclusivamente alla valutazione delle informazioni ricevute dai sensori per 
    # l'aggiornamento dello stato dell'automa e del enviroment conosciuto dall'automa (env_state)
    # e per definire l'azione da compiere in base a queste informazioni
    

    def __init__(self, state = State(run = True), env_state = dict(), obj_memory = dict(), automa = None  ):
        
        self._state = state #Class State 
        self._env_state = env_state
        self._obj_memory = obj_memory
        self._automa = automa

        #env_state = ( obj.pos, obj1, type = unknow, direction = (8, nord_est_up), aspect = away, estimated_distance = 7),  
        
        # obj_memory = dict(key = IdObj, _class = threat/obstacle/food, _typ = shooter/catcher/solid/liquid/gas, 
        # eval_dangerous_range = (x.range, y.range, z.range), danger = 1..100)
        self._obj_memory = obj_memory#dict( [ ("dummyObjId", ["OBSTACLE", "SOLID", [10, 10, 10], 0] ) ] )

        if not self.checkProperty():
            raise Exception("Invalid parameters! Object not istantiate.")

        logger.logger.debug('AI Instantiate')

    # Methods

    def checkProperty(self):

        if not self._state or not isinstance(self._state, State) or not isinstance(self._obj_memory, dict) or not isinstance(self._env_state, dict) :#or not self._env_state or not self._obj_memory
            return False
            
        return True

    def evalutate(self, percept_info, state):
        """Evalutate the info of the enviroments knows (percept_info), update internal and 
        enviroment state property of ai and return the action to execute. Raise an Generic Exception"""
        
        # updateInternalState --> updateEnvState --> evalutation --> Action
        action = self.evalutation(  percept_info, state )

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
        # nota l'env_state è la porzione dell'intero enviroments (contesto) conosciuto dalla AI.
        #        
        # utilizzare lo _env_state per valutare i vettori di spostamento degli obj già presenti utilizzando le nuove posizioni
        # rilevate nella preception_info. 
        # Utilizzando la memory_obj (memoria degli oggetti conosciuti) classificare i nuovi obj presenti nella perception_info
        # aggiornare quindi l'_env_state.
        # Questa funzione implementa le funzioni dell'algoritmo di AI che simulano le risposte "incondizionate" anche acquisite
        # esperenzialmente, che non coinvolgono processi di analisi sofisticati.
        #        
        # L'env_state potrebbe essere rappresentato da una tabella in cui c'è l'obj, la stima del typo e il vettore di spostamento 
        # interpretando la valutazione di questo vettore come un processo incondizionato preesistente.
        #
        # quindi env_state = ( 
        # (obj1, type = unknow, direction = (8, nord_est_up), aspect = away, estimated_distance = 7),  
        # (obj2, type = threath, direction = (2, south), aspect = approaching, estimated_distance = 20),  
        # (obj3, type = food, direction = None, aspect = stopped, estimated_distance = 9),  
        # (obj3, type = food, direction = None, aspect = stopped, estimated_distance = 3, estimated_Frontal_dimension = 300)
        # )
        # 
        # Nell'algoritmo AI basato su condizioni, si potrebbero valutare le azioni da eseguire considerando l'env_state        # L'env_state potrebbe essere rappresentato da una tabella in cui c'è l'obj, il vettore di spostamento (modulo = velocità presunta),
        # e la classificaione: pericolo (con magnitudo), cibo (con magnitudo), ostacolo (con dimensioni). Esempio
        # ( (obj1, "unknow", direction = (8, nord_est_up), aspect = away, best_direction_to_escape = (south_west_up), distance = 7, danger = 3), 
        # (obj2, "threat", vector = (10, south_west), aspect=approaching, best_direction_to_escape = (south_west_up), danger=10), (obj3, "food", vector=(10, north), aspect=away, danger=0)
        # In base a questa lista l'automa deve valutare la priorità di fuggire in una determinata direzione opposta all'eventuale pericolo, ovvero
        # in direzione di una preda ovvero aggirando un ostacolo. In una prima versione di AI basata su condizioni, possiamo valutare danger, pesando il tipo di minaccia (uno shooter è più pericoloso di un catcher),
        # la distanza della minaccia e l'aspect. Poi confrontando i valori di danger delle diverse minaccie insieme ai valori di obstacle_magnitudo e di food_magnitudo
        # stabiliere quale direzione prendere.
        
        for obj in perception_info:
             
            if obj.getId() in self._obj_memory: # l'oggetto è presente nella obj_memory = dict(key = IdObj, _class = threat/obstacle/food, _typ = shooter/catcher, eval_dangerous_range = (x.range, y.range, z.range), danger = 1..100)
                #obj_memory = dict(key = IdObj, _class = threat/obstacle/food, _typ = shooter/catcher, eval_dangerous_range = (x.range, y.range, z.range), danger = 1..100)
                evalutateAndUpdateObjInEnvState( obj.IdObj ) 
                # deve valutare/aggiornare l'eventuale danger, direction, e inserirli nell' _env_state .....
                #
                # o codice

            else:
                evalutateAndInsertNewObjInEnvState( obj ) 
                #valuta se l'oggetto è una possibile minaccia/cibo o un ostacolo sconosciuto in base alla distanza (vicino: scappa, lontano:ok), 
                # alle dimensioni (grande: scappa, piccolo:vedi). Poi lo inserisce nell' _env_state e nella _obj_memory
                #o codice                
                automa_volume = self._automa.getValueVolume()
                volume_ratio = obj.differenceWithValueVolume( automa_volume ) / automa_volume# obj_volume - automa_volume
                distance = obj.getDistance( self._automa._coord )# distance of obj from automa
                automa_max_speed = self._automa.getActuator("mover").speed

                if volume_ratio > 2:# questa và inserita nel metodo in cui viene implementato l'algoritmo di valutazione e scelta
                    f=1


        #new_threats = self._ev_threat( self._env_state, state )
        #new_resources = self._ev_resource( self._state, self._env_state, state )
        #new_obstacles = self._ev_obstacle( self._state, self._env_state, state )
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



        