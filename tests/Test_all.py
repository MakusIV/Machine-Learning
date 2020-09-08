

import Position_manager_test as pmt
import Object_test as obj
import Coordinate_test as coord

test = []

test.append(pmt.TestClassPosition_manager() )
test.append( obj.testClassObject()  )
test.append( coord.testClassCoordinate() )

result = True

for t in test:
    if not t:
        result = False

print("All test result: ", result)