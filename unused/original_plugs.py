# -*- coding: utf-8 -*-
"""
last modified: 06/08/21

@author: katie

description:
    codes to generate a dictionary of plugs and
    find solutions for sets of plugs
    
    gen_dict(max_len) generates a list of plugs by plug size:number of prongs
    in a dictionary that can be input to plug_solutions.
    Note that the 0-length plug has only one prong, and all others have two.
    
    plug_solutions(dictionary, flip, show) takes a dictionary of plugs and
    finds all possible solutions.
    The flip option defaults to true, meaning that flipped solutions
    are equivalent.  The show option shows progress.
    
    solve(max_len, save, show) is essentially a shortcut for
    plug_solutions(gen_dict(max_len)).
    If true, the save option saves the results to csv files.
    If true, the show option prints each solution.
"""

# uses distinct_permutations for possible future needs
from more_itertools import distinct_permutations as perm
import pandas as pd
         
# dictionary of lengths & number of pegs
# small test
test = {0:1,
        1:2,
        2:2}

def gen_dict(max_len):
    ''' takes: int with the max length between prongs
        returns: dictionary for plugs with two prongs
        
        note: 0-plug has one prong
    '''
    dictionary = {0:1}
    
    for i in range(1, max_len):
        dictionary[i] = 2
        
    return dictionary

def plug_solutions(dictionary, flip=True, show=False):
    ''' takes: dictionary of plug types and # of prongs
        returns: list of valid combinations
        
        assumes there's only one of each plug
        distance between each prong on a plug is equal
    '''

    # list of pegs and combos
    plugs = [x for x in dictionary]
    combos = perm(plugs)
    
    # total number of pegs, init list of solutions
    total = sum([dictionary[x] for x in dictionary])
    solutions = []
    i = -1
    
    # check each combo for validity
    for possible in combos:
        
        # initialize empty solution list, validity checker
        strip = ['empty'] * total
        good = 1
        i += 1
        
        # iterate over the pegs in the combos list and try to add
        for j in range(len(plugs)):
            
            # shortcut
            length = possible[j]
            
            # put first prong in first empty
            current = strip.index('empty')
            strip[current] = length
            
            # loop for number of prongs
            for k in range(dictionary[length] - 1):
            
                # potential next position
                current += (length + 1)
                
                # try to place next plug
                if current >= len(strip):
                    good = 0
                    break
                
                elif strip[current] != 'empty':
                    good = 0
                    break
                
                else:
                    strip[current] = length
                
            if good == 0:
                break
                   
        # add if there are no empty slots
        if 'empty' not in strip:
            solutions.append(strip)
            if show:
                print(str(i) + '.', end = '')
            
    # remove reflectively equal combos
    if flip:
        final = []
        for thing in solutions:
            if list(reversed(thing)) not in final:
                final.append(thing)
    else:
        final = solutions
                
    return final


#####

def solve(max_len=6, save=True, show=False):
    solutions = plug_solutions(gen_dict(max_len))
    print()
    print('number of solutions:', len(solutions))
    if show:
        for x in solutions:
            print(x)
    if save:
        df = pd.DataFrame(solutions)
        df.to_csv('solutions/original_plugs'+str(max_len)+'.csv',
                  header = False,
                  index = False)
    return