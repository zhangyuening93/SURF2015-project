function Sys = STLC_update_plot(Sys)
% STLC_update_plot updates the plots of an STLC_lti at runtime
%
% Input: Sys, the STLC_lti instance
% Output: Sys with plots modified
%
% :copyright: TBD
% :license: TBD

system_style= {'LineWidth',2};
model_style = {'--g'};
axis_style = {'Fontsize',12}; 

if isempty(Sys.h)
    Sys.h.hf = figure;
    nb_plots = numel(Sys.plot_x)+numel(Sys.plot_y)+numel(Sys.plot_u)+numel(Sys.plot_w);
    cur_plot = 1;
    
    
    for iX = Sys.plot_x
        subplot(nb_plots,2,cur_plot);
        hold on; grid on;
        Sys.h.Xpast(iX) = plot(Sys.system_data.time, Sys.system_data.X(iX,1:end-1),system_style{:});
        Sys.h.Xmodel(iX) = plot(Sys.model_data.time,Sys.model_data.X(iX,:), model_style{:});
        ylabel(Sys.xlabel{iX});
        cur_plot = cur_plot+1*2;
        set(gca,axis_style{:});

    end
    
    for iY = Sys.plot_y
        subplot(nb_plots,2,cur_plot);
        hold on;grid on;
        Sys.h.Ypast(iY) = plot(Sys.system_data.time, Sys.system_data.Y(iY,:),system_style{:});
        Sys.h.Ymodel(iY) = plot(Sys.model_data.time(1:end-1), Sys.model_data.Y(iY,:), model_style{:});
        ylabel(Sys.ylabel{iY});
        cur_plot = cur_plot+1*2;
        set(gca,axis_style{:});
    end
    
    
    for iU = Sys.plot_u
        subplot(nb_plots,2,cur_plot);
        hold on;grid on;
        Sys.h.Upast(iU) = stairs(Sys.system_data.time, Sys.system_data.U(iU,:),system_style{:});
        Sys.h.Umodel(iU) = stairs(Sys.model_data.time(1:end-1),Sys.model_data.U(iU,:), model_style{:});
        ylabel([Sys.ulabel{iU}]);
        cur_plot = cur_plot+1*2;
        set(gca,axis_style{:});
    end
    
    for iW = Sys.plot_w
        subplot(nb_plots,2,cur_plot);
        hold on;grid on;
        Sys.h.Wpast(iW) = plot(Sys.system_data.time, Sys.system_data.W(iW,:),system_style{:});
        Sys.h.Wmodel(iW) = plot(Sys.model_data.time(1:end-1),Sys.model_data.W(iW,1:end-1), model_style{:});
        ylabel(Sys.wlabel{iW});
        cur_plot = cur_plot+1*2;
        set(gca,axis_style{:});
    end
    
    subplot(nb_plots,2,[2, 4]);
    hold on; grid on;
    % You can put objectives here.
    if ~isempty(Sys.objective_ev)
        ops.shade = 0.1;
        ops.color = [1, 0, 0];
        for index = 1:numel(Sys.objective_ev)
            plot(getPoly(Sys.objective_ev{index}),ops);
        end
    end
    % You can put alw_objectives here.
    if ~isempty(Sys.objective_alw_ev)
        ops.shade = 0.1;
        ops.color = [0, 1, 1];
        for index = 1:numel(Sys.objective_alw_ev)
            plot(getPoly(Sys.objective_alw_ev{index}),ops);
        end
    end
    % You can put obstacle here.
    if ~isempty(Sys.obstacle)
        ops.shade = 0.1;
        ops.color = [0.5, 0.5, 0.5];
        %plot(getPoly([2 5 3 4]),ops);
        for index = 1:numel(Sys.obstacle)
            plot(getPoly(Sys.obstacle{index}),ops);
        end
    end
    % Change
    %ops.shade = 0.1;
    %ops.color = [0.5, 0.5, 0.5];
    %plot(getPoly([17.5 20 8 10]),ops);
    %plot(getPoly([12.5 15 10 12.5]),ops);
    %axis([0 20 0 20]);
    % Change 
    Sys.h.Xpast(3) = plot(Sys.system_data.X(1,1:end-1), Sys.system_data.X(2,1:end-1),system_style{:});
    Sys.h.Xmodel(3) = plot(Sys.model_data.X(1,:),Sys.model_data.X(2,:), model_style{:});
    ylabel(Sys.xlabel{2});
    xlabel(Sys.xlabel{1});
    % Modify here for the axis/boundary.
    if ~isempty(Sys.boundary)
        axis(Sys.boundary);
    end
    set(gca,axis_style{:});
    
    if Sys.stop_button
        Sys.h.hbutton=uicontrol(Sys.h.hf,'style','pushbutton',...
            'string','Stop',...
            'callback','Stop()'...
            );
    end
else
    
    for iX = Sys.plot_x
        set(Sys.h.Xpast(iX), 'Xdata', Sys.system_data.time, 'Ydata',Sys.system_data.X(iX,1:end-1));
        set(Sys.h.Xmodel(iX), 'Xdata', Sys.model_data.time,'Ydata', Sys.model_data.X(iX,:));
    end
    set(Sys.h.Xpast(3), 'Xdata', Sys.system_data.X(1,1:end-1), 'Ydata',Sys.system_data.X(2,1:end-1));
    set(Sys.h.Xmodel(3), 'Xdata', Sys.model_data.X(1,:),'Ydata', Sys.model_data.X(2,:));
    
    for iY = Sys.plot_y
        set(Sys.h.Ypast(iY), 'Xdata', Sys.system_data.time,'Ydata',  Sys.system_data.Y(iY,:));
        set(Sys.h.Ymodel(iY), 'Xdata', Sys.model_data.time(1:end-1),'Ydata', Sys.model_data.Y(iY,:));
    end
    
    for iU = Sys.plot_u
        set(Sys.h.Upast(iU), 'Xdata', Sys.system_data.time,'Ydata',  Sys.system_data.U(iU,:));
        set(Sys.h.Umodel(iU), 'Xdata', Sys.model_data.time(1:end-1),'Ydata', Sys.model_data.U(iU,:));
    end
    
    for iW = Sys.plot_w
        set(Sys.h.Wpast(iW), 'Xdata', Sys.system_data.time,'Ydata',  Sys.system_data.W(iW,:));
        set(Sys.h.Wmodel(iW), 'Xdata', Sys.model_data.time(1:end-1),'Ydata', Sys.model_data.W(iW,1:end-1));
    end
    xlabel('Time');
end
end
