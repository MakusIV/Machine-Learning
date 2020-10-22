import random
from Coordinate import Coordinate
import General
from State import State
from LoggerClass import Logger

# LOGGING --
 
logger = Logger(module_name = __name__, class_name = 'Actuator')


class Actuator:
    #position, range_max, typ, emissivity_perception = 1, power = 100, resilience = 100, delta_t = 0.01, accuracy = 5, name = None, state = None 
    def __init__(self, position, range_max, class_, typ, power = 100,  resilience = 100, delta_t = 0.01, name = None  ):

        if not self.checkParam( position, class_, typ, range_max, power, resilience, delta_t ):
            raise Exception("Invalid parameters! Actuator not istantiate.")

        self._name = name
        self._id = General.setId('Actuator_ID', None) # Id generator automaticamente
        self._power = power# nota l'energia è gestita nello stato in quanto è variabile  
        self._range = range_max# è rappresentato da una tupla di distanze (x_d:int, y_d:int, z_d:int)
        self._state = State( run = True )
        self._resilience = resilience # resistenza ad uno SHOT in termini di power (se shot power > resilence --> danno al actuatore)
        self._delta_t = delta_t # Il tempo necessario per eseguire l'attuazione serve per calcolare il consumo energetico. Puotrà essere utilizzato per gestire eventuali detection che necessitano di più cicli
        self._type = typ # il tipo di attuazione (vedi General.ACTUATOR_TYPE)
        self._class = class_ # la classe dell'attuatore (vedi General.ACTUATOR_TYPE)
        self._position = position
      

        if not name:
            self._name = General.setName('Actuator_Name')
        else:
            self._name = name


    #TEST: OK
    def checkParam( self, position, class_, typ, range_max,  power, resilience, delta_t ):
        """Return True if conformity of the parameters is verified"""
        if not( range_max and range_max[0] >0 and range_max[1] >0 and range_max[2] >0 and delta_t and delta_t <= 1 and delta_t >= 0 and power and power <= 100 and power >= 0 and  resilience and  resilience <= 100 and resilience >= 0 ):
            return False
        
        if not typ or not class_ or not ( General.checkActuatorTypeAndClass( typ, class_ ) and General.checkPosition( position ) ):
            return False

        return True


    def isType( self, actuator_type ):
        """Return True if actuator have self._type == actuator_type"""
        return self._type == actuator_type
                        
    

    def isClass( self, actuator_class ):
        """Return True if actuator have self._class == actuator_class"""   
        return self._class == actuator_class
    

    def isOperative(self):
        """Return true if sensor state is running"""
        return self._state.isRunning()
        

    #TEST: OK
    def isClassAndType( self, actuator_class, actuator_type ):
        """Return True if actuator have self._class == actuator_class and self._type == actuator_type """   
        return self._type == actuator_type and self._class == actuator_class


    def exec_command( self, mySelf, posManager, action_param ):
        # action param: actuators_activation: [ Automa, action_type, position or obj, ..other params ] ][ action_type, speed, strenght, duration ecc. ]
        # ACTION_TYPE = ( "move", "run", "take", "catch", "eat", "attack", "escape", "nothing", "shot", "hit" )
        # return actions_info = (action_type, energy_consume, position, object)
        # il controllo e la scelta dell'attuatore da utilizzare per un determinato comando viene
        # fatta in automa quindi qui dovresti eseguire l'azione indipendentemente dall'interpretazione del comando
        # l'eventuale movimento, colpo, e conseguenze varie è valutato in automa
        # qui dovresti considerare solo gli effetti sull'attuatore
        # due possibilità o crei speccializazioni di attuatori con exec_command in override
        # oppure inserisci nei parametri del metodo il tipo di attuatore e il comando e qui selezioni
        # il metodo di esecuzione specifico per quell'attuatore. Quindi qui dovrai definire i varii metodi per 
        # ogni attuatore. Forse è meglio utilizzare l'ereditarietà. No definisco qui le diverse funzioni da utilizzare per ogni attuatore       

        if self._class == "object_manipulator":
            return object_manipolating( mySelf, posManager, action_param )

        elif self._class == 'mover':       
            result_action = moving( mySelf, posManager, action_param )
            return [ result_action, energy_consume, new_automa_position ]

        elif self._class == "plasma_launcher":
            return plasma_launching( mySelf, posManager, action_param )

        elif self._class == "projectile_launcher":
            return projectile_launching( mySelf, posManager, action_param ) 

        elif self._class == "object_catcher":
            return object_catching( mySelf, posManager, action_param )

        elif self._class == "object_adsorber":
            return object_adsorbing( mySelf, posManager, action_param )
        
        elif self._class == "object_hitter":
            return object_hitting( mySelf, posManager, action_param )

        else:
            raise Exception("Actuator class not defined")


        return

    
    def object_manipolating( self, mySelf, posManager, action_param ):
        pass
        
    def object_catching( self, mySelf, posManager, action_param ):
        pass
    
    def object_adsorbing( self, mySelf, posManager, action_param ):
        pass
    
    def object_hitting( self, mySelf, posManager, action_param ):
        pass
    
    def moving( self, mySelf, posManager, action_param ):
        """Exec move action and return action_info"""
        # action_type: move
        # action_param: [position, speed], position è la posizione verso cui muovere
        # direction: "foward", "up" ecc
        new_coord = Coordinate( mySelf.getPosition() )
        direction = new_coord.eval_direction( new_coord.getPosition(), position))
    
        for _ in range( int( action_param[ 1 ] * General.MAX_SPEED / 100 ) ):# la velocità determina il numero di iterazioni
            new_coord.move( direction )
            
            if not posManager.moveObject( new_coord ):
                return False
        
        return True



    def projectile_launching( self, mySelf, posManager, action_param):
        pass
    
    def plasma_launching( self, mySelf, posManager, action_param):
        pass



    def setId( self, id = None ):

        if not id:
            return False
        else:
            self._id = id        
            
        return True


    def setName(self, name):

        if not name:
            return False
        else:
            self._name = name

        return True

    def eval_command(self, request_action):
        # Valuta quali attuatori attivare e come attivarli in base alle info contenute in request_action (class Action)
        # Restituisce le informazioni sulle azioni effettuate quali stato, posizione degli attuatori
        action_info = None
        return action_info


    #TEST: OK
    def checkActuatorClass(self, actuator):
        """Return True if actuators is a actuator object otherwise False"""
        if not actuator or not isinstance(actuator, Actuator):
            return False
        
        return True


    #TEST: OK
    def checkActuatorList(self, actuators):

        """Return True if actuators is a list of Actuator object otherwise False"""
        if actuators and isinstance(actuators, list) and all( isinstance(actuator, Actuator) for actuator in actuators ):
            return True

        return False


    def isOperative(self):
        """Return true if actuator state is running"""
        return self._state.isRunning()


    # TEST: OK
    def evalutateSelfDamage(self, energy, power):
        """Evalutate the damage on actuator and update state"""
        if power > self._resilience:
            damage = power - self._resilience# in realtà il danno dovrebbe essere proporzionale all'energia
            return self._state.decrementHealth( damage )
        
        return self._state.getHealth()
