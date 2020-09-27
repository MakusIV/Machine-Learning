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

    def __init__(self, name = 'Automa', dimension = [1, 1, 1], resilience = 10, state = State(run = True), ai = AI(), coord = None, sensors= None, actuators = None   ):

        Object.__init__(self, name = name, dimension = dimension, resilience = resilience, coord = coord, state = state)

        self._ai = ai #AI Engine
        self._power = power # nota l'energia è gestita nello stato in quanto è variabile        
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
        # l'evento riguarda una posizione indipendentemente dall'eventuale target impostato, quindi in base 
        # alle caratteristiche dell'evento che bissogna valutare quali elementi sono coinvolti e come sono
        # coinvolti
        
        for k, ev in events: # scorre gli eventi da eseguire della lista eventi attivi
            
            if ev.isShot(): # solo per l'evento SHOT viene valutato l'eventuale danno
                self.evalutateShot( ev )

            if ev.isPop(): # viene valutato se l'automa può essere preso (sollevato). Si potrebbe considerare come nuovo componente dell'oggetto che ha generato l'evento.
                self.evalutatePop( ev )

            if ev.isPush(): # viene valutato se l'automa può essere "spinto" (spostato). Valutare la nuova posizione dell'automa
                self.evalutatePush( ev )

            if ev.isEat(): # viene valutato se l'automa può essere mangiato. Eliminare l'automa aggiornando lo stato
                self.evalutateEat( ev )

    
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
        for k, act in self._actionsQueue.items():
            actions_info.append( self._actuators.eval_command(act) )
            self.updateStateForAction( actions_info )
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
