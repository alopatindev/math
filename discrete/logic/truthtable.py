#!/usr/bin/python3
# coding=utf-8

# This program calculates a truth table in HTML and ASCII format.
# Copyright (C) 2010-2011 Alexander Lopatin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

import sys 
import re
from copy import copy

lits_r = re.compile(r'([a-zA-Z01]|[~&+|_*()]|<->|->)')
MAX_SYMBOLS = 1000

def is_const(x):
    return x in '01'

def is_operand(x):
    return x.__class__ is str and \
           ('a' <= x <= 'z' or 'A' <= x <= 'Z' or is_const(x))

def is_operator(x):
    return not is_operand(x)

def is_unary_operator(x):
    return x == '~'

def brackets_ok(s):
    br = []
    for i in s:
        if i == '(':
            br.append(i)
        elif i == ')':
            if len(br) == 0 or br.pop() != '(':
                return False
    return len(br) == 0

def fix_input(s):
    s = s.replace(' ', '').replace('~~', '').replace('\r','').replace('\n', '')
    if len(s) > MAX_SYMBOLS:
        raise Exception('input line is too long')

    if not brackets_ok(s):
        raise Exception('check your brackets')

    return s

def formula(s):
    lits = lits_r.findall(s)
    operands = []

    for i in lits:
        if is_operand(i) and not is_const(i) and not operands.__contains__(i):
            operands.append(i)

    def expr(lits):
        if '(' not in lits or ')' not in lits:
            return lits

        br = []
        i = 0
        while i < len(lits):
            if lits[i] == '(':
                br.append((lits[i], i))  # bracket and opening offset
            elif lits[i] == ')':
                start = br.pop()[1]
                ex = lits[start+1:i]
                ex = expr(ex)  # processing subexpression

                # remove unnecessary brackets
                if len(ex) == 1:
                    ex = ex[0]

                # remove old literals' items
                for k in range(i-start+1):
                    lits.pop(start)

                lits.insert(start, ex)
                i = start
            i += 1

        return lits

    def quote_unary(lits, operator):
        i = 0
        while i < len(lits):
            if lits[i].__class__ is list:
                quote_unary(lits[i], operator)
            elif len(lits) > 2 and lits[i] == operator:
                quote_unary(lits[i+1], operator)
                lits[i] = [operator, lits.pop(i+1)]
            i += 1

    def quote_binary(lits, operator):
        i = 0
        another = False  # we've met a different operator than we're lookin' for
        while i < len(lits):
            if lits[i].__class__ == list:
                quote_binary(lits[i], operator)
            else:
                if lits[i] == operator:
                    if i < len(lits)-1-(not another):
                        lits[i-1] = [lits[i-1], lits[i], lits[i+1]]
                        lits.pop(i)
                        lits.pop(i)
                        i -= 1
                else:
                    another |= is_operator(lits[i])
            i += 1

    def autoconjuction(lits):
        i = 0
        while i < len(lits):
            if lits[i].__class__ is list:
                lits[i] = autoconjuction(lits[i])
            if i < len(lits) - 1:
                if (lits[i].__class__ is list or is_operand(lits[i])) and \
                   (lits[i+1].__class__ is list or is_operand(lits[i+1])):
                    lits = lits[:i+1] + ['&'] + lits[i+1:]
            i += 1
        return lits

    lits = expr(lits)
    quote_unary(lits, '~')

    # replace abc(a+b) with a&b&c&(a+b)
    lits = autoconjuction(lits)

    # fix priority (& — before everything, + before -> and <->)
    for i in ('|', '_', '&', '+', '*', '->', '<->'):
        quote_binary(lits, i)

    operands.sort()

    return lits, operands

def make_table(f, operands, startwith = 1):
    table = [copy(operands)]
    op_dict = {}
    leno = len(operands)
    lines = 2 ** leno

    l = lines // 2
    for o in operands:
        op_dict[o] = []

        i = 0
        nexti = i + l - 1
        truth = startwith
        while i < lines:
            op_dict[o].append(truth)
            if i == nexti:
                truth = int(not truth)
                nexti += l
            i += 1

        l //= 2

    solve(f, op_dict, 0, table, lines)

    for j in range(len(table[0])):
        for i in range(len(op_dict[table[0][j]])):
            if len(table) < i+2:
                table.append([op_dict[table[0][j]][i]])
            else:
                table[i+1].append(op_dict[table[0][j]][i])
                pass

    return table

def lits_to_formula(lits):
    s = ''
    for i in lits:
        if i.__class__ is list:
            s += lits_to_formula(i)
        else:
            s += str(i)

    return '(' + s + ')'

