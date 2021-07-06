# -*- coding: utf-8 -*-
"""
last modified: 07/06/21

@author: katie

description:
    function for a general overview of solutions given a dictionary of plugs.
    
    overview() takes a dictionary of plugs and returns a pandas dataframe
    of the number of solutions up to n total length.  Also gives completion
    updates.
    
    dependencies:
        pandas (pd)
        time
        
    note: does not currently support plugs with hanging ends
"""

import pandas as pd
import time
from flex_solver import flex
from convolve import *

def overview(plug_list, max_n = 10, style = 's', progress = False):
    ''' takes:
            mandatory:
                plug_list - a list or dict of the plugs to be used.
                (note that lists given assume endless plugs)
            optional:
                n - an int for max total length to go to, default 10.
                style - str of attribute to init Plugs.
                    'z' or 'zero_str' for zero_str,
                    's' or 'str_num' for str_num (default),
                    'n' or 'number' for number,
                    'c' or 'classic' for classic (style only),
                    'p' or 'plug' for full Plugs,
                    'f' or 'full' for full Strips (result_style only)
        returns: a dataframe of number of prime and composite solutions
    '''
    
    # start time for function
    start = time.time()
    
    # init totals and primes lists
    totals = []
    primes = []
    
    # iterate over total lengths in the range
    for n in range(1, max_n + 1):
        solutions = flex(n, plug_list, style = style, result_style = 'f')
        
        # add to total count
        totals.append(len(solutions))
        
        # find and add to primes count
        check = [1 if x.thickness.count(0) == 0 else 0 for x in solutions]
        primes.append(sum(check))
        
        # time check and update printing if progress requested
        if progress:
            current = time.time()
            elapsed = round(start - current)
            print(f'n = {n}, {elapsed}s elapsed.')
        
    # setting up dataframe to be returned
    result = pd.DataFrame(range(1, max_n + 1), columns = ['n'])
    result['total'] = totals
    result['prime'] = primes
    
    return result    