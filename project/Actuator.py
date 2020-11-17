import random
from Coordinate import Coordinate
import General
from State import State
from Event import Event
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
            #param: [object, destination]
            manipulated, energy_actuator, manipulate_terminated =  self.object_manipulating( automa, posManager, param )
            return [ manipulated, energy_actuator, manipulate_terminated] # [True or False, energy_consume]

        elif self._class == 'mover':                 
            #param: destination
            moved, energy_actuator, move_terminated = self.moving( automa, posManager, param )
            return [ moved, energy_actuator, move_terminated ] # [True or False, energy_consume, True or False]

        elif self._class == "plasma_launcher":
            return self.shooting( automa, posManager, param )

        elif self._class == "projectile_launcher":
            return self.shooting( automa, posManager, param ) 

        elif self._class == "object_catcher":
            #param[object]        
            catched, energy_actuator, catch_terminated =  self.object_catching( automa, posManager, param )
            return [ catched, energy_actuator, catch_terminated ] # [True or False, energy_consume]

        elif self._class == "object_assimilator":
            return self.object_assimilating( automa, posManager, param )
        
        elif self._class == "object_hitter":
            return self.shooting( automa, posManager, param )

        else:
            raise Exception("Actuator class not defined")


        return


    # TEST: OK
    def object_manipulating( self, automa, posManager, param ):
        #param[0] = object, param[1]= destination
        obj = param[ 0 ]
        destination = param[ 1 ]
        manipulation_terminated = True# serve per implementare la gestione di manipolazioni che richiedono più task per essere completate

        energy_actuator = self._state.updateEnergy( self._power, self._delta_t )
        # verifica se param[1] destinazione dello spostamento, range attuatore e posizione dell'automa sono idonei per l'esecuzione della attuaione
        if not self.isInRange( destination ):
            logger.logger.debug("Actuator: {0} not executed manipulate action because destination is out of range. destination: {1}, range: {2}, energy_actuator: {3}".format( self._id, destination, self._range, energy_actuator ))
            return [ False, energy_actuator, False ]

        result = posManager.moveObject( destination, obj )# lo spostamento dell'oggetto nella posizione di destinazione avviene sempre in quanto rientra nel range dell'attuatore. Quindi l'eventuale richiesta di più task per la conclusione dell'attuazione non può essere imputata al raggiungimento della destinazione come nella move action ma, eventualmente, ad un tempo e quindi gestita nellla classe Automa

        # Creazione evento e inserimento nella event queue qualora l'object è un automa
        self.setEvent( automa = automa, result = True, obj = obj, typ = 'PUSH', duration = 0 ) # duration = 0 -> effetti evento già applicati su object        
        logger.logger.debug("Actuator: {0} result manipulate = {1}. destination: {2}, range: {3}, energy_actuator: {4}".format( self._id, result, destination, self._range, energy_actuator ))        
        return result, energy_actuator, manipulation_terminated 

        
 
    def object_assimilating( self, automa, posManager, param ):
        """Execute catching action and return action_info"""
        # action_type: object_assimilting
        #param[0] = object, param[1]= destination
        assimilating_terminated = False# serve per implementare la gestione di catture che richiedono più task per essere completate
        obj = param[ 0 ]       
        energy_actuator = self._state.updateEnergy( self._power, self._delta_t )
        # verifica se param[1] destinazione dello spostamento, range attuatore e posizione dell'automa sono idonei per l'esecuzione della attuaione
        if not self.isInRange( obj.getPosition() ):
            logger.logger.debug("Actuator: {0} not executed assimilate action because object not in range. automa: {1}, object position: {2}, range: {3}, energy_actuator: {4}".format( self._id, obj.getCaught_from(), obj.getPosition(), self._range, energy_actuator ) )
            return [ False, energy_actuator, True ]# imposto assimilating_terminated = True per consentire l'eliminazione della action nella coda delle action
       

        if obj.getHealth() != obj.evalutateDamage( self._power ):# valuta se la power dell'attuatore è superiore alla resilience dell'obj e pertanto casua una diminuzione della health
            obj_resilience = obj.getResilience()            
            obj_health = obj._state.getHealth()
            obj_active = obj._state.isActive()
            obj_critical = obj._state.isCritical()
            obj_anomaly = obj._state.isAnomaly()
            obj_destroyed = obj._state.isDestroyed()
            obj_remove = obj._state.isRemoved()
            obj_energy = obj._state.getEnergy()
            logger.logger.debug("Actuator: {0} executed assimilate action with object damage. automa: {1}, object position: {2}, range: {3}, energy_actuator: {4}, object_resilience: {5}, object_health: {6}, object_active: {7}, object_critical: {8}, object_anomaly: {9}, object_destroyed: {10}, object_removed: {11}, object_energy: {12}".format( self._id, automa.getId(), obj.getPosition(), self._range, energy_actuator, obj_resilience, obj_health, obj_active, obj_critical, obj_anomaly, obj_destroyed, obj_remove, obj_energy ) )

            if obj_destroyed: # la conclusione dell'azione è condizionata dalla distruzione dell'oggetto.
                assimilating_terminated = True

                if posManager.removeObject( obj ):
                    energy_increment = int( obj_energy * obj._mass / automa._mass )
                    automa._state.incrementEnergy( energy_increment ) #energy assimilate                                               
                    logger.logger.debug("Actuator: {0} executed assimilate action with complete assimilation and energy gain: {1}. Object was removed from position manager. automa: {2}, range: {3}, energy_actuator: {4}".format( self._id, energy_increment, automa.getId(), self._range, energy_actuator ) )
                    # Creazione evento e inserimento nella event queue qualora l'object è un automa
                    self.setEvent( automa = automa, result = True, obj = obj, typ = 'ASSIMILATE', duration = 1, time2go = 0) # duration = 0 -> effetti evento già applicati su object
                    return [ True, energy_actuator, assimilating_terminated ]
        
                else:                
                    raise Exception("object_assimilating not executed but object was removed form position manager")

            else:
                logger.logger.debug("Actuator: {0} executed assimilate action. Action not complete, Object wasn't removed from position manager. automa: {1}, range: {2}, energy_actuator: {3}".format( self._id, automa.getId(), self._range, energy_actuator ) )

                # Creazione evento e inserimento nella event queue qualora l'object è un automa
                self.setEvent( automa = automa, result = True, obj = obj, typ = 'ASSIMILATE', duration = 0) # duration = 0 -> effetti evento già applicati su object
                return [ True, energy_actuator, assimilating_terminated ]

        logger.logger.debug("Actuator: {0} not executed assimilate action Automa power < Object resilience. Automa: {1}, object position: {2}, range: {3}, energy_actuator: {4}".format( self._id, automa.getId(), obj.getPosition(), self._range, energy_actuator ) )        
        return [ False, energy_actuator, assimilating_terminated ]


                
    
    # TEST: OK
    def moving( self, automa, posManager, param ):
        """Execute move action and return action_info"""
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
        
            if automa_position[ 0 ] == next_position[ 0 ] and automa_position[ 1 ] == next_position[ 1 ] and automa_position[ 2 ] == next_position[ 2 ]:
                logger.logger.debug("Actuator: {0} executed move action. Iteration: {1} Energy_actuator {2}  position_reached {3}".format( self._id, i, energy_actuator, position_reached ))
                return True, energy_actuator, position_reached
            
        return True, energy_actuator, position_reached

    # TEST: OK
    def object_catching( self, automa, posManager, param ):
        """Execute catching action and return action_info"""
        # action_type: catch
        #param[0] = object, param[1]= destination
        catch_terminated = True# serve per implementare la gestione di catture che richiedono più task per essere completate
        obj = param[ 0 ]       
        energy_actuator = self._state.updateEnergy( self._power, self._delta_t )
        # verifica se param[1] destinazione dello spostamento, range attuatore e posizione dell'automa sono idonei per l'esecuzione della attuaione
        if not self.isInRange( obj.getPosition() ):
            logger.logger.debug("Actuator: {0} not executed catch action because object not in range. automa catcher: {1}, object position: {2}, range: {3}, energy_actuator: {4}".format( self._id, obj.getCaught_from(), obj.getPosition(), self._range, energy_actuator ) )
            return [ False, energy_actuator, catch_terminated ]
       

        if posManager.removeObject( obj ):
            
            if automa.catchObject( obj ):
                logger.logger.debug("Actuator: {0} executed catch action. automa catcher: {1}, range: {2}, energy_actuator: {3}".format( self._id, obj.getCaught_from(), self._range, energy_actuator ) )
                return [ True, energy_actuator, catch_terminated ]
        
            else:                
                raise Exception("object_catching not executed but object was removed form position manager")

        logger.logger.debug("Actuator: {0} not executed catch action because remove object not carried out. automa catcher: {1}, object position: {2}, range: {3}, energy_actuator: {4}".format( self._id, obj.getCaught_from(), obj.getPosition(), self._range, energy_actuator ) )
        return [ False, energy_actuator, catch_terminated ]

        


    # TEST: OK
    def shooting( self, automa, posManager, param):
        """Execute projectile launching action and return action_info"""
        # action_type: shot
        #param[0] = object, param[1]= destination
        firing_terminated = False # Se l'oggetto è distrutto non è più necessario sparare
        obj = param[ 0 ]       
        energy_actuator = self._state.updateEnergy( self._power, self._delta_t )
        # verifica se param[1] destinazione del proiettile, range attuatore e posizione dell'automa sono idonei per l'esecuzione della attuaione
        if not self.isInRange( obj.getPosition() ):
            logger.logger.debug("Actuator: {0} not executed projectile launch action because object not in range. automa: {1}, object position: {2}, range: {3}, energy_actuator: {4}".format( self._id, automa.getId(), obj.getPosition(), self._range, energy_actuator ) )
            return [ False, energy_actuator, firing_terminated ]
       
        if obj.getHealth() != obj.evalutateDamage( self._power ):
            obj_resilience = obj.getResilience()            
            obj_health = obj._state.getHealth()
            obj_active = obj._state.isActive()
            obj_critical = obj._state.isCritical()
            obj_anomaly = obj._state.isAnomaly()
            obj_destroyed = obj._state.isDestroyed()
            obj_remove = obj._state.isRemoved()
            logger.logger.debug("Actuator: {0} executed projectile launch action with object damage. automa: {1}, object position: {2}, range: {3}, energy_actuator: {4}, object_resilience: {5}, object_health: {6}, object_active: {7}, object_critical: {8}, object_anomaly: {9}, object_destroyed: {10}, object_removed: {11}".format( self._id, automa.getId(), obj.getPosition(), self._range, energy_actuator, obj_resilience, obj_health, obj_active, obj_critical, obj_anomaly, obj_destroyed, obj_remove ) )

            if obj_destroyed:
                firing_terminated = True

                if posManager.removeObject( obj ):                                
                    logger.logger.debug("Actuator: {0} executed projectile launch action with object destruction and removal from position manager. automa: {1}, object_destroyed: {2}".format( self._id, automa.getId(), obj.getId() ) )
                    return [ True, energy_actuator, firing_terminated ]
        
                else:                
                    raise Exception("shooting executed but object wasn't removed from position manager")
                            
            logger.logger.debug("Actuator: {0} executed projectile launch action but object wasn't destroyed. automa: {1}, object destroyed: {2}".format( self._id, automa.getId(), obj.getId() ) )
            return [ True, energy_actuator, firing_terminated ]

        logger.logger.debug("Actuator: {0} Not executed projectile launch action Automa power < object resilience. automa: {1}, object destroyed: {2}".format( self._id, automa.getId(), obj.getId() ) )
        return [ False, energy_actuator, firing_terminated ]


    

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


    def isInRange(self, destination):
        """Return True if abs( destination - position) <= range"""
        return ( abs( destination[ 0 ] - self._position[ 0 ] ) <= self._range[ 0 ] ) and ( abs( destination[ 1 ] - self._position[ 1 ] ) <= self._range[ 1 ] ) and ( abs( destination[ 2 ] - self._position[ 2 ] ) <= self._range[ 2 ] ) 


    def setEvent( self, automa,  result, obj, typ, duration = 1, time2go = 0):
        """Set event in Object's Event Queue if object is an istance of Automa"""

        if automa.checkClass( obj ):
            #(self, typ, volume,  time2go = 1, duration = 1, energy = None, power = None, mass = None  
            event = Event( typ = typ, volume = obj.getVolume(), duration = duration, time2go = time2go ) # duration = 0 -> effetti evento già applicati su object
            obj.insertEvent( event ) 
            logger.logger.debug("Actuator: {0} result action = {1}. Inserted assimilate event in object's event queue: event._id: {2}, event._typ: {3}, event._volume: {4}, event._time2go: {5}, event._duration: {6}, event._energy: {7}, event._power: {8}, event._mass: {9}".format( self._id, result, event._id, event._type, event._volume, event._time2go, event._duration, event._energy, event._power, event._mass ))        

        return True
