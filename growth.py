"""
code to calculate growth rate for plug puzzles using
arbitrary numbers of cuisenaire plugs C_k = 11....1

last modified: 08/01/21

@author: Ethan Bolker
"""
import sys
import math
from convolve import p2t
from sympy import roots as sroots
from sympy import solve as solve
from sympy import factor as factor
from numpy import *
from utilities import *
from itertools import combinations

def mygcd(mylist):
    if len(mylist) == 1:
        return mylist[0]
    else:
        return math.gcd( mylist[0],mygcd(mylist[1:]))

def build_recursion_polynomial(bits):
    ''' from input bit string 1011 build recursion polynomial
        x**4 - x**3 -x**1 -1
    '''
    n = len(bits)
    polystr = 'x**'
    polystr += str(n)
    for j in range(n)[:-1]:
        b = int(bits[j])
        if b > 0:
            polystr += ('-x**') + str(n-j-1)
    polystr += '-1'
    return polystr

def build_recursion_polynomial_coeffs(bits):
    ''' from input bit string 1011 build recursion polynomial
        coefficients as list [1, -1, 0, -1, -1]
    '''
    n = len(bits)
    coeffs = [1]
    for j in range(n)[:-1]:
        b = int(bits[j])
        coeffs.append(-b)
    coeffs.append(-1)        
    return coeffs

    
def growthrate(d):
    ''' Calculate the growth rate for total solutions
    for the puzzle problem R(d). Here d is the  
    bit string specifying which C_k are allowed, 
    or that bit string as a plug number, 
    or a list [a,b,...] of positions of 1 bits.
    The algorithm pads with lots of 0s to stabilize growth.
    Adjusts when gcd of plug lengths > 1.
    '''
    if isinstance(d, str): # d is a bitstring like "101"
        xd = bitstring2bits(d)
    elif isinstance(d, int): # convert integer d to binary
        xd = [int(i) for i in bin(d)[2:]]
    elif isinstance(d, list):
        xd = spots2bits(d)
    else:
        print(f"type error {d}")
        return
    spots = bits2spots(xd)
    gcd = mygcd(spots)
    spotsum = sum(spots)
    expand = 300
    lookat = expand*gcd
    zeros = 2*lookat
    goodspot = spotsum + lookat - 1
    xd.extend([0]*zeros)
    totals = p2t(xd)
#     print(f"spots {spots} gcd {gcd} sum {spotsum}")
#     print(f"looking {totals[spotsum-1]} {totals[gcd+spotsum-1]}")
#     print(f"looking {totals[goodspot]} {totals[goodspot + gcd]}")
    rate =  (totals[goodspot + gcd]/totals[goodspot])**(1/gcd)
    return(rate)

def csvout(input):
    ''' Print string with data about the input d
        suitable for spreadsheet input. 
        Use '@' rather than a comma as the delimiter.
    '''
    if isinstance(input, str): # d is a bitstring like "101"
        bits = input
    elif isinstance(input, list):
        bits = spots2bitstring(input)
    else:
        print(f"type error {d}")
        return
    mypoly = build_recursion_polynomial(bits)
    fpoly = factor(mypoly)
    coeffs = build_recursion_polynomial_coeffs(bits)
    print(f"{bits}@ {bitstring2spots(bits)}@ {growthrate(bits)}@ {mypoly}@ {fpoly}")# @ {roots(coeffs)}")            
    return

csvheader="d@ spots@ growth rate@ poly@ factored@ roots"    

def growthratecsv(N):
    ''' Print spreadsheet input for odd plug numbers up to 2**N
        and for those numbers with prefixes 0, 00, 000 and 0000
    '''
    print(csvheader)
    for d in range(1, 1+2**N,2):
        todo = [bin(d)[2:], bin(2*d)[2:][::-1], bin(4*d)[2:][::-1],
                bin(8*d)[2:][::-1], bin(16*d)[2:][::-1] 
        ]
        for bits in todo:
            csvout(bits)
    return

# from //www.geeksforgeeks.org/itertools-combinations-module-python-print-possible-combinations/
def rSubset(arr, r):
    # return list of all subsets of length r
    # to deal with duplicate subsets use 
    # set(list(combinations(arr, r)))
    return list(combinations(arr, r))

def plugcountcsv( limit, count):
    ''' Print spreadsheet input for all cuisenaire plug of 
        length up to limit using at most count plugs
    '''
#     print(f"count {count} limit {limit}")
    print(csvheader)
    possibles = list(range(limit+1)[1:])
#     print(possibles)
#     for j in possibles:
#         print(j)
    counts = list(range(count+1))[1:]
#     print(counts)
    for j in counts:
#         print(j)
        spotsets = rSubset( possibles, j)
#         print(spotsets)
        for spots in spotsets:
            csvout(list(spots))
    return 

# I forget why I started this
# def extend_d(bits):
#     n = 20
#     rate = growthrate(bits)
#     print("len(011001001...001), growthrate, delta")
#     for i in range(n):
#         bits += '001'
#         # print(f"{bits}, {growthrate(bits)}, {poly}, {fpoly}")
#         newrate = growthrate(bits)
#         delta = newrate - rate
#         rate - newrate
#         print(f"{len(bits)}, {growthrate(bits)}, {delta}")        


#  Execute 
if __name__ == "__main__":

    if (len(sys.argv) == 1):
        print(f"usage: python {sys.argv[0]} bits1 bits2 ...")
    else:
         for bits in sys.argv[1:]:
             csvout(bits)             

#     plugcountcsv( 8, 3):             
#     growthratecsv(3)

#     print(roots([1, -1, -1]))
#     print(solve('x**2-x-1'))
#     print(sroots([1, 0, 0, -1]))
#     print(sroots([1, -1, 0, 0, 0, -1]))
#     print(solve('x**5-x-1'))
#     print(roots([1, -1, 0, 0, 0, -1]))    



