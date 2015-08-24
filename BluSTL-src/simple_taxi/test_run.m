clear;
close all;

%% Targets
loc_0 = [0 0];
loc_1 = [1 0];
loc_2 = [2 0];
loc_3 = [0 1];
loc_4 = [1 1];
des = [2 1];
target = getRandLoc(4, loc_0);
string = strcat('ev_[0,5] (',target,')');

%% Instantiate
controller = taxi_planning_discreet();
counter = taxi_planning_counter();
sys = taxi_navigation();

%% Objects
sys = sys.addObstacle([0.3 0.8], [1.4 1.1]);
sys = sys.addObstacle([1.8 0.3],[2 0.7]);

%% Boundary
sys = sys.addBoundary([-0.1 -0.1], [3.1 2.1]);

%% Control Section Starts.
display('Enter q to quit controller.');
succeed = 1;
req_0 = '0';
req_1 = '0';
req_2 = '0';

while (succeed == 1)
    prompt = 'What is [req_0, req_1, req_2]? Empty means the requests do not change.\n';
    x = input(prompt,'s');
    if (x == 'q')
        break
    end
    if (~isempty(x))
        x = strsplit(x,',');
        req_0 = x(1);
        req_1 = x(2);
        req_2 = x(3);
    end
    tic;
    controller = controller.move(req_0, req_1, req_2, num2str(counter.full));
    if (controller.loc_0 == 1)
        target = getRandLoc(4,loc_0);
        display('Location is 0');
    elseif (controller.loc_1 == 1)
        target = getRandLoc(4,loc_1);
        display('Location is 1');
    elseif (controller.loc_2 == 1)
        target = getRandLoc(4,loc_2);
        display('Location is 2');
    elseif (controller.loc_3 == 1)
        target = getRandLoc(4,loc_3);
        display('Location is 3');
    elseif (controller.loc_4 == 1)
        target = getRandLoc(4,loc_4);
        display('Location is 4');
    elseif (controller.des == 1)
        target = getRandLoc(4,des);
        display('Location is 5');
        display('Reaches destination.');
    end
    if (controller.pick == 1)
        display('Pick up.')
    end
    env_action = 'none';
    if (controller.pick == 1)
        env_action = 'pick';
    elseif (controller.des == 1)
        env_action = 'des';
    end
    counter = counter.move(env_action);
    if (counter.full == 1)
        display('Taxi is full now.');
    end
    toc;
    string = strcat('ev_[0,5] (',target,')');
    sys = sys.deleteSpec();
    sys = sys.addSpec(string);
    tic;
    sys.controller = sys.get_controller();
    toc;
    [sys, succeed] = sys.run_deterministic(sys.controller);
end

display('control section ends.')
