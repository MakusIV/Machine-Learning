# Automa
from Object import Object
from State import State
from Actuator import Actuator
from Sensor import Sensor
from AI import AI
import General

class Automa(Object):
    """Automa derived from Object. """

    def __init__(self, name = 'Automa', dimension = [1, 1, 1], coord = None, state = State(run = True), ai = AI(), sensors= None, actuators = None   ):

        Object.__init__(self, name = name, dimension = dimension, coord = coord, state = state)

        self._ai = ai #AI Engine
        self._state = state #Class State        
        self._sensors = sensors# Class Sensor
        self._actuators = actuators#Class Actuators
        self.action_executed = None
        self._eventsQueue = []
                         
        if not self.checkProperty():
            raise Exception("Invalid properties! Automata not istantiate.")

    
    
    # Methods


    # La sequenza è percept --> evalutate --> action. Bisogna decidere se queste tre azioni devono
    # essere svolte in una unità temporale ovvero ognuna in una unità temporale (forse è meglio)
    # in quest'ultimo caso è necessaria una Queue è deve essere valutato come gestire i cambiamenti
    # dell'enviroments che avvengono tra una azione e la successiva.
    # Per semplificare è meglio eseguire le tre azioni come unico task
    
    # La AI è deputata esclusivamente alla valutazione delle informazioni ricevute dai sensori per 
    # l'aggiornamento dello stato dell'automa per definire l'azione da compiere in base a queste informazioni.
    # la proprietà 'env_state che rappresenta l'enviromets conosciuto dall'automa è interna e gestita nella AI
    
    def runTask(self, posManager):

        self.updateStateForEvent() #check the eventsQueue and update state
        percptInf = self.percept(posManager)
        self.action_executed = self.evalutate( percptInf )
        return self.action(self.action_executed)

    


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
        self.current_action  = self.ai.evalutate(percept_info, self._state)
        return self.current_action

    def action(self, request_action):
        """Activates Actuators for execution of Action. Return action informations."""
        #action_info: le informazioni dopo l'attivazione degli attuatori e lo stato degli stessi( classe)
        action_info = self._actuators.eval_command(request_action)
        self.updateStateForAction( action_info )


    # vedi il libro
    def checkProperty(self):
        return General.checkAI( self._ai ) and General.checkState( self._internal_state ) and General.checkSensors (self._sensors ) and General.checkActuators( self._actuator )
        
    def updateStateForPercept(self, percept_info):
        """Update state, Sensor, Actuator states for Percept  info"""
        return True

    def updateStateForEvent(self):
        """Update state, Sensor, Actuator states for check of eventsQueue"""        
        for event in self._eventsQueue:
            # evalutation for update state
            pass

        self._eventsQueue.clear()
        return True

    def updateStateForAction(self, action_info):
        """Update state, Sensor, Actuator states for Action info"""
        return True

    def insertEvent(self, event):
        """insert event in eventsQueue"""
        if not checkEvent(event):
            return False

        self._eventsQueue.append(event)
        return True