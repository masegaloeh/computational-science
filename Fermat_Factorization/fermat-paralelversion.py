#!/home/itbsks213zagalo/root/usr/local/bin/python2.7

import time
import math
import sys
import multiprocessing
import Queue
import time

def isSquare(number):
    root = math.ceil(math.sqrt(number))
    return (root * root == number)

def modularFermatFactor(number, start, step, should_i_stop, factor1, factor2):
    limit = int(math.ceil((number + 1)/2))

    limit_time = 10750
    start_loop = time.time()
    
    if start < int(math.ceil(math.sqrt(number))):
        start = int(math.ceil(math.sqrt(number)))

    for a in xrange(start, limit + 1, step):

        time_now = time.time()
        if (time_now - start_loop) > limit_time:
            should_i_stop.value = start

        remainder = a * a - number

        if remainder == 0:
            factor1.value = a
            factor2.value = a
            #print 'Program {0} signalling for stop.'.format(start)
            should_i_stop.value = start
            break

        if isSquare(remainder):
            if a - int(math.sqrt(remainder)) != 1:
                 factor1.value = a + int(math.sqrt(remainder))
                 factor2.value = a - int(math.sqrt(remainder))
                 #print 'Program {0} signalling for stop.'.format(start)
                 should_i_stop.value = start
                 break

            #return a
   
        if should_i_stop.value != 0:
            #print 'Program {0} ended because {1}. Thanks for your cooperation.'.format(start, should_i_stop.value)
            break

    return -1   

def mp_wrapper(number, unknown_factor, prime_factor, nWorker=10):
    #number = 6724
    #nWorker = 10

    if number == 2:
         P.put(2)
         return None

    if number % 2 == 0:
         P.put(2)
         Q.put(number / 2)
         return None
          
    tmpval = multiprocessing.Value('i', 0)
    factor1 = multiprocessing.Value('i', -1)
    factor2 = multiprocessing.Value('i', -1)
   
    initial = int(math.ceil(math.sqrt(number)))
    jobs = []
    
    for i in range(nWorker):
        j = initial + i
        #print j
        p  = multiprocessing.Process(target=modularFermatFactor, args=(number, j, nWorker, tmpval, factor1, factor2, ))
        jobs.append(p)
        p.start()

    p.join()

    if factor2.value != -1:
        Q.put(factor1.value)
        Q.put(factor2.value)
    else:
        P.put(number)
     
    return None

#for testnum in xrange (987654321012345652, 987654321012345654):
#for testnum in xrange (9281451, 9281499):
#for testnum in xrange (110356113559705925, 110356113559705929):
for testnum in xrange (3806984503141, 3806984503150):
    Q = Queue.Queue()
    P = Queue.Queue()

#    M = sys.argv[1]
#    N = sys.argv[2]
    M = testnum
    N = 23

    Q.put(int(M))

    tstart = time.time()
    while not Q.empty():
        mp_wrapper(Q.get(), Q, P, int(N))
    
    tend = time.time()
    strout = ''
    while not P.empty():
        strout = strout + str(P.get()) + ', '
    print str(testnum) + " xxx " + strout + ' ' + str(tend - tstart)
