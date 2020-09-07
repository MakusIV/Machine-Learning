
# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/home/marco/Documenti/Machine Learning/Automata/project')

from Object import Object 
from Coordinate import Coordinate



def testClassObject():

    result = True

    coord = Coordinate (3, 4, 7)

    obj = Object( coord, 'Tullio', 1234, [10, 8, 6]  )

    if obj.name!='Tullio' or obj.id != 1234 or obj.dimension != [10, 8, 6] or obj.coord != coord:
        print('Object.__Initit__ Failed!! ', obj.name, obj.id, obj.dimension, obj.coord)
        result = False 

    obj = Object()

    if not obj.name or not obj.id or not obj.dimension or not obj.coord or not isinstance(obj.name,str) or not isinstance(obj.id,int) or not isinstance(obj.dimension,list) or not isinstance(obj.coord,Coordinate):
        print('Object.__Initit__ Failed!! ', obj.name, obj.id, obj.dimension, obj.coord)
        result = False 


    obj = Object( Coordinate(2,2,2), 'Gregory', 1234, [5,5,5] ) 

    if obj.name != 'Gregory' or obj.id != 1234 or obj.dimension != [5,5,5] or obj.getPosition() != [2,2,2]:
        print('Object.__Initit__ Failed!! ', obj.name, obj.id, obj.dimension, obj.getPosition())    
        result = False 

    obj.setName('Ollio')

    if obj.name != 'Ollio':
        print('Object.setName() Failed!! ', obj.name)
        result = False 


    if not obj.setName(12):
        print('Object.setName() Failed!! ', obj.name)
        result = False 

    obj.setId(999)

    if obj.id != 999:
        print('Object.setId() Failed!! ', obj.id)
        result = False 

    obj.setDimension([1,1,1])

    if obj.getDimension() != [1,1,1]:
        print('Object.setDimension() Failed!! ', obj.dimension)
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

print("test result:", testClassObject())

