#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
import truthtable

if __name__ == '__main__':
    form = cgi.FieldStorage()
    expr = form.getvalue('expr')
    startwith = form.getvalue('startwith')
    print('Content-Type: text/html; charset=utf-8\n\n')

    print('''<!DOCTYPE html>
<html lang="ru"><head><meta charset="utf-8" />
<style>
<!--
  tr { background-color: #ffffff }
  .highlight { background-color: #ffffcc }
//-->
</style>
<title>Truth table generator online</title></head>
<body>''')

    if startwith.__class__ != str or startwith not in '01':
        startwith = '1'

    if expr:
        truthtable.main(['', expr, startwith, 'html'])
        print('<br /><br />')
    else:
        expr = 'x & ~y -> (y + ~x -> ~z)'

    print('''Input an expression:<br /><form action="" method="get">
<textarea name="expr" cols="70" rows="5">
%s</textarea>
<br/>''' % expr)
    print('''Start table with:
<input type="radio" name="startwith" value="1" %s/>1
<input type="radio" name="startwith" value="0" %s/>0
<br/>
<input type="submit" value="Do it for me!"></form>''' % \
        ((startwith == '1' and 'checked ') or '',
         (startwith == '0' and 'checked ') or '')
    )

    print('''<hr/>A short help:<br/>
~ - negative (not)<br/>
& - conjuction (logical multiply)<br/>
+ - disjunction (logical addition)<br/>
-> - implication (if/then)<br/>
<-> - equivalence (equality)<br/>
| - NAND gate (Sheffer\'s line)<br/>
_ - logical NOR (Pirce\'s arrow, Lukasevich\'s line)<br/>
* - XOR operator (exclusive or).<br/>
<hr/>Coded by Alexander Lopatin. Source code is here:
<a href="https://github.com/sbar/math/tree/master/discrete/logic"
target="_blank">github.com/sbar/math/tree/master/discrete/logic</a>
</body></html>''')
