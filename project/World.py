# Define enviroments, object

# Enviroments

def createEnviroment(name, limits):
    
    return Position_manager(name, limits)


def createObstacles():
    pass

def createResource():
    pass

def createAutoma():
    pass

def runEnviroment(world, iterations):
    # attiva il thread(?) o processo di funzionamento
    execute = True
        
    if not iterations:
        iterations = 1000

    posMng = world.getPosMng()

    for i in range(iterations):

        if not execute:
            exit("stop execute")
            break
            
        if posMng.isNotMoreAutoma():
            exit("stop no more automa")

        automas = posMng.listAutoma()

        for automa in automas:
            actions = automa.executeTask()
            world.updateEnv(actions)#elabora l'azione definendo l'evento da inserire nella Queue Events dell'oggetto interessato
            world.createEvent(actions)

        