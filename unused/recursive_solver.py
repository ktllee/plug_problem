# -*- coding: utf-8 -*-
"""
last modified: 06/29/21

@author: katie

description:
    codes to solve for all valid arrangements of Plugs in a given list.
    
    solve(plugs, init_style) returns a list of all valid arrangements
    for the plugs given in either dictionary or list form.
    
    note: does not currently support plugs with hanging ends
"""

from plug_class import Plug
from strip_class import Strip

def solve(plug_list, strip = None, style = 'p'):
    ''' takes:
            mandatory: 
                plug_list - a list or dict of the plugs to be used.
            optional:  
                strip - a Strip with the current plugs to start solutions from
                style - str of attribute to init Plugs from.
                    'z' or 'zero_str' for zero_str,
                    's' or 'str_num' for str_num,
                    'n' or 'number' for number,
                    'c' or 'classic' for classic,
                    'p' or 'plug' for full Plugs (default)
        returns: a set of solutions
        
        recursively finds solutions for the plug problem.
        uses the "ball and strings" method,
        which searches along each "string" until it is found to be (in)valid.
    '''
    
    # check for type of list/dict of plugs and change to list
    if isinstance(plug_list, dict):
        plug_rep = []
        for key in plug_list:
            for i in range(plug_list[key]):
                plug_rep.append(key)
                
    elif isinstance(plug_list, list):
        plug_rep = plug_list
        
    else:
        raise TypeError('plug_list must be a list or dict')
    
    # standardize style input
    if not isinstance(style, str):
        raise TypeError('style must be a str')
        
    style = style[0]
    
    # initalize plugs
    if style == 'p':
        plugs = [x for x in plug_rep]
        
    else:
        plugs = [Plug(x, style) for x in plug_rep]
    
    # if no strip yet initiated, create one
    if strip == None:
        length = sum([x.prongs for x in plugs])
        strip = Strip(length)
        
    # else, make sure it is a strip
    else:
        if not isinstance(strip, Strip):
            raise TypeError('strip must be a Strip')
    
    # base case - run out of plugs, time to return
    if plugs == []:
        new_sol = [x.str_num for x in strip.plug_list]
        return [new_sol]
    
    # list of possible next plugs without repeats    
    next_plug = []
    for option in plugs:
        if option not in next_plug:
            next_plug.append(option)
    
    # initialize list of solutions
    solutions = []
    
    # recursive case - try plugs in existing spaces
    for option in next_plug:
        
        # try the next plug in a copy of the strip
        new_strip = strip.copy()
        result = new_strip.add(option, 'p')
        
        # if the add was successful, pass the copy to next iteration
        if result == 'added':
            
            # remove used plug from list
            new_plugs = plugs.copy()
            new_plugs.remove(option)
            
            # call solve
            recur = solve(new_plugs, new_strip)
            solutions.extend(recur)
    
    return solutions


#####

# testing

if __name__ == '__main__':
    print('testing recursive solver...')
    
    # set up some test lists
    test0 = [1]
    test1a = ['1', '5', '9']
    test1b = [1, 3, 4]
    test2a = ['1', '101', '101','1100001']
    test2b = {'1': 1,
              '101': 2,
              '1100001': 1}
    
    # solutions
    solve0 = [['1']]
    solve1 = [['5', '9', '1'],
              ['9', '1', '5']]
    solve2 = [['1', '97', '5', '5'],
              ['97', '5', '1', '5'],
              ['97', '5', '5', '1']]
    
    # answers from function
    ans0 = solve(test0, style = 'n')
    ans1a = solve(test1a, style = 's')
    ans1b = solve(test1b, style = 'c')
    ans2a = solve(test2a, style = 'z')
    ans2b = solve(test2b, style = 'z')
    
    tester = [('small', ans0, solve0),
              ('clssc, s', ans1a, solve1),
              ('clssc, c', ans1b, solve1),
              ('dbl, z', ans2a, solve2),
              ('dbl, d', ans2b, solve2)]
    
    # init list of failures
    fails = []
    
    # iterate through tests
    for test in tester:
        print(test[0] + '...')
        
        print(test[1])
        
        if test[1] != test[2]:
            fails.append(test[0])
    
                
    print('done.')
    
    # showing failures
    print()
    print('failed tests:')
    
    if fails == []:
        print('none.')
        
    else:
        for x in fails:
            print(x)