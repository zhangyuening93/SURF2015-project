close all;
clear;

sys = taxi_navigation();

%sys = sys.addSpec(strcat('alw_[0, Inf]( ev_[0, 10] (', target_1, ') )')); %and ( ev_[8, 16] (', target_2, ') ) )' ));
%sys = sys.addSpec(strcat('alw_[0, Inf]( ( ev_[0, 10] (', target_1, ') ) and ( ev_[10, 20] (', target_2, ') ) )' ));
%sys = sys.addSpec(strcat('alw_[0, Inf] ev_[10, 20] (', target_2, ')'));

%sys = sys.addSpec('alw_[0, Inf] (ev_[0, 8] (x1(t) > 10 and x1(t) < 12.5 and x2(t) > 17.5 and x2(t) < 20)) and (ev_[0, 8] (x1(t) > 12.5 and x1(t) < 15 and x2(t) > 10 and x2(t) < 12.5))');
%sys = sys.addSpec('alw_[0, Inf] ev_[0, 8] (x1(t) > 8 and x1(t) < 10 and x2(t) > 17.5 and x2(t) < 20)');
%sys = sys.addSpec('alw_[0, Inf] ev_[0, 8] (x1(t) > 12.5 and x1(t) < 15 and x2(t) > 10 and x2(t) < 12.5)');

% sys = sys.addObjective_alw([0 8],1,[10 17.5], [12.5 20]);
% sys = sys.addObjective_alw([0 8],1,[12.5 10], [15 12.5]);

%sys.stl_list{1} = strcat('ev_[0, 10] (', target_1, ')');
%sys.stl_list{2} = strcat('ev_[10, 20] (', target_2, ')');
%sys.stl_list{2} = getObstacle([2 3], [3 3.5]);
%sys.stl_list{2} = getObstacle([2 2], [5 3]);
%sys.stl_list{2} = getObstacle([2 3], [5 4]);

% sys.objFuncVersion = 1;
% sys.lambda_rho = 0.1;



%sys.controller = sys.get_controller();
%[sys, succeed] = sys.run_deterministic(sys.controller);

%sys = sys.addObjective([0,15],1,[7 9],2);
% sys = sys.addBoundary([-5 -5], 30);
%sys = sys.addObstacle([3 4], 3);



%% This is for testing if adding disturbance will work.
sys = sys.addBoundary([0, 0], 5);
sys = sys.addObjective_alw([0, 20], 1, [3.5, 3.5], 0.5);

Wref = zeros(4, 121);
% Wref(1, :) = 5;
% Wref(1, 5: 15 ) = 2.4;
Wref(1, 5: 15) = 1;
% Wref(1, 20: 34) = 1;
Wref(2, :) = 3.4;
Wref(4, 44: 60) = 1;
sys.Wref = Wref;


sys.objFuncVersion = 1;
% sys.lambda_rho = 1;

sys.u_lb = [-2; -2];
sys.u_ub = [2; 2];

% Note that the following actually will not work. Wref needs to be
% w(t)*location
% sys = sys.addSpec('alw_[0, Inf] (x1(t) <= (x1(t)+0.1)*w1(t) or x1(t) >= (x1(t)+ 0.6)*w1(t) or x2(t) <= (x2(t)-0.3)*w1(t) or x2(t) >= (x2(t)+0.3)*w1(t))');
% sys = sys.addSpec('alw_[0, Inf] (x1(t) <= (x1(t)-0.6)*w2(t) or x1(t) >= (x1(t)- 0.1)*w2(t) or x2(t) <= (x2(t)-0.3)*w2(t) or x2(t) >= (x2(t)+0.3)*w2(t))');
% sys = sys.addSpec('alw_[0, Inf] (x1(t) <= (x1(t)-0.3)*w3(t) or x1(t) >= (x1(t)+ 0.3)*w3(t) or x2(t) <= (x2(t)+0.1)*w3(t) or x2(t) >= (x2(t)+0.6)*w3(t))');
% sys = sys.addSpec('alw_[0, Inf] (x1(t) <= (x1(t)-0.3)*w4(t) or x1(t) >= (x1(t)+ 0.3)*w4(t) or x2(t) <= (x2(t)-0.6)*w4(t) or x2(t) >= (x2(t)-0.1)*w4(t))');

%sys = sys.addSpec('alw_[0, Inf] ( w1(t)> 0.5 => x1(t)~=2.4 and x2(t)~=2.4)');
%sys = sys.addSpec('alw_[0, Inf] (w4(t)>0.5 => ev_[0,15] (x1(t)<0.5 and x2(t)<0.5) )');
% sys = sys.addSpec('alw_[0, Inf] (x1(t) <= w1(t))');
% sys = sys.addSpec('alw_[0, Inf] (x2(t) <= w3(t))');
% sys = sys.addSpec('alw_[0, Inf] (x2(t) >= w4(t))');

sys.controller = sys.get_controller();
[sys, succeed] = sys.run_deterministic(sys.controller);

display(succeed);


% succeed_2 = model_checker(sys);
% display(succeed_2);


