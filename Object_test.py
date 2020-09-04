
from Object import Object 
from Coordinate import Coordinate



result = True

coord = Coordinate (3, 4, 7)

obj = Object( 'Tullio', 1234, [10, 8, 6], coord  )

if obj.name!='Tullio' or obj.id != 1234 or obj.dimension != [10, 8, 6] or obj.coord != coord:
    print('Object.__Initit__ Failed!! ', obj.name, obj.id, obj.dimension, obj.coord)
    result = False 

obj = Object()

if not obj.name or not obj.id or not obj.dimension or not obj.coord or not isinstance(obj.name,str) or not isinstance(obj.id,int) or not isinstance(obj.dimension,list) or not isinstance(obj.coord,Coordinate):
    print('Object.__Initit__ Failed!! ', obj.name, obj.id, obj.dimension, obj.coord)
    result = False 


obj = Object( 'Gregory', 1234, [5,5,5], Coordinate(2,2,2) ) 

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

if obj.setDimension != [1,1,1]:
    print('Object.setDimension() Failed!! ', obj.dimension)
    result = False 

obj.setCoord = Coordinate(2,2,2)

if obj.getPosition != [2, 2, 2]:
    print('Object.setCoord() Failed!! ', obj.getPosition())
    result = False 


print("Object_test: ", result)