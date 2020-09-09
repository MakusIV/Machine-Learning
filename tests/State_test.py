
# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/home/marco/Documenti/Machine Learning/Automata/project')

from State import State



def testClassState():

    result = True

    state = State()

    if state._start != True or state._run != False or state._stop != True or state._destroy != False or state._remove != False:
        print('State.__Init__ Failed!! ', state._start, state._run, state._stop, state._destroy, state._remove)
        result = False 

    state = State(start = False, run = True)

    if state._start != False or state._run != False:
        print('State.__Init__ Failed!! ', state._start, state._run )
        result = False

    state = State()

    if not state.isStarted() or state.isRunning() or not state.isStopped() or state.isRemoved() or state.isDestroyed():
        print('State.is<xxx> Failed!! ', state.isStarted(), state.isRunning(), state.isStopped(), state.isRemoved(), state.isDestroyed() )
        result = False

    
    if not state.checkState():
        print('State.checkState() Failed!! ', state.toString() )
        result = False



    state._start = False
    state._run = True
    

    try:
        state.checkState()
        
    except Exception:
        result = True

    else:
        print( 'State.checkState(): start:false and run: true Failed!! ', state.toString() )
        result = False


    state._start = True
    state._run = True
    state._stop = True

    try:
        state.checkState()
        
    except Exception:
        result = True

    else:
        print( 'State.checkState() start:true, run:true, stop:false Failed!! ', state.toString() )
        result = False

    state._start = True
    state._run = True
    state._stop = False
    state._remove = True

    try:
        state.checkState()
        
    except Exception:
        result = True

    else:
        print( 'State.checkState() start:true, run:true, stop:false Failed!! ', state.toString() )
        result = False


    state._start = True
    state._run = True
    state._stop = False
    state._destroy = True

    try:
        state.checkState()
        
    except Exception:
        result = True

    else:
        print( 'State.checkState() start:true, run:true, stop:false Failed!! ', state.toString() )
        result = False


    state._start = False
    state._run = False
    state._stop = True
    state._remove = True

    try:
        state.checkState()
        
    except Exception:
        print( 'State.checkState() start:true, run:true, stop:false Failed!! ', state.toString() )
        result = False        

    else:
        result = True

    state._start = True
    state._run = False
    state._stop = True

    try:
        state.checkState()
        
    except Exception:
        result = True

    else:
        print( 'State.checkState() start:true, run:true, stop:false Failed!! ', state.toString() )
        result = False

    return result

print("Test class test result:", testClassState())