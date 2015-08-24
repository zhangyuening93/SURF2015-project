import sys
import numpy as np

from tulip import spec, synth, dumpsmach, hybrid, transys
from polytope import box2poly
from tulip.abstract import prop2part, discretize
# from tomatlab import write_matlab_case

# @env_specs_section@
env_vars = {'req_0', 'req'}
env_vars |= {'car_0_succeed', 'car_1_succeed'}

env_init = {'!req_0'}
env_init |= {'car_0_succeed && car_1_succeed'}
env_safe = {'(req_0 && !car_0 && !car_1) -> X(req_0)'}
env_prog = {'car_0_succeed'}
env_prog |= {'car_1_succeed'}
# @env_specs_section_ends@

# @sys_specs_section@
sys_vars = {'car_0', 'car_1'}
sys_vars |= {'car_0_full', 'car_1_full'}

sys_init = {'!car_0_full && !car_1_full'}

sys_safe = {'!car_0 || !car_1'}

sys_safe |= {'car_0_full -> X(!car_0_succeed -> car_0_full)'}
sys_safe |= {'car_1_full -> X(!car_1_succeed -> car_1_full)'}
sys_safe |= {'car_0_full -> X(car_0_succeed -> !car_0_full)'}
sys_safe |= {'car_1_full -> X(car_1_succeed -> !car_1_full)'}
# sys_safe |= {'!car_0_full -> X(car_0 -> car_0_full'}
# sys_safe |= {'!car_1_full -> X(car_1 -> car_0_full'}
sys_safe |= {'car_0 -> car_0_full'}
sys_safe |= {'car_1 -> car_1_full'}
sys_safe |= {'!car_0_full -> X(!car_0 -> !car_0_full)'}
sys_safe |= {'!car_1_full -> X(!car_1 -> !car_1_full)'}

#sys_safe |= {'req_0 -> <>(car_0 || car_1)'} # ev
sys_vars |= {'temp'}
sys_prog = {'temp'}
sys_init |= {'temp'}
sys_safe |= {'X(temp) <-> (car_0 || car_1 || (temp && !req_0))'}

sys_safe |= {'(car_0 || car_1) -> (req_0)'}

sys_safe |= {'car_0_full -> X(!car_0)'}
sys_safe |= {'car_1_full -> X(!car_1)'}

# TODO: May be unnecessary
# sys_safe |= {'(req_0 && car_0_full) -> (car_1_full || car_1)'}
# sys_safe |= {'(req_0 && car_1_full) -> (car_0_full || car_0)'}
# @sys_specs_section_end@

# Initialize GRspec
specs = spec.GRSpec(env_vars, sys_vars, env_init, sys_init,
                   env_safe, sys_safe, env_prog, sys_prog)

ctrl = synth.synthesize('gr1c', specs)

print(ctrl)

#dumpsmach.write_python_case("dispatcher_controller.py", ctrl,classname="dispatcher_controller")

#write_matlab_case("dispatcher_controller_3.m", ctrl, classname="dispatcher_controller_3")

#if not ctrl.save('dispatcher.png'):
#    print(ctrl)

ctrl.states.current = ['Sinit']
ctrl.simulate(inputs_sequence='manual', iterations=50)
