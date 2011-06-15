#!/usr/bin/python3
# coding=utf8

import sys
import re

MAX_SYMBOLS = 1000

unary_operators = ['sin', 'cos']
binary_operators = '^*/+-'

diff_table = {
    ['sin', 'VAR1'] : ['cos', 'VAR1'],
    ['cos', 'VAR1'] : [-1, '*', ['sin', 'VAR1']],
    ['VAR1', '^', 'VAR2'] : ['VAR2', '*', ['VAR1', '^', ['VAR2', '+', -1]]],
}

funcs = ''
for i in unary_operators:
    funcs += "%s|" % i
lits_r = re.compile('(' + funcs + '[a-zA-Z]|[()' + \
                    binary_operators + ']|[0-9]*)')

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
    s = s.replace(' ', '') \
         .replace('\r','') \
         .replace('\n', '') \
         .replace('\t', '')
    if len(s) > MAX_SYMBOLS:
        raise Exception('input line is too long')
    if not brackets_ok(s):
        raise Exception('check your brackets')
    return s

def is_operator(x):
    return x in unary_operators or x in binary_operators

def is_operand(x):
    return not is_operator(x)

def parse(func):
    func = fix_input(func)
    print('func: "%s"' % func)
    lits = lits_r.findall(func)
    lits.pop()

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

    def automultiply(lits):
        i = 0
        while i < len(lits):
            if lits[i].__class__ is list:
                lits[i] = automultiply(lits[i])
            if i < len(lits) - 1:
                if (lits[i].__class__ is list or is_operand(lits[i])) and \
                   (lits[i+1].__class__ is list or is_operand(lits[i+1])):
                    lits = lits[:i+1] + ['*'] + lits[i+1:]
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

    lits = expr(lits)
    for i in unary_operators:
        quote_unary(lits, i)

    lits = automultiply(lits)

    for i in binary_operators:
        quote_binary(lits, i)

    return lits

def unparse(farr):
    return ""

def unparsetex(farr):
    return ""

def differ(pfunc, var, times=1):
    print('parsed', pfunc)
    for i in range(times):
        pass
    return []

def differ_composite(pfunc, df, var):
    return differ(pfunc, var) * differ(df, var)

def main(argv):
    if len(argv) < 3:
        print("Syntax: %s function variable [times]" % argv[0])
        print("Example: %s 'ln(sin(x)^2)' x 2" % argv[0])
        return 1

    try:
        func, var = argv[1], argv[2]
        times = 1 if len(argv) < 4 else int(argv[3])

        if times < 0:
            print("Only positive number of times we can to differentiate!")
            return 2
    except Exception as text:
        print("Error occured while parsing your input data:", text)

    try:
        result = differ(parse(func), var, times)
        print(unparse(result))
        print(unparsetex(result))
    except Exception as text:
        print("Error occured while differentiating a function:", text)
        return 3
        
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
