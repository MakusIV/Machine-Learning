# Automa
from Object import Object
from State import State
from Actuator import Actuator
from Sensor import Sensor
from AI import AI
import General
from Event import Event
from Action import Action
from LoggerClass import Logger


# LOGGING --
 
logger = Logger( module_name = __name__, set_consolle_log_level = 30, set_file_log_level = 10, class_name = 'Automa' )


class Automa(Object):
    """Automa derived from Object. """

    # TEST: OK
    def __init__( self, name = 'Automa', dimension = [1, 1, 1], resilience = 100, power = 100, emissivity = {"radio": 50, "thermal": 50, "optical": 100, "nuclear": 0, "electric": 50, "acoustics": 100, "chemist": 0}, coord = None, sensors= None, actuators = None ):

        Object.__init__( self, name = name, dimension = dimension, resilience = resilience, emissivity = emissivity, coord = coord )

        self._ai = AI() #AI Engine
        self._power = power # nota l'energia è gestita nello stato in quanto è variabile        
        self._state = State( run = True ) #Class State        
        self._sensors = sensors# list of Sensor objects
        self._actuators = actuators# list of Actuator objects. NO DEVE ESSERE UNA CLASSE CHE CONTIENE LA LISTA DEGLI ATTUATORI. QUESTA CLASSE DEVE IMPLEMENTARE IL METODO PER VALUTARE QUALI ATTUATORI ATTIVARE IN BASE AL COMANDO RICEVUTO
        self.action_executed = None
        self._eventsQueue = {} #  {key: event id, value = event}
        self._actionsQueue = {} #  {key: event id, value = action}
        self._objectCatched = []

        if not self.checkParamAutoma( power, sensors, actuators ):
            raise Exception( "Invalid properties! Automata not istantiate." )

        logger.logger.info( "Automa {0} created".format( self._id ) )
    
    # Methods


    # La sequenza è update --> percept --> evalutate --> action. 
    # update: aggiorna lo stato dell'automa in base agli eventi contenuti nella coda degli eventi
    # percept: utilizza i sensori per conoscere l'enviroment locale e aggiorna lo stato dell'automa
    # evalutate: valuta le informazioni ottenute e determina l'azione da eseguite
    # action: utilizza l'azione da eseguire per attivare gli attuatori necessari per lo svolgimento della stessa
    
    # Bisogna decidere se queste tre azioni devono
    # essere svolte in una unità temporale ovvero ognuna in una unità temporale (più complicato)
    # in quest'ultimo caso è necessaria una Queue per le azioni da eseguire e deve essere valutato come gestire i cambiamenti
    # dell'enviroments che avvengono tra una azione e la successiva.

    # Per semplificare è meglio eseguire le tre azioni come unico task
    
    # La AI è deputata esclusivamente alla valutazione delle informazioni ricevute dai sensori per 
    # l'aggiornamento dello stato dell'automa per definire l'azione da compiere in base a queste informazioni.
    # la proprietà 'env_state che rappresenta l'enviromets conosciuto dall'automa è interna e gestita nella AI
    
    def runTask( self, posManager ):
        
        self.update() #check the eventsQueue and update state
        list_obj = self.percept( posManager )
        self.evalutate( list_obj ) # create the action info to execute and inserts in the action Queue
        logger.logger.info( "Automa: {0} running task: update internal state, execute perception and detected {1} object, evalutate and executed action()".format( self._id, len( list_obj ) ))
        return self.action( posManager ) # return the Queue of the action info executed in a single task



    def update(self):
        """Update state, Sensor, Actuator states for check of eventsQueue"""        
        events = self.getEventActive()
        # l'evento riguarda una posizione indipendentemente dall'eventuale target impostato, quindi in base 
        # alle caratteristiche dell'evento che bissogna valutare quali elementi sono coinvolti e come sono
        # coinvolti
        
        for _, ev in events: # scorre gli eventi da eseguire della lista eventi attivi
            logger.logger.debug("Automa: {0} active event {1}".format( self._id, ev._type ))

            if ev.isShot(): # solo per l'evento SHOT viene valutato l'eventuale danno
                self.evalutateShot( ev )

            if ev.isPop(): # viene valutato se l'automa può essere preso (sollevato). Si potrebbe considerare come nuovo componente dell'oggetto che ha generato l'evento.
                self.evalutatePop( ev )

            if ev.isPush(): # viene valutato se l'automa può essere "spinto" (spostato). Valutare la nuova posizione dell'automa
                self.evalutatePush( ev )

            if ev.isAssimilate(): # viene valutato se l'automa può essere mangiato. Eliminare l'automa aggiornando lo stato
                self.evalutateEat( ev )

        logger.logger.debug("Automa: {0} executed update internal state".format( self._id ))
        return True
        
    # TEST: OK
    def percept(self, posMng):
        """Percepts the enviroments with sensors, update the state and return percept informations."""
        #percept_info: le informazioni dopo l'attivazione dei sensori: (energy_consumption, list_obj_detected)
        #request_percept: le informazioni riguardo tipo di sensori e modalità di attivazione
        list_obj = list()
        operative_sensors = [ sensor for sensor in self._sensors if sensor.isOperative() ]# Lista dei sensori attivi
        percept_infos = [ sensor.perception( posMng, self.getPosition() ) for sensor in operative_sensors ]# lista delle perception info ottenuta interrogando tutti i sensori operativi. La percept_info: percept_info: (energy_sensor, detected_objs) detected. detected_objs = { ( x, y, z): obj }
        list_item =  [ percept_info[ 1 ].values() for percept_info in percept_infos ]# lista degli object    
        
        for item in list_item:
            for obj in item:
                if obj._id != self._id:
                    list_obj.append( obj )# lista degli object    
        energy_consume = [ percept_info[ 0 ] for percept_info in percept_infos ]
        self.updateStateForEnergyConsume( energy_consume )# aggiorna lo stato dell'automa
        logger.logger.debug("Automa: {0} execute perception: activated {1} sensor, detected {2} object, energy consumed: {3}".format( self._id, len( operative_sensors ), len( list_obj ), energy_consume  ))
        return list_obj 


    def evalutate(self, percept_info ):
        """Evalutate the info of the enviroments knows (percept info) and return the action to execute"""       
        # determina quali sono le azioni che può svolgere in questo singolo task e le inserisce nella queue action
        self._actionsQueue = self.ai.evalutate(percept_info, self._state) # noota: la queue si resetta ad ogni task
        logger.logger.debug("Automa: {0} execute evalutate percept_info: created actionQueue with {1} items".format( self._id, len( self._actionsQueue ) ))
        return True

    # TEST: OK
    def action(self, posManager ):
        """Activates Actuators for execution of Action. Return action informations."""
        #action_info: le informazioni dopo l'attivazione degli attuatori e lo stato degli stessi( classe)
        actions_info = [] # (action_type, energy_consume, position, object)
        active_actions = self.getActionActive()

        for action in active_actions:           
            # actuators_activation: [ actuator,  [ position or obj, ..other params ] ]
            actuator_activation = self.eval_actuators_activation( action.getActionParam() ) # questa funzione deve anche valutare gli attuatori attivi e se questi sono sufficienti per compiere l'atto altrimenti deve restituire false o un atto ridotto            
            action_info = actuator_activation[0].exec_command( self, posManager, actuator_activation[ 1 ] )
            actions_info.append( action_info )            
            self.updateStateForAction( action, actuator_activation[0], action_info )

        logger.logger.debug("Automa: {0} executed action: created action_info with {1} items".format( self._id, len( actions_info ) ))
        return actions_info

    
    # vedi il libro
    def checkParamAutoma(self, power, sensors, actuators):            
        """Return True if conformity of the parameters is verified"""
        
        if not power or not isinstance(power, int) or not( power <= 100 and power >= 0 ) or not sensors or not isinstance(sensors[0], Sensor) or not Sensor.checkSensorList(sensors[0], sensors) or not actuators or not isinstance(actuators[0], Actuator) or not Actuator.checkActuatorList(actuators[0], actuators):
            return False
        return True

     # TEST: OK (indirect from percept method)
    def updateStateForEnergyConsume(self, energy_consume):
        """Update state, Sensor, Actuator states for Percept  info"""                
        total_sensor_consume = sum( energy_consume )
        self._state.decrementEnergy( total_sensor_consume )
        logger.logger.debug("Automa: {0} update state for energy consume: total_sensor_consume: {1}, self._state._energy: {2}".format( self._id, total_sensor_consume, self._state._energy ))
        return True

    # TEST: OK (indirect from action method)
    def updateStateForAction(self, action, actuator, action_info):
        """Update state, Sensor, Actuator states for Action info"""

        if not action_info[2]:# l'azione è non stata completata nell'iterazione
            # action.setDuration(2)# ripristina la durata della action. L'ho eliminato in quanto, a differenza della move,  ci potrebbero essere action utilizzano la duration per la loro esecuzione in più task 
            logger.logger.debug("Automa: {0}. Actuator: {1}, execute action: {2}, action not complete".format( self._id, actuator.getId(), action_info[2] ))
            
        else:# l'azione è stata completata nell'iterazione
            action.setDuration(1)# imposta ad 1 la durata della action affinchè venga eliminata nella successiva scansione della queue
            logger.logger.debug("Automa: {0}. Actuator: {1}, execute action: {2}, action complete: removed from queue".format( self._id, actuator.getId(), action_info[2] ))           
    
        return True

    # TEST: OK (indirect from action method)
    def insertAction( self, action ):

        if not action or not isinstance( action, Action ):
            return False
        self._actionsQueue[ action._id  ] = action
        logger.logger.debug("Automa: {0} inserted new action in queue, action id: {1}, actions in queue: {2}".format( self._id, action._id, len( self._actionsQueue ) ))
        return True

    # TEST: OK (indirect from action method)
    def removeAction( self, action ):
        """remove action in eventsQueue"""
        if not isinstance(action._id, int) :
            return False

        self._actionsQueue.pop( action._id )        
        logger.logger.debug("Automa: {0} removed action in queue, action id: {1}, actions in queue: {2}".format( self._id, action._id, len( self._actionsQueue ) ))
        return True

    def resetActionQueue( self ):
        """Reset the Action Queue"""
        self._actionsQueue.clear()

    # TEST: OK (indirect from action method)
    def getActionActive( self ):
        """Return a list with activable actions for a single task. Update the event Queue"""
        active = [] # list of active actions
        
        for act in list( self._actionsQueue.values() ):

            if act.isAwaiting(): # event not activable in this task
                act.decrTime2Go() # decrement time to go
                self._actionsQueue[ act.getId() ] = act # update actions queue

            elif act.isActivable(): # action activable
                act.decrDuration() # decrement duration
                self._actionsQueue[ act.getId() ] = act # update actions queue
                active.append( act ) # insert the action in action events list

            else: # expired action
                self._actionsQueue.pop( act.getId() ) #remove element from events queue 

        return active



    def insertEvent(self, event):
        """insert event in eventsQueue"""
        if not General.checkEvent(event):
            return False

        self._eventsQueue[ event._id ] = event
        logger.logger.debug("Automa: {0} inserted new event in queue, event id: {1}, events in queue: {2}".format( self._id, event._id, len( self._eventsQueue ) ))
        return True

    def removeEvent(self, event):
        """remove event in eventsQueue"""
        if not isinstance(event._id, int) :
            return False

        self._eventsQueue.pop( event._id )        
        logger.logger.debug("Automa: {0} removed event in queue, event id: {1}, events in queue: {2}".format( self._id, event._id, len( self._eventsQueue ) ))
        return True

    def getEventActive(self):
        """Return a list with activable events for a single task. Update the event Queue"""
        active = [] # list of active events
        
        for ev in list( self._eventsQueue.values() ):

            if ev.isAwaiting(): # event not activable in this task
                ev.decrTime2Go() # decrement time to go
                self._eventsQueue[ ev.getId() ] = ev # update events queue

            elif ev.isActivable(): # event activable
                ev.decrDuration() # decrement duration
                self._eventsQueue[ ev.getId() ] = ev # update events queue
                active.append( ev ) # insert the event in active events list

            else: # expired event
                self._eventsQueue.pop( ev.getId() ) #remove element from events queue 

        return active

    def evalutateShot( self, ev ):
        """" evalutate event shot effect """
        #la action da eseguire e l'inserimento di questa nella action queue.Eliminare l'automa aggiornando lo stato
        
        for sensor in self._sensors:
            if sensor.evalutateDamage(ev._energy, ev._power) == 0: # valutazione del danno per il sensore. Se restituisce 0 il sensore è dsitrutto
                self._sensors.pop( sensor ) # elimina il sensore dalla lista sensori dell'automa
                logger.logger.debug("Automa: {0} deleted sensor: {1} for damage".format( self._id, sensor._id ))

        for actuator in self._actuators:
            if actuator.evalutateDamage(ev._energy, ev._power)  == 0: # valutazione del danno per l'attuatore. Se restituisce 0 l'attuatore è dsitrutto
                self._actuators.pop( actuator ) # elimina il attuatore dalla lista attuatori dell'automa
                logger.logger.debug("Automa: {0} deleted actuator: {1} for damage".format( self._id, actuator._id ))

        if self.evalutateDamage(ev._energy, ev._power) == 0: # valutazione del danno per l'automa. Se restituisce 0 l'automa è dsitrutto
            self._state.destroy()
            logger.logger.debug("Automa: {0} destroyed for damage".format( self._id ))

        if self._state.isActive():
            # determinare la action da eseguire e l'inserimento di questa nella action queue.Eliminare l'automa aggiornando lo stato
            pass

        return True


    def evalutatePop( self, ev ):
        """" evalutate event pop effect """
        # viene valutato se l'automa può essere preso (sollevato). Si potrebbe considerare come nuovo componente dell'oggetto che ha generato l'evento. la action da eseguire e l'inserimento di questa nella action queue.Eliminare l'automa aggiornando lo stato
        pass

    def evalutatePush( self, ev ):
        """" evalutate event push effect """
        # viene valutato se l'automa può essere "spinto" (spostato). Valutare la nuova posizione dell'automa la action da eseguire e l'inserimento di questa nella action queue.Eliminare l'automa aggiornando lo stato
        pass

    def evalutateAssimilate( self, ev ):
        """" evalutate event eat effect """
        # viene valutato se l'automa può essere assorbito, la action da eseguire e l'inserimento di questa nella action queue.Eliminare l'automa aggiornando lo stato


    def evalutateMove( self, ev ):
        """" evalutate event move effect """
        # viene valutata l'esecuzione del movimento dell'automa, la action da eseguire e l'inserimento di questa nella action queue.
        pass

    
    # TEST: OK parziale
    def eval_actuators_activation( self, act ):
        """Choice the actuators for activation in relation with act and define parameter for execute action"""
        # act: (action_type, position or object)
        # return: # actuators_activation: [ actuators,  [ position or obj, ..other params, self ] ]
        
        if not act or not isinstance(act, list) or not General.checkActionType( act[0] ) or not( isinstance( act[1], Object) or General.checkPosition( act[1] ) ):
            raise Exception("action not found!")

        action_type = act[0]

        # actuators:  { key: actuator_type, value: actuator }
        if action_type == 'move' or action_type == 'run':
            actuator = self.getActuator( actuator_class = 'mover' )            

            if action_type == 'move': # OK                
                speed_perc = act[2] #0.7 # % della speed max. Il consumo di energia è calcolato applicando questa % al dt*power
            
            else:
                speed_perc = 1 # % della speed max. Il consumo di energia è calcolato applicando questa % al dt*power
                        

            target_position = act[ 1 ]            
            logger.logger.debug("Automa: {0}, created actuators_activation, action_type: {1}, target_position: {2} and speed_perc: {3}".format( self._id, action_type, target_position, speed_perc ))
            # NOTA!!!: L'esecuzione dell'azione move da parte di un attuatore, comporta lo spostamento effettivo dell'automa, quindi n attutori effettueranno complessivamente n move -> SBAGLIATO
            # Ciò significa che per l'esecuzione della action_type move deve essere azionato un solo attuatore che rappresenta l'insieme dei dispositivi dedicati a questo tipo di azione
            # nella actuators lista sarà quindi composta da un solo attuatore
            return [ actuator,  [ target_position, speed_perc ] ]            
            
        elif action_type == 'translate': # OK
            actuator = self.getActuator( actuator_class = 'object_manipulator' )
            obj = act[ 1 ]    
            destination = act[ 2 ]        
            logger.logger.debug("Automa: {0}, created actuators_activation with included: action_type: {1}, object: {2}".format( self._id, action_type, obj._id ))
            return [ actuator, [ obj, destination ] ]

        elif action_type == 'catch':
            actuator = self.getActuator( actuator_class = 'object_catcher' )
            obj = act[ 1 ]
            logger.logger.debug("Automa: {0}, created actuators_activation with included: action_type: {1}, object: {2}".format( self._id, action_type, obj._id ))
            return [ actuator, [ obj ] ]
        
        elif action_type == 'eat':
            actuator = self.getActuator( actuator_class = 'object_assimilator' )
            obj = act[ 1 ]
            logger.logger.debug("Automa: {0}, created actuators_activation with included: action_type: {1}, object: {2}".format( self._id, action_type, obj._id ))
            return [ actuator, [ obj ] ]

        elif action_type == 'shot':
            actuators = []
            plasma_actuators = self.getActuator( actuator_class = 'plasma_launcher' )
            projectile_actuators = self.getActuator( actuator_class = 'projectile_launcher' )
            
            if plasma_actuators:                                
                actuators.append( plasma_actuators )
            
            if projectile_actuators:
                actuators.append( projectile_actuators )

            actuator = actuators[ 0 ] #self.eval_best_actuators( actuators ) # Qui logica per decidere quale attuatore è meglio utilizzare

            obj = act[ 1 ]
            logger.logger.debug("Automa: {0}, created actuators_activation with included: action_type: {1}, object: {2}".format( self._id, action_type, obj._id ))
            return [ actuator, [ obj ] ]

        elif action_type == 'hit':
            actuator = self.getActuator( actuator_class = 'object_hitter' )
            obj = act[ 1 ]
            logger.logger.debug("Automa: {0}, created actuators_activation with included:  action_type: {1}, object: {2}".format( self._id, action_type, obj._id ))
            return [ actuator, [ obj ] ]
        
        elif action_type == 'attack':
            actuators = []
            catcher_actuators = self.getActuator( actuator_class = 'object_catcher' ) 
            projectile_actuators = self.getActuator( actuator_class = 'projectile_launcher' )
            plasma_actuators = self.getActuator( actuator_class = 'plasma_launcher' )
            hitter_actuators = self.getActuator( actuator_class = 'object_hitter' )

            if plasma_actuators:
                actuators.append( plasma_actuators )
            
            if projectile_actuators:
                actuators.append( projectile_actuators )

            if catcher_actuators:
                actuators.append( catcher_actuators )
            
            if hitter_actuators:
                actuators.append( hitter_actuators )
            
            actuator = actuators[ 0 ] #self.eval_best_actuators( actuators ) # Qui logica per decidere quale attuatore è meglio utilizzare

            obj = act[ 1 ]
            logger.logger.debug("Automa: {0}, created actuators_activation with included: list of {1} acutators, action_type: {2}, object: {3}".format( self._id, len( actuators ), action_type, obj._id ))
            return [ actuator, [ obj ] ]
        
        else:
            logger.logger.error("Automa: {0}, raised exception: 'action_type not found!!' ".format( self._id, len( actuators ), action_type, obj._id ))
            raise Exception("action_type not found!!")

        return

    def getActuator( self, actuator_class ):
        """Return actuator with actuator_class propriety. If actuator doesn't exists or is not operative return False """

        for actuator in self._actuators:

            if actuator.isClass( actuator_class ) and actuator.isOperative():        
                return actuator

        return False

    def setActuator( self, actuator):
        """Insert an Actuator in actuators list"""
        if not actuator or not isinstance(actuator, Actuator):
            return False
        self._actuators.append( actuator )
        return True



    def catchObject( self, obj):
        """Inserted obj in object catched list and set id automa in object take_from property"""
        if not obj:
            return False

        obj.setCaught_from( self._id )
        self._objectCatched.append( obj )

        return True

    def checkCaught( self, obj):
        """Return True if obj exist in object catched list, otherwise False"""
        for obj_ in self._objectCatched:
            if obj == obj_:
                return True
        return False