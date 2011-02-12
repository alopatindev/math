#!/usr/bin/python3
# coding=utf-8

# This program calculates a truth table in html and ascii format.

import sys 
import re

lits_r = re.compile(r'([~&+|_*()]|[a-zA-Z]|<->|->)')
MAX_SYMBOLS = 1000

def formula(s):
    s = s.replace(' ', '').replace('~~', '').replace('\r','').replace('\n', '')
    if len(s) > MAX_SYMBOLS:
        raise Exception('input line is too long')

    lits = lits_r.findall(s)
    operands = []

    for i in lits:
        if ('a' <= i <= 'z' or 'A' <= i <= 'Z') and \
            not operands.__contains__(i):
            operands.append(i)

    def expr(lits, i, operands): 
        lits.pop(i)  # removing (
        ex = []
        j = i
        while j < len(lits) and not lits[j] == ')':
            if lits[j] != '(':
                ex.append(lits.pop(j))
            else:
                expr(lits, j, operands)
        if lits[j] == ')':
            lits.pop(j)  # removing )
        lits.insert(i, ex) 

    def quote_unary(lits, operator):
        i = 0
        while i < len(lits):
            if lits[i].__class__ is list:
                quote_unary(lits[i], operator)
            elif lits[i] == operator:
                lits[i] = [lits[i], lits[i+1]]
                lits.pop(i+1)
            i += 1

    def quote_binary(lits, operator):
        i = 0
        while i < len(lits):
            if lits[i].__class__ == list:
                quote_binary(lits[i], operator)
            elif lits[i] == operator:
                lits[i] = [lits[i-1], operator, lits[i+1]]
                lits.pop(i-1)  # removing old operands
                lits.pop(i)
            i += 1

    i = 0
    while i < len(lits):
        if lits[i] == '(':
            expr(lits, i, operands)
        i += 1

    # fix priority (& — before everything, + before -> and <->)
    quote_unary(lits, '~')
    #quote_binary(lits, '&')
    #quote_binary(lits, '+')
    for i in '|_&+':
        quote_binary(lits, i)

    operands.sort()

    return lits, operands

def make_table(f, operands, startwith = 1):
    table = [operands]
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

    solve(f, op_dict, 0, table)

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

def calculate(f, ff, op_dict, op):
    xx = lits_to_clean_formula(f[0])
    yy = lits_to_clean_formula(f[2])

    # FIXME: quotes hack
    if not (xx in op_dict) and xx[:1] == '(' and xx[len(xx)-1] == ')':
        xx = xx[1::][:len(xx)-2]

    for i in range(len(op_dict[xx])):
        op_dict[ff].append(op(op_dict[xx][i], op_dict[yy][i]))

def binary_action(f, ff, op_dict):
    op_dict[ff] = []

    # FIXME: hack with removing quotes
    while len(f) == 1:
        f = f[0]

    if f[1] == '&':
        calculate(f, ff, op_dict, lambda x, y: int(x and y))
    elif f[1] == '+':
        calculate(f, ff, op_dict, lambda x, y: int(x or y))
    elif f[1] == '->':  # implication
        calculate(f, ff, op_dict, lambda x, y: int(not(x == 1 and y == 0)))
    elif f[1] == '<->':  # equivalence
        calculate(f, ff, op_dict, lambda x, y: int(x == y))
    elif f[1] == '|':  # NAND gate, Sheffer's line
        calculate(f, ff, op_dict, lambda x, y: int(not(x and y)))
    elif f[1] == '_':  # Logical NOR (Pirce's arrow, Lukachevich's line)
        calculate(f, ff, op_dict, lambda x, y: int(not(x or y)))
    elif f[1] == '*':  # XOR
        calculate(f, ff, op_dict, lambda x, y: int(x ^ y))

def solve(f, op_dict, action, table):
    if f.__class__ is list:
        for i in f:
            if i.__class__ is list:
                action = solve(i, op_dict, action, table)

    ff = lits_to_clean_formula(f)
    #print('%d. ' % action, f)
    #print('%s' % ff, f)  # shows the actions in order to do

    # FIXME: hack with removing quotes
    if len(f) == 1:
        f = f[0]
        return action

    for i in f:
        if f[0] == '~':
            op_dict[ff] = [int(not i) for i in op_dict[f[1]]]
        else:
            binary_action(f, ff, op_dict)

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

    return 1 if tautology else 0 if absurdity else -1

def pprint(table, html=True):
    if html:
        print('<table border="1">')
    for i in range(len(table)):
        if html:
            print('<tr>')
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

def main(argv):
    if len(argv) < 2:
        print('usage: %s \'x & ~y -> (y + ~x -> ~z)\' [html | ascii] [1 | 0]' \
            % argv[0])
        return 1

    try:
        s = argv[1]
        f, operands = formula(s)
        print('Processing formula "%s"' % s)
    except Exception as text:
        print('Input error. Check your input expression. More info: %s' % text)
        return 1

    #pprint(table, len(argv) > 2 and argv[2] == 'html')
    startwith = (len(argv) > 2 and argv[2] == '1' and 1) or 0
    html = len(argv) > 3 and argv[3] == 'html'

    table = make_table(f, operands, startwith)
    pprint(table, html)

    t = identic(table)
    if t == 1:
        print('Expression is tautology')
    elif t == 0:
        print('Expression is absurdity')
    else:
        print('Expression is not identical')

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
