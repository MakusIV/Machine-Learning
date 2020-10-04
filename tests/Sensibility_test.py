

# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'project')
from Sensibility import Sensibility
import General


def testClassSensibility():

    result = True

    #try:
    sensibility = Sensibility(max_range = (1000, 900, 800) )
    
    #except Exception:
     #   print( 'Sensibility Failed!!  Launch Exception', sensibility.toString() )
      #  result = False 

    if sensibility._max_range != (1000, 900, 800) or sensibility._type_space != 'TETRAHEDRIC':
        print('Sensibility Failed!! ', sensibility._max_range != 1000 or sensibility._type_space != 'TETRAHEDRIC')
        result = False 
    

    scanning_volume = sensibility.get_probability_of_perception(start_percept_position = (0, 0, 0) )

    if not scanning_volume or not isinstance( scanning_volume, list) or not isinstance(scanning_volume[0], list) or not General.checkVolume(scanning_volume[0][0]) or not isinstance(scanning_volume[0][1], float):
        print('Sensibility.get_probability_of_perception(self, start_percept_position)  - max_range = (1000, 900, 800) -  start_percept_position = (-700, -900, -1300)  -   Failed!! ', sensibility._max_range, sensibility._type_space)
        result = False 
    
    scanning_volume = sensibility.get_probability_of_perception(start_percept_position = (101, 234, 200) )

    if not scanning_volume or not isinstance( scanning_volume, list) or not isinstance(scanning_volume[0], list) or not General.checkVolume(scanning_volume[0][0]) or not isinstance(scanning_volume[0][1], float):
        print('Sensibility.get_probability_of_perception(self, start_percept_position) - max_range = (1000, 900, 800) -  start_percept_position = (101, 234, 200)  -    Failed!! ', sensibility._max_range, sensibility._type_space)
        result = False 

    scanning_volume = sensibility.get_probability_of_perception(start_percept_position = (-700, -900, -1300) )

    if not scanning_volume or not isinstance( scanning_volume, list) or not isinstance(scanning_volume[0], list) or not General.checkVolume(scanning_volume[0][0]) or not isinstance(scanning_volume[0][1], float):
        print('Sensibility.get_probability_of_perception(self, start_percept_position) - max_range = (1000, 900, 800) -  start_percept_position = (-700, -900, -1300)  -   Failed!! ', sensibility._max_range, sensibility._type_space)
        result = False 
    
    sensibility = Sensibility( max_range = (-1000, -900, -800) )

    scanning_volume = sensibility.get_probability_of_perception( start_percept_position = (0, 0, 0) )

    if not scanning_volume or not isinstance( scanning_volume, list) or not isinstance(scanning_volume[0], list) or not General.checkVolume(scanning_volume[0][0]) or not isinstance(scanning_volume[0][1], float):
        print('Sensibility.get_probability_of_perception(self, start_percept_position) - max_range = (-1000, -900, -800) -  start_percept_position = (0, 0, 0)  -  Failed!! ', sensibility._max_range, sensibility._type_space)
        result = False 
    
    scanning_volume = sensibility.get_probability_of_perception(start_percept_position = (101, 234, 200) )

    if not scanning_volume or not isinstance( scanning_volume, list) or not isinstance(scanning_volume[0], list) or not General.checkVolume(scanning_volume[0][0]) or not isinstance(scanning_volume[0][1], float):
        print('Sensibility.get_probability_of_perception(self, start_percept_position) - max_range = (1000, 900, 800) -  start_percept_position = (101, 234, 200)  -    Failed!! ', sensibility._max_range, sensibility._type_space)
        result = False 

    scanning_volume = sensibility.get_probability_of_perception(start_percept_position = (-700, -900, -1300) )

    if not scanning_volume or not isinstance( scanning_volume, list) or not isinstance(scanning_volume[0], list) or not General.checkVolume(scanning_volume[0][0]) or not isinstance(scanning_volume[0][1], float):
        print('Sensibility.get_probability_of_perception(self, start_percept_position) - max_range = (1000, 900, 800) -  start_percept_position = (-700, -900, -1300)  -   Failed!! ', sensibility._max_range, sensibility._type_space)
        result = False 

    return result

print("Sensor class test result:", testClassSensibility())