def lits_to_clean_formula(lits):
    if lits.__class__ == list:
        ff = lits_to_formula(lits)
        ff = ff[1::][:len(ff)-2]  # remove unnecessary ()
    else:
        ff = lits
    return ff

def unary_action(f, ff, op_dict, lines):
    if f[1].__class__ is list:
        xx = lits_to_clean_formula(f[1])
    else:
        xx = f[1]

    if is_const(xx):
        op_dict[ff] = [int(not int(xx)) for i in range(lines)]
    else:
        op_dict[ff] = [int(not i) for i in op_dict[xx]]

def calc_binary(f, ff, op_dict, n, op):
    xx = lits_to_clean_formula(f[0])
    yy = lits_to_clean_formula(f[2])

    for i in range(n):
        x = int(xx) if is_const(xx) else op_dict[xx][i]
        y = int(yy) if is_const(yy) else op_dict[yy][i]
        op_dict[ff].append(op(x, y))

def binary_action(f, ff, op_dict, n):
    op_dict[ff] = []
    if len(f) < 2:
        print("wtf", f, ff)

    if f[1] == '&':
        calc_binary(f, ff, op_dict, n, lambda x, y: int(x and y))
    elif f[1] == '+':
        calc_binary(f, ff, op_dict, n, lambda x, y: int(x or y))
    elif f[1] == '->':  # implication
        calc_binary(f, ff, op_dict, n, lambda x, y: int(not(x == 1 and y == 0)))
    elif f[1] == '<->':  # equivalence
        calc_binary(f, ff, op_dict, n, lambda x, y: int(x == y))
    elif f[1] == '|':  # NAND gate, Sheffer's line
        calc_binary(f, ff, op_dict, n, lambda x, y: int(not(x and y)))
    elif f[1] == '_':  # Logical NOR (Pirce's arrow, Lukasevich's line)
        calc_binary(f, ff, op_dict, n, lambda x, y: int(not(x or y)))
    elif f[1] == '*':  # XOR
        calc_binary(f, ff, op_dict, n, lambda x, y: int(x ^ y))

def solve(f, op_dict, action, table, lines):
    if f.__class__ is list:
        for i in f:
            if i.__class__ is list:
                action = solve(i, op_dict, action, table, lines)

    ff = lits_to_clean_formula(f)
    #print('%d. ' % action, f)
    #print('%s' % ff, f)  # shows the actions in order to do

    for i in f:
        if is_unary_operator(f[0]):
            unary_action(f, ff, op_dict, lines)
        else:
            if len(f) > 1:
                binary_action(f, ff, op_dict, lines)
            else:
                return action + 1

    table[0].append(ff)

    return action + 1

def identic(table):
    tautology = True
    absurdity = True
    n, m = len(table), len(table[0])
    for j in range(n):
        if table[j][m-1] == 0 and tautology:
            tautology = False
        if table[j][m-1] == 1 and absurdity:
            absurdity = False
    #return 1 if tautology else 0 if absurdity else -1
    if tautology:
        return 'Expression is tautology'
    elif absurdity:
        return 'Expression is absurdity'
    else:
        return 'Expression is not identical'

def dnf(table, operands):
    n = len(table)
    m = len(table[0])-1
    on = len(operands)
    s = ''
    for i in range(1, n):
        if table[i][m]:
            for j in range(on):
                s += (table[i][j] and operands[j]) or '~' + operands[j]
            s += '+'
    return s[:len(s)-1]  # do not return last +

def pprint(table, operands, html=True):
    if html:
        print('<table border="1">')
    for i in range(len(table)):
        if html:
            print('''<tr onMouseOver="this.className='highlight'" \
onMouseOut="this.className='normal'">''')
        for j in range(len(table[0])):
            if html:
                print('<td>%s</td>' % str(table[i][j]))
            else:
                try:
                    sys.stdout.write(str(table[i][j]) + ' | ')
                except IndexError:
                    sys.stdout.write('? |')
        if html:
            print('</tr>\n')
        else:
            print()
            sys.stdout.flush()
    if html:
        print('</table>')

    print(identic(table))

    if html:
        print('<br />')

    print('DNF is', dnf(table, operands))

def main(argv):
    if len(argv) < 2:
        print('usage: %s \'x & ~y -> (y + ~x -> ~z)\' [1 | 0] [html | ascii]' \
            % argv[0])
        return 1

    try:
        s = fix_input(argv[1])
        f, operands = formula(s)
        print('Processing formula "%s"' % lits_to_clean_formula(f))

        startwith = (len(argv) > 2 and argv[2] == '1' and 1) or 0
        html = len(argv) > 3 and argv[3] == 'html'

        table = make_table(f, operands, startwith)
        pprint(table, operands, html)
    except Exception as text:
        print('Input error. Check your input expression. More info: %s' % text)
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
