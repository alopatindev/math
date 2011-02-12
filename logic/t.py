#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
import tt

if __name__ == '__main__':
    form = cgi.FieldStorage()
    test = form.getvalue('test')
    print('Content-Type: text/html; charset=utf-8\n\n')

    print('''<!DOCTYPE html>
<html lang="ru"><head><meta charset="utf-8" />
<title>Truth table generator online</title></head>
<body>''')

    if test:
        tt.main(['', test, 'html'])
        print('<br /><br />')
    else:
        test = 'x & ~y -> (y + ~x -> ~z)'

    print('''Input an expression:<form action="" method="post">
<textarea name="test" cols="70" rows="5">
%s</textarea>
<input type="submit" value="Do it for me!"></form>''' % test)

    print('''<hr/>A short help:<br/>
~ - negative<br/>
& - conjuction (logical multiply)<br/>
+ - disjunction (logical addition)<br/>
-> - implication (if/then)<br/>
<-> - equivalence<br/>
| - NAND gate (Sheffer\'s line)<br/>
_ - logical NOR (Pirce\'s arrow, Lukachevich\'s line)<br/>
* - XOR operator.<br/>
<hr/>Coded by Alexander Lopatin. Source code is here:
<a href="https://github.com/sbar/math/tree/master/logic" target="_blank">
github.com/sbar/math/tree/master/logic</a>
</body></html>''')
