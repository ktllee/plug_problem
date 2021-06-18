# -*- coding: utf-8 -*-
"""
last modified: 06/15/21

@author: katie

description:
    codes to solve for all valid arrangements of Plugs in a given list.
    
    solve(plugs, init_style) returns a list of all valid arrangements
    for the plugs given in either dictionary or list form.
    
    note: not yet compatible with strip class or Plug(clean_ends = False)
"""

from plug_class import Plug

def solve(plug_list, strip = [], style = 'p', clean_ends = True):
    ''' takes:
            mandatory: 
                plug_list - a list or dict of the plugs to be used.
                strip - a list of plugs currently in strip (default [])
            optional:  style - str of attribute to init Plugs from.
                'z' or 'zero_str' for zero_str (default),
                's' or 'str_num' (*sigh*) for num_str,
                'n' or 'number' for number,
                'c' or 'classic' for classic,
                'p' or 'plug' for full Plugs
        returns: a set of solutions
        
        recursively finds solutions for the plug problem.
        uses the "ball and strings" method,
        which searches along each "string" until it is found to be (in)valid.
    '''
    solutions = []
    
    # check for type of list/dict of plugs
    if isinstance(plug_list, dict):
        plug_rep = []
        for key in plug_list:
            for i in range(plug_list[key]):
                plug_rep.append(key)
                
    elif isinstance(plug_list, list):
        plug_rep = plug_list
        
    else:
        raise TypeError('plug_list must be a list or dict')
    
    # standardize style
    if not isinstance(style, str):
        raise TypeError('style must be a str')
    
    style = style[0]
    
    # initalize plugs (may change later with update to Plug class)
    if style == 'p':
        plugs = [x for x in plug_rep]
        
    else:
        plugs = [Plug(x, style) for x in plug_rep]
    
    # no check for strip atm because unlikely for mistake, will change later
    # also no check for solutions, similar reason
    
    # base case - run out of plugs, time to return
    if plugs == []:
        new_sol = [x.num_str for x in strip]
        if new_sol not in solutions:
            solutions.append(new_sol)
        return solutions
    
    # strip class should fix messiness here
    total = sum([x.prongs for x in plugs]) + sum([x.prongs for x in strip])
    zstrip = [x.zero_str for x in strip]
    filled = ['0'] * total
    for i in range(len(zstrip)):
        first = filled.index('0')
        indices = [j + first for j, x in enumerate(zstrip[i]) if x == '1']
        copied = filled[:]
        filled = ['1' if (copied[i] == '1' or i in indices) else '0' \
                  for i in range(total)]
        
    
    next_plug = []
    for option in plugs:
        if option not in next_plug:
            next_plug.append(option)
    
    # recursive case - try plugs in existing spaces
    for option in next_plug:
        first = filled.index('0')
        indices = [j + first for j, x in enumerate(option.zero_str) if x == '1']
        if all([x < total for x in indices]):
            if all([filled[k] == '0' for k in indices]):
                new_plugs = plugs[:]
                new_strip = strip[:]
                correct = new_plugs.pop(plugs.index(option))
                new_strip.append(correct)
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