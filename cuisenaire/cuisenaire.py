# -*- coding: utf-8 -*-
"""
main code to explore families of finite rod sets

last modified: jul 6, 2022

@author: Ethan Bolker, Katie Lee

to do: 

Refactor to get remove translations to and from  bitstrings. 
Rod sets are now specified by lists of rod lengths.

Improve plotroots so that it plots all the circles corresponding to 
the roots of the minimal polynomial, not just the one for the growth 
rate.
- problem same as below

Add to rodsetattributes
    data.shiftpoly({"shiftpoly":spolystr})
containing the shift polynomial - that's the
quotient of the cpoly and the minimal poly.
- problem: the code in rodsetattributes knows only the
  growth rate, not the factor of the cpoly that's the
  minimal polynomial. If we can't easily figure this
  out here, we might have to do it in findfamilies, when we 
  know the minimal polynomial because it's (usually) the
  first one encountered.
"""

## dependencies

# from packages
import sys

import numpy as np
import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt

from sympy import factor as factor
from itertools import combinations

# from directory
from multiset import multi

######################################
## helpers and shortcuts

def gcd(mylist):
    '''shortcut to allow for gcd of a list'''
    return np.gcd.reduce(mylist)

#     zzzzzzzzz
def build_recursion_polynomial(spots):
    ''' from input spots = [1,2,2,2,4] build recursion polynomial
        x**3 - 3*x**2 - x**1 - 1
    '''    
    coeffs = build_cuisenaire_poly_coefficients(spots)
    polystr = str(coeffs[0])
    for i in range(1,len(coeffs)-1):
        if coeffs[i] != 0:
            c = coeffs[i]
            if c > 0:
                sign = str('+')
            else:
                sign = str('-')            
            polystr +=  sign +  str(abs(c)) + '*x**' + str(i)
    polystr += '+ x**' + str(len(coeffs)-1)
    return polystr

def growthrate(rods):
    coeffs = build_cuisenaire_poly_coefficients(rods)
    r1 = poly.polyroots(coeffs)
#     maxroot = np.round(np.abs(max(r1)),10)
    maxroot = np.abs(max(r1))
    return maxroot
    
def rodsetattributes(input):
    ''' Create dictionary of attributes the input rod set.
        Rod set should really be an object.
    '''
#     if isinstance(input, str): # d is a bitstring like "101"
#         bits = input
#     elif isinstance(input, list):
#         bits = spots2bitstring(input)
#     else:
#         print(f"type error {input}")
#         return
    data = {}
    mypoly = build_recursion_polynomial(input)
    fpoly = factor(mypoly)
    coeffs = build_cuisenaire_poly_coefficients(input)    
#     print("xxx mypoly", mypoly)
#     print("xxx fpoly", fpoly)
#     print("xxx", coeffs)
    r1      = poly.polyroots(coeffs)
    maxroot = np.round(max(np.abs(r1)),10)
    theroots = list(np.round(np.abs(r1),3))
    rootlengths = list(set(theroots))    
    fpolystr = str(fpoly)
    fpolystr = fpolystr.replace("**","^").replace("*","").replace("^1 ","").replace("1x","x")        
    mypolystr = str(mypoly)
    mypolystr = mypolystr.replace("**","^").replace("*","").replace("^1 ","").replace("1x","x").replace("^1-","-")
#     data.update({"bits":bits})
    data.update({"spots":input})
    data.update({"growthrate":maxroot})
    data.update({"cpoly":mypolystr})
    data.update({"factors":fpolystr})
#     data.update({"roots":theroots})
    data.update({"rootlengths":rootlengths})            
    return data

