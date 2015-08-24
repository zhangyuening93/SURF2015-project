function [loc, poly] = getRandLoc(varargin)
% get random location from (x1,x2) with range l and divided by n*m.
% if num(arg)=2, n=divider, [x1,x2] is the start location, l = 1.
% if num(arg)=3, n=divider, [x1,x2] is the start location, l is the range.
% if num(arg)=3, n=divider, [x1,x2] is the start location, [x3,x4] is the end location.
% output is [spec, poly_array].


if numel(varargin) == 2
    n = varargin{1};
    ranNum_1 = floor(rand(1)*n);
    ranNum_2 = floor(rand(1)*n);
    step = 1/n;
    start_loc = varargin{2};
    x = [start_loc(1)+ranNum_1*step start_loc(2)+ranNum_2*step];
    x_2 = [x(1)+step x(2)+step];
    poly = [x(1) x_2(1) x(2) x_2(2)];
    %loc = strcat('x1(t)>',num2str(x(1)),' and x1(t)<', num2str(x_2(1)), ' and x3(t)>', num2str(x(2)),' and x3(t)<', num2str(x_2(2)));
    loc = strcat('x1(t)>',num2str(x(1)),' and x1(t)<', num2str(x_2(1)), ' and x2(t)>', num2str(x(2)),' and x2(t)<', num2str(x_2(2)));
elseif numel(varargin) == 3
    n = varargin{1};
    start_loc = varargin{2};
    l = varargin{3};
    ranNum_1 = floor(rand(1)*n);
    ranNum_2 = floor(rand(1)*n);
    if size(l,2) == 2
        step_1 = (l(1)-start_loc(1))/n;
        step_2 = (l(2)-start_loc(2))/n;
    else
        step_1 = l/n;
        step_2 = step_1;
    end
    x = [start_loc(1)+ranNum_1*step_1 start_loc(2)+ranNum_2*step_2];
    x_2 = [x(1)+step_1 x(2)+step_2];
    poly = [x(1) x_2(1) x(2) x_2(2)];
    %loc = strcat('x1(t)>',num2str(x(1)),' and x1(t)<', num2str(x_2(1)), ' and x3(t)>', num2str(x(2)),' and x3(t)<', num2str(x_2(2)));
    loc = strcat('x1(t)>',num2str(x(1)),' and x1(t)<', num2str(x_2(1)), ' and x2(t)>', num2str(x(2)),' and x2(t)<', num2str(x_2(2)));
else
    display('Other options are not implemented yet.')
end
    