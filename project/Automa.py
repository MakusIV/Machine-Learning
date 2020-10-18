# Automa
from Object import Object
from State import State
from Actuator import Actuator
from Sensor import Sensor
from AI import AI
import General
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
        return self.action() # return the Queue of the action info executed in a single task



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

            if ev.isEat(): # viene valutato se l'automa può essere mangiato. Eliminare l'automa aggiornando lo stato
                self.evalutateEat( ev )

        logger.logger.debug("Automa: {0} executed update internal state".format( self._id ))
        return True
        
    # TEST: OK
    def percept(self, posMng):
        """Percepts the enviroments with sensors, update the state and return percept informations."""
        #percept_info: le informazioni dopo l'attivazione dei sensori: (energy_consumption, list_obj_detected)
        #request_percept: le informazioni riguardo tipo di sensori e modalità di attivazione
        operative_sensors = [ sensor for sensor in self._sensors if sensor.isOperative() ]# Lista dei sensori attivi
        percept_infos = [ sensor.perception( posMng, self.getPosition() ) for sensor in operative_sensors ]# lista delle perception info ottenuta interrogando tutti i sensori operativi. La percept_info: percept_info: (energy_sensor, detected_objs) detected. detected_objs = { ( x, y, z): obj }
        list_obj = [ percept_info[ 1 ] for percept_info in percept_infos ]# lista degli object
        energy_consumption = [ percept_info[ 0 ] for percept_info in percept_infos ]
        self.updateStateForEnergyConsumption( energy_consumption )# aggiorna lo stato dell'automa
        logger.logger.debug("Automa: {0} execute perception: activated {1} sensor, detected {2} object, energy consumed: {3}".format( self._id, len( operative_sensors ), len( list_obj ), energy_consumption  ))
        return list_obj 


    def evalutate(self, percept_info ):
        """Evalutate the info of the enviroments knows (percept info) and return the action to execute"""       
        # determina quali sono le azioni che può svolgere in questo singolo task e le inserisce nella queue action
        self._actionsQueue = self.ai.evalutate(percept_info, self._state) # noota: la queue si resetta ad ogni task
        logger.logger.debug("Automa: {0} execute evalutate percept_info: created actionQueue with {1} items".format( self._id, len( self._actionsQueue ) ))
        return True


    def action(self, request_action):
        """Activates Actuators for execution of Action. Return action informations."""
        #action_info: le informazioni dopo l'attivazione degli attuatori e lo stato degli stessi( classe)
        actions_info = [] # (action_type, position, object)

        for _, act in self._actionsQueue.items():
            # in base ad act devi determinare quali attuatori sono coinvolti e attivarli
            # actuators_activation: (actuator, action_description)
            actuators_activation = self.eval_actuators_activation( act ) # questa funzione deve anche valutare gli attuatori attivi e se questi sono sufficienti per compiere l'atto altrimenti deve restituire false o un atto ridotto
            logger.logger.debug("Automa: {0} execute action: act:created actionQueue with {1} items".format( self._id, len( self._actionsQueue ) ))

            for act in actuators_activation:               
                actions_info.append( act[0].exec_command( act[ 1 ]) )# act[0]: actuator, act[1]: action_description

            self.updateStateForAction( actions_info )

        logger.logger.debug("Automa: {0} executed action: created action_info with {1} items".format( self._id, len( action_info ) ))
        return actions_info

    
    # vedi il libro
    def checkParamAutoma(self, power, sensors, actuators):            
        """Return True if conformity of the parameters is verified"""
        
        if not power or not isinstance(power, int) or not( power <= 100 and power >= 0 ) or not sensors or not isinstance(sensors[0], Sensor) or not Sensor.checkSensorList(sensors[0], sensors) or not actuators or not isinstance(actuators[0], Actuator) or not Actuator.checkActuatorList(actuators[0], actuators):
            return False
        return True

        
    def updateStateForEnergyConsumption(self, energy_consumption):
        """Update state, Sensor, Actuator states for Percept  info"""                
        total_sensor_consumption = sum( energy_consumption )
        self._state.decrementEnergy( total_sensor_consumption )
        return True

    def updateStateForAction(self, action_info):
        """Update state, Sensor, Actuator states for Action info"""
        return True

    def insertEvent(self, event):
        """insert event in eventsQueue"""
        if not General.checkEvent(event):
            return False

        self._eventsQueue[ event._id ] = event
        return True

    def removeEvent(self, event):
        """remove event in eventsQueue"""
        if not isinstance(event._id, int) :
            return False

        self._eventsQueue.pop( event._id )        
        return True

    def getEventActive(self):
        """Return a list with activable events for a single task. Update the event Queue"""
        active = [] # list of active events
        
        for k, ev in self._eventsQueue.items():

            if ev.isAwaiting(): # event not activable in this task
                ev.decrTime2Go() # decrement time to go
                self._eventsQueue[ k ] = ev # update events queue

            elif ev.isActivable(): # event activable
                ev.decrDuration() # decrement duration
                self._eventsQueue[ k ] = ev # update events queue
                active.append( ev ) # insert the event in active events list

            else: # expired event
                self._eventsQueue.pop( ev.event_id ) #remove element from events queue 

        return active

    def evalutateShot( self, ev ):
        """" valuta gli effetti dell'evento shot sui tutti gli elementi dell'automa """
        
        for sensor in self._sensors:
            if sensor.evalutateDamage(ev._energy, ev._power) == 0: # valutazione del danno per il sensore. Se restituisce 0 il sensore è dsitrutto
                self._sensors.pop( sensor )# elimina il sensore dalla lista sensori dell'automa

        for actuator in self._actuators:
            if actuator.evalutateDamage(ev._energy, ev._power)  == 0: # valutazione del danno per l'attuatore. Se restituisce 0 l'attuatore è dsitrutto
                self._actuators.pop( actuator )# elimina il attuatore dalla lista attuatori dell'automa

        if self.evalutateDamage(ev._energy, ev._power) == 0: # valutazione del danno per l'automa. Se restituisce 0 l'automa è dsitrutto
            self._state.destroy()

        return True


    def evalutatePop( self, ev ):
        """" valuta gli effetti dell'evento pop sull'automa """
        # viene valutato se l'automa può essere preso (sollevato). Si potrebbe considerare come nuovo componente dell'oggetto che ha generato l'evento.
        pass

    def evalutatePush( self, ev ):
        """" valuta gli effetti dell'evento push sull'automa """
        # viene valutato se l'automa può essere "spinto" (spostato). Valutare la nuova posizione dell'automa
        pass

    def evalutateEat( self, ev ):
        """" valuta gli effetti dell'evento eat sull'automa """
        # viene valutato se l'automa può essere mangiato. Eliminare l'automa aggiornando lo stato
        pass

    

    def eval_actuators_activation( self, act ):
        """Choice the actuators for activation in relation with act"""
        # act: (action_type, position or object)
        # return: # actuators_activation: (actuator, action_description)
        
        if not act or not isinstance(act, list) or not General.checkActionType( act[0] ) or not( isinstance( act[1], Object) or General.checkPosition( act[1] ) ):
            raise Exception("action not found!")

        action_type = act[0]

        # actuators:  { key: actuator_type, value: actuator }
        if action_type == 'move' or action_type == 'run' or action_type == 'escape':
            actuators = self.getActuators( actuator_class = 'mover', only_active = True )
            
            if action_type == 'move':
                speed = 0.7 # % della speed max. Il consumo di energia è calcolato applicando questa % al dt*power

            else:
                speed = 1 # % della speed max. Il consumo di energia è calcolato applicando questa % al dt*power
            
            position = act[ 1 ]            
            return [ actuators, action_type, position, speed ]
            
        elif action_type == 'take':
            actuators = self.getActuators( actuator_class = 'object_manipulator' )
            obj = act[ 1 ]
            return [ actuators, action_type, obj ]

        elif action_type == 'catch':
            actuators = self.getActuators( actuator_class = 'object_catcher' )
            obj = act[ 1 ]
            return [ actuators, action_type, obj ]
        
        elif action_type == 'eat':
            actuators = self.getActuators( actuator_class = 'object_adsorber' )
            obj = act[ 1 ]
            return [ actuators, action_type, obj ]

        elif action_type == 'shot':
            actuators = self.getActuators( actuator_class = 'plasma_launcher' )  + self.getActuators( actuator_class = 'projectile_launcher' )
            obj = act[ 1 ]
            return [ actuators, action_type, obj ]

        elif action_type == 'hit':
            actuators = self.getActuators( actuator_class = 'object_hitter' )
            obj = act[ 1 ]
            return [ actuators, action_type, obj ]
        
        elif action_type == 'attack':
            actuators = self.getActuators( actuator_class = 'object_catcher' ) + self.getActuators( actuator_class = 'projectile_launcher' ) + self.getActuators( actuator_class = 'plasma_launcher' ) +     actuators.append( self.getActuators( actuator_class = 'object_hitter' ) )
            actuators = self.eval_best_actuators( actuators )
            obj = act[ 1 ]
            return [ actuators, action_type, obj ]
        
        else:
            raise Exception("action_type not found!!")

        return

    def getActuators( self, actuator_class, only_active = None ):
        """Return list of actuator with actuator_class propriety """
        actuators = list()


        for actuator in self._actuators:

            if actuator.isType( actuator_class ):
                
                if not only_active:
                    actuators.append( actuator )

                elif actuator.isOperative():
                    actuators.append( actuator )
        
        return actuators
