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
    
    methods 
        function sys = taxi_navigation()
            A = [0 0 ;0 0];
            Bu = [1 0; 0 1];
            %Bw = [0 ; 0];
            Bw = zeros(2, 4);


            C = [0 0];
            Du = [0 0];
            %Dw = 0;
            Dw = zeros(1, 4);

            sys = sys@STLC_lti(A,Bu,Bw,C,Du,Dw); 

            sys.x0 = [0.1 ; 0.1];
            sys.time = 0:0.2:24;
            sys.ts = 0.2;
            sys.L = 10;
            sys.nb_stages = 1;
            
            % Please delete: This is for the automaton script
            sys.objFuncVersion = 1;

            % This is the parameters for taxi problem.
            %sys.u_lb= [-1 ; -1];
            %sys.u_ub= [1 ; 1];
            %sys.u_delta = [-10 ; 10];
            
            sys.u_lb= [-20 ; -20];
            sys.u_ub= [20 ; 20];

        end
        
        function obj = addSpec(obj, specs)
            num = numel(obj.stl_list)+1;
            obj.stl_list{num} = specs;
            if isempty(obj.specIndex)
                obj.specIndex(1) = num;
            else
                obj.specIndex(end+1) = num;
            end
        end
        
        function obj = addObjective_alw(obj, time_range, varargin)
            % alw_[0, Inf] ev_[<time_range>] <objective>.
            % time_range is [t0, t1].
            % if num(arg)=2, n=divider, [x1,x2] is the start location, l = 1.
            % if num(arg)=3, n=divider, [x1,x2] is the start location, l is the range.
            % if num(arg)=3, n=divider, [x1,x2] is the start location, [x3,x4] is the end location.
            num = numel(obj.stl_list)+1;
            [specs, poly] = getRandLoc(varargin{:});
            specs = strcat('alw_[0, Inf] ev_[', num2str(time_range(1)),', ', num2str(time_range(2)),'] (', specs,')');
            obj.stl_list{num} = specs;
            if isempty(obj.specIndex)
                obj.specIndex(1) = num;
            else
                obj.specIndex(end+1) = num;
            end
            obj.objective_alw_ev{numel(obj.objective_alw_ev)+1} = poly;
        end
        
        function obj = addObjective(obj, time_range, varargin)
            % ev_[<time_range>] <objective>.
            % time_range is [t0, t1].
            % if num(arg)=2, n=divider, [x1,x2] is the start location, l = 1.
            % if num(arg)=3, n=divider, [x1,x2] is the start location, l is the range.
            % if num(arg)=3, n=divider, [x1,x2] is the start location, [x3,x4] is the end location.
            num = numel(obj.stl_list)+1;
            [specs, poly] = getRandLoc(varargin{:});
            specs = strcat('ev_[', num2str(time_range(1)),', ', num2str(time_range(2)),'] (', specs,')');
            obj.stl_list{num} = specs;
            if isempty(obj.specIndex)
                obj.specIndex(1) = num;
            else
                obj.specIndex(end+1) = num;
            end
            obj.objective_ev{numel(obj.objective_ev)+1} = poly;
        end
        
        function obj = deleteSpec(obj)
            %delete all objective specs.
            while ~isempty(obj.specIndex)
                obj.stl_list(obj.specIndex(end)) = [];
                obj.specIndex(end) = [];
            end
            obj.objective_ev = [];
            obj.objective_alw_ev = [];
        end
        
        function obj = addObstacle(obj,varargin)
            % get obstacle for class.
            % if [x1 y1], [x2 y2] is the start location and end location of the obstacle.
            % if [x1 y1], l is the start location and the range.
            if numel(varargin) == 2
                x = varargin{1};
                x_2 = varargin{2};
                if size(x_2,2) == 2
                    obj.obstacle{numel(obj.obstacle)+1} = [x(1) x_2(1) x(2) x_2(2)];
                    loc = strcat('x1(t)<',num2str(x(1)),' or x1(t)>', num2str(x_2(1)), ' or x2(t)<', num2str(x(2)),' or x2(t)>', num2str(x_2(2)));
                    obj.stl_list{numel(obj.stl_list)+1} = strcat('alw_[0, Inf] (', loc,')');
                else
                    step = x_2;
                    x_2 = [x(1)+step x(2)+step];
                    obj.obstacle{numel(obj.obstacle)+1} = [x(1) x_2(1) x(2) x_2(2)];
                    loc = strcat('x1(t)<',num2str(x(1)),' or x1(t)>', num2str(x_2(1)), ' or x2(t)<', num2str(x(2)),' or x2(t)>', num2str(x_2(2)));
                    obj.stl_list{numel(obj.stl_list)+1} = strcat('alw_[0, Inf] (', loc,')');
                end
            else
                display('Other options are not implemented yet.')
            end
        end
        
        function obj = addBoundary(obj,varargin)
        % get obstacle for class.
        % if [x1 y1], [x2 y2] is the start location and end location of the obstacle.
        % if [x1 y1], l is the start location and the range.
            if numel(varargin) == 2
                x = varargin{1};
                x_2 = varargin{2};
                if size(x_2,2) == 2
                    obj.boundary = [x(1) x_2(1) x(2) x_2(2)];
                    loc = strcat('x1(t)>',num2str(x(1)),' and x1(t)<', num2str(x_2(1)), ' and x2(t)>', num2str(x(2)),' and x2(t)<', num2str(x_2(2)));
                    obj.stl_list{numel(obj.stl_list)+1} = strcat('alw_[0, Inf] (', loc,')');
                else
                    step = x_2;
                    x_2 = [x(1)+step x(2)+step];
                    obj.boundary = [x(1) x_2(1) x(2) x_2(2)];
                    loc = strcat('x1(t)>',num2str(x(1)),' and x1(t)<', num2str(x_2(1)), ' and x2(t)>', num2str(x(2)),' and x2(t)<', num2str(x_2(2)));
                    obj.stl_list{numel(obj.stl_list)+1} = strcat('alw_[0, Inf] (', loc,')');
                end
            else
                display('Other options are not implemented yet.')
            end
        end
        
    end
end