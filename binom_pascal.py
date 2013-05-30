#!/usr/bin/python3
# coding=utf8

# This program calculates (a +- b)^n formula using binomial equation or
# Pascal triangle. Outputs in (La)TeX format.

import sys
from math import factorial

FORMAT = """\\documentclass[12pt]{letter}
\\usepackage{mathtext}

\\begin{document}
$(a\\pm b)^{%d}=%s$
\\end{document}""" 

# Next line in Pascal trangle
def nextLine(k):
    j = [1]
    for i in range(1, len(k)):
        j.append(k[i-1] + k[i])
    j.append(1)
    return j

def pascal_formula(ex):
    k = [1]; i = 1
    while i <= ex:
        i += 1
        k = nextLine(k)
    f = ''
    a = ex; b = 0
    for i in range(len(k)):
        #f += "%d*a^%d*b^%d +" % (i, a, b),
        if k[i] > 1: f += str(k[i])
        if a > 0: f += "a"
        if a > 1: f += "^{%d}" % a
        if b > 0: f += "b"
        if b > 1: f += "^{%d}" % b
        if i < len(k)-1:
            f += "+" if i % 2 else "\\pm "
        a -= 1
        b += 1
    return f

# Neuton's binomial
def binom(fn, n, k):
    # fn = factorial(n)
    return fn // (factorial(k) * factorial(n-k))

def binom_formula(ex):
    fn = factorial(ex)
    f = ''
    for k in range(ex + 1):
        #f += "%da^{%d}b^{%d}+" % (binom(ex, k), ex-k, k)
        bin = binom(fn, ex, k)
        if bin > 1:
            f += str(int(bin))
        if ex-k > 0: f += "a"
        if ex-k > 1: f += "^{%d}" % (ex-k)
        if k > 0: f += "b"
        if k > 1: f += "^{%d}" % k
        if k < ex:
            f += "+" if k % 2 else "\\pm "

    return f


def update_sign(formula, ex):
    if ex < 0:
        formula = "\\frac{1}{%s}" % formula
    return formula


def main():
    try:
        ex = int(sys.argv[1])
    except IndexError:
        print("Syntax: %s number" % sys.argv[0])
        return 1

    #formula = pascal_formula(abs(ex))
    formula = binom_formula(abs(ex))

    formula = update_sign(formula, ex)
    print(FORMAT % (ex, formula))

sys.exit(main())
