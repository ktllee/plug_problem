#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
last modified: 2024-10-02

@author: katie

description:
    for finding patterns in recursions
"""

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
            [(x, f(x)), (x-1, f(x-1)), (x-b, f(x-b)), (x-b-1, f(x-b-1))]
            
            where f(x)/f(x-b) = f(x-1)/f(x-b-1) and
            quotients have no remainder.
    '''
    # get the sequence
    seq = seq_gen(seed, maxn)
    
    # check through for each term
    final = []
    for i in range(1, maxn):
        
        # find any even divisors
        rems = [False if x == 0 else (seq[i] % x) == 0 for x in seq[:i]]
            
        # check through for even divisors right below
        xbs = [i for i, x in enumerate(rems) if x]
        for j in xbs:
            if (j == 0) or (seq[j - 1] == 0):
                continue
            if (seq[i - 1] / seq[j - 1]) == (seq[i] / seq[j]):
                final.append([(k, seq[k]) for k in [i, i-1, j, j-1]])
        
    return final
