# should rewrite this function to call rodsetattributes(input)
def csvout(input):
    ''' Print string with data about the input (bit string or rod set)
        suitable for spreadsheet input. 
        Use '@' rather than a comma as the delimiter.
    '''
    if isinstance(input, str): # d is a bitstring like "101"
        bits = input
    elif isinstance(input, list):
        ##! remember to add check for integer elements of list, etc.
        
        ['1' if x in input else '0' for x in range(1, max(input))]
        bits = spots2bitstring(input)
    else:
        print(f"type error {input}")
        return
    mypoly = build_recursion_polynomial(input)
    fpoly = factor(mypoly)
    coeffs = build_cuisenaire_poly_coefficients(input)
    r1 = poly.polyroots(coeffs)
    maxroot = np.round(np.abs(max(r1)),10)
    theroots = list(np.round(np.abs(r1),3))
    print(f"{bits}@ {input}@ {maxroot}@ {mypoly}@ {fpoly} @ {theroots}")
    return

csvheader="d@ spots@ growth rate@ poly@ factored@ |roots|"    

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

# This should be refactored to call rodcount(limit, count)
def rodcountcsv( limit, count):
    ''' Print spreadsheet input for all cuisenaire rod sets of 
        length up to limit using at most count rods
    '''
#     print(f"count {count} limit {limit}")
    print(csvheader)
    possibles = list(range(limit+1)[1:])
    counts = list(range(count+1))[1:]
    for j in counts:
        spotsets = rSubset( possibles, j)
        for spots in spotsets:
            csvout(list(spots))
    return 

# yyyyyyyyyy
def build_cuisenaire_poly_coefficients(rods):
#     degree = rods[len(rods)-1] # last entry
#     degree = max(rods)
    degree = max(max(rods),-min(rods))
    if degree==max(rods):
        globalsign = 1
    else:
        globalsign = -1
    coeffs = [0]*(degree+1)
    for r in rods:
#         print(r, sign(r))        
#         coeffs[degree-abs(r)] += -1
        coeffs[degree-abs(r)] -= np.sign(r)*globalsign
#         print(r, sign(r))
    coeffs[degree] = 1
#     print(coeffs)
    return coeffs

def get_cuisenaire_poly_roots(rods):
    coeffs = build_cuisenaire_poly_coefficients(rods)
    return np.array(poly.polyroots(coeffs))

def plotroots(rods):
    # plot the roots     
    data = get_cuisenaire_poly_roots(rods)
    x = data.real
    y = data.imag

    # plot the circle through the largest root
    r = growthrate(rods);
    theta = np.linspace(0, 2*np.pi, 100)
    x1 = r*np.cos(theta)
    x2 = r*np.sin(theta)

    fig, ax = plt.subplots(1)
    ax.plot(x, y, 'b*')
    plt.xlabel(str(rods))
    ax.plot(x1, x2,'r')
    ax.set_aspect(1)
    plt.xlim(-2,2)
    plt.ylim(-2,2)

    plt.show()    
    
def checkAP(spots, m):
    print(f"{spots} + {m}k")
    max = 80
    equiv = spots + list([m])
    equiv.sort()
    long = spots.copy()
    for r in spots:
        nextr = r+m
        while nextr < max:
            long.append(nextr)
            nextr += m
    long.sort()
    print(f"{long} {growthrate(long)}")
    print(f"{equiv} {growthrate(equiv)}")

def xfindfamilies( limit, count):
    ''' Collect cuisenaire rod sets of 
        length up to limit using at most count rods
        into families keyed by growthrate.
    '''
    families = {}    
#     print(f"count {count} limit {limit}")
    possibles = list(range(limit+1)[1:])
    counts = list(range(count+1))[1:]
    for j in counts:
        spotsets = rSubset( possibles, j)
        for spots in spotsets:
            if gcd(spots) > 1:
                break
            attributes = rodsetattributes(list(spots))
            key = attributes.get("growthrate")
            if families.get(key) == None:
                families[key] = [list(attributes["spots"])]
            else:
                families[key].append(list(attributes["spots"]))
    return families

def findfamilies( length, count):
    ''' Collect cuisenaire rod sets of 
        length up to length using at most count rods
        into families keyed by growthrate.
    '''
    families = {}
    spotsetattributes = rodcountmultisets(length, count )
    for spots in spotsetattributes:
        
#         if len(spots['bits']) == 1:
#             continue
        key = spots.get("growthrate")
#         print(key)
        if families.get(key) == None:
#             families[key] = spots
            families[key] = []
        families[key].append(spots)
    return families

