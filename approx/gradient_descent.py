#!/usr/bin/env python2

# https://www.youtube.com/watch?v=tIpKfDc295M
# https://www.youtube.com/watch?v=umAeJ7LMCfU

import numpy as np

f = lambda x, y: x * x + 2.0 * y
d_dx = lambda x, y: 2.0 * x
d_dy = lambda x, y: 2.0
gradient = lambda x, y: np.array([d_dx(x, y), d_dy(x, y)])

mu = 0.00005
num_iterations = 100000

xy = np.array([5.0, 10.0])
for _ in xrange(num_iterations):
    xy -= mu * gradient(*xy)

print xy, f(*xy)
