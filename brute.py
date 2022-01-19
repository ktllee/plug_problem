#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 15:11:37 2021

@author: katie
"""

# trying to brute force backwards flow on trees
# dependencies
import itertools as it

# initializing a few different start combinations
start = list(range(1, 21))
tworod = it.combinations(start, 2)
threerod = it.combinations(start, 3)

# recursive function to look for all possible equalities
def family(base, depth, root = 0, current = 0):
    ''' takes:
            base - a list of integers
            depth - the depth of tree to try until
            root - where to start from
            current - current depth
        returns: the whole family to depth
        
        does the thing recursively
    '''
    # base case
    if current > depth:
        return None
    
    # start with root
    start = [x + root for x in base]
    
    # initialize family list
    combos = [[] for i in range(len(start))]
    
    # creates a tree and finds all possible prunings
    for i in range(len(start)):
        combos[i].append([start[i]])
        deeper = family(start, depth, start[i], current + 1)
        if deeper != None:
            combos[i].extend(deeper)
    
    # combine legs
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

# function to look through a list for backwards
def backwards(base, equal):
    ''' takes:
            base - a list of integers
            equal - a list to look through
        returns: a list of backwards-possible combos
        
        does the thing recursively
    '''
    # differences
    ordered = sorted(base)
    diff = [x - ordered[0] for x in ordered]
    
    # sorted equal
    fixed = [sorted(x) for x in equal]
    
    # looking through lists
    maybe = []
    for state in fixed:
        for group in it.combinations(state, len(diff)):
            ordy = sorted(group)
            norm = [x - ordy[0] for x in ordy]
            
            if norm == diff:
                maybe.append([state, group])
                
    # check through maybes
    final = []
    for possible in maybe:
        poss = possible[0].copy()
        for piece in possible[1]:
            poss.remove(piece)
        poss.append(possible[1][0] - ordered[0])
        poss.sort()
        if poss not in fixed:
            final.append([poss, possible[0]])
            
    return final

if False:
    # looking for others backwards with two as base
    for base in tworod:
        group = family(base, 1)
        result = backwards(base, group)
        
        if len(result) > 1:
            print(result)
            
    print("---")
            
    # three as a base
    for base in threerod:
        group = family(base, 1)
        result = backwards(base, group)
        
        if len(result) > 1:
            print(result)
        



















