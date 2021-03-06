import time
import signal
from math import log10, floor, sqrt

timeout = 90


def handler(signum, frame):
    """Raise exception if script runs too long."""
    msg = "SCRIPT TIMED OUT!!!\n More than " + str(timeout) + " seconds have elapsed."
    raise Exception(msg)


def round_sig(x, sig=4):
    """Round to significant figures."""
    return round(x, sig-int(floor(log10(abs(x))))-1)

signal.signal(signal.SIGALRM, handler)
signal.alarm(timeout)
start = time.time()

'''
Highly divisible triangular number
Problem 12

The sequence of triangle numbers is generated by adding the natural numbers. So the 7th triangle number would 
be 1 + 2 + 3 + 4 + 5 + 6 + 7 = 28. The first ten terms would be:

1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...

Let us list the factors of the first seven triangle numbers:

 1: 1
 3: 1,3
 6: 1,2,3,6
10: 1,2,5,10
15: 1,3,5,15
21: 1,3,7,21
28: 1,2,4,7,14,28
We can see that 28 is the first triangle number to have over five divisors.

What is the value of the first triangle number to have over five hundred divisors?
'''


def triangle_number_generator():
    total = 0
    count = 0
    while True:
        total += count
        yield total
        count += 1


def get_factors_of(n):
    factors_of_n = [1, n]
    for i in range(2, int(sqrt(n))+1):
        if n % i == 0:
            factors_of_n.append(i)
            factors_of_n.append(n//i)
    factors_of_n.sort()
    return factors_of_n


tri_gen = triangle_number_generator()
triangle_number = None
current_number_of_factors = 0
desired_number_of_factors = 500  
while current_number_of_factors < desired_number_of_factors:
    triangle_number = next(tri_gen)
    factors = get_factors_of(triangle_number)
    current_number_of_factors = len(factors)

answer = triangle_number
elapsed = time.time() - start
print("The answer is %s." % answer)
print("Solved in %s seconds." % round_sig(elapsed))
signal.alarm(0)
