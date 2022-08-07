# -*- coding: utf-8 -*-
"""
last modified: aug 6, 2022

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
        Rodset class from rods.py
        
        tqdm (optional for convenience with big datasets)
        
"""

# dependencies
import itertools as it
from rods import Rodset
from tqdm import tqdm

# aliases
comb = it.combinations_with_replacement


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
        
        finds everything possible in the tree recursively
        where a tree is created solely by expansion
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
def growthsearch(seed, maxcount, maxsmall = 50):
    ''' takes:
            seed - base rod set to match to
            maxcount - max number of rods in set
            maxsmall - the largest rod length to test to
        returns: all rod sets with reasonable growth rate matches
        
        finds rod sets with matching growth rates up to a max number of rods
        riffs on ethan's idea to close in on a growth rate
    '''
    # set up initial rodset
    start = Rodset(seed)
    growth = start.growth
    found = []
    
    # search through everything with maxcount or fewer rods
    # with all rods of length <= maxsmall
        
        
    
    
    
    return


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



















