#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 13:06:17 2021

@author: katie

# factors
"""

from strip_class import *

def validate(length):
    ''' takes: n, an int for strip length
        returns: none
    '''
    
    print(f"checking factors at length {length}...")
    print()
    
    # base10 length
    n = 2**length - 1
    
    # find factors of n
    factors = ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)
    
    for pair in factors:
        # first
        num = bin(pair[1])[2:].count('1')
        status1 = True
        try:
            Strip(length, [pair[0]]*num)
        except:
            status1 = False
            
        # second
        num = bin(pair[0])[2:].count('1')
        status2 = True
        try:
            Strip(length, [pair[1]]*num)
        except:
            status2 = False
            
        if status1 == status2:
            print([bin(x)[2:] for x in pair], status1)
        else:
            print([bin(x)[2:] for x in pair], status1, status2, '!')
        
        print()
            
    print('done.')
            
    return