# zzzzzzzzzz
def rodcountmultisets( length, limit):
    ''' Create list of attributes for all cuisenaire rod multisets of 
        length up to limit using at most count rods
    '''
    rodcounts = []
    spotsets = multi(length, limit)
    for spots in spotsets:
        if len(spots) == 1:
            continue
#             if mygcd(spots) > 1:
#                 continue
        attributes = rodsetattributes(list(spots))
        rodcounts.append(attributes)
    return rodcounts

def rodcount( limit, count):
    ''' Create list of attributes for all cuisenaire rod sets of 
        length up to limit using at most count rods
    '''
    rodcounts = []
    possibles = list(range(limit+1)[1:])
    counts = list(range(count+1))[1:]
    for j in counts:
        spotsets = rSubset( possibles, j)
        for spots in spotsets:
#             if mygcd(spots) > 1:
#                 continue
            attributes = rodsetattributes(list(spots))
            rodcounts.append(attributes)
    return rodcounts


def findrodsfor(target, epsilon, rods=None):
#     print(f"target {target} epsilon {epsilon} start {rods}")
    if rods is None:
        rods = [1] 
    g = growthrate(rods)
    if g > target:
        print("target smaller than start")
        return rods
    while np.abs(target-g) > epsilon:
        while g < target:
            rods.append(rods[-1])
            g = growthrate(rods)        
        rods[-1] = 1+rods[-1]
        g = growthrate(rods)    
#         print(f"{rods} {g}")
    return(rods)

def findrodsclassicfor(target, epsilon):
#     print(f"{target} {epsilon}")
    rods = [1]
    g = growthrate(rods)
    print(f"{rods} {g}")    
    while np.abs(target-g) > epsilon:
        rods.append(1+rods[-1])
        g = growthrate(rods)
#         print(f"{rods} {g}")            
        while g > target:
            rods[-1] = 1+rods[-1]
            g = growthrate(rods)
    return(rods)

def hasduplicates(listOfElems, skipstart= 0):
    ''' Check if given list contains any duplicates 
        ignoring first skipstart items
    '''
    return not len(listOfElems[skipstart:]) == len(set(listOfElems[skipstart:]))

def compareg(rods, extra):
    g = growthrate(rods)
    rods.append(extra)
    gx = growthrate(rods)
    return rods, extra, gx-g

def buildtree(rods, level):
    ''' find rod sets in the tree build by expanding
        the rods in R by R
    '''
    tree = [[rods]]
    for i in range(level):
        nextlevel =[]
        for rodset in tree[i]:
            for r in rodset:
                next = rodset.copy()
                next.remove(r)
                for s in rods:
                    next.append(r+s)
                next.sort()
                nextlevel.append(next)
        tree.append(nextlevel)
    return tree


def commonexpansion(rods1, rods2, depth):
    from itertools import chain    
    t1 = buildtree(rods1, depth);
    t2 = buildtree(rods2, depth);
    f1 = list(chain(*t1))
    f2 = list(chain(*t2))    
    return [value for value in f1 if value in f2]    

def cpolyisminimal(rods):
    data = rodsetattributes(rods)
    return not "(" in data.get("factors")

def getrandomrodset(length, candidates):
    rods = length*[0]
    for i in range(length):
        rods[-i] =  np.random.choice(candidates)
    return list(np.sort(rods))

def countminimalcpolys(count, length, rodrange):
    ''' find the proportion of rod sets with minimal cpoly
    in a random selection of count rod sets of given length
    with elemens chosen from rodrange.
    '''
    minimalcount = 0
    for i in range(count):
        rods = getrandomrodset(length, rodrange)
#         print(i,rods)
        if cpolyisminimal(rods):
            minimalcount += 1
#         else:
#             print(rodsetattributes(rods))
    return minimalcount/count
    
###  code to execute here
if __name__ == "__main__":

## default:
##   Print details about rod set from command line
    
    if len(sys.argv) > 1:       
        rodset =  list(map(int, sys.argv[1:]))
        print(rodsetattributes( rodset))
        plotroots(rodset)
