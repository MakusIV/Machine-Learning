# Automa
from Object import Object
from State import State
from Actuator import Actuator
from Sensor import Sensor
from AI import AI
import General
from LoggerClass import Logger

# LOGGING --
 
logger = Logger(module_name = __name__, class_name = 'Automa')


class Automa(Object):
    """Automa derived from Object. """

    def __init__(self, name = 'Automa', dimension = [1, 1, 1], coord = None, state = State(run = True), ai = AI(), sensors= None, actuators = None   ):

        Object.__init__(self, name = name, dimension = dimension, coord = coord, state = state)

        self._ai = ai #AI Engine
        self._state = state #Class State        
        self._sensors = sensors# Class Sensor
        self._actuators = actuators#Class Actuators
        self.action_executed = None
        self._eventsQueue = {} #  {key: event id, value = event}
        self._actionsQueue = {} #  {key: event id, value = action}

        if not self.checkProperty():
            raise Exception("Invalid properties! Automata not istantiate.")

    
    
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
    
    def runTask(self, posManager):

        self.update() #check the eventsQueue and update state
        percptInf = self.percept(posManager)
        self.evalutate( percptInf ) # create the action info to execute and inserts in the action Queue
        return self.action() # return the Queue of the action info executed in a single task



    def update(self):
        """Update state, Sensor, Actuator states for check of eventsQueue"""        
        events = self.getEventActive()
        # managed events active to update state, sensor, actuator
        return True
        


    def percept(self, posMng):
        """Percepts the enviroments with sensors, update the state and return percept informations."""
        #percept_info: le informazioni dopo l'attivazione dei sensori e lo stato degli stessi (classe)
        #request_percept: le informazioni riguardo tipo di sensori e modalità di attivazione
        request_percept = None #definire la logica di utilizzo dei sensori (funzione dello stato??: minacciato, insicuro, allerta, normale, affamato, critico, ecc. ma sono info da chiedere alla ai?)
        percept_info = self._sensors.perception( request_percept, posMng )# attiva i sensori per ottenere le informazioni sull'ambiente       
        self.updateStateForPercept( percept_info )# aggiorna lo stato dell'automa
        return percept_info 


    def evalutate(self, percept_info ):
        """Evalutate the info of the enviroments knows (percept info) and return the action to execute"""       
        # determina quali sono le azioni che può svolgere in questo singolo task e le inserisce nella queue action
        self._actionsQueue = self.ai.evalutate(percept_info, self._state) # noota: la queue si resetta ad ogni task
        return True


    def action(self, request_action):
        """Activates Actuators for execution of Action. Return action informations."""
        #action_info: le informazioni dopo l'attivazione degli attuatori e lo stato degli stessi( classe)
        actions_info = []
        for act in self._actionsQueue:
            action_info.append( self._actuators.eval_command(act) )
            self.updateStateForAction( action_info )
        return actions_info


    # vedi il libro
    def checkProperty(self):
        return General.checkAI( self._ai ) and General.checkState( self._internal_state ) and General.checkSensors (self._sensors ) and General.checkActuators( self._actuator )
        
    def updateStateForPercept(self, percept_info):
        """Update state, Sensor, Actuator states for Percept  info"""
        return True

    def updateStateForAction(self, action_info):
        """Update state, Sensor, Actuator states for Action info"""
        return True

    def insertEvent(self, event):
        """insert event in eventsQueue"""
        if not General.checkEvent(event):
            return False
        self._eventsQueue.insert( event._id = event )
        return True

    def removeEvent(self, event_id):
        """remove event in eventsQueue"""
        if not isinstance(event_id, int) :
            return False
        self._eventsQueue.pop( event_id )        
        return True

    def getEventActive(self):
        """Return a list with activable events for a single task. Update the event Queue"""
        active = []
        for _, ev in self._eventsQueue:
            if ev._t2g > 1: # event not activable in this task
                ev._t2g = ev._t2g - 1 # decrement time to go
            elif ev._t2g == 1 and ev._duration > 1: # event activable
                ev._duration = ev._duration - 1
                active.append(ev)
            else: # end duration of the activate event
                self.removeEvent( ev.event_id )         
        return active

    