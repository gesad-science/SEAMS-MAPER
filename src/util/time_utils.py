import time
from system_config import LOOP_TIME
START_TIME = time.time()

def get_system_uptime():
    elapsed = time.time() - START_TIME
    return elapsed

def verify_loop(iteration:int):

    current_time = get_system_uptime()
    iteration_limit = iteration*LOOP_TIME

    if current_time >= iteration_limit:
        return True
    else:
        time.sleep(2)
        verify_loop(iteration=iteration)

