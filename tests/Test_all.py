

import Position_manager_test as pmt
import Object_test as obj
import Coordinate_test as coord
import State_test as st
import Actuator_test as act
import Sensor_test as sen
import Sensibility_test as sensi
import Automa_test as au

test = []

test.append(pmt.TestClassPosition_manager() )
test.append( obj.testClassObject()  )
test.append( coord.testClassCoordinate() )
test.append( st.testClassState() )
test.append( sen.testClassSensor() )
test.append( act.testClassActuator() )
test.append( sensi.testClassSensibility() )
test.append( au.testClassAutoma() )

result = True

for t in test:
    if not t:
        result = False

print("All test result: ", result)