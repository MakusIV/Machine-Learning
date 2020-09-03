
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

 

print("Object_test: ", result)