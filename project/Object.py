import random
from Coordinate import Coordinate
import General
from State import State
from LoggerClass import Logger
from Event import Event

# LOGGING --
 
logger = Logger(module_name = __name__, class_name = 'Object')

class Object:
    

    def __init__(self, dimension = (1, 1, 1), mass = 0,  resilience = 100, emissivity = {"radio": 0, "thermal": 0, "optical": 0, "nuclear": 0, "electric": 0, "acoustics": 0, "chemist": 0}, coord = None, name = None, state = None ):

            self._name = name
            self._id = None
            self._dimension = dimension
            self._mass = mass
            self._resilience = resilience # resistenza ad uno SHOT in termini di power (se shot power > resilence --> danno all'oggetto)            
            self._coord = coord
            self._state = state
            self.setState(state)
            self._emissivity = emissivity
            self._caught_from = None #l'id dell'oggetto che ha preso (catturato) questo oggetto
            self._eventsQueue = {} #  {key: event id, value = event}
            
            if not self.checkParam( dimension, mass, resilience, state, coord ):
                raise Exception("Invalid parameters! Object not istantiate.")


            if emissivity and self.checkEmissivityParam( emissivity ):
                self._emissivity = emissivity
            else:
                raise Exception("Invalid emissivity! Object not istantiate.")

            

            if not name:
                self._name = General.setName('Object_Name')
                self._id = General.setId('Object_ID', None)
            else:
                self._name = name
                self._id = General.setId(name + '_ID', None)
                
            if not coord:
                self._coord = Coordinate(0, 0, 0)


    def runTask( self, posManager ):
        
        self.update() #check the eventsQueue and update state
        logger.logger.info( "Object: {0} running task: update".format( self._name ))
        return True


    def update(self, posManager ):
        """Update state for check of eventsQueue"""        

        events = self.getEventActive()
        # l'evento riguarda una posizione indipendentemente dall'eventuale target impostato, quindi in base 
        # alle caratteristiche dell'evento che bisogna valutare quali elementi sono coinvolti e come sono
        # coinvolti
        
        for _, ev in events: # scorre gli eventi da eseguire della lista eventi attivi
            logger.logger.debug("Object: {0} active event {1}".format( self._name, ev._type ))

            if ev._duration <= 0: # effetti dell'evento applicati durante la action dell'oggetto che ha generato l'evento
                    logger.logger.debug("Object: {0} event._duration <= 0, maybe damage already evalutated in action execution".format( self._name ) )
                

            if ev.isHit(): # solo per l'evento SHOT viene valutato l'eventuale danno
                # NOTA: tu lo fai risolvere direttamente nell'azione (valuta il danno e se l'obj è distrutto lo rimuove), qui invece è previsto
                # che l'azione registra un evento nella lista eventi dell'automa (ma se non è un automa quindi non ha event queue anzi ogni oggetto in questo caaso dovrebbe avere una queue event e un methodo di update) e successivamente gli effetti dell'evento vengono valutati
                # posso lasciare che alcune azioni vengano immediatamente valutati gli effetti e effettuati gli aggiornamenti mentre per altre vengano create eventi da gestire tramite coda queue
                self.evalutateHit( ev._power, random_hit = True, posManager = posManager )
                # è necessario implementare l'utilizzo dei metodi in Position_manager per la gestione dell'eventuale eliminazione dell'oggetto


            if ev.isPop(): # viene valutato se l'automa può essere "spinto" (spostato). Valutare la nuova posizione dell'automa
                self.evalutatePop( ev._power, ev._mass, posManager )
                # è necessario implementare l'utilizzo dei metodi in Position_manager per la gestione dell'eventuale spostamento dell'oggetto

            if ev.isPush(): # viene valutato se l'automa può essere "spinto" (spostato). Valutare la nuova posizione dell'automa
                self.evalutatePush( ev._power, ev._mass, posManager )
                # è necessario implementare l'utilizzo dei metodi in Position_manager per la gestione dell'eventuale spostamento dell'oggetto

            if ev.isAssimilate(): # viene valutato se l'automa può essere mangiato. Eliminare l'automa aggiornando lo stato
                self.evalutateEat( ev._power, ev._mass, posManager )
                # è necessario implementare l'utilizzo dei metodi in Position_manager per la gestione dell'eventuale eliminazione dell'oggetto

        logger.logger.debug("Object: {0} executed update internal state".format( self._name ))
        return True

    
    

    def evalutateHit( self, power, posManager, random_hit = True ):
        """" evalutate event hit effect """
        
        if random_hit:
            energy_hit_power = int( power * random.uniform(0, 1) )
            
        else:
            energy_hit_power = power
            
        logger.logger.debug("Object: {0} - energy_hit_power: {1}".format( self._id, energy_hit_power ))
                
        health = self.evalutateDamage( energy_hit_power )
        resilience = self._resilience                    
        active = self._state.isActive()
        critical = self._state.isCritical()
        anomaly = self._state.isAnomaly()

        if health == 0: # valutazione del danno per l'automa. Se restituisce 0 l'automa è dsitrutto
            self._state.destroy()
            logger.logger.debug("Object: {0} object's health = 0, object destroyed".format( self._id ))
        
            
            destroyed = self._state.isDestroyed()                                                
            remove = self._state.isRemoved()
            logger.logger.debug("Object: {0} Evalutate Hit damage with power: {1}. resilience: {2}, health: {3}, active: {4}, critical: {5}, anomaly: {6}, destroyed: {7}, removed: {8}".format( self._id, power, resilience, health, active, critical, anomaly, destroyed, remove ) )
        
            if destroyed:
        
                if posManager.removeObject( self ):                                
                    logger.logger.debug("Object: {0} object removed from position manager".format( self._id ) )
                    # valutare se è opportuno inviare un evento da inviare ... a chi? (l'eventuale esecutore del HIT non è conosciuto da object)
                    return True
        
                else:                
                    raise Exception("Object: {0} was destructed but not removed from position manager".format( self._id ) )
                            
        logger.logger.debug("Object: {0} object was hit but not destructed. Health = {0}, resilience: {1}, active: {2}, critical: {3}, anomaly: {4}".format( self._id, health, resilience, active, critical, anomaly ) )            
        return True

    


    def evalutatePop( self, power, mass, posManager ):
        
        ratio = self._power * self._mass / ( mass * power )
        logger.logger.debug("Automa: {0} Evalutate POP with power: {1}. ratio: {2}".format( self._id, power, ratio ) )

        if ratio <= 1:
            logger.logger.debug("Automa: {0} Confirmed POP effect: {1}. ratio: {2}".format( self._id, power, ratio ) )
            return True
        
        logger.logger.debug("Automa: {0} Ininfluence POP effect: {1}. ratio: {2}".format( self._id, power, ratio ) )
        return False


    def insertEvent(self, event):
        """insert event in eventsQueue"""
        if not event or not isinstance( event, Event ):
            return False

        self._eventsQueue[ event._id ] = event
        logger.logger.debug("Object: {0} inserted new event in queue, event id: {1}, events in queue: {2}".format( self._name, event._id, len( self._eventsQueue ) ))
        return True

    def removeEvent(self, event):
        """remove event in eventsQueue"""
        if not isinstance(event._id, int) :
            return False

        self._eventsQueue.pop( event._id )        
        logger.logger.debug("Object: {0} removed event in queue, event id: {1}, events in queue: {2}".format( self._name, event._id, len( self._eventsQueue ) ))
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


    #TEST: OK (indiretto)
    def setCaught_from( self, automa_id ):

        if not automa_id or not isinstance(automa_id, str):
            return False
        
        self._caught_from = automa_id
        return True

    #TEST: OK (indiretto)
    def getCaught_from( self ):

        return self._caught_from
        
    #TEST: OK (indiretto)
    def checkEmissivityParam( self, emissivity ):
        """Return True if conformity of the emissivity is verified"""
        if not emissivity or not isinstance(emissivity, dict) or len(emissivity) != len( General.SENSOR_TYPE ):
            return False

        # Verificare se possibile utilizzare la comphrension:
        #res = any( [True for typ in self._emissivity.keys if typ == ele for ele in General.SENSOR_TYPE] )
        
        return all( [  [ True for typ in emissivity if typ == ele ]  for ele in General.SENSOR_TYPE ] )
    
    #TEST: OK (indiretto)
    def getEmissivityForType( self, emissivity_type ):
        """Return emissivity level for that emissivity_type. If emissivity_type not presents in General.SENSOR_TYPE return False"""
        try:
            return self._emissivity.get( emissivity_type )

        except ValueError:
            return False
    #TEST: OK (indiretto)
    def getResilience( self ):
        return self._resilience

    #TEST: OK (indiretto)
    def getEmissivity(self):
        return self._emissivity

    def setEmissivity(self, emissivity):

        if emissivity == 'default':
            emissivity = dict()
            for val in General.SENSOR_TYPE:
                emissivity[val] = 0
        else:
            self._emissivity = emissivity
        
        return emissivity

    #TEST: OK (indiretto)
    def evalutateDamage(self, power):
        """Evalutate the damage on sensor and update state"""
        # questo metodo dovrebbe essere rivisto per una valutazione più corretta della diminuzione della health e della resilence
        # utilizzando in prospettiva l'eventuale influennza dell'energia coinvolta
        if power > self._resilience:
            damage = power - self._resilience# in realtà il danno dovrebbe essere proporzionale all'energia: No alla potenza e' ok in quanto è il danno istantaneo (per task)
            self._resilience = self._resilience - damage #da rivedere
            return self._state.decrementHealth( damage )
        
        return self._state.getHealth()



    def getVertex(self):

        llr = self._coord.getPosition()
        
        if len(self._dimension) == 3:
            dim_x = self._dimension[0]
            dim_y = self._dimension[1]
            dim_z = self._dimension[2]
        
        elif len(self._dimension) == 1:
            dim_x, dim_y, dim_z = self._dimension[0], self._dimension[0], self._dimension[0]
        
        else:
            raise ValueError("sel._dimension as length != 1 or 3")

        vertex = {  'llr': llr, 
                    'lhr': [llr[0], llr[1], llr[2] + dim_z], 
                    'rhr': [llr[0] + dim_x, llr[1], llr[2] + dim_z],
                    'rlr': [llr[0] + dim_x, llr[1], llr[2] ],
                    'llf': [llr[0], llr[1] + dim_y, llr[2]],
                    'lhf': [llr[0], llr[1] + dim_y, llr[2] + dim_z],
                    'rhf': [llr[0] + dim_x, llr[1] + dim_y, llr[2] + dim_z],
                    'rlf': [llr[0] + dim_x, llr[1] + dim_y, llr[2]]  }
        return vertex

    #TEST: OK (indiretto)    
    def setState(self, state):

        if not state or not isinstance(state, State):
            self._state = State( run = True )
        else:
            self._state = state

        return True

    #TEST: OK (indiretto)
    def getState(self):
        return self._state


    def setId(self, id):

        if not id:
            return False

        elif isinstance(id, str):
            self._id = id       
        
        else:
            self._id = str( id )       
            
        return True


    def setName(self, name):

        if not name:
            return False
        else:
            self._name = name

        return True
            

    
    def setDimension(self, dimension):

        if not dimension or not isinstance(dimension, tuple) and not len(dimension) == 3 or not isinstance( dimension[0], int) or not  isinstance( dimension[1], int) or not  isinstance( dimension[2], int):
            return False
        else:
            self._dimension = dimension

     
        #if not General.checkDimension(dimension): # not dimension or not isinstance(dimension, list) and not len(dimension) == 3 or not isinstance( dimension[0], int) or not  isinstance( dimension[1], int) or not  isinstance( dimension[2], int) :
         #   return False
        #else:
         #   self._dimension = dimension

        return True


    #TEST: OK (indiretto)
    def setCoord(self, coord):
            
        if not coord or not isinstance(coord, Coordinate):
            return False
        else:
            self._coord = coord

        return True


    #TEST: OK (indiretto)
    def isCollision(self, volume):
        """Return True if object's volume collide with volume"""
        # xd = dimension[0], yd = dimension[1], zd =dimension[2]
        # xvol_low = volume[0][0], yvol_low = volume[0][1], zvol_low = volume[0][2]
        # xvol_high = volume[1][0], yvol_high = volume[1][1], zvol_high = volume[1][2]
        # not intersection in x axes: x > xvol_high and x + xd < xvol_low
        # not intersection in y axes: y > yvol_high and y + yd < yvol_low
        # not intersection in z axes: z > zvol_high and z + zd < zvol_low
        # not interection -> one or more axis not intersection

        ## NOTA: volume = [ [xl, yl, zl],  [xh, yh, zh] ] dove xl, yl, zl <= xh, yh, zh

        if not General.checkVolume(volume): #not volume or not isinstance( volume, list ):
            raise Exception('Invalid parameters')

        pos = self._coord.getPosition()

        x_not_intersection =  pos[0] > volume[1][0] or pos[0] + self._dimension[0] < volume[0][0] 
        y_not_intersection =  pos[1] > volume[1][1] or pos[1] + self._dimension[1] < volume[0][1] 
        z_not_intersection =  pos[2] > volume[1][2] or pos[2] + self._dimension[2] < volume[0][2] 

        # not interection -> one or more axis not intersection
        if x_not_intersection or y_not_intersection or z_not_intersection:
            return False

        return True


    #TEST: OK (indiretto)
    def getDistance(self, coord):
        """Return distance (d, xd, yd, zd) from object.coordinate to pos:[x, y, z]""" 

        if not coord or not isinstance(coord, Coordinate):
            return False       

        return self._coord.distance(coord)
        

    #TEST: OK (indiretto)
    def getHealth( self ):
        return self._state.getHealth()

    #TEST: OK (indiretto)
    def getId(self):
        return self._id


    def getName(self):
        return self._name

    #TEST: OK (indiretto)
    def getMass( self ):
        return self._mass

    #TEST: OK (indiretto)
    def setMass( self, mass):
        
        if not mass or not isinstance(mass, int) or mass < 0:
            return False
        self._mass = mass
        return True
    
    #TEST: OK (indiretto)
    def getPosition(self):
        return self._coord.getPosition()

    #TEST: OK (indiretto)
    def setPosition(self, position):
        self._coord.setPosition( position )

    #TEST: OK (indiretto)
    def getDimension(self):
        return self._dimension

    def to_string(self):
        return 'Name: {0}  -  Id: {1}'.format(self.getName(), str(self._id))

    
    def checkObjectClass(self, object):
        """Return True if objects is a Object object otherwise False"""
        if not object or not isinstance(object, Object):
            return False
        
        return True

    def checkObjectList(self, objects):
        """Return True if objectsobject is a list of Object object otherwise False"""

        if objects and isinstance(objects, list) and all( isinstance(object, Object) for object in objects ):
            return True

        return False


     # vedi il libro
    def checkParam(self, dimension, mass, resilience, state, coord ):
        """Return True if conformity of the parameters is verified"""   
    
        if state != None and not isinstance( state, State ) or coord != None and not isinstance( coord, Coordinate ) or resilience != None and ( not isinstance( resilience, int )  or not( resilience <= 100 and resilience >= 0 ) ) or not( mass >= 0 ) or not General.checkDimension( dimension ):
            return False
                
        return True


    def getVolumePosition( self ):
        """Return the position of the object's volume"""
        
        position = self.getPosition()
        dimension = self.getDimension()
        volume_position = dict()

        for z in range( position[ 2 ], position[ 2 ] + dimension[ 2 ] ):           
           for y in range( position[ 1 ], position[ 1 ] + dimension[ 1 ] ):              
              for x in range( position[ 0 ], position[ 0 ] + dimension[ 0 ] ):
                  volume_position[ ( x, y, z ) ] = True

        return volume_position


    def getVolume( self, position = None, dimension = None ):
        """Return [ [ position ], [ position + dimensione ] ] """
        
        if position == None:
            position = self.getPosition() 
        
        if dimension == None:
            dimension = self.getDimension()

        return [ position, [ position[ 0 ] + dimension[ 0 ], position[ 1 ] + dimension[ 1 ], position[ 2 ] + dimension[ 2 ] ] ] 