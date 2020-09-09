

import Position_manager_test as pmt
import Object_test as obj
import Coordinate_test as coord
import State_test as st

test = []

test.append(pmt.TestClassPosition_manager() )
test.append( obj.testClassObject()  )
test.append( coord.testClassCoordinate() )
test.append( st.testClassState() )

result = True

for t in test:
    if not t:
        result = False

print("All test result: ", result)