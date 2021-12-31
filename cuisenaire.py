"""
Code to explore families of finite rod sets

Usage: uncomment fragments after the line
###  code to execute here

last modified: 12/31/2021

@author: Ethan Bolker

to do: refactor to get remove the bitstrings. 
Rod sets are specified by lists of rod lengths.
"""
import sys
import math
from utilities import *
from multi import multi
from convolve import p2t
from sympy import roots as sroots
from sympy import solve as solve
from sympy import factor as factor
from numpy import *
import numpy as np
import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt

from itertools import combinations

def mygcd(mylist):
    if len(mylist) == 1:
        return mylist[0]
    else:
        return math.gcd( mylist[0],mygcd(mylist[1:]))

def build_recursion_polynomial(spots):
    ''' from input spots = [1,2,2,2,4] build recursion polynomial
        x**3 - 3*x**2 - x**1 - 1
    '''    
    coeffs = build_cuisenaire_poly_coefficients(spots)
#     print(coeffs)
    polystr = str(coeffs[0])
    for i in range(1,len(coeffs)-1):
        if coeffs[i] != 0:
            polystr += str(coeffs[i]) + '*x**' + str(i)
    polystr += '+ x**' + str(len(coeffs)-1)
    return polystr
    
def build_recursion_polynomial_coeffs(bits):
    ''' from input bit string 1011 build recursion polynomial
        coefficients as list [-1, -1, 0, -1, 1].
        Coefficients from constant term to degree 4.
    '''
    n = len(bits)
    coeffs = [1]
    for j in range(n)[:-1]:
        b = int(bits[j])
        coeffs.append(-b)
    coeffs.append(-1)        
    coeffs.reverse()
    return coeffs

# This function is no longer called. The growth rate is
# the largest root of the Cuisenaire polynomial.
def xgrowthrate(d):
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
    rate =  (totals[goodspot + gcd]/totals[goodspot])**(1/gcd)
    return(rate)

def growthrate(rods):
    coeffs = build_cuisenaire_poly_coefficients(rods)
    r1 = poly.polyroots(coeffs)
#     maxroot = np.round(np.abs(max(r1)),10)
    maxroot = np.abs(max(r1))
    return maxroot
    
def rodsetattributes(input):
    ''' Create dictionary of attributes the input (rod set, maybe bit string).
        Rod set should really be an object.
    '''
    if isinstance(input, str): # d is a bitstring like "101"
        bits = input
    elif isinstance(input, list):
        bits = spots2bitstring(input)
    else:
        print(f"type error {input}")
        return
    data = {}
    mypoly = build_recursion_polynomial(input)
    fpoly = factor(mypoly)
    coeffs = build_cuisenaire_poly_coefficients(input)
    r1 = poly.polyroots(coeffs)
    maxroot = np.round(np.abs(max(r1)),10)
    theroots = list(np.round(np.abs(r1),3))
#     data.update({"bits":bits})
    data.update({"spots":input})
    data.update({"growthrate":maxroot})
    data.update({"cpoly":mypoly})
    data.update({"factors":fpoly})
#     data.update({"roots":theroots})        
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

def build_cuisenaire_poly_coefficients(rods):
#     degree = rods[len(rods)-1] # last entry
    degree = max(rods)
    coeffs = [0]*(degree+1)
    for r in rods:
        coeffs[degree-r] += -1 
    coeffs[degree] = 1
    return coeffs

def get_cuisenaire_poly_roots(rods):
    coeffs = build_cuisenaire_poly_coefficients(rods)
    return np.array(poly.polyroots(coeffs))

def plotroots(rods):
    # plot the roots     
    data = get_cuisenaire_poly_roots(rods)
    x = data.real
    y = data.imag

    # plot the unit circle
    theta = np.linspace(0, 2*np.pi, 100)
    r = np.sqrt(1.0)
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
            if mygcd(spots) > 1:
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
        if len(spots['bits']) == 1:
            continue
#         print(spots)
#         print()
        key = spots.get("growthrate")
#         print(key)
        if families.get(key) == None:
#             families[key] = spots
            families[key] = []
        families[key].append(spots)
    return families

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

###  code to execute here
if __name__ == "__main__":

##    Print details about any particular rod set
     print(rodsetattributes([1,2]))

##    Print the tree of expansions of a rod set to specified depth    
#     rods = [2,3]    
#     tree23 = buildtree(rods,3)
#     for level in tree23:
#         print(level)

##    Print the intersection of the trees from two rod sets
#     print(commonexpansion([1,5],[2,3],3))

##    Print the growthrate for a rod set
#     print(growthrate([1,3,4]))

