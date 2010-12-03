#!/usr/bin/python3
# coding=utf8

# Bisection and secant root-finding methods

a = 1.0; b = 100.0; e = 0.01

def f(x):
    return 10*x-2*x*x

y1 = f(a); y2 = f(b)

if y1 * y2 >= 0:
    print("There are no roots")
else:
    n = 1

    #c = (a+b)/2
    c = (y2*a - y1*b)/(y2 - y1);

    y3 = f(c)
    while (abs(y3) > e):
        #c = (a+b)/2
        c = (y2*a - y1*b)/(y2 - y1);

        y3 = f(c)
        if y1 * y3 < 0:
            b = c
        else:
            a = c
        n += 1
    print("c=%f y3=%f n=%f" % (c, y3, n))
