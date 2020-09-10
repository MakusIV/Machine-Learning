
# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/home/marco/Documenti/Machine Learning/Automata/project')

from State import State



def testClassState():

    result = True

    state = State()

    if state._active != True or state._run != False or state._destroy != False or state._remove != False:
        print('State.__Init__ Failed!! ', state._active, state._run, state._stop, state._destroy, state._remove)
        result = False 

    state = State(active = False, run = True)

    if state._active != False or state._run != False:
        print('State.__Init__ Failed!! ', state._active, state._run )
        result = False

    state = State()

    if not state.isActive() or state.isRunning() or state.isRemoved() or state.isDestroyed() or state.isCritical() or state.isAnomaly():
        print('State.is<xxx> Failed!! ', state.isActive(), state.isRunning(), state.isRemoved(), state.isDestroyed(), state.isCritical(), state.isAnomaly() )
        result = False

    
    if not state.checkState():
        print('State.checkState() Failed!! ', state.toString() )
        result = False



    state._active = False
    state._run = True
    

    try:
        state.checkState()
        
    except Exception:
        result = True

    else:
        print( 'State.checkState(): Failed!!  Not launch Exception', state.toString() )
        result = False


    state._active = True
    state._run = True

    try:
        state.checkState()
        
    except Exception:
        print( 'State.checkState() Failed!!  Launch Exception', state.toString() )
        result = False

    else:        
        result = True

    state._active = True
    state._run = True
    state._remove = True

    try:
        state.checkState()
        
    except Exception:
        result = True

    else:
        print( 'State.checkState() Failed!!  Not launch Exception', state.toString() )
        result = False


    state._active = True
    state._run = True
    state._destroy = True

    try:
        state.checkState()
        
    except Exception:
        result = True

    else:
        print( 'State.checkState() Failed!!  Not launch Exception', state.toString() )
        result = False





    state._active = False
    state._run = False
    state._remove = True
    state._destroy = False

    try:
        state.checkState()
        
    except Exception:
        print( 'State.checkState() Failed!!  Launch Exception', state.toString() )
        result = False        

    else:
        result = True

    state._active = True
    state._run = False
    state._remove = True
    state._destroy = False

    try:
        state.checkState()
        
    except Exception:
        result = True

    else:
        print( 'State.checkState() Failed!! Not launch Exception', state.toString() )
        result = False

    
    

    state._active = False
    state._run = False
    state._remove = True
    state._destroy = True

    try:
        state.checkState()
        
    except Exception:
        print( 'State.checkState() Failed!!  Launch Exception', state.toString() )
        result = False        

    else:
        result = True



    state._active = True
    state._run = False

    try:
        state.checkState()
        
    except Exception:
        result = True

    else:
        print( 'State.checkState() Failed!!  Not launch Exception', state.toString() )
        result = False



    state._active = True
    state._run = False
    state._remove = True
    state._destroy = False

    try:
        state.checkState()
        
    except Exception:
        result = True

    else:
        print( 'State.checkState() Failed!!  Not launch Exception', state.toString() )
        result = False

    
    state._active = False
    state._run = False
    state._remove = True
    state._destroy = False

    try:
        state.checkState()
        
    except Exception:
        print( 'State.checkState() Failed!!  Launch Exception', state.toString() )        
        result = False

    else:
        result = True

    state._active = False
    state._run = False
    state._remove = False
    state._destroy = False
    state._anomaly = True
    state._critical = False

    try:
        state.checkState()
        
    except Exception:
        result = True

    else:
        print( 'State.checkState() Failed!!  Not launch Exception', state.toString() )
        result = False

    state._active = False
    state._run = False
    state._remove = False    
    state._destroy = False
    state._anomaly = False
    state._critical = True

    try:
        state.checkState()
        
    except Exception:
        result = True

    else:
        print( 'State.checkState() Failed!!  Not launch Exception', state.toString() )
        result = False


    state._active = True
    state._run = False
    state._remove = False    
    state._destroy = False    
    state._anomaly = True
    state._critical = True

    try:
        state.checkState()
        
    except Exception:
        print( 'State.checkState() Failed!!  Launch Exception', state.toString() )
        result = False

    else:
        result = True



    return result

print("Test class test result:", testClassState())