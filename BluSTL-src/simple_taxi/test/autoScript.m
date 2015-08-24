
num_example = 5;
num_objFunc = 7;
num_env = 3;

%alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T']
line = 2;
for i = 1:num_example
    temp = strcat('C', num2str(line),':J',num2str(line));
    temp = xlsread('BluSTL report.xlsx',temp);
    temp = double(temp);
    x1 = temp(1);
    x2 = temp(2);
    y1 = temp(3);
    y2 = temp(4);
    x1_2 = temp(5);
    x2_2 = temp(6);
    y1_2 = temp(7);
    y2_2 = temp(8);
    for j = 1:num_objFunc
        for n = 1:num_env
            close all; % not necessary, can turn off the graph.
            clear sys;
            sys = taxi_navigation();  
            sys = sys.addObjective_alw([0 8],1,[x1 y1], [x2 y2]);
            sys = sys.addObjective_alw([0 8],1,[x1_2 y1_2], [x2_2 y2_2]);
            if (n==2)
                sys = sys.addBoundary([0,0],20);
            elseif (n==3)
                sys = sys.addBoundary([-5,-5],30);
            end
            if (j==1)
                sys.lambda_rho = 0;
                sys.objFuncVersion = 1;
            elseif (j==2)
                sys.lambda_rho = 1;
                sys.objFuncVersion = 2;
            elseif (j==3)
                sys.lambda_rho = 5;
                sys.objFuncVersion = 2;
            elseif (j==4)
                sys.lambda_rho = 0.1;
                sys.objFuncVersion = 2;
            elseif (j==5)
                sys.lambda_rho = 1;
                sys.objFuncVersion = 1;
            elseif (j==6)
                sys.lambda_rho = 5;
                sys.objFuncVersion = 1;
            elseif (j==7)
                sys.lambda_rho = 0.1;
                sys.objFuncVersion = 1;
            end    
            sys.controller = sys.get_controller();
            [sys, succeed] = sys.run_deterministic(sys.controller);
            if (succeed)
                succeed_2 = model_checker(sys);
                xlswrite('examples_blustl\taxi\BluSTL report.xlsx',succeed_2,strcat('B',num2str(line),':B',num2str(line)));
            end 
            if (n==3)
                line = line + 3;
            else
                line = line + 1;
            end
        end
    end
end


                
            