import sys
import numpy as np

from tulip import spec, synth, dumpsmach, hybrid, transys
from polytope import box2poly
from tulip.abstract import prop2part, discretize
# from tomatlab import write_matlab_case

import logging
logging.basicConfig(filename='s_d.log',level=logging.DEBUG, filemode='w')
logger = logging.getLogger(__name__)

# @env_specs_section@
env_vars = {}
env_vars["req_1"] = 'boolean'
env_vars["req_2"] = 'boolean'
env_vars["req_3"] = 'boolean'
env_vars["car_0_full"] = 'boolean'
env_vars["car_1_full"] = 'boolean'

env_init = {'!req_1 && !req_2 && !req_3'}
env_init |= {'!car_0_full && !car_1_full'}

env_safe = {'(req_1 && !car_0=1 && !car_1=1) -> X(req_1)'}
env_safe |= {'(req_2 && !car_0=2 && !car_1=2) -> X(req_2)'}
env_safe |= {'(req_3 && !car_0=3 && !car_1=3) -> X(req_3)'}

env_safe |= {'(!car_0_full && car_0=0) -> X(!car_0_full)'}
env_safe |= {'(!car_1_full && car_1=0) -> X(!car_1_full)'}
env_prog = {'!car_0_full'}
env_prog |= {'!car_1_full'}
# @env_specs_section_ends@

# @sys_specs_section@
sys_vars = {}
sys_vars['car_0'] = (0, 3)
sys_vars['car_1'] = (0, 3)

# This is to make sure a req is not taken by both cars.
sys_safe = {'car_0=1 -> !car_1=1'}
sys_safe |= {'car_0=2 -> !car_1=2'}
sys_safe |= {'car_0=3 -> !car_1=3'}

# This is to specify the transitions of counter/full.
# sys_safe |= {'car_0_full=1 -> X((!car_0_succeed && car_0=0) -> car_0_full=1)'}
# sys_safe |= {'car_1_full=1 -> X((!car_1_succeed && car_1=0) -> car_1_full=1)'}
# sys_safe |= {'car_0_full=1 -> X((car_0_succeed && car_0=0) -> car_0_full=0)'}
# sys_safe |= {'car_1_full=1 -> X((car_1_succeed && car_1=0) -> car_1_full=0)'}
# sys_safe |= {'car_0_full=1 -> X((!car_0_succeed && car_0=1) -> car_0_full=2)'}
# sys_safe |= {'car_1_full=1 -> X((!car_1_succeed && car_1=1) -> car_1_full=2)'}
# sys_safe |= {'car_0_full=1 -> X((car_0_succeed && car_0=1) -> car_0_full=1)'}
# sys_safe |= {'car_1_full=1 -> X((car_1_succeed && car_1=1) -> car_1_full=1)'}

sys_init = {'car_0=0 && car_1=0'}

# sys_safe |= {'!car_0_full -> X(car_0 -> car_0_full'}
# sys_safe |= {'!car_1_full -> X(car_1 -> car_0_full'}
sys_safe |= {'(car_0=1 || car_1=1) -> (req_1)'}
sys_safe |= {'(car_0=2 || car_1=2) -> (req_2)'}
sys_safe |= {'(car_0=3 || car_1=3) -> (req_3)'}

sys_safe |= {'car_0_full -> car_0=0'}
sys_safe |= {'car_1_full -> car_1=0'}

#sys_safe |= {'req_0 -> <>(car_0 || car_1)'} # ev
#sys_safe |= {'req_1 -> <>(car_0 || car_1)'} # ev
#sys_safe |= {'req_2 -> <>(car_0 || car_1)'} # ev
sys_vars["temp2_0"] = 'boolean'
sys_vars["temp2_1"] = 'boolean'
sys_vars["temp2_2"] = 'boolean'
sys_prog = {'temp2_0'}
sys_prog |= {'temp2_1'}
sys_prog |= {'temp2_2'}
sys_init |= {'temp2_0', 'temp2_1', 'temp2_2'}
sys_safe |= {'X(temp2_0) <-> (car_0=1 || car_1=1 || (temp2_0 && !req_1))'}
sys_safe |= {'X(temp2_1) <-> (car_0=2 || car_1=2 || (temp2_1 && !req_2))'}
sys_safe |= {'X(temp2_2) <-> (car_0=3 || car_1=3 || (temp2_2 && !req_3))'}

# TODO: May be unnecessary
sys_safe |= {'((req_1 || req_2 || req_3) && car_0_full) -> (car_1_full || !car_1=0)'}
sys_safe |= {'((req_1 || req_2 || req_3) && car_1_full) -> (car_0_full || !car_0=0)'}

# @sys_specs_section_end@

# Initialize GRspec
specs = spec.GRSpec(env_vars=env_vars, sys_vars=sys_vars, env_init=env_init, sys_init=sys_init,
                   env_safety=env_safe, sys_safety=sys_safe, env_prog=env_prog, sys_prog=sys_prog)

ctrl = synth.synthesize('jtlv', specs)

print(ctrl)

#write_matlab_case("dispatcher_controller_3.m", ctrl, classname="dispatcher_controller_3")

# if not ctrl.save('dispatcher.png'):
#    print(ctrl)

# ctrl.states.current = ['Sinit']
# ctrl.simulate(inputs_sequence='manual', iterations=50)
