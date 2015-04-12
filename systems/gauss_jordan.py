#!/usr/bin/python3
# coding=utf8

import sys
from copy import copy, deepcopy

def make_one(a, b, i):
    d = 1. / a[i][i]

    for k in range(len(a[i])):
        a[i][k] *= d

    b[i] *= d
    return a, b

def make_zero(a, b, i, j):
    n = len(a)
    m = len(a[0])

    d = a[i][j]

    for l in range(m):
        a[i][l] -= a[j][l]*d

    b[i] -= b[j]*d

    return a, b

def solve(a, b):
    n = len(a)
    m = len(a[0])

    a = deepcopy(a); b = copy(b)

    for j in range(m):
        a, b = make_one(a, b, j)
        r = list(range(n)); r.remove(j)
        for i in r:
            a, b = make_zero(a, b, i, j)

    return a, b

def input_data(argv):
    a = []; b = []
    b = argv[2].split(' ')

    m = len(b)
    b = [float(b[j]) for j in range(m)]

    t = argv[1].split(' ')
    n = len(t) // m

    k = 0
    for i in range(n):
        a.append([])
        for j in range(m):
            a[i].append(float(t[k]))
            k += 1

    return a, b

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: %s '1 1 1 4 2 1 9 3 1' '0 1 3'" % sys.argv[0])
        sys.exit(1)

    a, b = input_data(sys.argv)
    a, b = solve(a, b)
    print(b)
