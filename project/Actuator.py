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
        self._delta_t = delta_t # Il tempo necessario per eseguire l'attuazione serve per calcolare il consumo energetico. Potrà essere utilizzato per gestire eventuali attuazioni che necessitano di più cicli
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

    #TEST: OK
    def exec_command( self, automa, posManager, param ):
        # param: [ position or obj, ..other params ]
        # ACTION_TYPE = ( "move", "run", "take", "catch", "eat", "attack", "escape", "nothing", "shot", "hit" )
        # return actions_info = [boolean for execute action, energy level of actuator]
        # il controllo e la scelta dell'attuatore da utilizzare per un determinato comando viene
        # fatta in automa quindi qui dovresti eseguire l'azione indipendentemente dall'interpretazione del comando
        # l'eventuale movimento, colpo, e conseguenze varie è valutato in automa
        # qui dovresti considerare solo gli effetti sull'attuatore
        # due possibilità o crei speccializazioni di attuatori con exec_command in override
        # oppure inserisci nei parametri del metodo il tipo di attuatore e il comando e qui selezioni
        # il metodo di esecuzione specifico per quell'attuatore. Quindi qui dovrai definire i varii metodi per 
        # ogni attuatore. Forse è meglio utilizzare l'ereditarietà. No definisco qui le diverse funzioni da utilizzare per ogni attuatore       

        if self._class == "object_manipulator":            
            return self.object_manipolating( automa, posManager, param )

        elif self._class == 'mover':                   
            moved, energy_actuator, position_reached = self.moving( automa, posManager, param )
            return [ moved, energy_actuator, position_reached ] # [True or False, energy_consume, True or False]

        elif self._class == "plasma_launcher":
            return self.plasma_launching( automa, posManager, param )

        elif self._class == "projectile_launcher":
            return self.projectile_launching( automa, posManager, param ) 

        elif self._class == "object_catcher":
            return self.object_catching( automa, posManager, param )

        elif self._class == "object_assimilator":
            return self.object_assimilating( automa, posManager, param )
        
        elif self._class == "object_hitter":
            return self.object_hitting( automa, posManager, param )

        else:
            raise Exception("Actuator class not defined")


        return

    
    def object_manipolating( self, mySelf, posManager, param ):
        pass
        
    def object_catching( self, mySelf, posManager, param ):
        pass
    
    def object_assimilating( self, mySelf, posManager, param ):
        pass
    
    def object_hitting( self, mySelf, posManager, param ):
        pass
    
    # TEST: OK
    def moving( self, automa, posManager, param ):
        """Exec move action and return action_info"""
        # action_type: move
        # param: [target_position, speed_perc], position è la posizione verso cui muovere[ action_type, position or obj, ..other params ]
        # direction: 
        # foward, foward_left. foward_right, foward_up_left, foward_up_right, foward_down_left, foward_down_right, foward_up, foward_down
        # backward, backward_left. backward_right, backward_up_left, backward_up_right, backward_down_left, backward_down_right, bacward_up, backward_down       
        # _left, _up_left, _down_left
        # _right, _up_right, _down_right
        # _up, _down
        position_reached = False
        automa_position = automa.getPosition()
        automa_coord = Coordinate( automa_position )
        next_position = param[ 0 ]
        speed_perc = param[ 1 ]
        direction = automa_coord.eval_direction( automa_position, next_position)
        logger.logger.debug("Actuator: {0} from: {1} to: {2} -  Evalutate direction: {3}".format( self._id, automa_position, next_position, direction ))
        energy_actuator = self._state.getEnergy()
        max_dist_for_single_iteration = int( speed_perc * General.MAX_SPEED ) 
        min_dist_from_pos_to_dest = min( abs( automa_position[ 0 ] - next_position[ 0 ] ), abs( automa_position[ 1 ] - next_position[ 1 ] ), abs( automa_position[ 2 ] - next_position[ 2 ] ) )
        num_iteration = min( max_dist_for_single_iteration,  min_dist_from_pos_to_dest) # min_dist_from_pos_to_dest determina il massimo numero di posizioni che è possibile percorrere limitando di fatto lo spostamento possibile nelle altre dimensioni: sarebbe necessario gestire il movimento distinguendo ogni lo spostamento in ogni dimensione

        if max_dist_for_single_iteration >= min_dist_from_pos_to_dest:
            position_reached = True

        logger.logger.debug("Actuator: {0} -  max_dist_for_single_iteration: {1},  min_dist_from_pos_to_dest: {2},  num Iteration: {3} ".format( self._id, max_dist_for_single_iteration,  min_dist_from_pos_to_dest, num_iteration ))

        for i in range( num_iteration ):# la velocità determina il numero di iterazioni
            automa_coord.move( direction )
            automa_position = automa_coord.getPosition()
            
            if not posManager.moveObject( automa_coord.getPosition(), automa ):
                logger.logger.debug("Actuator: {0} not executed move action. Iteration: {1} Energy_actuator {2}  position_reached {3}".format( self._id, i, energy_actuator, position_reached ))
                return False, energy_actuator, position_reached
            # l'energia è presente nello stato dell'attuatore, tuttavia è l'automa che fornisce energia all'attuatore quindi ha senso 
            # restituire all'automa la info sul consumo energetico relativo alla perception
            # In questa prima versione decremento solo l'energia dell'attuatore, quando questa diventa 0 l'automa deve provveedere
            # a ricaricare l'energia dell'attuatore tramite la propria energia (con un fattore di  moltiplicazione: 1 energia automa = x energia sensore)
            energy_actuator = self._state.updateEnergy( self._power * speed_perc, self._delta_t )
            logger.logger.debug("Actuator: {0} executed move action. Iteration: {1} Energy_actuator {2} position_reached {3}".format( self._id, i, energy_actuator, position_reached ))
        
            if automa_position[ 0 ] == next_position[ 0 ] or automa_position[ 0 ] == next_position[ 0 ] or automa_position[ 0 ] == next_position[ 0 ]:
                logger.logger.debug("Actuator: {0} executed move action. Iteration: {1} Energy_actuator {2}  position_reached {3}".format( self._id, i, energy_actuator, position_reached ))
                return True, energy_actuator, position_reached
            
        return True, energy_actuator, position_reached



    def projectile_launching( self, mySelf, posManager, param):
        pass
    
    def plasma_launching( self, mySelf, posManager, param):
        pass



    def setId( self, id = None ):

        if not id:
            return False
        else:
            self._id = id        
            
        return True

    def getId( self ):
        return self._id

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
