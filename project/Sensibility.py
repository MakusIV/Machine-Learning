from LoggerClass import Logger

# LOGGING --
 
logger = Logger(module_name = __name__, class_name = 'Sensibility')

class Sensibility:
    
    def __init__(self, sensibility = None,  state = None  ):


            self.range = None
            self.power = None
            self.delta_t_for_detection = None 
                        
            if not(self.setName(name) or not self.setState(state):
                raise Exception("Invalid parameters! Object not istantiate.")
    
    def area(distance):
        pass

    def accuracy(distance):
        pass

    