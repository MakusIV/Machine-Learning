# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'project')

from State import State
from Sensor import Sensor
from Sensibility import Sensibility


def testClassSensor():

    result = True    
    sensor = Sensor( range_max = 10 )


    if not sensor._sensibility or not isinstance(sensor._sensibility, Sensibility) or sensor._power != 100 or sensor._resilience != 100 or not sensor._name or not sensor._state:
        print('Sensor Failed!! ', sensor._sensibility, sensor._power, sensor._resilience)
        result = False 
    
    sensor = Sensor(range_max = 100, accuracy=20, power=20, resilience=20, name='tullio', state = State())

    if sensor._sensibility != 20 or sensor._power != 20 or sensor._resilience != 20 or sensor._name != 'tullio' or not sensor._state:
        print('Sensor Failed!! ', sensor._sensibility, sensor._power, sensor._resilience, sensor._name, sensor._state)
        result = False 
    


    try:
        sensor = Sensor(sensibility=-1, power=-1, resilience=-1)
        
    except Exception:
        pass

    else:
        print( 'Sensor Failed!!  Not launch Exception', sensor._sensibility, sensor._power, sensor._resilience, sensor._name, sensor._state )
        result = False


    try:
        sensor = Sensor(sensibility=10, power=1, resilience=101)
        
    except Exception:
        pass

    else:
        print( 'Sensor Failed!!  Not launch Exception', sensor._sensibility, sensor._power, sensor._resilience, sensor._name, sensor._state )
        result = False


    
    # Sensor.evalutateDamage( energy, power )
    sensor = Sensor(range_max=50, power=50, resilience=50)
    sensor.evalutateDamage(energy = 100, power = 60)

    if sensor._state._health != 90:
        print('Sensor.evalutateDamage(energy = 100, power = 60) Failed!! ', sensor._sensibility, sensor._power, sensor._resilience, sensor._name, sensor._state, sensor._state._health)
        result = False 
    

    if not Sensor.checkSensorClass(sensor, sensor):
        print('Sensor.checkSensorClass(sensor) Failed!! ', sensor._state, sensor._state._health)
        result = False 
    
    sensors = [Sensor( range_max = 100 ), Sensor( range_max = 100  ), Sensor(range_max = 100 ), Sensor( range_max = 100 )]

    if not Sensor.checkSensorList(sensor, sensors):
        print('Sensor.checkSensorList(sensors) Failed!! ', sensors[0]._id, sensors[0]._state, sensors[0]._state._health)
        result = False

    sensors = [Sensor( range_max = 100 ), Sensor(range_max = 100 ), list(), Sensor(range_max = 100 )]

    if Sensor.checkSensorList(sensor, sensors):
        print('Sensor.checkSensorList(sensors) Failed!! ', sensors[0]._id, sensors[0]._state, sensors[0]._state._health)
        result = False  
    

    return result

print("Sensor class test result:", testClassSensor())