#!/bin/env python

import math
import sys

def isSquare(N):
    root = math.ceil(math.sqrt(N))
    return (root * root == N)

def FermatFactor(N):
    num = int(math.ceil(math.sqrt(N)))
    remainder = num * num - N

    while not isSquare(remainder):
        num = num + 1
        remainder = num * num - N
        if num > N:
           break

    x = num - int(math.sqrt(remainder))
    y = N / x
    print x
    print y


M = sys.argv[1]
FermatFactor(int(M))

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

