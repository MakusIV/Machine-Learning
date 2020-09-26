# Define enviroments, object


from LoggerClass import Logger
from Position_manager import Position_manager
import random
from Coordinate import Coordinate
from Automa import Automa

# LOGGING --
 
logger = Logger(module_name = __name__, class_name = 'World')


# Enviroments




# METHODS --

def createEnviroment(name = 'default_env', limits = [100, 100, 10]):
    
    return Position_manager(name, limits)


def createObstacles():
    pass

def createResourceObject( num = 300 ):
    """Create and position Resource Object into enviroments"""
    pass

def createAutoma( num = 50 ):
    """Create and position Automa into enviroments"""
    pass

def updateEnv( actions ):    
    """Update enviroments after execution of Automa task"""
    pass

def createEvent(actions):
    """create and managed Events after execution of Automa task. Event are inserted in Autom queue events
    """
    # elabora l'azione definendo l'evento da inserire nella Queue Events dell'oggetto interessato
    pass

def runEnviroment(posMng, iterations):
    # attiva il thread(?) o processo di funzionamento
    execute = True
        
    if not iterations or not isinstance(iterations, int):
        iterations = 1000

    for i in range(iterations):

        if not execute:
            exit("stop execute")
            break
            
        if posMng.isNotMoreAutoma():
            exit("stop no more automa")

        automas = posMng.listAutoma()

        for automa in automas:
            actions = automa.executeTask()
            updateEnv(actions) 
            createEvent(actions) # elabora l'azione definendo l'evento da inserire nella Queue Events dell'oggetto interessato

    
    
    
    # MAIN
    createEnviroment()
    createResourceObject()
    createAutoma()
    runEnviroment()