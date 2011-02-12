#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
import tt

if __name__ == '__main__':
    form = cgi.FieldStorage()
    expr = form.getvalue('expr')
    startwith = form.getvalue('startwith')
    print('Content-Type: text/html; charset=utf-8\n\n')

    print('''<!DOCTYPE html>
<html lang="ru"><head><meta charset="utf-8" />
<title>Truth table generator online</title></head>
<body>''')

    if startwith == None:
        startwith = 1

    if expr:
        tt.main(['', expr, startwith, 'html'])
        print('<br /><br />')
    else:
        expr = 'x & ~y -> (y + ~x -> ~z)'

    print('''Input an expression:<form action="" method="post">
<textarea name="expr" cols="70" rows="5">
%s</textarea>
<br/>''' % expr)
    print('''Start table with:
<input type="radio" name="startwith" value="1" %s/>1
<input type="radio" name="startwith" value="0" %s/>0
<br/>
<input type="submit" value="Do it for me!"></form>''' % \
    (startwith and "checked", (startwith == 0) and "checked"))

    print('''<hr/>A short help:<br/>
~ - negative (not)<br/>
& - conjuction (logical multiply)<br/>
+ - disjunction (logical addition)<br/>
-> - implication (if/then)<br/>
<-> - equivalence (equality)<br/>
| - NAND gate (Sheffer\'s line)<br/>
_ - logical NOR (Pirce\'s arrow, Lukachevich\'s line)<br/>
* - XOR operator (exclusive or).<br/>
<hr/>Coded by Alexander Lopatin. Source code is here:
<a href="https://github.com/sbar/math/tree/master/logic" target="_blank">
github.com/sbar/math/tree/master/logic</a>
</body></html>''')
