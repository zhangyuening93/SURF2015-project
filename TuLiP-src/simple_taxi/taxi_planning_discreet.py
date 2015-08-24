
import sys
import numpy as np

from tulip import spec, synth, dumpsmach, hybrid, transys
from polytope import box2poly
from tulip.abstract import prop2part, discretize
from tomatlab import write_matlab_case

visualize = True
from tulip.abstract.plot import plot_partition

sys = transys.FTS()

sys.states.add_from({'X0','X1','X2','X3','X4','X5'})
sys.states.initial.add('X0')
sys.transitions.add_comb({'X0'}, {'X0', 'X1', 'X2', 'X3', 'X4', 'X5'})
sys.transitions.add_comb({'X1'}, {'X0', 'X1', 'X2', 'X3', 'X4', 'X5'})
sys.transitions.add_comb({'X2'}, {'X0', 'X1', 'X2', 'X3', 'X4', 'X5'})
sys.transitions.add_comb({'X3'}, {'X0', 'X1', 'X2', 'X3', 'X4', 'X5'})
sys.transitions.add_comb({'X4'}, {'X0', 'X1', 'X2', 'X3', 'X4', 'X5'})
sys.transitions.add_comb({'X5'}, {'X0', 'X1', 'X2', 'X3', 'X4', 'X5'})

sys.atomic_propositions.add_from({'loc_0', 'loc_1', 'loc_2', 'loc_3', 'loc_4', 'des'})
sys.states.add('X5', ap={'des'})
sys.states.add('X0', ap={'loc_0'})
sys.states.add('X1', ap={'loc_1'})
sys.states.add('X2', ap={'loc_2'})
sys.states.add('X3', ap={'loc_3'})
sys.states.add('X4', ap={'loc_4'})

# @env_specs_section@
env_vars = {'full'}
env_vars |= {'req_0'}
env_vars |= {'req_1'}
env_vars |= {'req_2'}
env_vars |= {'req_3'}

env_init = {'!full'}

env_safe = {'(pick && loc_0 && req_0) -> X(!req_0)'}
env_safe |= {'(!(pick && loc_0) && req_0) -> X(req_0)'}
env_safe |= {'(pick && loc_1 && req_1) -> X(!req_1)'}
env_safe |= {'(!(pick && loc_1) && req_1) -> X(req_1)'}
env_safe |= {'(pick && loc_2 && req_2) -> X(!req_2)'}
env_safe |= {'(!(pick && loc_2) && req_2) -> X(req_2)'}
env_safe |= {'(pick && loc_3 && req_3) -> X(!req_3)'}
env_safe |= {'(!(pick && loc_3) && req_3) -> X(req_3)'}

env_safe |= {'(full && !des) -> X(full)'}
env_safe |= {'(!full && !pick) -> X(!full)'}
env_safe |= {'des -> X(!full)'}

env_prog = {}
# @env_specs_section_end@

# @sys_specs_section@
sys_vars = {'pick'}
sys_vars |= {'temp_0_1'}
sys_vars |= {'wait_0'}
sys_vars |= {'temp_1_1'}
sys_vars |= {'wait_1'}
sys_vars |= {'temp_2_1'}
sys_vars |= {'wait_2'}
sys_vars |= {'temp_3_1'}
sys_vars |= {'wait_3'}

sys_vars |= {'temp_0_2'}

sys_init = {'temp_0_1'}
sys_init |= {'!wait_0'}
sys_init |= {'temp_1_1'}
sys_init |= {'!wait_1'}
sys_init |= {'temp_2_1'}
sys_init |= {'!wait_2'}
sys_init |= {'temp_3_1'}
sys_init |= {'!wait_3'}

sys_init |= {'temp_0_2'}

sys_safe = {'X(temp_0_1) <-> ((loc_0 && pick) || (temp_0_1 && !req_0))'}
sys_safe |= {'X(temp_1_1) <-> ((loc_1 && pick) || (temp_1_1 && !req_1))'}
sys_safe |= {'X(temp_2_1) <-> ((loc_2 && pick) || (temp_2_1 && !req_2))'}
sys_safe |= {'X(temp_3_1) <-> ((loc_3 && pick) || (temp_3_1 && !req_3))'}

sys_safe |= {'X(temp_0_2) <-> (des || (temp_0_2 && !wait_0 && !wait_1 && !wait_2 && !wait_3))'}

sys_safe |= {'full -> !pick'}

sys_safe |= {'pick -> ((loc_0 && req_0)||(loc_1 && req_1)||(loc_2 && req_2)||(loc_3 && req_3))'}

sys_safe |= {'(pick && loc_0 && req_0) -> X(wait_0)'}
sys_safe |= {'des -> X(!wait_0)'}
sys_safe |= {'(wait_0 && !des) -> X(wait_0)'}
sys_safe |= {'(pick && loc_1 && req_1) -> X(wait_1)'}
sys_safe |= {'des -> X(!wait_1)'}
sys_safe |= {'(wait_1 && !des) -> X(wait_1)'}
sys_safe |= {'(pick && loc_2 && req_2) -> X(wait_2)'}
sys_safe |= {'des -> X(!wait_2)'}
sys_safe |= {'(wait_2 && !des) -> X(wait_2)'}
sys_safe |= {'(pick && loc_3 && req_3) -> X(wait_3)'}
sys_safe |= {'des -> X(!wait_3)'}
sys_safe |= {'(wait_3 && !des) -> X(wait_3)'}


sys_prog = {'temp_0_1'}
sys_prog |= {'temp_1_1'}
sys_prog |= {'temp_2_1'}
sys_prog |= {'temp_3_1'}

sys_prog |= {'temp_0_2'}
# @sys_specs_section_end@

# Initialize GRspec
specs = spec.GRSpec(env_vars, sys_vars, env_init, sys_init,
                   env_safe, sys_safe, env_prog, sys_prog)

ctrl = synth.synthesize('gr1c', specs, sys=sys)

write_matlab_case("taxi_planning_discreet.m", ctrl, classname="taxi_planning_discreet")

#if not ctrl.save('taxi_planning_3person.png'):
#    print(ctrl)

