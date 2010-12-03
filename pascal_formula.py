#!/usr/bin/python3
# coding=utf8

# This program calculates (a + b)^n formula using Pascal trangle and
# outputs it in (La)TeX format

import sys

try:
    ex = int(sys.argv[1])
except IndexError:
    print("Syntax: %s number" % sys.argv[0])
    sys.exit(1)

def nextLine(k):
    j = [1]
    for i in range(1, len(k)):
        j.append(k[i-1] + k[i])
    j.append(1)
    return j

def formula(ex):
    k = [1]; i = 1
    while i <= ex:
        i += 1
        k = nextLine(k)

    f = "(a+b)^{%d}=" % ex
    a = ex; b = 0
    for i in range(len(k)):
        #f += "%d*a^%d*b^%d +" % (i, a, b),

        if (k[i] > 1): f += str(k[i])

        if (a > 0): f += "a"
        if (a > 1): f += "^{%d}" % a

        if (b > 0): f += "b"
        if (b > 1): f += "^{%d}" % b

        if (i < len(k)-1):
            f += "+"

        a -= 1; b += 1

    return f

print (
"""\\documentclass[12pt]{letter}
\\usepackage{mathtext}

\\begin{document}
\\LARGE$%s$
\\end{document}""" % formula(ex))
