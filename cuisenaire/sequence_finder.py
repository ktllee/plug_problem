#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
last modified: 2025-08-03

@author: katie

description:
    for finding patterns in recursions
"""

import itertools as it

from tqdm import tqdm

# sequence finder
def seq_gen(seed, n):
    ''' takes:
            seed - list of rods.
            n - number of terms to find.
        
        returns: list of n terms in sequence.
    '''
    # intitial conditions
    final = [1]
    
    # recurse
    for i in range(n):
        
        # ignore initial conditions
        if i <= (len(final) - 1):
            continue
        
        # get next term
        term = 0
        for k in seed:
            if i < abs(k):
                continue
            if k < 0:
                term -= final[i - abs(k)]
            else:
                term += final[i - abs(k)]
            
        final.append(term)
    
    return final

# pattern finder
def seq_search(seed = [2,3], maxn = 100, verbose = True):
    ''' takes:
            seed - list of rods.
            maxn - max number of terms to search to in sequence.
            
        returns:
            list of lists with entries:   
            [[rodset], (x, f(x)), (x-b, f(x-b))]
            
            where f(x)/f(x-b) = f(x-1)/f(x-b-1) and
            quotients have no remainder.
    '''
    # get the sequence
    seq = seq_gen(seed, maxn + 1)
    
    # layers of requirements
    r = max([abs(x) for x in seed]) - 1
    
    # add 0s to the end of seq for n < 0
    seq.extend([0] * r)
    
    # check through for each term
    final = []
    try:
        for i in tqdm(range(maxn)):
            
            # find any even divisors
            if seq[i] == 0:
                xbs = range(maxn)
            else:
                rems = [all((x != 0, (x % seq[i]) == 0)) for x in seq[i:-r]]
                xbs = [y + i for y, x in enumerate(rems) if x]
            
            # check through the even divisors
            for j in xbs:
                # determine ratio
                low = i
                high = j
                # go to next pair if low term is 0
                while seq[low] == 0:
                    high -= 1
                    low -= 1
                # go to next if the below-terms aren't even divisors
                if (seq[high] % seq[low] == 0) and (seq[high] != 0):
                    alpha = seq[high] // seq[low]
                else:
                    continue
                
                # go to next if term above matches the ratio
                if seq[j + 1] == (alpha * seq[i + 1]):
                    continue
                
                # check through for even divisors, up to r below
                good = True
                for k in range(r):
                    # using integer division to avoid float limits
                    if seq[j - k] != (alpha * seq[i - k]):
                        good = False
                        break
                
                # add remaining good ones to final
                if good:
                    # send back a, b, and counts
                    found = [{j - i: alpha,
                              j + 1: seq[j + 1] - (alpha * seq[i + 1])}]
                    # send back x, f(x) and x-b, f(x-b) if verbose
                    if verbose: found.extend([(k, seq[k]) for k in [i, j]])
                    final.append(found)
                    
                
    except KeyboardInterrupt:
         print('manual interrupt.')
         return final
        
    return final

##################################################
# uses

# check all combinations of two rods up to length 5
def two_search(path = '/Users/katie/Downloads/rods.txt', maxlen = 6):
    x = it.product(it.combinations(range(1, maxlen), 2), [1,-1], [1,-1])
    for r, a, b in x:
        
        if max(r) == 2:
            continue
        
        if min(r) != 1 and (r[1] % r[0] == 0):
            continue
        
        rods = [r[0] * a, r[1] * b]
        res = seq_search(rods, 1000, verbose = False)
        
        with open(path, 'a') as text_file:
            print(f"{rods}:\n{res}\n\n", file = text_file)
    return

# check a bunch of combinations of naryana and padovan
def multi_two_search(path = '/Users/katie/Downloads/rods.txt'):
    x = it.product(([2,3], [1,3]), range(1,5), range(1,5), [1,-1], [1,-1])
    for r, s, t, a, b in x:
        
        rods = [r[0] * a] * s + [r[1] * b] * t
        res = seq_search(rods, 1000, verbose = False)
        
        if len(res) > 100:
            res = res[:10]
            res.append('... many more omitted')
        elif len(res) > 10:
            res = res[:10]
            res.append('... a few more omitted')
        
        rodlist = {r[0]: s * a, r[1]: t * b}
        
        with open(path, 'a') as text_file:
             print(f"{rodlist}:\n{res}\n\n", file = text_file)
            
    return












