#!/usr/bin/python3
# coding=utf-8

# This program calculates binary relations. R with S, R^n, R^+, R^*.
# Copyright (C) 2011 Alexander Lopatin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from copy import copy

#a = [[0, 0, 1, 0],
#     [0, 0, 1, 0],
#     [0, 0, 0, 0],
#     [0, 1, 0, 0]]

#b = [[1, 0, 0, 0],
#     [0, 0, 1, 0],
#     [0, 0, 0, 1],
#     [1, 0, 0, 0]]

a = [[1, 0, 1],
     [0, 0, 1],
     [1, 0, 0]]

def multiply(a, b):
    res = []
    n = len(a)

    for i in range(n):
        z = []
        for j in range(n):
            x = 0
            for k in range(n):
                x += a[i][k] & b[k][j]
            z.append(int(bool(x)))
        res.append(z)

    return res

def pow(a, n):
    aa = copy(a)
    bb = copy(a)
    for i in range(n):
    #for i in range(n-1):
        aa = multiply(aa, bb)
    return aa

def powPlus(a):
    n = len(a)
    return pow(a, n)

def powPlusWarshall(r):
    s = copy(r)
    t = copy(s)
    n = len(s)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                t[j][k] = s[j][k] | s[j][i] & s[i][k]
        s = copy(t)
    return s

def identMatrix(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]

def add(a, b):
    n = len(a)
    #z = []
    #for i in range(n):
    #    x = []
    #    for j in range(n):
    #        x.append(int(bool(a[i][j] | b[i][j])))
    #    z.append(x)
    #return z
    return [[int(bool(a[i][j] | b[i][j])) for j in range(n)] for i in range(n)]

def powStar(a):
    n = len(a)
    return add(identMatrix(n), powPlusWarshall(a))

#print(multiply(a, b))
#print(pow(a, 2))
print(powPlusWarshall(a))
print(powPlus(a))
print(powStar(a))
#print(identityMatrix(3))
