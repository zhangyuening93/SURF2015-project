from tulip import spec, synth, transys
import dumpsmach

import logging
logging.basicConfig(filename='s_d.log',level=logging.DEBUG, filemode='w')
logger = logging.getLogger(__name__)



def spec_gen(num_req, num_taxi):
    env_vars = set()
    env_init = set()
    env_safe = set()
    env_prog = set()
    sys_vars = set()
    sys_init = set()
    sys_safe = set()
    sys_prog = set()

    # Add variables
    for m in range(num_req):
        env_vars.add('req_'+str(m))
        sys_vars.add('temp_'+str(m))
        for n in range(num_taxi):
            sys_vars.add('taxi_'+str(n)+'_'+str(m))

    for m in range(num_taxi):
        env_vars.add('full_'+str(m))

    # Add env specifications
    for n in range(num_req):
        all_taxi_zero = ''
        for m in range(num_taxi):
            if m == 0:
                all_taxi_zero += '!taxi_'+str(m)+'_'+str(n)
            else: 
                all_taxi_zero += ' && !taxi_'+str(m)+'_'+str(n)
        env_safe.add('req_'+str(n)+' && '+all_taxi_zero+' -> X(req_'+str(n)+')')

    for m in range(num_taxi):
        all_taxi_zero = ''
        for n in range(num_req):
            if n == 0:
                all_taxi_zero += '!taxi_'+str(m)+'_'+str(n)
            else: 
                all_taxi_zero += ' && !taxi_'+str(m)+'_'+str(n)
        env_safe.add('!full_'+str(m)+' && '+all_taxi_zero+' -> X(!full_'+str(m)+')')

    for m in range(num_taxi):
        env_prog.add('!full_'+str(m))

    # Add sys specifications
    # The following three is for eventually spec.
    for n in range(num_req):
        at_least_one_taxi = ''
        for m in range(num_taxi):
            if m == 0:
                at_least_one_taxi += 'taxi_'+str(m)+'_'+str(n)
            else: 
                at_least_one_taxi += ' || taxi_'+str(m)+'_'+str(n)
        sys_safe.add('X(temp_'+str(n)+') <-> (!req_'+str(n)+' && temp_'+str(n)+') || '+ at_least_one_taxi)

    for n in range(num_req):
        sys_prog.add('temp_'+str(n))

    for n in range(num_req):
        sys_init.add('temp_'+str(n))

    # The following eliminate unreasonable behavior.
    for n in range(num_req):
        all_taxi_zero = ''
        for m in range(num_taxi):
            if m == 0:
                all_taxi_zero += '!taxi_'+str(m)+'_'+str(n)
            else: 
                all_taxi_zero += ' && !taxi_'+str(m)+'_'+str(n)
        sys_safe.add('!req_'+str(n)+' -> '+all_taxi_zero)

    for m in range(num_taxi):
        all_taxi_zero = ''
        for n in range(num_req):
            if n == 0:
                all_taxi_zero += '!taxi_'+str(m)+'_'+str(n)
            else: 
                all_taxi_zero += ' && !taxi_'+str(m)+'_'+str(n)
        sys_safe.add('full_'+str(m)+' -> '+ all_taxi_zero)

    # Change the report
    if num_taxi > 1:
        for n in range(num_req):
            for m in range(num_taxi):
                all_taxi_zero = ''
                for k in range(num_taxi):
                    if m != k:
                        if m == 0 and k == 1:
                            all_taxi_zero += '!taxi_'+str(k)+'_'+str(n)
                        elif k == 0:
                            all_taxi_zero += '!taxi_'+str(k)+'_'+str(n)
                        else: 
                            all_taxi_zero += ' && !taxi_'+str(k)+'_'+str(n)
                sys_safe.add('taxi_'+str(m)+'_'+str(n)+' -> '+ all_taxi_zero)

    # Change the report
    if num_req > 1:
        for m in range(num_taxi):
            for n in range(num_req):
                all_taxi_zero = ''
                for k in range(num_req):
                    if n != k:
                        if n == 0 and k == 1:
                            all_taxi_zero += '!taxi_'+str(m)+'_'+str(k)
                        elif k == 0:
                            all_taxi_zero += '!taxi_'+str(m)+'_'+str(k)
                        else: 
                            all_taxi_zero += ' && !taxi_'+str(m)+'_'+str(k)
                sys_safe.add('taxi_'+str(m)+'_'+str(n)+' -> '+ all_taxi_zero)


    specs = spec.GRSpec(env_vars=env_vars, sys_vars=sys_vars, env_init=env_init, sys_init=sys_init,
                   env_safety=env_safe, sys_safety=sys_safe, env_prog=env_prog, sys_prog=sys_prog)

    return specs


specs = spec_gen(3, 2)

ctrl = synth.synthesize('gr1c', specs)

ctrl.states.current = ['Sinit']
ctrl.simulate(inputs_sequence='manual', iterations=50)

# dumpsmach.write_python_case("TuLiPstrategy.py", ctrl,classname="strategy")
# dumpsmach.write_ROS_srv("TuLiP_service.srv", ctrl)