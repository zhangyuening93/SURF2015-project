function succeed = model_checker(sys)
% This function will check if it succeeds.
% If yes, than succeed = -1, else, succeed = 0, or 1, 2 times.

list = [1, 40, 80, 112];

x1 = sys.objective_alw_ev{1}(1);
x2 = sys.objective_alw_ev{1}(2);
y1 = sys.objective_alw_ev{1}(3);
y2 = sys.objective_alw_ev{1}(4);
x1_2 = sys.objective_alw_ev{2}(1);
x2_2 = sys.objective_alw_ev{2}(2);
y1_2 = sys.objective_alw_ev{2}(3);
y2_2 = sys.objective_alw_ev{2}(4);

succeed = 0;

for i = 1:(size(list,2)-1)
    st_point = list(i);
    en_point = list(i+1);
    goal_1 = 0;
    goal_2 = 0;
    while ((st_point<=en_point) && (~goal_1 || ~goal_2))
        x = sys.system_data.X(1,st_point);
        y = sys.system_data.X(2,st_point);
        if (x>x1 && x<x2 && y>y1 && y<y2)
            goal_1 = 1;
        end
        if (x>x1_2 && x<x2_2 && y>y1_2 && y<y2_2)
            goal_2 = 1;
        end
        st_point = st_point + 1;
    end
    if (goal_1 && goal_2)
        succeed = succeed + 1;
    end
end

if succeed == size(list,2)-1
    succeed = -1;
end
end
