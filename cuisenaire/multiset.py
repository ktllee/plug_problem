#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 18:26:00 2021

@author: katie

function to find multisets
"""

# dependencies
from itertools import combinations_with_replacement as comb

# the function
def multi(length, limit):
    ''' takes:
            length - maximum length of the multisets, inclusive
            limit - maximum integer to be included, inclusive
            
        returns: a list of all multisets with positive ints and constraints
        
        finds all multisets with a maximum length containing
        positive integers up to a maximum limit.
        
        dependant on itertools package.
    '''
    
    if not all((isinstance(length, int), isinstance(limit, int))):
        raise TypeError('length and limit must be ints')
        
    if not all(((length > 0), (limit > 0))):
        raise ValueError('length and limit must be positive')
    
    # set up a list of integers to be used
    integers = list(range(1, limit + 1))
    
    # initiate a list
    final = []
    
    # find combinations with replacement for each length
    for i in range(1, length + 1):
        final.extend([list(x) for x in comb(integers, i)])
    
    return final