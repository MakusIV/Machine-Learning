### CLASSI

class Coordinate:
    
    """ Rappresents a coordinate in an x, y, z  system """
    
    
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z
    
    
    def move(self, direct):
        """ return new Coordinate istance evalutated from direction string:
        foward, back, right, lef, foward_up, back_up, right_up, left_up,
        foward_down, back_down, right_down, left_down.
        Not recognized direction raise a ValueError exception
        """
        if direct == 'foward':
            self.foward()
        
        elif direct == 'foward_left':
            self.foward()
            self.left()
            
        elif direct == 'foward_right':
            self.foward()
            self.right()            
            
        elif direct == 'foward_up':            
            self.foward()
            self.up()
            
        elif direct == 'foward_up_left':
            self.foward()
            self.up()
            self.left()
            
        elif direct == 'foward_up_right':
            self.foward()
            self.up()
            self.right()
            
        elif direct == 'foward_down':            
            self.foward()
            self.down()
        
        elif direct == 'foward_down_left':
            self.foward()
            self.down()
            self.left()
            
        elif direct == 'foward_down_right':
            self.foward()
            self.down()
            self.right()                
            
        elif direct == 'back':
            self.back()
            
        elif direct == 'back_left':
            self.back()
            self.left()
            
        elif direct == 'back_right':
            self.back()
            self.right()            
            
        elif direct == 'back_up':            
            self.back()
            self.up()
            
        elif direct == 'back_up_left':
            self.back()
            self.up()
            self.left()
            
        elif direct == 'back_up_right':
            self.back()
            self.up()
            self.right()
            
        elif direct == 'back_down':            
            self.back()
            self.down()        
        
        elif direct == 'back_down_left':
            self.back()
            self.down()
            self.left()
            
        elif direct == 'back_down_right':
            self.back()
            self.down()
            self.right()
                            
        elif direct == 'left':                    
            self.left()
            
        elif direct == 'left_up':
            self.left()
            self.up()
                    
        elif direct == 'right':
            self.right()
            
        elif direct == 'right_up':
            self.right()
            self.up()                                    
            
        else:
            return False
        
        return True
    
    
    def foward(self):
        """decrease y of 1"""
        self.y = self.y - 1

    def back(self):
        """increase y of 1"""
        self.y = self.y + 1

    def left(self):
        """decrease x of 1"""
        self.x = self.x - 1

    def right(self):
        """increase x of 1"""
        self.x = self.x + 1
 
    def up(self):
        """increase z of 1"""
        self.z = self.z + 1

    def down(self):
        """decrease y , of 1"""
        self.z = self.z - 1

    def duplicate(self):
        """ return a clone """
        return Coordinate(self.x, self.y, self.z)
    
    def distance(self, coord):
        """return absolute distance from coords =sqrt( (x - x)^2 + (t - y)^2 + (z-z)^2))"""        
        return ( (self.x - coord.x) ** 2 + (self.y - coord.y) ** 2 + (self.z - coord.z) ** 2 ) ** 0.5

    
    def distance_x(self, coord):
        """ return relative distance from x"""        
        return self.x - coord.x
    
    def distance_y(self, coord):
        """ return relative distance from y"""
        return self.y - coord.y
    
    def distance_z(self, coord):
        """ return relative distance from z"""
        return self.z - coord.z
    
    def is_same(self, coord):
        """return true if coord is self"""
        if coord == self:
            return True
        else:
            return False
    
    def is_egual(self, coord):
        """return true if coord have same x,y,z of self"""
        if coord.x == self.x and coord.z == self.z and coord.z == self.z:
            return True
        else:
            return False
            
    
    
    def is_in_range(self, coord, dist):
        """return true if coord distance from self is eugual or less of dist"""
        
        if coord.distance(self) <= abs(dist):
            return True
        else:
            return False

    
    
    def in_limits(self, limits):
        """return 2D-Array with state of corrispective coordinate:
        limits = [ [x-min, y_min, z_min], [x-max, y_max, z_max] ]

        """
        
        out_limit = [ [False, False, False], [False, False, False] ]
        result = True

        if self.x > limits[1][0]:
            out_limit[1][0] = True
            result = False
        
        if self.y > limits[1][1]:
            out_limit[1][1] = True
            result = False
        
        if self.z > limits[1][2]:
            out_limit[1][2] = True
            result = False

        if self.x < limits[0][0]:
            out_limit[0][0] = True
            result = False
        
        if self.y < limits[0][1]:
            out_limit[0][1] = True
            result = False
        
        if self.z < limits[0][2]:
            out_limit[0][2] = True
            result = False
                
        return result, out_limit
    
    
    def to_string(self):
    
        return str(self.x) + ','+ str(self.y) + ',' + str(self.z)


    def getId(self):
        """Return (x, y, z) tuple"""
        return ( self.x, self.y, self.z )
    
    
    def update(self, tupla):
        """update x,y,z with tupla values"""

        if not tupla:
            return False

        self.x = tupla[0]
        self.y = tupla[1]
        self.z = tupla[2]