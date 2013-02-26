#!/usr/bin/env python

import time

k = 'fcvccfvfcfvcvfcfvc'

n = 'fcvccfvfcfvcvfcfvc'

a = lambda x, y: int(x==y)

def getsum(x, y):
    count = 0
    for i in xrange(len(x)):
        if x[i] == y[i]:
            count += 1
    return count

oldtime = time.time()
print map(a, k, n)
fulltime = time.time() - oldtime
print fulltime

oldtime = time.time()
print getsum(k, n)
fulltime = time.time() - oldtime
print fulltime