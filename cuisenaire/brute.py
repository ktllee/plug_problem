# -*- coding: utf-8 -*-
"""
last modified: aug 7, 2022

@author: katie

description:
    contains functions to "brute force" data involving rod sets
    (for problems involving sets of cuisenaire rods)
    
    note: many of the functions SHOULD NOT be run on a large scale
    
    functions:
        multi - finds all multisets up to a certain length
        expandall - finds all members of a tree by expanding only
        growsearch - finds rod sets with particular growth rate
        
    dependencies:
        itertools as it
        numpy as np
        math
        Rodset class from rods.py
        
        tqdm (optional for convenience with big datasets)
        
"""

# dependencies
import itertools as it
import numpy as np
import math
from rods import Rodset
from tqdm import tqdm

# aliases
comb = it.combinations_with_replacement
polyroots = np.polynomial.polynomial.polyroots


# the function
def multi(length, limit):
    ''' takes:
            length - maximum length of the multisets, inclusive
            limit - maximum integer to be included, inclusive
            
        returns: a list of all multisets with positive ints and constraints
        
        finds all multisets with a maximum length (minimum 2) containing
        positive integers up to a maximum limit.
        
        dependencies:
            combinations_with_replacement from itertools as comb
    '''
    
    if not all((isinstance(length, int), isinstance(limit, int))):
        raise TypeError('length and limit must be ints')
        
    if not all(((length > 1), (limit > 0))):
        raise ValueError('limit must be positive and length must be > 1')
    
    # set up a list of integers to be used
    integers = list(range(1, limit + 1))
    
    # initiate a list
    final = []
    
    # find combinations with replacement for each length
    for i in range(2, length + 1):
        final.extend([list(x) for x in comb(integers, i)])
    
    return final


# recursive function to look for all things in a tree by expanding only
def expandall(seed, depth, root = 0, current = 0):
    ''' takes:
            seed - a list of integers
            depth - the depth of tree to try until
            root - where to start from [do not use]
            current - current depth [do not use]
        returns: the whole family to depth levels
        
        finds everything possible in a tree recursively,
        where a tree is created solely by expansion.
    '''
    # base case
    if current > depth:
        return None
    
    # account for latest "root" (e.g the root is 2 for the 2-leg in [2,3])
    start = [x + root for x in seed]
    
    # initialize family list
    combos = [[] for i in range(len(start))]
    
    # finds all possible prunings for each leg recursively
    for i in range(len(start)):
        combos[i].append([start[i]])
        deeper = expandall(seed, depth, start[i], current + 1)
        if deeper != None:
            combos[i].extend(deeper)
    
    # combine different legs by taking all combos
    final = [[]]
    for i in range(len(start)):
        new = []
        for semi in final:
            for piece in combos[i]:
                listy = semi + piece
                listy.sort()
                new.append(listy)
        final = new
    
    return final


# find rod sets of a certain size that have a particular growth rate
### ! NOT CERTAIN THIS IS FUNCTIONAL BUT ABANDONED BECAUSE FAMILY REDEF
def growthsearch(seed, maxcount, maxlen = 50, tol = 0.01, tune = True):
    ''' takes:
            seed - base rod set to match to
            maxcount - max number of rods in set
            maxlen - the largest rod length to test to
            tol - the tolerance to keep testing to*
        returns: all rod sets with reasonable growth rate matches
        
        finds rod sets with matching growth rates up to a max number of rods.
        riffs on ethan's idea to close in on a growth rate.
        
        *tol sets a value of difference in growth rates at which to stop
        where the difference is (growth - 1)*tol.
    '''
    # checks
    if not all((isinstance(maxcount, int), isinstance(maxlen, int))):
        raise TypeError('maxcount and maxlen must be positive integers')
    if not isinstance(tol, float):
        raise TypeError('tol must be a float')
    if (tol < 0) or (tol > 1):
        raise ValueError('tol must be between 0 and 1')
    
    # debugging
    tester = False
    
    # set up initial rodset
    start = Rodset(seed)
    growth = start.growth
    tol_scaled = (growth - 1) * (1 - tol)
    found = []
    progress = tqdm(desc = 'current first rod', total = maxlen)
    
    # function to move from one candidate to next when one rod is at max
    def reducemax(candlist, maxlen = maxlen, tune = tune):
        # find the rod at maximum
        maxind = candlist.index(maxlen)
        # stop if all of them are
        if maxind == 0:
            if tune:
                print('reached full max rods')
            return None
        # if the second one is, go to the next first rod
        elif maxind == 1:
            candlist = [candlist[0] + 1, candlist[0] + 1]
            progress.update(candlist[0])
        # if it's any other, remove it and increase the one before it
        else:
            candlist[maxind - 1] += 1
            candlist = candlist[:maxind]
        return candlist
    
    # search through everything with maxcount or fewer rods
    # with all rods of length <= maxlen
    # first candidate
    candlist = [1, 1]
    progress.update(1)
    try:
        while True:
            # find growthrate
            counts = Rodset.spotcon(candlist)
            coeffs = \
                [-counts[x + 1] for x in range(max(counts.keys()))][::-1] + [1]
            candgrowth = max(np.round(np.abs(polyroots(coeffs)), 10))
            diff = growth - candgrowth
            
            # debugging
            if tester:
                print(candlist)
                print('growth:', growth, ', candgrowth:', candgrowth)
            
            # add to list if the current candidate matches
            if diff == 0:
                found.append(candlist.copy())
                # try a set with a larger rod if possible
                if any([x >= maxlen for x in candlist]):
                    candlist = reducemax(candlist)
                    if candlist == None:
                        break
                else:
                    candlist[-1] += 1
            
            # if cand growth is too small
            elif diff > 0:
                # if possible, add a rod
                if maxcount > len(candlist):
                    candlist.append(candlist[-1])
                # if rod limit has been reached:
                else:
                    # stop if all rods are the same
                    if len(set(candlist)) == 1:
                        if tune:
                            print('reached max identical set')
                        break
                    # stop if difference is too much
                    if diff > tol_scaled:
                        if tune:
                            print('reached tolerance')
                        break
                    # skip to next if a rod is too large
                    if any([x >= maxlen for x in candlist]):
                        candlist = reducemax(candlist)
                        if candlist == None:
                            break
                    # otherwise remove the final rod and increase
                    else:
                        candlist[-2] += 1
                        candlist = candlist[:-1]
                        
            # if cand growth is too large
            elif diff < 0:
                if any([x >= maxlen for x in candlist]):
                    candlist = reducemax(candlist)
                    if candlist == None:
                        break
                else:
                    candlist[-1] += 1
                
    except KeyboardInterrupt:
        print('manual interrupt.')
        progress.close()
        return found
            
    progress.close()
    return found


