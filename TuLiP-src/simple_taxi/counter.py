from tulip import transys, synth, spec
import numpy as np
from scipy import sparse as sp
from tomatlab import write_matlab_case

sys = transys.OpenFTS()

sys.states.add_from({'s0','s1','s2','s3'})
sys.states.initial.add('s0')
sys.atomic_propositions.add('full')
sys.states.add('s3', ap={'full'})

sys.env_actions.add_from({'des','pick','none'})

transmat1 = sp.lil_matrix(np.array(
                [[1,0,0,0],
                 [1,0,0,0],
                 [1,0,0,0],
                 [1,0,0,0]]
            ))
                     
sys.transitions.add_adj(transmat1, ['s0','s1','s2','s3'], env_actions='des')

transmat2 = sp.lil_matrix(np.array(
                [[0,1,0,0],
                 [0,0,1,0],
                 [0,0,0,1],
                 [0,0,0,1]]
            ))
                     
sys.transitions.add_adj(transmat2, ['s0','s1','s2','s3'], env_actions='pick')

transmat2 = sp.lil_matrix(np.array(
                [[1,0,0,0],
                 [0,1,0,0],
                 [0,0,1,0],
                 [0,0,0,1]]
            ))
                     
sys.transitions.add_adj(transmat2, ['s0','s1','s2','s3'], env_actions='none')

print(sys)


sys_vars = {}
sys_init = {}
sys_safe = {}
sys_prog = {}

env_vars = {}
env_init = {}
env_safe = {}
env_prog = {}

specs = spec.GRSpec(env_vars, sys_vars, env_init, sys_init,
                    env_safe, sys_safe, env_prog, sys_prog)

ctrl = synth.synthesize('gr1c',specs,sys=sys)


print(ctrl.inputs)

if not ctrl.save('counter_graph_2.png'):
    print(ctrl)

write_matlab_case("taxi_planning_counter_3.m", ctrl, classname="taxi_planning_counter_3")

