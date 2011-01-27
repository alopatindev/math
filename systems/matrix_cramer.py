#!/usr/bin/python3
# coding=utf8

# Matrix and Cramer root-find algorithms

from copy import deepcopy

a = [[2., 5., 4.],
     [1., 3., 2.],
     [2., 10., 9.]]

b = [[30., 150., 110.],]

def multiply(a, b):
    n = len(a); m = len(a[0]); k = len(b)
    c = []

    for i in range(n):
        c.append([])
        for s in range(k):
            sum = 0.
            for j in range(n):
                sum += a[i][j]*b[s][j]
            c[len(c)-1].append(sum)

    if len(c[0]) > 1:
        return c
    else:
        cc = []
        for i in range(len(c)):
            cc.append(c[i][0])
        return cc

def transp(a):
    b = []
    for i in range(len(a[0])):
        x = []
        for j in range(len(a)):
            x.append(a[j][i])
        b.append(x)
    return b

def minor(a, i, j):
    b = []; n = len(a)
    for ii in range(n):
        if ii != i:
            b.append([])
            for jj in range(n):
                if jj != j:
                    b[len(b)-1].append(a[ii][jj])
    return det(b)

def alg_add(a, i, j):
    return minor(a, i, j) * ((-1) ** (i + j))

def inverse(a):
    b = []
    n = len(a)
    det_a = det(a)
    for i in range(n):
        b.append([])
        for j in range(n):
            b[len(b)-1].append(alg_add(a, i, j) / det_a)
    return transp(b)

def det(a):
    n = len(a)
    if n == 0 or n != len(a[0]):
        return False
    elif n == 2:
        return a[0][0]*a[1][1] - a[0][1]*a[1][0]
    else:
        s = 0.
        for i in range(n):
            s += a[i][0]*alg_add(a, i, 0)
        return s

def matrix_method(a, b):
    return multiply(inverse(a), b)

def cramer_method(a, b):
    n = len(a); m = len(a[0])
    x = []

    d = det(a)

    for j in range(m):
        da = deepcopy(a)
        for i in range(n):
            da[i][j] = b[0][i]
        x.append(det(da) / d)

    return x

if __name__ == "__main__":
    print(matrix_method(a, b))
    print(cramer_method(a, b))
