
# some_file.py
from math import sqrt
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'project')

from Coordinate import Coordinate

def testClassCoordinate():
    
    coord1 = Coordinate(1,2,3)
    
    result = True
    
    if coord1.x != 1:
        result = False
        print("testClassCoordinate().x Failed!")
        
    if coord1.y != 2:        
        result = False
        print("testClassCoordinate().y Failed!")
        
    if coord1.z != 3:
        result = False
        print("testClassCoordinate().z Failed!")
        
    
    
    coord2 = coord1.duplicate()
    
    
    
    if coord2.x != 1 or coord2.y != 2 or coord2.z != 3 :
        result = False
        print("testClassCoordinate().duplicate() Failed!")  
        
    if 0 != coord1.distance_x(coord2):        
        result = False
        print("testClassCoordinate().distance_x() Failed!")
    
    if 0 != coord1.distance_y(coord2):
        result = False
        print("testClassCoordinate().distance_y() Failed!")
        
    if 0 != coord1.distance_z(coord2):
        result = False
        print("testClassCoordinate().distance_x() Failed!")
        
      
    if 0 != coord1.distance(coord2):
        result = False
        print("testClassCoordinate().distance() Failed!", coord1.distance(coord2))
        
    
    
    coord3 = coord1

    
    
    if coord1.is_same(coord2) or not coord1.is_same(coord3): 
        result = False
        print("testClassCoordinate().coord1.is_same() Failed!", coord1.to_string(), coord2.to_string(), coord3.to_string())
        
    if not coord1.is_egual(coord2) or not coord1.is_egual(coord3): 
        result = False
        print("testClassCoordinate().coord1.is_egual() Failed!", coord1.to_string(), coord2.to_string(), coord3.to_string())
    
    coord2.right()
    
    if coord2.x != 2:
        result = False
        print("testClassCoordinate().right() Failed!", coord2.x)      
    
    coord2.back()
    
    if coord2.y != 1:
        result = False
        print("testClassCoordinate().back() Failed!", coord2.y)      
    
    coord2.up()    
    
    if coord2.z != 4:
        result = False
        print("testClassCoordinate().up() Failed!", coord2.z)  
        
    
    if coord1.is_in_range(coord2, 1.7319) or not coord1.is_in_range(coord2, 1.7321):
        result = False
        print("testClassCoordinate().coord1.is_in_range(coord2, 1) Failed!", coord1.to_string(), coord2.to_string(), coord1.distance(coord2))

    
    
    coord3.move('foward_right')
        
    if coord3.x != 2 and coord3.y != 3 and coord3.z !=3:
        result = False
        print("testClassCoordinate().move(foward_right) Failed!", coord3.to_string())      
    
    coord3.move('foward_left')
    
    if coord3.x != 1 and coord3.y != 4 and coord3.z !=3:
        result = False
        print("testClassCoordinate().move(foward_left) Failed!", coord3.to_string())      
        
    
    coord3.move('foward_up')  
    
    if coord3.x != 1 and coord3.y != 5 and coord3.z !=4:
        result = False
        print("testClassCoordinate().move(foward_up) Failed!", coord3.to_string())      
    
    coord3.move('foward_down')    
    
    if coord3.x != 1 and coord3.y != 6 and coord3.z !=3:
        result = False
        print("testClassCoordinate().move(foward_down) Failed!", coord3.to_string())     
        
    coord3.move('foward_down_right')    
    
    if coord3.x != 2 and coord3.y != 7 and coord3.z !=2:
        result = False
        print("testClassCoordinate().move(foward_down_right) Failed!", coord3.to_string())   
        
    coord3.move('foward_down_left')    
    
    if coord3.x != 1 and coord3.y != 8 and coord3.z !=1:
        result = False
        print("testClassCoordinate().move(foward_down_left) Failed!", coord3.to_string())   
        
        
    coord3.move('foward_up_right')    
    
    if coord3.x != 2 and coord3.y != 9 and coord3.z !=2:
        result = False
        print("testClassCoordinate().move(foward_up_right) Failed!", coord3.to_string())   
        
    coord3.move('foward_up_left')    
    
    if coord3.x != 1 and coord3.y != 10 and coord3.z !=3:
        result = False
        print("testClassCoordinate().move(foward_up_left) Failed!", coord3.to_string())   

    
    coord3.move('backward_right')
        
    if coord3.x != 2 and coord3.y != 9 and coord3.z !=3:
        result = False
        print("testClassCoordinate().move(back_right) Failed!", coord3.to_string())      
    
    coord3.move('backward_left')
    
    if coord3.x != 1 and coord3.y != 8 and coord3.z !=3:
        result = False
        print("testClassCoordinate().move(back_left) Failed!", coord3.to_string())      
        
    
    coord3.move('backward_up')  
    
    if coord3.x != 1 and coord3.y != 7 and coord3.z !=4:
        result = False
        print("testClassCoordinate().move(backward_up) Failed!", coord3.to_string())      
    
    coord3.move('backward_down')    
    
    if coord3.x != 1 and coord3.y != 6 and coord3.z !=3:
        result = False
        print("testClassCoordinate().move(backward_down) Failed!", coord3.to_string())     
        
    coord3.move('backward_down_right')    
    
    if coord3.x != 2 and coord3.y != 5 and coord3.z !=2:
        result = False
        print("testClassCoordinate().move(backward_down_right) Failed!", coord3.to_string())   
        
    coord3.move('backward_down_left')    
    
    if coord3.x != 1 and coord3.y != 4 and coord3.z !=1:
        result = False
        print("testClassCoordinate().move(backward_down_left) Failed!", coord3.to_string())   
        
        
    coord3.move('backward_up_right')    
    
    if coord3.x != 2 and coord3.y != 3 and coord3.z != 2:
        result = False
        print("testClassCoordinate().move(backward_up_right) Failed!", coord3.to_string())   
        
    coord3.move('backward_up_left')    
    
    if coord3.x != 1 and coord3.y != 2 and coord3.z != 3:
        result = False
        print("testClassCoordinate().move(backward_up_left) Failed!", coord3.to_string())   
    
    coord3.move('_up_left')    
    
    if coord3.x != 0 and coord3.y != 2 and coord3.z != 4:
        result = False
        print("testClassCoordinate().move(_up_left) Failed!", coord3.to_string())   
    
    coord3.move('_down_left')    
    
    if coord3.x != -1 and coord3.y != 2 and coord3.z != 3:
        result = False
        print("testClassCoordinate().move(_down_left) Failed!", coord3.to_string())   
    
    coord3.move('_left')    
    
    if coord3.x != -2 and coord3.y != 2 and coord3.z != 3:
        result = False
        print("testClassCoordinate().move(_left) Failed!", coord3.to_string())   

    coord3.move('_right')    
    
    if coord3.x != -1 and coord3.y != 2 and coord3.z != 3:
        result = False
        print("testClassCoordinate().move(_right) Failed!", coord3.to_string())   
    
    coord3.move('_up_right')    
    
    if coord3.x != 0 and coord3.y != 2 and coord3.z != 4:
        result = False
        print("testClassCoordinate().move(_up_right) Failed!", coord3.to_string())   
    
    coord3.move('_down_right')    
    
    if coord3.x != 1 and coord3.y != 2 and coord3.z != 3:
        result = False
        print("testClassCoordinate().move(_up_right) Failed!", coord3.to_string())   
    

    coord3.move('_down')    
    
    if coord3.x != 1 and coord3.y != 2 and coord3.z != 2:
        result = False
        print("testClassCoordinate().move(_down) Failed!", coord3.to_string())   
    

    coord3.move('_up')    
    
    if coord3.x != 1 and coord3.y != 2 and coord3.z != 3:
        result = False
        print("testClassCoordinate().move(_up) Failed!", coord3.to_string())   
    


    limits = [ [0, 0, 0], [2, 2, 2]] 
    res, val = coord1.in_limits(limits)    
    coord1 = Coordinate(1,1,1)

    if [ [False, False, False], [False, False, False] ]!= val and res:
        result = False
        print("testClassCoordinate().in_limits(limits) Failed!", coord1.to_string(), limits)   
    
    coord1 = Coordinate(0,0,0)

    if [ [False, False, False], [False, False, False] ] != val and res:
        result = False
        print("testClassCoordinate().in_limits(limits) Failed!", coord1.to_string(), limits)   
    

    coord1 = Coordinate(2,2,2)

    if [ [False, False, False], [False, False, False] ] !=  val and res:
        result = False
        print("testClassCoordinate().in_limits(limits) Failed!", coord1.to_string(), limits)   

    coord1 = Coordinate(-1,0,0)

    if [ [True, False, False], [False, False, False] ] !=  val and res:
        result = False
        print("testClassCoordinate().in_limits(limits) Failed!", coord1.to_string(), limits) 

    coord1 = Coordinate(-1,-1,0)

    if [ [True, True, False], [False, False, False] ] !=  val and res:
        result = False
        print("testClassCoordinate().in_limits(limits) Failed!", coord1.to_string(), limits)   
    
    coord1 = Coordinate(-1,-1,-1)

    if [ [True, True, True], [False, False, False] ] !=  val and res:
        result = False
        print("testClassCoordinate().in_limits(limits) Failed!", coord1.to_string(), limits)  

    coord1 = Coordinate(3,-1,-1)

    if [ [False, True, True], [True, False, False] ] !=  val and res:
        result = False
        print("testClassCoordinate().in_limits(limits) Failed!", coord1.to_string(), limits) 


    coord1 = Coordinate(3,3,-1)

    if [ [False, False, True], [True, True, False] ] !=  val and res:
        result = False
        print("testClassCoordinate().in_limits(limits) Failed!", coord1.to_string(), limits) 
 
    coord1 = Coordinate(3,3,3)

    if [ [False, False, False], [True, True, True] ] !=  val and res:
        result = False
        print("testClassCoordinate().in_limits(limits) Failed!", coord1.to_string(), limits) 

    coord1 = Coordinate(3,-5,1)

    if [ [False, True, False], [True, False, False] ] !=  val and res:
        result = False
        print("testClassCoordinate().in_limits(limits) Failed!", coord1.to_string(), limits) 
 

    if coord1.to_string() != '3,-5,1':
        result = False
        print("testClassCoordinate().to_string() Failed!", coord1.to_string()) 


    if coord1.getId() != (3, -5, 1):
        result = False
        print("testClassCoordinate().getId() Failed!", coord1.to_string()) 

    

    coord1.setPosition( (1,1,1) )
    
    if (1,1,1) != coord1.getPosition():
        result = False
        print("testClassCoordinate().setPosition() Failed!", coord1.getPosition()) 


    if coord1.eval_direction( ( 0, 0, 0 ), ( 1, 1, 1 ) ) != 'foward_up_right':
        result = False
        print("testClassCoordinate().eval_direction() Failed!", coord1.eval_direction( ( 0, 0, 0 ), ( 1, 1, 1 ) ) ) 

    
    if coord1.eval_direction( ( 0, 0, 0 ), ( -1, 1, 1 ) ) != 'foward_up_left':
        result = False
        print("testClassCoordinate().eval_direction() Failed!", coord1.eval_direction( ( 0, 0, 0 ), ( -1, 1, 1 ) ) ) 


    if coord1.eval_direction( ( 0, 0, 0 ), ( 0, 1, 1 ) ) != 'foward_up':
        result = False
        print("testClassCoordinate().eval_direction() Failed!", coord1.eval_direction( ( 0, 0, 0 ), ( 0, 1, 1 ) ) ) 

    if coord1.eval_direction( ( 0, 0, 0 ), ( 1, 1, -1 ) ) != 'foward_down_right':
        result = False
        print("testClassCoordinate().eval_direction() Failed!", coord1.eval_direction( ( 0, 0, 0 ), ( 1, 1, -1 ) ) ) 

    if coord1.eval_direction( ( 0, 0, 0 ), ( -1, 1, -1 ) ) != 'foward_down_left':
        result = False
        print("testClassCoordinate().eval_direction() Failed!", coord1.eval_direction( ( 0, 0, 0 ), ( -1, 1, -1 ) ) ) 


    if coord1.eval_direction( ( 0, 0, 0 ), ( 0, 1, -1 ) ) != 'foward_down':
        result = False
        print("testClassCoordinate().eval_direction() Failed!", coord1.eval_direction( ( 0, 0, 0 ), ( 0, 1, -1 ) ) ) 

    if coord1.eval_direction( ( 0, 0, 0 ), ( 0, 1, 0 ) ) != 'foward':
        result = False
        print("testClassCoordinate().eval_direction() Failed!", coord1.eval_direction( ( 0, 0, 0 ), ( 0, 1, 0 ) ) ) 


    if coord1.eval_direction( ( 0, 0, 0 ), ( 1, -1, 1 ) ) != 'backward_up_right':
        result = False
        print("testClassCoordinate().eval_direction() Failed!", coord1.eval_direction( ( 0, 0, 0 ), ( 1, -1, 1 ) ) ) 

    
    if coord1.eval_direction( ( 0, 0, 0 ), ( -1, -1, 1 ) ) != 'backward_up_left':
        result = False
        print("testClassCoordinate().eval_direction() Failed!", coord1.eval_direction( ( 0, 0, 0 ), ( -1, -1, 1 ) ) ) 


    if coord1.eval_direction( ( 0, 0, 0 ), ( 0, -1, 1 ) ) != 'backward_up':
        result = False
        print("testClassCoordinate().eval_direction() Failed!", coord1.eval_direction( ( 0, 0, 0 ), ( 0, -1, 1 ) ) ) 


    if coord1.eval_direction( ( 0, 0, 0 ), ( 1, -1, -1 ) ) != 'backward_down_right':
        result = False
        print("testClassCoordinate().eval_direction() Failed!", coord1.eval_direction( ( 0, 0, 0 ), ( 1, -1, -1 ) ) ) 

    if coord1.eval_direction( ( 0, 0, 0 ), ( -1, -1, -1 ) ) != 'backward_down_left':
        result = False
        print("testClassCoordinate().eval_direction() Failed!", coord1.eval_direction( ( 0, 0, 0 ), ( -1, -1, -1 ) ) ) 

    if coord1.eval_direction( ( 0, 0, 0 ), ( 0, -1, -1 ) ) != 'backward_down':
        result = False
        print("testClassCoordinate().eval_direction() Failed!", coord1.eval_direction( ( 0, 0, 0 ), ( 0, -1, -1 ) ) ) 

    if coord1.eval_direction( ( 0, 0, 0 ), ( 0, -1, 0 ) ) != 'backward':
        result = False
        print("testClassCoordinate().eval_direction() Failed!", coord1.eval_direction( ( 0, 0, 0 ), ( 0, -1, 0 ) ) ) 

    if coord1.eval_direction( ( 0, 0, 0 ), ( -1, 0, 0 ) ) != '_left':
        result = False
        print("testClassCoordinate().eval_direction(): _left, Failed!", coord1.eval_direction( ( 0, 0, 0 ), ( -1, 0, 0 ) ) ) 

    if coord1.eval_direction( ( 0, 0, 0 ), ( -1, 0, -1 ) ) != '_down_left':
        result = False
        print("testClassCoordinate().eval_direction(): _down_left, Failed!", coord1.eval_direction( ( 0, 0, 0 ), ( -1, 0, -1 ) ) ) 

    if coord1.eval_direction( ( 0, 0, 0 ), ( -1, 0, 1 ) ) != '_up_left':
        result = False
        print("testClassCoordinate().eval_direction(): _up_left, Failed!", coord1.eval_direction( ( 0, 0, 0 ), ( -1, 0, 1 ) ) ) 

    if coord1.eval_direction( ( 0, 0, 0 ), ( 1, 0, 0 ) ) != '_right':
        result = False
        print("testClassCoordinate().eval_direction(): _right, Failed!", coord1.eval_direction( ( 0, 0, 0 ), ( 1, 0, 0 ) ) ) 

    if coord1.eval_direction( ( 0, 0, 0 ), ( 1, 0, -1 ) ) != '_down_right':
        result = False
        print("testClassCoordinate().eval_direction(): _down_right, Failed!", coord1.eval_direction( ( 0, 0, 0 ), ( 1, 0, -1 ) ) ) 

    if coord1.eval_direction( ( 0, 0, 0 ), ( 1, 0, 1 ) ) != '_up_right':
        result = False
        print("testClassCoordinate().eval_direction(): _up_right, Failed!", coord1.eval_direction( ( 0, 0, 0 ), ( 1, 0, 1 ) ) ) 

    if coord1.eval_direction( ( 0, 0, 0 ), ( 0, 0, 1 ) ) != '_up':
        result = False
        print("testClassCoordinate().eval_direction(): _up, Failed!", coord1.eval_direction( ( 0, 0, 0 ), ( 1, 0, 1 ) ) ) 

    if coord1.eval_direction( ( 0, 0, 0 ), ( 0, 0, -1 ) ) != '_down':
        result = False
        print("testClassCoordinate().eval_direction(): _down, Failed!", coord1.eval_direction( ( 0, 0, 0 ), ( 1, 0, 1 ) ) ) 

    coord1 = Coordinate(2,2,2)
    res = coord1.getVector( (4,4,4) )

    if res[0] != (2,2,2) or res[1]!= sqrt(12):
        result = False
        print("testClassCoordinate().getVector( (4,4,4) ), A - Failed!", res[0], res[1] ) 
    
    
    res = coord1.getVector( (1,1,1) )

    if res[0] != (-1,-1,-1) or res[1]!= sqrt(3):
        result = False
        print("testClassCoordinate().getVector( (1,1,1) ), B - Failed!", res[0], res[1] ) 
    

    res = coord1.getVectorAspect( (2,2,2), (4,4,4) )

    if res[0] != "approach" or res[1]<=0 or res[2]!=(0, 0, 0):
        result = False
        print("testClassCoordinate().getVectorAspect( (2,2,2), (4,4,4) ), Failed!", res[0], res[1], res[2] ) 

    res = coord1.getVectorAspect( (0,0,-3), (0,0,+3) )

    if res[0] != "away" or res[1]>0 or res[2]!=(0, 0, 0):
        result = False
        print("testClassCoordinate().getVectorAspect( (0,0,-3), (0,0,+3) ), Failed!", res[0], res[1], res[2] ) 

    res = coord1.getVectorAspect( (1,5,-5), (-1,-5,+5) )

    if res[0] != "away" or res[1]>0 or res[2]!=(0, 0, 0):
        result = False
        print("testClassCoordinate().getVectorAspect( (1,5,-5), (-1,-5,+5) ), Failed!", res[0], res[1], res[2] ) 

    res = coord1.getVectorAspect( (1,5,5), (2,7,6) )

    if res[0] != "approach" or res[1]<0 or res[2]==(0, 0, 0):
        result = False
        print("testClassCoordinate().getVectorAspect( (1,5,5), (2,7,6) ), Failed!", res[0], res[1], res[2] ) 

    res = coord1.getVectorAspect( (0,0,1), (1,1,0) )

    if res[0] != "tangent" or res[1]!=0 or res[2]==(0, 0, 0):
        result = False
        print("testClassCoordinate().getVectorAspect( (0,0,1), (1,1,0) ), Failed!", res[0], res[1], res[2] ) 


    return result

print("Coordinate class test result:", testClassCoordinate())