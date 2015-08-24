
import sys
import numpy as np

from tulip import spec, synth, dumpsmach, hybrid, transys
from polytope import box2poly
from tulip.abstract import prop2part, discretize
# from tomatlab import write_matlab_case

import logging
logging.basicConfig(filename='s_d.log',level=logging.DEBUG, filemode='w')
logger = logging.getLogger(__name__)

# print(sys)
# sys.save('s_d.pdf')

# @env_specs_section@
env_vars = {}
env_vars["req"] = 'boolean'
env_vars["ready"] = 'boolean'

env_init = {'ready'}
env_init |= {'!req'}

env_safe = {'req -> X(!req)'}   # not necessary
env_safe |= {'full -> X(!req)'}

env_prog = {'ready'}
# @env_specs_section_end@

# @sys_specs_section@
sys_vars = {}
sys_vars["full"] = 'boolean'
sys_safe = {'full <-> (seat || hold)'}

sys_vars["seat"] = 'boolean'
sys_vars["hold"] = 'boolean'

sys_vars["loc"] = (0, 3)
sys_init = {'loc=0'}
sys_safe |= {'loc=0 -> X( ready -> (loc=0 || loc=1 || loc=2 || loc=3))'}
sys_safe |= {'loc=1 -> X( ready -> (loc=0 || loc=1 || loc=2 || loc=3))'}
sys_safe |= {'loc=2 -> X( ready -> (loc=0 || loc=1 || loc=2 || loc=3))'}
sys_safe |= {'loc=3 -> X( ready -> (loc=0 || loc=1 || loc=2 || loc=3))'}
sys_safe |= {'loc=0 -> X( !ready -> loc=0)'}
sys_safe |= {'loc=1 -> X( !ready -> loc=1)'}
sys_safe |= {'loc=2 -> X( !ready -> loc=2)'}
sys_safe |= {'loc=3 -> X( !ready -> loc=3)'}

sys_init |= {'!seat'}
sys_init |= {'!hold'}

# This is to make sure the requests will be accommodated.
sys_safe |= {'req -> seat'}

# This is to specify the transition relations.
sys_safe |= {'seat -> X(!loc=0 -> seat)'}
sys_safe |= {'seat -> X(loc=0 -> (!seat && hold))'}
sys_safe |= {'!seat -> X(!req -> !seat)'}
sys_safe |= {'!hold || !seat'}

# This is to specify the transition relations of hold.
sys_safe |= {'hold -> X(!loc=3 -> hold)'}
sys_safe |= {'hold-> X(loc=3 -> !hold)'}
sys_safe |= {'!hold -> ( !(seat && X(loc=0)) -> X(!hold) )'}

# eventually constraints
#sys_safe |= {'(seat1 || seat_11) -> <>loc=0'}
sys_vars["temp_1"] = 'boolean'
sys_init |= {'temp_1'}
sys_prog = {'temp_1'}
sys_safe |= {'X(temp_1) <-> (loc=0 || (temp_1 && !seat))'}

#sys_safe |= {'(!hold0 || !hold_10) -> <>loc=3'}
sys_vars["temp_4"] = 'boolean'
sys_init |= {'temp_4'}
sys_prog |= {'temp_4'}
sys_safe |= {'X(temp_4) <-> (loc=3 || (temp_4 && !hold))'}

# @sys_specs_section_end@

# Initialize GRspec
specs = spec.GRSpec(env_vars, sys_vars, env_init, sys_init,
                   env_safe, sys_safe, env_prog, sys_prog)

ctrl = synth.synthesize('gr1c', specs)

#dumpsmach.write_python_case("strategy_discrete.py", ctrl, classname="strategy")
# write_matlab_case("strategy_discrete_3.m", ctrl, classname="strategy_discrete_3")

# if not ctrl.save('taxi_planning_3person.png'):
#     print(ctrl)
print(ctrl)

# either select current state before simulation
ctrl.states.current = ['Sinit']
ctrl.simulate(inputs_sequence='manual', iterations=50)
    
# or pass it to simulate
#ctrl.simulate(inputs_sequence='random', iterations=10, current_state=0)
