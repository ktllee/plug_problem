# -*- coding: utf-8 -*-
"""
last modified: 08/09/21

@author: katie

description:
    codes to solve for all valid arrangements of Plugs in a Strip of given
    total number of plugs (and given types of plugs).
    
    cts(number, plugs, init_style) returns a list of all valid arrangements
    for the plugs given in either dictionary or list form.
    
    note: does not currently support plugs with hanging ends
"""

from plug_class import Plug
from strip_class import Strip
from flex_solver import flex

def cts(number, plug_list, style = 's', result_style = 's'):
    ''' takes:
            mandatory: 
                number - an int for total number of plugs to begin with.
                plug_list - a list or dict of the plugs to be used.
                (note that lists given assume endless plugs)
            optional:
                style, result - str of attribute to init and return Plugs.
                    'z' or 'zero_str' for zero_str,
                    's' or 'str_num' for str_num (default),
                    'n' or 'number' for number,
                    'c' or 'classic' for classic (style only),
                    'p' or 'plug' for full Plugs,
                    'f' or 'full' for full Strips (result_style only)
        returns: a set of solutions
        
        recursively finds solutions for the plug problem.
        uses the "ball and strings" method,
        which searches along each "string" until it is found to be (in)valid.
    '''
    
    # check for type of list/dict of plugs and change to dict
    if isinstance(plug_list, list):
        plugs = {}
        for key in plug_list:
            # -1 is used to represent endless plugs
            plugs[key] = -1
    
    elif isinstance(plug_list, dict):
        plugs = plug_list
        # make sure dict values are valid
        for key in plugs:
            if not isinstance(plugs[key], int):
                raise TypeError('frequency keys must be ints')
            if plugs[key] < -1:
                raise ValueError('frequency keys must be >= -1')
        # make sure dictionary values add to over number
        total = [plugs[key] for key in plugs]
        if (-1 not in total) and (sum(total) < number):
            raise ValueError('not enough plugs to make total number given')
        
    else:
        raise TypeError('plug_list must be a list or dict')
    
    # standardize style inputs
    if not all((isinstance(style, str),
                isinstance(result_style, str))):
        raise TypeError('styles must be str')
    style = style[0]
    result_style = result_style[0]
    
    # find minimum and maximum lengths given inputs
    bounds = []
    for func in [min, max]:
        left = number
        length = 0
        plugs_temp = {x:y for (x,y) in plugs.items()}
        while left > 0:
            next_plug = [x for x in plugs_temp if plugs_temp[x] != 0]
            select = func(next_plug, key = lambda x: Plug(x, style).prongs)
            length += Plug(select, style).prongs
            if plugs_temp[select] != -1:
                plugs_temp[select] -= 1
            left -= 1
        bounds.append(length)
        
    # iterate over all possible lengths to find solutions using flex
    solutions = []
    for length in range(bounds[0], bounds[1] + 1):
        solutions.extend(flex(length, plug_list, None, style, result_style))
    
    return solutions


#####

# testing

if __name__ == '__main__':
    print('testing recursive solver...')
    
    # set up some test lists
    test_a1 = {'1': -1}
    test_a2 = ['1']
    test_b = {'3': -1, '5': -1}
    test_c = {'1': 1, '5': -1}
    test_d = ['9', '19']
    
    # solutions
    solve_a = [['1', '1', '1']]
    solve_b3 = [['3', '3', '3'],
                ['3', '5', '5'],
                ['5', '5', '3']]
    solve_b6 = flex(12, {'3': -1, '5': -1})
    solve_c2 = [['1', '1'],
                ['5', '1'],
                ['5', '5']]
    solve_c5 = [['1', '5', '5', '5', '5'],
                ['5', '5', '1', '5', '5'],
                ['5', '5', '5', '5', '1']]
    solve_d = []
    
    # answers from function
    ans_a1 = cts(3, test_a1)
    ans_a2 = cts(3, test_a2)
    ans_b3 = cts(3, test_b)
    ans_b6 = cts(6, test_b)
    ans_c2 = cts(2, test_c)
    ans_c5 = cts(5, test_c)
    ans_d2 = cts(2, test_d)
    
    tester = [('small dict', ans_a1, solve_a),
              ('small list', ans_a2, solve_a),
              ('empty, inf', ans_b3, solve_b3),
              ('some, inf', ans_b6, solve_b6),
              ('some, lim', ans_c2, solve_c2),
              ('some(2), lim', ans_c5, solve_c5),
              ('empty, inf', ans_d2, solve_d)]
    
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