% Please first remember to rosinit.

classdef Navigation_2 < handle
    
    properties
        my_sub
        my_sub_2
        my_pub
        my_pub_2
        taxi_sys
        loc
    end
    
    methods
        function obj = Navigation_2()
            % Constructor of Navigation level.
            obj.taxi_sys = taxi_navigation();
            obj.taxi_sys.x0 = [1; 0; 1; 0];
            obj.taxi_sys = obj.taxi_sys.addBoundary([0, 0], 5);
            obj.taxi_sys.objFuncVersion = 1;
            obj.taxi_sys.lambda_rho = 0.1;
            obj.loc = struct();
            obj.loc.loc_0 = [0.5, 3];
            obj.loc.loc_1 = [0.5, 0.5];
            obj.loc.loc_2 = [1.5, 1];
            obj.loc.loc_3 = [4.5, 3];
            obj.loc.loc_4 = [3.5, 2];
            obj.my_pub = rospublisher('/Matlab_output_1', 'strategy_discrete/Matlab_output');
            obj.my_pub_2 = rospublisher('/position_1', 'strategy_discrete/position');
            obj.my_sub = rossubscriber('/Matlab_input_1', @obj.callback);
            obj.my_sub_2 = rossubscriber('/disturbance_signal_1', @obj.callback_2);
            
        end
        
        function callback(obj, ~, data)
            obj.taxi_sys = obj.taxi_sys.deleteSpec();
            if data.Loc == 0
                obj.taxi_sys = obj.taxi_sys.addObjective_alw([0 8],1,obj.loc.loc_0, 0.5);
            elseif data.Loc == 1
                obj.taxi_sys = obj.taxi_sys.addObjective_alw([0 8],1,obj.loc.loc_1, 0.5);
            elseif data.Loc == 2
                obj.taxi_sys = obj.taxi_sys.addObjective_alw([0 8],1,obj.loc.loc_2, 0.5);
            elseif data.Loc == 3
                obj.taxi_sys = obj.taxi_sys.addObjective_alw([0 8],1,obj.loc.loc_3, 0.5);
            elseif data.Loc == 4
                obj.taxi_sys = obj.taxi_sys.addObjective_alw([0 8],1,obj.loc.loc_4, 0.5);
            else
                display('Location not assigned in the map.')
            end
            obj.taxi_sys = obj.taxi_sys.addSpec('alw_[0, Inf] (w1(t)>0.5 => x2(t)<0.1)');
            obj.taxi_sys = obj.taxi_sys.addSpec('alw_[0, Inf] (w2(t)>0.5 => x4(t)<0.1)');
            obj.taxi_sys = obj.taxi_sys.addSpec('alw_[0, Inf] (w3(t)>0.5 => x2(t)>-0.1)');
            obj.taxi_sys = obj.taxi_sys.addSpec('alw_[0, Inf] (w4(t)>0.5 => x4(t)>-0.1)');
            obj.taxi_sys.controller = obj.taxi_sys.get_controller();
            [obj.taxi_sys, succeed] = obj.taxi_sys.run_deterministic(obj.taxi_sys.controller, obj.my_pub_2);
            if (succeed)
                signal = rosmessage(obj.my_pub);
                signal.Succeed = 1;
                send(obj.my_pub, signal);
            else
                signal = rosmessage(obj.my_pub);
                signal.Succeed = 0;
                send(obj.my_pub, signal);
            end
        end
        
        function callback_2(obj, ~, data)
            % Because Matlab is single threaded, is it going to wait
            % forever, without the run_deterministic ever going forward.
            % while obj.taxi_sys.getmutex()==2
            % end
            % This might be unnecessary since Matlab is single threaded.
            % obj.taxi_sys = obj.taxi_sys.setmutex(1);
            % The following is unnecessary.
            % obj.taxi_sys.current_w = [data.w1 ; data.w2 ; data.w3 ; data.w4];
            str = sprintf('Receive update for W with ID = %d', data.ID);
            display(str);
            obj.taxi_sys.current_w_ID = data.ID;
            obj.taxi_sys.Wref_discrete(:, obj.taxi_sys.current_w_ID) = [data.W1 ; data.W2 ; data.W3 ; data.W4];
            for iwx = 1:obj.taxi_sys.nw
                obj.taxi_sys.Wref(iwx,:) = interp1(obj.taxi_sys.time_discrete, obj.taxi_sys.Wref_discrete(iwx,:), obj.taxi_sys.time);
            end
            display('Finish updating taxi_navigation.');
            % obj.taxi_sys = obj.taxi_sys.setmutex(0);
        end
        
    end
    
end

                    
                    
                
            
            


