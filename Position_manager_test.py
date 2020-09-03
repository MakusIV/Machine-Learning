from Position_manager import Position_manager
from Coordinate import Coordinate
from Object import Object

def TestClassPosition_manager():

    pm = Position_manager()

    result = True

    if 'Fuffy' != pm.getName():
        print("Position_manager.getName() Failed!", pm.getName())
        result = False

    if [ [-50, -50, -50], [50, 50, 50] ] != pm.getLimits():
        print("Position_manager.getLimits() Failed!", pm.getLimits())
        result = False
    

    pm = Position_manager('Tullius', [ [-1000, -500, -350], [1250, 750, 150] ])

    if 'Tullius' != pm.getName():
        print("Position_manager.getName() Failed!", pm.getName())
        result = False

    if [ [-1000, -500, -350], [1250, 750, 150] ] != pm.getLimits():
        print("Position_manager.getLimits() Failed!", pm.getLimits())
        result = False
    
    pm.setLimits([ [-50, -50, -50], [50, 50, 50] ])
   
    if [ [-50, -50, -50], [50, 50, 50] ] != pm.getLimits():
        print("Position_manager.setLimits() Failed!", pm.getLimits())
        result = False
    
    
    coord = (10, 10, 10)
    obj = Object('Citrullus')

    if True != pm.insertObject( coord, obj ):
        result = False
        print("Position_manager.insertObject( coord, obj ) Failed! Object not inserted", coord)

    
    if True == pm.insertObject( coord, obj ):
        result = False
        print("Position_manager.insertObject( coord, obj ) Failed! Object inserted over existens object position ", coord)


    if True == pm.insertObject( None, obj ):
        result = False
        print("Position_manager.insertObject( coord, obj ) Failed! None coord not detected", coord)

    if True == pm.insertObject( coord, None ):
        result = False
        print("Position_manager.insertObject( coord, obj ) Failed! None obj nt detected", coord)


    pm.setLimits([ [-5, -5, -5], [5, 5, 5] ])
    
    if True == pm.insertObject( coord, obj ):
        result = False
        print("Position_manager.insertObject( coord, obj ) Failed! Limits coord not detected", coord.to_string(), pm.getLimits(), pm.pos[coord].getName())

    obj = Object('Citrullus')
    coord = (2, 2, 2)
    pm.insertObject( coord, obj )

    if coord != pm.searchObject( obj ):
        result = False
        print("Position_manager.searchObject( obj ) Failed! Object not found")

    obj = Object('_test')
    coord = (1, 1, 1)

    if coord == pm.searchObject( obj ):
        result = False
        print("Position_manager.searchObject( obj ) Failed! Not inserted object found")

    pm.insertObject( coord, obj )    

    if coord != pm.removeObject( obj ):
        result = False
        print("Position_manager.removeObject( obj ) Failed! Object not removed")

    if pm.removeObject( obj ):
        result = False
        print("Position_manager.removeObject( obj ) Failed! Unexistent object removed")

    pm.insertObject( coord, obj )

    if obj != pm.removeObjectAtCoord( coord ):
        result = False
        print("Position_manager.removeObjectAtCoord( obj ) Failed! Object not removed")

    if pm.removeObjectAtCoord( coord ):
        result = False
        print("Position_manager.removeObjectAtCoord( obj ) Failed! Unexistent object removed")
    

    old_obj = Object('Old')
    new_obj = Object('New')
    coord = (4, 4, 4)
    coord1 = coord
    pm.insertObject( coord, old_obj )


    if old_obj != pm.changeObject(coord, new_obj):
        result = False
        print("Position_manager.changeObject(coord, new_obj) Failed!")


    if new_obj != pm.changeObject(coord, old_obj):
        result = False
        print("Position_manager.changeObject(coord, new_obj) Failed!")
    
    coord = (3, 3, 3)

    if new_obj == pm.changeObject(coord, old_obj):    
        result = False
        print("Position_manager.changeObject(coord, new_obj) Failed! Changed object at unexistens position")


    if old_obj != pm.getObject( old_obj ):
        result = False
        print("Position_manager.pm.getObject( obj ) Failed!")
    
    if old_obj != pm.getObjectAtCoord( coord1 ):
        result = False
        print("Position_manager.pm.getObjectAtCoord( coord ) Failed!")


    limits = [ [-50, -50, -50], [50, 50, 50] ]

    if not pm.normalizeVolume(limits) and limits != pm.getLimits():
        result = False
        print("Position_manager.pm.normalizeVolume(limits) Failed!", limits, pm.getLimits(), detected.count())


    detected = pm.getObjectInVolume( [ [-50, -50, -50], [50, 50, 50] ] )

    if not detected or len( detected )!= 2:
        result = False
        print("Position_manager.pm.getObjectInVolume( limits ) Failed!", pm.getLimits(), len( detected ) )


    pm.setLimits( [ [-50, -50, -50], [50, 50, 50] ] )

    detected = pm.getObjectInVolume( pm.getLimits() )

    if not detected or len( detected )!= 3:
        result = False
        print("Position_manager.pm.getObjectInVolume( limits ) Failed!", pm.getLimits(), len( detected ) )

    pm.show()

    return result

print("test result:", TestClassPosition_manager())