% Please first remember to rosinit.

classdef Navigation < handle
    
    properties
        my_sub
        my_sub_2
        my_pub
        my_pub_2
        taxi_sys
        loc
    end
    
    methods
        function Obj = Navigation()
            % Constructor of Navigation level.
            Obj.taxi_sys = taxi_navigation();
            Obj.taxi_sys.x0 = [3.8; 0; 2.3; 0];
            Obj.taxi_sys = Obj.taxi_sys.addBoundary([0, 0], 5);
            Obj.taxi_sys.objFuncVersion = 1;
            Obj.taxi_sys.lambda_rho = 0.1;
            Obj.loc = struct();
            Obj.loc.loc_0 = [0.5, 3];
            Obj.loc.loc_1 = [0.5, 0.5];
            Obj.loc.loc_2 = [1.5, 1];
            Obj.loc.loc_3 = [4.5, 3];
            Obj.loc.loc_4 = [3.5, 2];
            Obj.my_pub = rospublisher('/Matlab_output_0', 'strategy_discrete/Matlab_output');
            Obj.my_pub_2 = rospublisher('/position_0', 'strategy_discrete/position');
            Obj.my_sub = rossubscriber('/Matlab_input_0', @Obj.callback);
            Obj.my_sub_2 = rossubscriber('/disturbance_signal_0', @Obj.callback_2);
            
        end
        
        function callback(Obj, ~, data)
            Obj.taxi_sys = Obj.taxi_sys.deleteSpec();
            if data.Loc == 0
                Obj.taxi_sys = Obj.taxi_sys.addObjective_alw([0 8],1,Obj.loc.loc_0, 0.5);
            elseif data.Loc == 1
                Obj.taxi_sys = Obj.taxi_sys.addObjective_alw([0 8],1,Obj.loc.loc_1, 0.5);
            elseif data.Loc == 2
                Obj.taxi_sys = Obj.taxi_sys.addObjective_alw([0 8],1,Obj.loc.loc_2, 0.5);
            elseif data.Loc == 3
                Obj.taxi_sys = Obj.taxi_sys.addObjective_alw([0 8],1,Obj.loc.loc_3, 0.5);
            elseif data.Loc == 4
                Obj.taxi_sys = Obj.taxi_sys.addObjective_alw([0 8],1,Obj.loc.loc_4, 0.5);
            else
                display('Location not assigned in the map.')
            end
            Obj.taxi_sys = Obj.taxi_sys.addSpec('alw_[0, Inf] (w1(t)>0.5 => x2(t)<0.1)');
            Obj.taxi_sys = Obj.taxi_sys.addSpec('alw_[0, Inf] (w2(t)>0.5 => x4(t)<0.1)');
            Obj.taxi_sys = Obj.taxi_sys.addSpec('alw_[0, Inf] (w3(t)>0.5 => x2(t)>-0.1)');
            Obj.taxi_sys = Obj.taxi_sys.addSpec('alw_[0, Inf] (w4(t)>0.5 => x4(t)>-0.1)');
            %Obj.taxi_sys.controller = Obj.taxi_sys.get_controller();
            %[Obj.taxi_sys, succeed] = Obj.taxi_sys.run_deterministic(Obj.taxi_sys.controller, Obj.my_pub_2);
            Obj.taxi_sys.run_test(Obj.my_pub_2);
            succeed = 1;
            if (succeed)
                signal = rosmessage(Obj.my_pub);
                signal.Succeed = 1;
                send(Obj.my_pub, signal);
            else
                signal = rosmessage(Obj.my_pub);
                signal.Succeed = 0;
                send(Obj.my_pub, signal);
            end
        end
        
        function callback_2(Obj, ~, data)
            % Because Matlab is single threaded, is it going to wait
            % forever, without the run_deterministic ever going forward.
            % while Obj.taxi_sys.getmutex()==2
            % end
            % This might be unnecessary since Matlab is single threaded.
            % Obj.taxi_sys = Obj.taxi_sys.setmutex(1);
            % The following is unnecessary.
            % Obj.taxi_sys.current_w = [data.w1 ; data.w2 ; data.w3 ; data.w4];
            str = sprintf('Receive update for W with ID = %d', data.ID);
            display(str);
            Obj.taxi_sys.current_w_ID = data.ID;
            Obj.taxi_sys.Wref_discrete(:, Obj.taxi_sys.current_w_ID+1) = [data.W1 ; data.W2 ; data.W3 ; data.W4];
            for iwx = 1:Obj.taxi_sys.nw
                Obj.taxi_sys.Wref(iwx,:) = interp1(Obj.taxi_sys.time_discrete, Obj.taxi_sys.Wref_discrete(iwx,:), Obj.taxi_sys.time);
            end
            display('Finish updating taxi_navigation.');
            % Obj.taxi_sys = Obj.taxi_sys.setmutex(0);
        end
        
    end
    
end

                    
                    
                
            
            


