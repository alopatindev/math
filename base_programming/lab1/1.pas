var
    a, b, eps, x, y, y1, y2 : real;
    i : integer;
    func_number, calc_method, exact_type : byte;

procedure input_data;
begin
    write('Input a = '); readln(a);
    write('Input b = '); readln(b);
    write('Input eps = '); readln(eps);

    writeln;
    writeln('1) f(x) = 10*x - 2*x*x');
    writeln('2) f(x) = 2*x - 20');
    write('Select the function: '); readln(func_number);

    writeln;
    writeln('1) Half-division method');
    writeln('2) Chords method');
    write('Select the calculation method: '); readln(calc_method);

    writeln;
    writeln('1) |y| <= eps');
    writeln('2) |b - a| <= eps');
    writeln('3) |(y2*a - y1*b) / (y2 - y1) - x| <= eps');
    write('Select the exactness type: '); readln(exact_type);
end;

function f(x : real) : real;
begin
    case func_number of
        1: f := 10*x - 2*x*x;  { x = 5 }
        2: f := 2*x - 20;  { x = 10 }
    end;
end;

function exact_reached : boolean;
begin
    case exact_type of
        1: exact_reached := abs(y) <= eps;
        2: exact_reached := abs(b - a) <= eps;
        3: exact_reached := abs((y2*a - y1*b)/(y2 - y1) - x) <= eps;
    end;
end;

procedure calculate_root;
begin
    y1 := f(a); y2 := f(b);

    if y1*y2 >= 0 then
    begin
        writeln('There are no roots');
        halt(1);
    end;

    i := 0;
    repeat
        case calc_method of
            1: x := (a + b) / 2;
            2: x := (y2*a - y1*b) / (y2 - y1);
        end;

        y := f(x);

        if y1*y < 0 then
            b := x
        else
            a := x;
        inc(i);
    until exact_reached;
end;

procedure print_result;
begin
    writeln('x = ', x:15:15,
            ', y = ', y:15:15,
            ', eps = ', eps:15:15,
            ', i = ', i);
end;

begin
    writeln;
    writeln('Calculate the root of the function');
    writeln;

    input_data;
    calculate_root;
    print_result;
end.
