#!/usr/bin/python3
# coding=utf8

import unittest

class SystemsTest(unittest.TestCase):
    a = [1, 1, 1, 4, 2, 1, 9, 3, 1]
    b = [0, 1, 3]
    n = len(b)
    abn = (a, b, n)

    def test_gauss_jordan_functional(self):
        from gauss_jordan_functional import solve
        a_out, b_out = solve(self.abn)
        self.assertEqual(b_out, [0.5, -0.5, 0.0])

    def test_gauss_jordan(self):
        from gauss_jordan import input_data, solve
        to_str = lambda a: ' '.join((str(i) for i in a))
        a, b = input_data(['', to_str(self.a), to_str(self.b)])
        a_out, b_out = solve(a, b)
        self.assertEqual(b_out, [0.5, -0.5, 0.0])

if __name__ == '__main__':
    unittest.main()
