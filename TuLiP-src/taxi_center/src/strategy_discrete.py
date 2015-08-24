
import sys
import numpy as np

from tulip import spec, synth, hybrid, transys
from polytope import box2poly
from tulip.abstract import prop2part, discretize
# from tomatlab import write_matlab_case
import dumpsmach

# import logging
# logging.basicConfig(filename='s_d_2.log',level=logging.DEBUG, filemode='w')
# logger = logging.getLogger(__name__)

# @env_specs_section@
env_vars = {}
env_vars["req"] = (0, 3)
env_init = {'req=0'}

env_vars["ready"] = 'boolean'
env_init |= {'ready'}

env_safe = {'full -> X(req=0)'}

env_prog = {'ready'}
# @env_specs_section_end@

# @sys_specs_section@
sys_vars = {}
sys_vars["full"] = 'boolean'
sys_safe = {'full <-> ((!seat_0=0 || !hold_0=0) && (!seat_1=0 || !hold_1=0))'}

sys_vars["seat_0"] = (0, 3)
sys_vars["hold_0"] = (0, 3)
sys_vars["seat_1"] = (0, 3)
sys_vars["hold_1"] = (0, 3)

sys_vars["loc"] = (0, 4)
sys_init = {'loc=4'}
sys_safe |= {'loc=0 -> X( ready -> (loc=0 || loc=1 || loc=2 || loc=4))'}
sys_safe |= {'loc=1 -> X( ready -> (loc=0 || loc=1 || loc=2 || loc=4))'}
sys_safe |= {'loc=2 -> X( ready -> (loc=0 || loc=1 || loc=2 || loc=4))'}
sys_safe |= {'loc=3 -> X( ready -> (loc=4 || loc=3))'}
sys_safe |= {'loc=4 -> X( ready -> (loc=0 || loc=1 || loc=2 || loc=3))'}
sys_safe |= {'loc=0 -> X( !ready -> loc=0 )'}
sys_safe |= {'loc=1 -> X( !ready -> loc=1 )'}
sys_safe |= {'loc=2 -> X( !ready -> loc=2 )'}
sys_safe |= {'loc=3 -> X( !ready -> loc=3 )'}
sys_safe |= {'loc=4 -> X( !ready -> loc=4 )'}

sys_init |= {'seat_0=0'}
sys_init |= {'hold_0=0'}
sys_init |= {'seat_1=0'}
sys_init |= {'hold_1=0'}

# This is to give preference and make sure they won't go true at the same time
sys_safe |= {'(seat_0=0 && seat_1=0 && hold_0=0 && hold_1=0) -> X(req=1 -> (seat_0=1 && seat_1=0))'}
sys_safe |= {'(seat_0=0 && seat_1=0 && hold_0=0 && hold_1=0) -> X(req=2 -> (seat_0=2 && seat_1=0))'}
sys_safe |= {'(seat_0=0 && seat_1=0 && hold_0=0 && hold_1=0) -> X(req=3 -> (seat_0=3 && seat_1=0))'}

# This is to make sure another pickup at the same location will be counted differently.
sys_safe |= {'(seat_0=1 || seat_1=1) -> X(req=1 -> ((seat_0=1 || hold_0=1) && (seat_1=1 || hold_1=1)))'}
sys_safe |= {'(seat_0=2 || seat_1=2) -> X(req=2 -> ((seat_0=2 || hold_0=2) && (seat_1=2 || hold_1=2)))'}
sys_safe |= {'(seat_0=3 || seat_1=3) -> X(req=3 -> ((seat_0=3 || hold_0=3) && (seat_1=3 || hold_1=3)))'}

# This is to make sure the requests will be accommodated.
sys_safe |= {'req=1 -> (seat_0=1 || seat_1=1)'}
sys_safe |= {'req=2 -> (seat_0=2 || seat_1=2)'}
sys_safe |= {'req=3 -> (seat_0=3 || seat_1=3)'}

# This is to specify the transition relations.
sys_safe |= {'seat_0=1 -> X(!loc=0 -> seat_0=1)'}
sys_safe |= {'seat_0=2 -> X(!loc=1 -> seat_0=2)'}
sys_safe |= {'seat_0=3 -> X(!loc=2 -> seat_0=3)'}

sys_safe |= {'seat_1=1 -> X(!loc=0 -> seat_1=1)'}
sys_safe |= {'seat_1=2 -> X(!loc=1 -> seat_1=2)'}
sys_safe |= {'seat_1=3 -> X(!loc=2 -> seat_1=3)'}

