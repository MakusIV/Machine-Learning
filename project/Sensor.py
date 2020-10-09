
from Coordinate import Coordinate
import General
from State import State
from LoggerClass import Logger
import random
from Sensibility import Sensibility

# LOGGING --
 
logger = Logger(module_name = __name__, class_name = 'Sensor')

class Sensor:
    # Il sensore non è una specializzazione di Object

    # Unit test: ok
    def __init__(self, position, range_max, power = 100, resilience = 100, delta_t = 0.01, accuracy = 5, name = None, state = None  ):

        if not self.checkParam( range_max, accuracy,  power, resilience, delta_t ):
            raise Exception("Invalid parameters! Sensor not istantiate.")

        self._name = name
        self._id = General.setId('Sensor_ID', None) # Id generator automaticamente 
        self._state = state
        self._position = position
        self._power = power# nota l'energia è gestita nello stato in quanto è variabile
        self._range = range_max# è rappresentato da una tupla di distanze (x_d:int, y_d:int, z_d:int)
        self._sensibility = Sensibility( range_max, accuracy = accuracy )
        self._resilience = resilience # resistenza ad uno SHOT in termini di power (se shot power > resilence --> danno al sensore)
        self._delta_t = delta_t # Il tempo necessario per eseguire la detection serve per calcolare il consumo energetico. Puotrà essere utilizzato per gestire eventuali detection che necessitano di più cicli

        if not name or not isinstance(name, str):
            self._name = General.setName('Sensor_Name')
        else:
            self._name = name

        if not state or not isinstance(state, State):
            self._state = State()
        else:
            self.state = state


    def checkParam(self, range_max, accuracy,  power, resilience, delta_t):
        
        if not( range_max and range_max[0] >0 and range_max[1] >0 and range_max[2] >0 and delta_t and delta_t <= 1 and delta_t >= 0 and power and power <= 100 and power >= 0 and  resilience and  resilience <= 100 and resilience >= 0):
            return False
        
        if accuracy and accuracy <=0:
            return False

        return True

    # Unit test: 0k
    def evalutateSelfDamage(self, energy, power):
        """Evalutate the damage on sensor and update state"""
        if power > self._resilience:
            damage = power - self._resilience# in realtà il danno dovrebbe essere proporzionale all'energia
            return self._state.decrementHealth( damage )
        
        return self._state.getHealth()


    def setId(self, id = None):

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

    def perception(self, posMng, request_perception = None):
        # Attiva il sensore in base alle info contenute in request_perception, se request_perception è None utilizza i parametri di default
        # Restituisce le informazioni sulle azioni effettuate quali stato, posizione degli attuatori

        percept_info = None
        # la perception individua gli oggetti presenti nel volume di scansione in base alla probabilità nel
        # punto di scansione dove è presente l'oggetto. Per quanto riguarda la perceprion dell'enviroment tenere
        # presente che una zona a temperatura pericolosa è rappresentata da un oggetto di volume pari alla zona
        #interessata con proprietà temperaatura. Quindi durante la perception, individutato, l'oggetto
        # obj.isGas() ---> automa.MaxTemp >= obj._temperature
        
        scanning_volumes = self._sensibility.get_probability_of_perception( self._position ) # scanning_volume = (volume, probability)



        detected_objs = None

        for item in scanning_volumes:   

            scan_vol = item[0]
        
            _, low_vertex, high_vertex, _, _ = posMng.volumeInLimits( scan_vol )

            if not low_vertex:
                #vertici minimi volume fuori i limiti interrompe l'iterazione e l'esecuzione della scansione del volume di ricerca
                break

            if not high_vertex:
                #vertici massimi volume superiori ai limti scaltatura volume di ricerca 
                scan_vol = posMng.volumeNormalization(scan_vol)    
            
            logger.logger.debug("scanning volume {0} to detect object".format( scanning_volumes.index( item ) ))
            prob = random.randint( 1, 100 ) / 100
            volume_prob = item[ 1 ] * self._state.getEfficiency()
            logger.logger.debug( "prob:{0}, volume_prob:{1}".format( prob, volume_prob ) )

            if prob < volume_prob:
                detected_objs = posMng.getObjectInVolume( scan_vol )
                logger.logger.debug("detected {0} objects and inserted in detected object list".format( len(detected_objs)))

        energy_sensor = self._state.updateEnergy( self._power, self._delta_t )
        
        # l'energia è presente nello stato del sensore, tuttavia è l'automa che fornisce energia al sensore quindi ha senso 
        # restituire all'automa la info sul consumo energetico relativo alla perception
        # In questa prima versione decremento solo l'energia del sensore, quando questa diventa 0 l'automa deve provveedere
        # a ricaricare l'energia del sensore tramite la propria energia (con un fattore di  moltiplicazione: 1 energia automa = x energia sensore)

        #enviroment perception:  temp, emc, gas ecc

        percept_info = (energy_sensor, detected_objs)

        return percept_info




    # test: ok
    def checkSensorClass(self, sensor):
        """Return True if sensors is a Sensor object otherwise False"""
        if not sensor or not isinstance(sensor, Sensor):
            return False
        
        return True

    def checkSensorList(self, sensors):

        """Return True if sensors is a list of Sensor object otherwise False"""
        if sensors and isinstance(sensors, list) and all( isinstance(sensor, Sensor) for sensor in sensors ):
            return True

        return False

    def isOperative(self):
        """Return true if sensor state is running"""
        return self._state.isRunning()