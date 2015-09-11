# The detailed specifications written in this file can be found in the report.
# Otherwise, the strategy_discrete.py in src folder also uses similar specs.
# Or, uncomment the logger, the generated specs will be displayed in the file s_d.log

# Results show that if you give locations in the order of 3,2 or 2,1 or 3,1 it can pick up
# both and then go to destination, but if reverse order, it will pick up and drop off
# one at a time. Also, there must as least be an input !ready once immediately after 
# every pick up, otherwise, it will go back to a fixed location for no reason.

from tulip import spec, synth, transys
import dumpsmach
# import tomatlab

# import logging
# logging.basicConfig(filename='s_d.log',level=logging.DEBUG, filemode='w')
# logger = logging.getLogger(__name__)

def spec_gen(num_req, num_pas):
    env_vars = set()
    env_init = set()
    env_safe = set()
    env_prog = set()
    sys_vars = set()
    sys_init = set()
    sys_safe = set()
    sys_prog = set()

     # Add variables
    for n in range(num_req):
        env_vars.add('req_'+str(n))
        sys_vars.add('loc_'+str(n))
        sys_vars.add('temp_'+str(n))
        for l in range(num_pas):
            sys_vars.add('wait_'+str(l)+'_'+str(n))
            sys_vars.add('seat_'+str(l)+'_'+str(n))

    sys_vars.add('full')
    sys_vars.add('temp')
    sys_vars.add('des')
    env_vars.add('ready')

    # Add env specification
    env_prog.add('ready')

    all_req_zero = ''
    for n in range(num_req):
        if n == 0:
            all_req_zero += '!req_'+str(n)
        else:
            all_req_zero += ' && !req_'+str(n)
    env_safe.add('full -> X('+ all_req_zero +')')

    if num_req > 1:
        for n in range(num_req):
            all_req_zero = ''
            for k in range(num_req):
                if n != k:
                    if n == 0 and k == 1:
                        all_req_zero += '!req_'+str(k)
                    elif k == 0:
                        all_req_zero += '!req_'+str(k)
                    else: 
                        all_req_zero += ' && !req_'+str(k)
            env_safe.add('req_'+str(n)+' -> '+ all_req_zero)

    # Add sys specification

    # @ For our special example, we add a bridge to connect locations and the destination. @
    # TODO: Currently, if you give locations in the order of 3,2 or 2,1 or 3,1 it can pick up
    #       both and then go to destination, but if reverse order, it will pick up and drop off
    #       one at a time. I think if more intermediate locations like bridge are added, in 
    #       theory the taxi should pick up more passengers then go to des?
    sys_vars.add('bridge')
    sys_safe |= {'bridge -> X(!ready -> bridge)'}
    sys_safe |= {'loc_0 -> X(ready -> loc_0 || loc_1 || loc_2 || bridge)'}
    sys_safe |= {'loc_1 -> X(ready -> loc_0 || loc_1 || loc_2 || bridge)'}
    sys_safe |= {'loc_2 -> X(ready -> loc_0 || loc_1 || loc_2 || bridge)'}
    sys_safe |= {'bridge -> X(ready -> loc_0 || loc_1 || loc_2 || bridge || des)'}
    sys_safe |= {'des -> X(ready -> bridge || des)'}
    # @ End: For our special example, we add a bridge to connect locations and the destination. @

    full_def = ''
    for l in range(num_pas):
        at_least_wait = ''
        for n in range(num_req):
            if n == 0:
                at_least_wait += 'wait_'+str(l)+'_'+str(n)
            else:
                at_least_wait += ' || wait_'+str(l)+'_'+str(n)
        at_least_seat = ''
        for n in range(num_req):
            if n == 0:
                at_least_seat += 'seat_'+str(l)+'_'+str(n)
            else:
                at_least_seat += ' || seat_'+str(l)+'_'+str(n)
        at_least_one = at_least_wait+' || '+at_least_seat
        if l == 0:
            full_def += '(' + at_least_one + ')'
        else:
            full_def += ' && ('+ at_least_one + ')'
    sys_safe.add('full <-> ('+ full_def+')')

    if num_req > 1:
        for n in range(num_req):
            all_req_zero = ''
            for k in range(num_req):
                if n != k:
                    if n == 0 and k == 1:
                        all_req_zero += '!loc_'+str(k)
                    elif k == 0:
                        all_req_zero += '!loc_'+str(k)
                    else: 
                        all_req_zero += ' && !loc_'+str(k)
            all_req_zero += '&& !des && !bridge' # For special cases
            sys_safe.add('loc_'+str(n)+' -> '+ all_req_zero)

    all_req_zero = ''
    for n in range(num_req):
        if n == 0:
            all_req_zero += '!loc_'+str(n)
        else:
            all_req_zero += ' && !loc_'+str(n)
    sys_safe.add('des -> '+ all_req_zero + ' && !bridge') # For special cases
    sys_safe.add('bridge -> ' + all_req_zero + ' && !des') # For special cases

    at_least_req = ''
    for n in range(num_req):
        if n == 0:
           at_least_req += 'loc_'+str(n)
        else:
           at_least_req += ' || loc_'+str(n)
    at_least_req += ' || des || bridge' # For special cases
    sys_safe.add(at_least_req)

    if num_req > 1:
        for l in range(num_pas):
            for n in range(num_req):
                all_req_zero = ''
                for k in range(num_req):
                    if n != k:
                        if n == 0 and k == 1:
                            all_req_zero += '!wait_'+str(l)+'_'+str(k)
                        elif k == 0:
                            all_req_zero += '!wait_'+str(l)+'_'+str(k)
                        else: 
                            all_req_zero += ' && !wait_'+str(l)+'_'+str(k)
                sys_safe.add('wait_'+str(l)+'_'+str(n)+' -> '+all_req_zero)

    if num_req > 1:
        for l in range(num_pas):
            for n in range(num_req):
                all_req_zero = ''
                for k in range(num_req):
                    if n != k:
                        if n == 0 and k == 1:
                            all_req_zero += '!seat_'+str(l)+'_'+str(k)
                        elif k == 0:
                            all_req_zero += '!seat_'+str(l)+'_'+str(k)
                        else: 
                            all_req_zero += ' && !seat_'+str(l)+'_'+str(k)
                sys_safe.add('seat_'+str(l)+'_'+str(n)+' -> '+all_req_zero)

    for l in range(num_pas):
        all_wait_zero = ''
        for n in range(num_req):
            if n == 0:
                all_wait_zero += '!wait_'+str(l)+'_'+str(n)
            else:
                all_wait_zero += ' && !wait_'+str(l)+'_'+str(n)
        all_seat_zero = ''
        for n in range(num_req):
            if n == 0:
                all_seat_zero += '!seat_'+str(l)+'_'+str(n)
            else:
                all_seat_zero += ' && !seat_'+str(l)+'_'+str(n)
        at_least_one = '('+all_wait_zero+') || ('+all_seat_zero+')'
        sys_safe.add(at_least_one)

    for n in range(num_req):
        sys_safe.add('loc_'+str(n)+' -> X(!ready -> loc_'+str(n)+')')

    sys_safe.add('des -> X(!ready -> des)')

    for l in range(num_pas):
        for n in range(num_req):
            sys_init.add('!seat_'+str(l)+'_'+str(n))

    sys_init.add('des')

    for n in range(num_req):
        for l in range(num_pas):
            sys_vars.add('last_wait_'+str(l)+'_'+str(n))
            sys_safe.add('X(last_wait_'+str(l)+'_'+str(n)+') <-> wait_'+str(l)+'_'+str(n))
            sys_init.add('!last_wait_'+str(l)+'_'+str(n))

    for n in range(num_req):
        at_least_one = ''
        for l in range(num_pas):
            if l == 0:
                at_least_one += '(!last_wait_'+str(l)+'_'+str(n)+ ' && '+ 'wait_'+str(l)+'_'+str(n)+')'
            else:
                at_least_one += ' || (!last_wait_'+str(l)+'_'+str(n)+ ' && '+ 'wait_'+str(l)+'_'+str(n)+')'
        sys_safe.add('req_'+str(n)+ ' -> ('+at_least_one+')')

    if num_pas > 1:
        for n in range(num_req):
            for l in range(num_pas):
                all_no_change = ''
                for k in range(num_pas):
                    if l != k:
                        if l == 0 and k == 1:
                            all_no_change += '(!last_wait_'+str(k)+'_'+str(n)+ ' -> !wait_'+str(k)+'_'+str(n)+')'
                        elif k == 0:
                            all_no_change += '(!last_wait_'+str(k)+'_'+str(n)+ ' -> !wait_'+str(k)+'_'+str(n)+')'
                        else: 
                            all_no_change += ' && (!last_wait_'+str(k)+'_'+str(n)+ ' -> !wait_'+str(k)+'_'+str(n)+')'
                sys_safe.add('(!last_wait_'+str(l)+'_'+str(n)+ ' && '+ 'wait_'+str(l)+'_'+str(n)+') -> '+all_no_change)

    for l in range(num_pas):
        for n in range(num_req):
            sys_safe.add('wait_'+str(l)+'_'+str(n)+' -> X(!loc_'+str(n)+' -> wait_'+str(l)+'_'+str(n)+')')

    for l in range(num_pas):
        for n in range(num_req):
            sys_safe.add('wait_'+str(l)+'_'+str(n)+' -> X(loc_'+str(n)+' -> !wait_'+str(l)+'_'+str(n)+' && '+'seat_'+str(l)+'_'+str(n)+')')

    for l in range(num_pas):
        all_wait_zero = ''
        all_req_zero = ''
        for n in range(num_req):
            if n == 0:
                all_wait_zero += '!wait_'+str(l)+'_'+str(n)
                all_req_zero += '!req_'+str(n)
            else:
                all_wait_zero += ' && !wait_'+str(l)+'_'+str(n)
                all_req_zero += ' && !req_'+str(n)
        sys_safe.add('('+all_wait_zero+') -> X('+all_req_zero+' -> '+ all_wait_zero +')')

    for l in range(num_pas):
        for n in range(num_req):
            sys_safe.add('seat_'+str(l)+'_'+str(n)+' -> X(!des -> seat_'+str(l)+'_'+str(n)+')')

    for l in range(num_pas):
        at_least_seat = ''
        all_seat_zero = ''
        for n in range(num_req):
            if n == 0:
                at_least_seat += 'seat_'+str(l)+'_'+str(n)
                all_seat_zero += '!seat_'+str(l)+'_'+str(n)
            else:
                at_least_seat += ' || seat_'+str(l)+'_'+str(n)
                all_seat_zero += ' && !seat_'+str(l)+'_'+str(n)
        sys_safe.add('('+at_least_seat+') -> X(des -> ('+all_seat_zero+'))')

    for l in range(num_pas):
        all_seat_zero = ''
        all_no_reach = ''
        for n in range(num_req):
            if n == 0:
                all_seat_zero += '!seat_'+str(l)+'_'+str(n)
                all_no_reach += '!(wait_'+str(l)+'_'+str(n)+' && X(loc_'+str(n)+'))'
            else:
                all_seat_zero += ' && !seat_'+str(l)+'_'+str(n)
                all_no_reach += ' && !(wait_'+str(l)+'_'+str(n)+' && X(loc_'+str(n)+'))'
        sys_safe.add('('+all_seat_zero+') -> (('+all_no_reach+') -> X('+all_seat_zero+'))')

    # Two eventually constraints
    for n in range(num_req):
        all_wait_zero = ''
        for l in range(num_pas):
            if l == 0:
                all_wait_zero += '!wait_'+str(l)+'_'+str(n)
            else:
                all_wait_zero += ' && !wait_'+str(l)+'_'+str(n)
        sys_safe.add('X(temp_'+str(n)+') <-> (('+all_wait_zero+' && temp_'+str(n)+') || loc_'+str(n)+')')
        sys_prog.add('temp_'+str(n))
        sys_init.add('temp_'+str(n))

    all_seat_zero = ''
    for l in range(num_pas):
        for n in range(num_req):
            if l == 0 and n == 0:
                all_seat_zero += '!seat_'+str(l)+'_'+str(n)
            else:
                all_seat_zero += ' && !seat_'+str(l)+'_'+str(n)
    sys_safe.add('X(temp) <-> (('+all_seat_zero+' && temp) || des)')
    sys_prog.add('temp')
    sys_init.add('temp')

    specs = spec.GRSpec(env_vars, sys_vars, env_init, sys_init,
                   env_safe, sys_safe, env_prog, sys_prog)
    return specs

specs = spec_gen(3, 2)

ctrl = synth.synthesize('gr1c', specs)

# either select current state before simulation
# ctrl.states.current = ['Sinit']
# ctrl.simulate(inputs_sequence='manual', iterations=50)


# dumpsmach.write_python_case("strategy_class.py", ctrl,classname="strategy")
# dumpsmach.write_ROS_srv("strategy_srv.srv", ctrl)

# tomatlab.write_matlab_case('strategy.m', ctrl, classname="strategy")