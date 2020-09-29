
# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'project')

from Object import Object 
from Coordinate import Coordinate



def testClassObject():

    result = True

    coord = Coordinate (3, 4, 7)

    obj = Object( coord, 'Tullio', [10, 8, 6]  )

    if obj._name!='Tullio' or obj._dimension != [10, 8, 6] or obj._coord != coord:
        print('Object.__Initit__ Failed!! ', obj._name, obj._id, obj._dimension, obj._coord)
        result = False 

    obj = Object()

    if not obj._name or not obj._id or not obj._dimension or not obj._coord or not isinstance(obj._name,str) or not isinstance(obj._id,str) or not isinstance(obj._dimension,list) or not isinstance(obj._coord,Coordinate):
        print('Object.__Initit__ Failed!! ', obj._name, obj._id, obj._dimension, obj._coord)
        result = False 


    obj = Object( coord = Coordinate(2,2,2), name = 'Gregory', dimension = [5,5,5] ) 

    if obj._name != 'Gregory' or obj._dimension != [5,5,5] or obj.getPosition() != [2,2,2]:
        print('Object.__Initit__ Failed!! ', obj._name, obj._id, obj._dimension, obj.getPosition())    
        result = False 

    obj.setName('Ollio')

    if obj._name != 'Ollio':
        print('Object.setName() Failed!! ', obj._name)
        result = False 


    if not obj.setName(12):
        print('Object.setName() Failed!! ', obj._name)
        result = False 

    obj.setId(999)

    if obj._id != '999':
        print('Object.setId() Failed!! ', obj._id)
        result = False 

    obj.setDimension([1,1,1])

    if obj.getDimension() != [1,1,1]:
        print('Object.setDimension() Failed!! ', obj._dimension)
        result = False 

    obj.setCoord( Coordinate(2,2,2) )

    if obj.getPosition() != [2, 2, 2]:
        print('Object.setCoord() Failed!! ', obj.getPosition())
        result = False 

    if obj.getDistance( Coordinate(3,3,3) ) != 3**0.5:
        print('Object.getDistance() Failed!! ', obj.getDistance( Coordinate(5,5,5) ) )
        result = False 

    # isCollision(volume) test
    # NOTA: volume = [ [xl, yl, zl],  [xh, yh, zh] ] dove xl, yl, zl <= xh, yh, zh

    coord = Coordinate(0,0,0)
    dimension = [3,3,3]
    volume = [ [0, 0, 0 ], [5, 5, 5] ]

    obj.setCoord( coord )
    obj.setDimension( dimension )

    if not obj.isCollision( volume ):
        print('isCollision(volume) Failed!! ', obj.getPosition(), obj.getDimension(), volume)
        result = False 


    coord = Coordinate(0,0,0)
    dimension = [3,3,3]
    volume = [ [4,4,4], [15, 15, 15] ]

    obj.setCoord( coord )
    obj.setDimension( dimension )

    if obj.isCollision( volume ):
        print('isCollision(volume) Failed!! ', obj.getPosition(), obj.getDimension(), volume)
        result = False 


    coord = Coordinate(0,0,0)
    dimension = [3,3,3]
    volume = [ [3,3,3], [15, 15, 15] ]

    obj.setCoord( coord )
    obj.setDimension( dimension )

    if not obj.isCollision( volume ):
        print('isCollision(volume) Failed!! ', obj.getPosition(), obj.getDimension(), volume)
        result = False 


    coord = Coordinate(0,0,0)
    dimension = [3,3,3]
    volume = [ [-3,-3,-3], [0, 0, 0] ]

    obj.setCoord( coord )
    obj.setDimension( dimension )

    if not obj.isCollision( volume ):
        print('isCollision(volume) Failed!! ', obj.getPosition(), obj.getDimension(), volume)
        result = False 


    coord = Coordinate(0,0,0)
    dimension = [3,3,3]
    volume = [ [-3,-3,-3], [-1, -1, -1] ]

    obj.setCoord( coord )
    obj.setDimension( dimension )

    if obj.isCollision( volume ):
        print('isCollision(volume) Failed!! ', obj.getPosition(), obj.getDimension(), volume)
        result = False 


    coord = Coordinate(0,0,0)
    dimension = [3,3,3]
    volume = [ [-3, 0, 1], [-1, 2, 5] ]

    obj.setCoord( coord )
    obj.setDimension( dimension )

    if obj.isCollision( volume ):
        print('isCollision(volume) Failed!! ', obj.getPosition(), obj.getDimension(), volume)
        result = False 



    coord = Coordinate(0,0,0)
    dimension = [3,3,3]
    volume = [ [3, -1, 0], [3, -2, 5] ]

    obj.setCoord( coord )
    obj.setDimension( dimension )

    if obj.isCollision( volume ):
        print('isCollision(volume) Failed!! ', obj.getPosition(), obj.getDimension(), volume)
        result = False 


    coord = Coordinate(0,0,0)
    dimension = [3,3,3]
    # NOTA: volume = [ [xl, yl, zl],  [xh, yh, zh] ] dove xl, yl, zl <= xh, yh, zh
    volume = [ [3, -2, 0], [3, 0, 5] ]

    obj.setCoord( coord )
    obj.setDimension( dimension )

    if not obj.isCollision( volume ):
        print('isCollision(volume) Failed!! ', obj.getPosition(), obj.getDimension(), volume)
        result = False 


    return result

print("Object class test result:", testClassObject())