##    Print the start of infinite rod set for a given growthrate
#     to specified precision with optional beginning
#     rate = growthrate([3,4])
#     eps = 0.0000001
#     print(findrodsfor(rate, eps))
#     print(findrodsfor(rate, eps, rods=[2]))
#     print(findrodsfor(rate, eps, [3]))        

######################################################################
#     
#     Only special purpose code from here on
#     
#     print(f"{growthrate([1,10,20])}")
#     print(f"{growthrate([1,10,10,20])}")        
#     print(compareg([1,10,20], 10))    

#     check to see if we ever get nonclassic rod sets
#     start = 1.1
#     step = 0.001
#     epsilon = 0.00000001
#     count = 10
#     for i in range(count):
#         rate = start + i*step
#         rods = findrodsfor(rate, epsilon)
#         print(rods)
#         if hasduplicates(rods):
#             print(rate, rods)

#     eps = 0.00000001
#     rate = 1.6
#     print(findrodsfor(rate, eps))
#     print(findrodsfor(rate, eps, rods=[2]))
#     print(findrodsfor(rate, eps, rods=[3]))
#     print(findrodsfor(rate, eps, rods=[4]))
#     print(findrodsfor(rate, eps, rods=[2,5]))                
    
#     print(hasduplicates([1,2,3]))
#     print(hasduplicates([1,2,2]))    
#     print(findrodsfor(rate, eps,[2]))    
#     print(findrodsfor(rate, eps,[3]))
#     print(findrodsfor(rate, eps,[4]))    
#     print(findrodsclassicfor(rate,eps))

                
#     rods=[1]
#     for j in range(100):
#         rods.append
#         print(f"{growthrate(rods)}")

        
#     findrodsfor(3.5, 0.00000001)
#     findrodsfor(sqrt(2), 0.00000001)

#     families = findfamilies(2,50)
#     for f in families.values():
#         if len(f) > 1:
#             print()

#  put families into latex table
#     families = findfamilies(6,10)
#     for f in families.values():
#         if len(f) > 4:
#             print()
#             print("\\documentclass{standalone}")
#             print("\\begin{document}")
#             print()
#             print("\\begin{tabular}{llllllllllllllllllll}")
#             allspots = list(f[i]['spots'] for i in range(len(f)))
#             allspots.sort(key=max)
#             allspots.sort(key=len)            
#             row = len(allspots[0])
#             count = 0            
#             for spots in allspots:
#                 if row != len(spots):
#                     print(" \\\\")
#                     print(" \\\\")
#                     print(" \\\\")
#                     print(" \\\\")                    
#                     row = len(spots)
#                     count = 0
#                 if count > 7:
#                     print(" \\\\")
#                     print(" \\\\")                    
#                     print("", end="")
#                     count = 0
#                 count += 1
#                 print("$"+str(spots).replace(" ",""), end="$ & ")
#             print()
#             print("\\end{tabular}")
#             print("\\end{document}")            
#     testing sorting
#     ll = [[1, 6, 10],[1, 7, 8],[2, 4, 8],[2, 5, 6],[3, 3, 7],[3, 4, 5]]
#     print(ll)
#     ll.sort()
#     print(ll)        
#     ll.sort(key=max)
#     print(ll)    

#     families = findfamilies(3,3)
#     for f in families.values():
#         if len(f) > 1:
#             print(f"{f[0]['growthrate']}")
#             for i in range(len(f)):
#                 cpoly = str(f[i]['cpoly']).replace("**","^")
#                 cpoly = cpoly.replace("*","")
#                 cpoly = cpoly.replace("^1","")                                
#                 factors = str(f[i]['factors']).replace("**","^")
#                 factors = factors.replace("*","")
#                 factors = factors.replace("^1","")           
#                 print(f"@{f[i]['spots']}@{cpoly}@{factors}")
#                 print

#     csvout([1,3])
#     csvout([3,5,5,5,6,7,7])
#     csvout([1,2,2,2,4])
#     print(rodsetattributes([1,2,2,2,4]))
#     csvout([1,3,4])
#     print(rodsetattributes([1,3,4]))

#     rods = [1,3,5,7,9,11,13,15,16]
#     rods= [1, 4, 7, 10, 12]
#     plotroots(rods)
    
#     find all rod sets of length 2, extract growthrate and rods for excel
#       data = rodcount(40,2)
#       for spots in data:
#           if len(spots["spots"]) == 2:
#               print(f"{spots['spots']}@{spots['spots'][0]}@{spots['spots'][1]}@ {spots['growthrate']} ")
                 
