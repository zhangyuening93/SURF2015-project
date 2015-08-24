classdef taxi_navigation < STLC_lti
    
    properties
        boundary
        obstacle
        objective_alw_ev
        objective_ev
    end
    
    properties % Please delete: This is for the automaton script
        objFuncVersion
    end
    
    properties (Access = private)
        specIndex
    end
    
    properties % For updating disturbance signal
        % current_w
        current_w_ID
        mutex % 0 is none. 1 is updating value. 2 is using value.
        Wref_discrete
        time_discrete
    end
    
    methods 
        function sys = taxi_navigation()
            A = [0 1 0 0 ;0 0 0 0; 0 0 0 1; 0 0 0 0];
            Bu = [ 0 0; 1 0;0 0; 0 1];
            %Bw = [0 ; 0];
            Bw = zeros(4, 4);

            C = zeros(1,4);
            Du = zeros(1,2);
            %Dw = 0;
            Dw = zeros(1, 4);

            sys = sys@STLC_lti(A,Bu,Bw,C,Du,Dw); 

            sys.x0 = [0.1; 0 ; 0.1; 0];
            % If change the maxi time, also change sys.time_discrete
            sys.time = 0:0.2:15;
            sys.ts = 0.2;
            sys.L = 10;
            sys.nb_stages = 1;
            
            % Please delete: This is for the automaton script
            sys.objFuncVersion = 1;

            % This is the parameters for taxi problem.
            %sys.u_lb= [-1 ; -1];
            %sys.u_ub= [1 ; 1];
            %sys.u_delta = [-10 ; 10];
            
            sys.u_lb= [-2 ; -2];
            sys.u_ub= [2 ; 2];
            
            sys.time_discrete = 0:sys.ts:15;
            sys.Wref_discrete = zeros(size(Bw,2), size(sys.time_discrete,2));
            sys.Wref = zeros(size(Bw,2), size(sys.time,2));
            sys.current_w_ID = 0;

        end
        
        function Obj = addSpec(Obj, specs)
            num = numel(Obj.stl_list)+1;
            Obj.stl_list{num} = specs;
            if isempty(Obj.specIndex)
                Obj.specIndex(1) = num;
            else
                Obj.specIndex(end+1) = num;
            end
        end
        
        function Obj = addObjective_alw(Obj, time_range, varargin)
            % alw_[0, Inf] ev_[<time_range>] <objective>.
            % time_range is [t0, t1].
            % if num(arg)=2, n=divider, [x1,x2] is the start location, l = 1.
            % if num(arg)=3, n=divider, [x1,x2] is the start location, l is the range.
            % if num(arg)=3, n=divider, [x1,x2] is the start location, [x3,x4] is the end location.
            num = numel(Obj.stl_list)+1;
            [specs, poly] = getRandLoc(varargin{:});
            specs = strcat('alw_[0, Inf] ev_[', num2str(time_range(1)),', ', num2str(time_range(2)),'] (', specs,')');
            Obj.stl_list{num} = specs;
            if isempty(Obj.specIndex)
                Obj.specIndex(1) = num;
            else
                Obj.specIndex(end+1) = num;
            end
            Obj.objective_alw_ev{numel(Obj.objective_alw_ev)+1} = poly;
        end
        
        function Obj = addObjective(Obj, time_range, varargin)
            % ev_[<time_range>] <objective>.
            % time_range is [t0, t1].
            % if num(arg)=2, n=divider, [x1,x2] is the start location, l = 1.
            % if num(arg)=3, n=divider, [x1,x2] is the start location, l is the range.
            % if num(arg)=3, n=divider, [x1,x2] is the start location, [x3,x4] is the end location.
            num = numel(Obj.stl_list)+1;
            [specs, poly] = getRandLoc(varargin{:});
            specs = strcat('ev_[', num2str(time_range(1)),', ', num2str(time_range(2)),'] (', specs,')');
            Obj.stl_list{num} = specs;
            if isempty(Obj.specIndex)
                Obj.specIndex(1) = num;
            else
                Obj.specIndex(end+1) = num;
            end
            Obj.objective_ev{numel(Obj.objective_ev)+1} = poly;
        end
        
        function Obj = deleteSpec(Obj)
            %delete all objective specs.
            while ~isempty(Obj.specIndex)
                Obj.stl_list(Obj.specIndex(end)) = [];
                Obj.specIndex(end) = [];
            end
            Obj.objective_ev = [];
            Obj.objective_alw_ev = [];
            % changed for Wref.
            Obj.Wref_discrete(:,:) = 0;
            Obj.Wref(:,:) = 0;
            Obj.current_w_ID = 0;
        end
        
        function Obj = addObstacle(Obj,varargin)
            % get obstacle for class.
            % if [x1 y1], [x2 y2] is the start location and end location of the obstacle.
            % if [x1 y1], l is the start location and the range.
            if numel(varargin) == 2
                x = varargin{1};
                x_2 = varargin{2};
                if size(x_2,2) == 2
                    Obj.obstacle{numel(Obj.obstacle)+1} = [x(1) x_2(1) x(2) x_2(2)];
                    loc = strcat('x1(t)<',num2str(x(1)),' or x1(t)>', num2str(x_2(1)), ' or x3(t)<', num2str(x(2)),' or x3(t)>', num2str(x_2(2)));
                    Obj.stl_list{numel(Obj.stl_list)+1} = strcat('alw_[0, Inf] (', loc,')');
                else
                    step = x_2;
                    x_2 = [x(1)+step x(2)+step];
                    Obj.obstacle{numel(Obj.obstacle)+1} = [x(1) x_2(1) x(2) x_2(2)];
                    loc = strcat('x1(t)<',num2str(x(1)),' or x1(t)>', num2str(x_2(1)), ' or x3(t)<', num2str(x(2)),' or x3(t)>', num2str(x_2(2)));
                    Obj.stl_list{numel(Obj.stl_list)+1} = strcat('alw_[0, Inf] (', loc,')');
                end
            else
                display('Other options are not implemented yet.')
            end
        end
        
        function Obj = addBoundary(Obj,varargin)
        % get obstacle for class.
        % if [x1 y1], [x2 y2] is the start location and end location of the obstacle.
        % if [x1 y1], l is the start location and the range.
            if numel(varargin) == 2
                x = varargin{1};
                x_2 = varargin{2};
                if size(x_2,2) == 2
                    Obj.boundary = [x(1) x_2(1) x(2) x_2(2)];
                    loc = strcat('x1(t)>',num2str(x(1)),' and x1(t)<', num2str(x_2(1)), ' and x3(t)>', num2str(x(2)),' and x3(t)<', num2str(x_2(2)));
                    Obj.stl_list{numel(Obj.stl_list)+1} = strcat('alw_[0, Inf] (', loc,')');
                else
                    step = x_2;
                    x_2 = [x(1)+step x(2)+step];
                    Obj.boundary = [x(1) x_2(1) x(2) x_2(2)];
                    loc = strcat('x1(t)>',num2str(x(1)),' and x1(t)<', num2str(x_2(1)), ' and x3(t)>', num2str(x(2)),' and x3(t)<', num2str(x_2(2)));
                    Obj.stl_list{numel(Obj.stl_list)+1} = strcat('alw_[0, Inf] (', loc,')');
                end
            else
                display('Other options are not implemented yet.')
            end
        end
        
        % Overload the STL_lti class.
        function [Sys, flag, params] = run_deterministic(Sys, controller, publisher)
            [Sys, flag, params] = STLC_run_deterministic(Sys, controller, publisher);
        end
        
        function value_mutex = getmutex(Obj)
            value_mutex = Obj.mutex;
        end
        
        function Obj = setmutex(Obj, value)
            Obj.mutex = value;
        end
        
        function [value_current_w, ID] = getW(Obj)
            value_current_w = Obj.Wref;
            ID = Obj.current_w_ID;
        end
        
        function run_test(Obj, publisher)
            iter = 0;
            while iter<20
                display(iter);
                my_msg = rosmessage(publisher);
                my_msg.X = iter/4;
                my_msg.Y = iter/5;
                my_msg.ID = iter;
                send(publisher, my_msg);
                
                [W, ID] = Obj.getW();
                while ID < iter
                    str = sprintf('%d < %d now.',ID,iter);
                    display(str)
                    display('Run_test is waiting for update.')
                    pause(1);
                    [W, ID] = Obj.getW();
                    display('Update result is following:');
                    display(W);
                    display(ID);
                end
                display('Final step result is:')
                display(W);
                display(ID);
                iter = iter + 1;
            end
        end
    end
end