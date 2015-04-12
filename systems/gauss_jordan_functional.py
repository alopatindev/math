#!/usr/bin/python3
# coding=utf8

import sys

def get_line(abn, i):
    a, b, n = abn
    start = i * n
    return a[start : (start + n)], b[i]

def aij(an, i, j):
    a, n = an
    return a[i * n + j]

def update_line(abn, i, f):
    def update_line_internal(a1a2n, f):
        a1, a2, n = a1a2n
        am = zip(a1, a2)
        return list(map(f, am))
    a, b, n = abn
    i1, i2 = i
    a1, b1 = get_line((a, b, n), i1)
    a2, b2 = get_line((a, b, n), i2)
    a_new = update_line_internal((a1, a2, n), f)
    b_new = f([b1, b2])
    return a_new, b_new

def replace_line(abn, ai, bi, i):
    a, b, n = abn
    a_new = a[0 : i*n] + ai + a[((i + 1) * n) : (n * n)]
    b_new = b[0 : i] + [bi] + b[(i + 1) : n]
    return a_new, b_new

def make_one(abn, i):
    a, b, n = abn
    mul = 1.0 / aij((a, n), i, i)
    ai, bi = get_line(abn, i)
    ai_new = list(map(lambda a: a * mul, ai))
    bi_new = bi * mul
    return replace_line(abn, ai_new, bi_new, i)

def make_zero(abn, i, j):
    a, b, n = abn
    mul = aij((a, n), i, j)
    ai, bi = update_line(abn, (i, j), lambda a: a[0] - a[1] * mul)
    return replace_line(abn, ai, bi, i)

def make_zero_recursive(abn, i, j):
    a, b, n = abn
    if i < n:
        if i != j:
            a_new, b_new = make_zero(abn, i, j)
            return make_zero_recursive((a_new, b_new, n), i + 1, j)
        else:
            return make_zero_recursive((a, b, n), i + 1, j)
    else:
        return a, b

def solve(abn):
    def solve_internal(abn, j):
        a, b, n = abn
        a_new, b_new = make_one((a, b, n), j)
        a, b = make_zero_recursive((a_new, b_new, n), 0, j)
        return a, b

    def solve_internal_recursive(abn, j):
        a, b, n = abn
        if j < n:
            a_new, b_new = solve_internal((a, b, n), j)
            return solve_internal_recursive((a_new, b_new, n), j + 1)
        else:
            return a, b

    return solve_internal_recursive(abn, 0)

def input_data(argv):
    f = lambda s: [float(i) for i in s.split(' ')]
    a = f(argv[1])
    b = f(argv[2])
    return a, b

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: %s '1 1 1 4 2 1 9 3 1' '0 1 3'" % sys.argv[0])
        sys.exit(1)

    a, b = input_data(sys.argv)
    a_solved, b_solved = solve((a, b, len(b)))
    print(b_solved)
