
# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/home/marco/Documenti/Machine Learning/Automata/project')

from State import State



def testClassState():

    result = True

    state = State()

    if state._active != True or state._run != False or state._stop != True or state._destroy != False or state._remove != False:
        print('State.__Init__ Failed!! ', state._active, state._run, state._stop, state._destroy, state._remove)
        result = False 

    state = State(active = False, run = True)

    if state._active != False or state._run != False:
        print('State.__Init__ Failed!! ', state._active, state._run )
        result = False

    state = State()

    if not state.isActive() or state.isRunning() or not state.isStopped() or state.isRemoved() or state.isDestroyed():
        print('State.is<xxx> Failed!! ', state.isActive(), state.isRunning(), state.isStopped(), state.isRemoved(), state.isDestroyed() )
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
        print( 'State.checkState(): active:False and run: True Failed!! ', state.toString() )
        result = False


    state._active = True
    state._run = True
    state._stop = True

    try:
        state.checkState()
        
    except Exception:
        result = True

    else:
        print( 'State.checkState() active:True, run:True, stop:True Failed!! ', state.toString() )
        result = False

    state._active = True
    state._run = True
    state._stop = False
    state._remove = True

    try:
        state.checkState()
        
    except Exception:
        result = True

    else:
        print( 'State.checkState() active:True, run:True, stop:False, remove:True Failed!! ', state.toString() )
        result = False


    state._active = True
    state._run = True
    state._stop = False
    state._destroy = True

    try:
        state.checkState()
        
    except Exception:
        result = True

    else:
        print( 'State.checkState() active:true, run:true, stop:false destroy:True  Failed!! ', state.toString() )
        result = False





    state._active = False
    state._run = False
    state._stop = True
    state._remove = True

    try:
        state.checkState()
        
    except Exception:
        print( 'State.checkState() active:False, run:False, stop:True remove:True Failed!! ', state.toString() )
        result = False        

    else:
        result = True

    state._active = True
    state._run = False
    state._stop = True

    try:
        state.checkState()
        
    except Exception:
        result = True

    else:
        print( 'State.checkState() active:True, run:False, stop:True Failed!! ', state.toString() )
        result = False

    
    


    state._active = False
    state._run = False
    state._stop = True
    state._destroy = True

    try:
        state.checkState()
        
    except Exception:
        print( 'State.checkState() active:False, run:True, stop:True Failed!! ', state.toString() )
        result = False        

    else:
        result = True



    state._active = True
    state._run = False
    state._stop = True

    try:
        state.checkState()
        
    except Exception:
        result = True

    else:
        print( 'State.checkState() active:true, run:False, stop:True Failed!! ', state.toString() )
        result = False



    state._active = True
    state._run = False
    state._stop = True
    state._remove = True
    state._destroy = False

    try:
        state.checkState()
        
    except Exception:
        result = True

    else:
        print( 'State.checkState() active:False, run:False, stop:True, remove:True, destroy: True Failed!! ', state.toString() )
        result = False

    
    state._active = False
    state._run = False
    state._stop = False
    state._remove = True
    state._destroy = False

    try:
        state.checkState()
        
    except Exception:
        print( 'State.checkState() active:False, run:False, stop:False, remove:True, destroy: False Failed!! ', state.toString() )        
        result = False

    else:
        result = True




    return result

print("Test class test result:", testClassState())