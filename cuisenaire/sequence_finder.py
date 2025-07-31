#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
last modified: 2025-01-20

@author: katie

description:
    for finding patterns in recursions
    
next: make it work for larger max(R).
"""

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
def seq_search(seed = [2,3], maxn = 100):
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
    seq = seq_gen(seed, maxn)
    
    # layers of requirements
    r = max([abs(x) for x in seed]) - 1
    
    # check through for each term
    final = []
    try:
        for i in tqdm(range(1, maxn)):
            
            # find any even divisors
            rems = [False if x == 0 else (seq[i] % x) == 0 for x in seq[:i]]
                
            # indices of even divisors
            xbs = [i for i, x in enumerate(rems) if (x and (i >= r))]
            for j in xbs:
                # no 0s
                if any([seq[j - k] == 0 for k in range(r)]):
                    continue
                
                # check through for even divisors, up to r below
                good = True
                for k in range(r):
                    # using integer division to avoid float limits
                    if  (seq[i - k] % seq[j - k] != 0) or \
                        (seq[i - k] // seq[j - k]) != (seq[i] // seq[j]):
                            good = False
                            break
                
                # add remaining good ones to final
                if good:
                    # send back x, f(x) and x-b, f(x-b)
                    # note, can add others back by adding to [i, j]
                    final.append([[i+1, i-j]] + [(k, seq[k]) for k in [i, j]])
                
    except KeyboardInterrupt:
         print('manual interrupt.')
         return final
        
    return final
