sys_safe |= {'seat_0=1 -> X(loc=0 -> (seat_0=0 && hold_0=1))'}
sys_safe |= {'seat_0=2 -> X(loc=1 -> (seat_0=0 && hold_0=2))'}
sys_safe |= {'seat_0=3 -> X(loc=2 -> (seat_0=0 && hold_0=3))'}

sys_safe |= {'seat_1=1 -> X(loc=0 -> (seat_1=0 && hold_1=1))'}
sys_safe |= {'seat_1=2 -> X(loc=1 -> (seat_1=0 && hold_1=2))'}
sys_safe |= {'seat_1=3 -> X(loc=2 -> (seat_1=0 && hold_1=3))'}

sys_safe |= {'seat_0=0 -> X(req=0 -> seat_0=0)'}
sys_safe |= {'seat_1=0 -> X(req=0 -> seat_1=0)'}

sys_safe |= {'hold_0=0 || seat_0=0'}
sys_safe |= {'hold_1=0 || seat_1=0'}

# This is to specify the transition relations of hold.

sys_safe |= {'hold_0=1 -> X(!loc=3 -> hold_0=1)'}
sys_safe |= {'hold_0=2 -> X(!loc=3 -> hold_0=2)'}
sys_safe |= {'hold_0=3 -> X(!loc=3 -> hold_0=3)'}

sys_safe |= {'hold_1=1 -> X(!loc=3 -> hold_1=1)'}
sys_safe |= {'hold_1=2 -> X(!loc=3 -> hold_1=2)'}
sys_safe |= {'hold_1=3 -> X(!loc=3 -> hold_1=3)'}

sys_safe |= {'!hold_0=0-> X(loc=3 -> hold_0=0)'}
sys_safe |= {'!hold_1=0-> X(loc=3 -> hold_1=0)'}

sys_safe |= {'hold_0=0 -> ( !( (seat_0=1 && X(loc=0)) || (seat_0=2 && X(loc=1)) || (seat_0=3 && X(loc=2)) ) -> X(hold_0=0) )'}
sys_safe |= {'hold_1=0 -> ( !( (seat_1=1 && X(loc=0)) || (seat_1=2 && X(loc=1)) || (seat_1=3 && X(loc=2)) ) -> X(hold_1=0) )'}

# eventually constraints
#sys_safe |= {'(seat_01 || seat_11) -> <>loc=0'}
#sys_safe |= {'(seat_02 || seat_12) -> <>loc=1'}
#sys_safe |= {'(seat_03 || seat_13) -> <>loc=2'}
sys_vars["temp_1"] = 'boolean'
sys_vars["temp_2"] = 'boolean'
sys_vars["temp_3"] = 'boolean'
sys_init |= {'temp_1 && temp_2 && temp_3'}
sys_prog = {'temp_1'}
sys_prog |= {'temp_2'}
sys_prog |= {'temp_3'}
sys_safe |= {'X(temp_1) <-> (loc=0 || (temp_1 && !seat_0=1 && !seat_1=1))'}
sys_safe |= {'X(temp_2) <-> (loc=1 || (temp_2 && !seat_0=2 && !seat_1=2))'}
sys_safe |= {'X(temp_3) <-> (loc=2 || (temp_3 && !seat_0=3 && !seat_1=3))'}

#sys_safe |= {'(!hold_00 || !hold_10) -> <>loc=3'}
sys_vars["temp_4"] = 'boolean'
sys_init |= {'temp_4'}
sys_prog |= {'temp_4'}
sys_safe |= {'X(temp_4) <-> (loc=3 || (temp_4 && hold_0=0 && hold_1=0))'}

# @sys_specs_section_end@

# Initialize GRspec
specs = spec.GRSpec(env_vars, sys_vars, env_init, sys_init,
                   env_safe, sys_safe, env_prog, sys_prog)

ctrl = synth.synthesize('gr1c', specs)

dumpsmach.write_python_case("TuLiPstrategy.py", ctrl,classname="strategy")
dumpsmach.write_ROS_srv("TuLiP_service.srv", ctrl)

# write_matlab_case("strategy_discrete_3.m", ctrl, classname="strategy_discrete_3")

# if not ctrl.save('taxi_planning_3person.png'):
#     print(ctrl)
# print(ctrl)

# either select current state before simulation
# ctrl.states.current = ['Sinit']
# ctrl.simulate(inputs_sequence='manual', iterations=50)
    
# or pass it to simulate
#ctrl.simulate(inputs_sequence='random', iterations=10, current_state=0)