# find rod sets of a certain size that have a particular growth rate
# and which only have a specified number or unique rods
def twosearch(seed, maxcount, maxlen = 50, setlim = 2):
    ''' takes:
            seed - base rod set to match to
            maxcount - max number of each type of rod in set
            maxlen - the largest rod length (abs)
            setlim - number of unique rod lengths (default 2)
        returns: all rod sets in a family with limited unique rods
        
        finds rod sets in a family with only a certain number of rods.
    '''
    # checks
    if not all((isinstance(maxcount, int),
                isinstance(maxlen, int),
                isinstance(setlim, int))):
        raise TypeError('maximums must be positive integers')
    
    # debugging
    tester = False
    
    # set up initial rodset, list of found
    start = Rodset(seed)
    base = start.coefs
    found = []
    
    # generate list of possibilities to use
    candlist = it.product(it.combinations(range(1, maxlen + 1), setlim),
                          it.product(range(1, maxcount + 1), repeat = setlim),
                          it.product([-1, 1], repeat = setlim))
    total = math.comb(maxlen, setlim) * (maxcount**setlim) * (2**setlim)
    
    # search everything
    try:
        for info in tqdm(candlist, total = total):
            cand = [0] * (info[0][-1] + 1)
            for i in range(setlim):
                cand[info[0][-1] - info[0][i]] = info[1][i] * info[2][i]
            cand[-1] = 1
            
            if tester:
                print(info, cand)
            
            if all(np.polydiv(cand, base)[1] == 0):
                cand.pop(-1)
                rods = {}
                for i in range(len(cand)):
                    if cand[i] != 0:
                        if cand[i] < 0:
                            rods[len(cand) - i] = cand[i] * -1
                        else:
                            rods[(len(cand) - i) * -1] = cand[i]
                    
                found.append(rods)
                
    except KeyboardInterrupt:
        print('manual interrupt.')
        return found
            
    return found


##################################################
# uses
# a few different start combinations to use
start = list(range(1, 31))
tworod = it.combinations(start, 2)
threerod = it.combinations(start, 3)


# big data search
def everything(maxcount, maxlen, path):
    ''' takes:
            maxcount - maximum number of rods per rodset
            maxlen - maximum length of any single rod
            path - path to text file to save the data
        returns: None
        
        saves a bunch of data, no particular family just everything
        gives a progress bar
    '''
    for x in tqdm(multi(maxcount, maxlen)):
        attr = Rodset(x)
        print(x, attr.growth, attr.minimal, attr.shift, sep = '\t',
              file = open(path, 'a'))
    return


# debbie request - twos
import pandas as pd
def twos(path, seed, maxcount, maxlen, setlim = 2):
    ''' takes:
            path - path to text file to save the data
            seed - base rod set to match to
            maxcount - max number of each type of rod in set
            maxlen - the largest rod length (abs)
            setlim - number of unique rod lengths (default 2)
        returns: none
        
        saves sets with two kinds of rods.
    '''
    
    final = pd.DataFrame({'rods': twosearch(seed, maxcount, maxlen, setlim)})
    final.to_csv(path, sep = '\t', index = False)
    
        
















