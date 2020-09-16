# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'project')

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
    
    
    pos = (10, 10, 10)
    obj = Object('Citrullus')

    if True != pm.insertObject( pos, obj ):
        result = False
        print("Position_manager.insertObject( coord, obj ) Failed! Object not inserted", pos)

    
    if True == pm.insertObject( pos, obj ):
        result = False
        print("Position_manager.insertObject( coord, obj ) Failed! Object inserted over existens object position ", pos)


    if True == pm.insertObject( None, obj ):
        result = False
        print("Position_manager.insertObject( coord, obj ) Failed! None coord not detected", pos)

    if True == pm.insertObject( pos, None ):
        result = False
        print("Position_manager.insertObject( coord, obj ) Failed! None obj nt detected", pos)


    pm.setLimits([ [-5, -5, -5], [5, 5, 5] ])
    
    if True == pm.insertObject( pos, obj ):
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
    pos = (4, 4, 4)
    pos1 = pos
    pm.insertObject( pos, old_obj )


    if old_obj != pm.changeObject(pos, new_obj):
        result = False
        print("Position_manager.changeObject(pos, new_obj) Failed!")


    if new_obj != pm.changeObject(pos, old_obj):
        result = False
        print("Position_manager.changeObject(pos, new_obj) Failed!")
    
    pos = (3, 3, 3)

    if new_obj == pm.changeObject(pos, old_obj):    
        result = False
        print("Position_manager.changeObject(pos, new_obj) Failed! Changed object at unexistens position")


    if old_obj != pm.getObject( old_obj ):
        result = False
        print("Position_manager.pm.getObject( obj ) Failed!")
    
    if old_obj != pm.getObjectAtCoord( pos1 ):
        result = False
        print("Position_manager.pm.getObjectAtCoord( pos ) Failed!")


    limits = [ [-50, -50, -50], [50, 50, 50] ]

    if not pm.normalizeVolume(limits) and limits != pm.getLimits():
        result = False
        print("Position_manager.pm.normalizeVolume(limits) Failed!", limits, pm.getLimits(), detected.count())


    detected = pm._getObjectInVolumeFromVolumeIteration( [ [-50, -50, -50], [50, 50, 50] ], [0, 0, 0] )

    if not detected or len( detected )!= 2:
        result = False
        print("Position_manager.pm._getObjectInVolumeFromVolumeIteration( volume ) Failed!", pm.getLimits() )


    
    pm.setLimits( [ [-50, -50, -50], [50, 50, 50] ] )

    detected = pm._getObjectInVolumeFromVolumeIteration( pm.getLimits(), [5, 5, 5] )

    if not detected or len( detected )!= 3:
        result = False
        print("Position_manager.pm._getObjectInVolumeFromVolumeIteration( volume ) Failed!", pm.getLimits() )

    

    detected = pm._getObjectInVolumeFromObjectList( [ [-50, -50, -50], [50, 50, 50] ] )

    if not detected or len( detected )!= 3:
        result = False
        print("Position_manager.pm._getObjectInVolumeFromObjectList( volume ) Failed!", detected )


    detected = pm._getObjectInVolumeFromObjectList( [ [0, 0, 0], [1, 1, 1] ] )

    if detected:
        result = False
        print("Position_manager.pm._getObjectInVolumeFromObjectList( volume ) Failed!", detected )
    


    detected = pm._getObjectInVolumeFromObjectList( [ [0, 0, 0], [4, 4, 4] ] )

    if not detected or len( detected )!= 2:
        result = False
        print("Position_manager.pm._getObjectInVolumeFromObjectList( volume ) Failed!", detected )


    
    for i in range(30):
        pm.insertObject( (20 + i, 20 + i, 20 + i), Object('New_'+str(i)) )
    

    detected = pm.getObjectInVolume( [ [0, 0, 0], [100, 100, 100] ] )

    if not detected or len( detected )!= 33:
        result = False
        print("Position_manager.pm.getObjectInVolume( volume ) Failed!", detected )


    detected = pm.getObjectInVolume( [ [2, 2, 2], [2, 2, 2] ] )

    if not detected or len( detected )!= 1:
        result = False
        print("Position_manager.pm.getObjectInVolume( volume ) Failed!", detected )


    pm.getObjectAtCoord( (10, 10, 10) ).setDimension( [ 5, 5, 5] )

    detected = pm._getObjectInVolumeFromObjectList( [ [13, 13, 13], [14, 14, 14] ] )

    if not detected or len( detected )!= 1:
        result = False
        print("Position_manager.pm._getObjectInVolumeFromObjectList( volume ) Failed!", detected )



    detected = pm._getObjectInVolumeFromObjectList( [ [14, 13, 16], [19, 14, 19] ] )

    if detected:
        result = False
        print("Position_manager.pm._getObjectInVolumeFromObjectList( volume ) Failed!", detected )


    detected = pm._getObjectInVolumeFromObjectList( [ [14, 13, 14], [19, 14, 16] ] )

    if not detected or len( detected )!= 1:
        result = False
        print("Position_manager.pm._getObjectInVolumeFromObjectList( volume ) Failed!", detected )

    


    detected = pm.getObjectInRange( Coordinate(0, 0, 0), [3], [0, 0, 0] )

    if not detected or len( detected )!= 1:
        result = False
        print("Position_manager.pm.getObjectInRange( coord, range ) Failed!" )


    detected = pm.getObjectInRange( Coordinate(0, 0, 0), [4], [0, 0, 0] )

    if not detected or len( detected )!= 2:
        result = False
        print("Position_manager.pm.getObjectInRange( coord, range ) Failed!" )


    detected = pm.getObjectInRange( Coordinate(0, 0, 0), [10], [0, 0, 0] )

    if not detected or len( detected )!= 3:
        result = False
        print("Position_manager.pm.getObjectInRange( coord, range ) Failed!" )

    
    


    
    
    #pm.show()

    return result

print("Position_manager class test result:", TestClassPosition_manager())