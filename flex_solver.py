# -*- coding: utf-8 -*-
"""
last modified: 06/29/21

@author: katie

description:
    codes to solve for all valid arrangements of Plugs in a Strip of given
    total length (and given types of plugs).
    
    flex(length, plugs, init_style) returns a list of all valid arrangements
    for the plugs given in either dictionary or list form.
    
    note: does not currently support plugs with hanging ends
"""

from plug_class import Plug
from strip_class import Strip

def flex(length, plug_list, strip = None, style = 's'):
    ''' takes:
            mandatory: 
                length - an int for total length to begin with.
                plug_list - a list or dict of the plugs to be used.
                (note that lists given assume endless plugs)
            optional:  
                strip - a Strip with the current plugs to start solutions from
                style - str of attribute to init Plugs from.
                    'z' or 'zero_str' for zero_str,
                    's' or 'str_num' for str_num (default),
                    'n' or 'number' for number,
                    'c' or 'classic' for classic,
                    'p' or 'plug' for full Plugs
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
        
    else:
        raise TypeError('plug_list must be a list or dict')
    
    # standardize style input
    if not isinstance(style, str):
        raise TypeError('style must be a str')
    style = style[0]
    
    # if no strip yet initiated, create one
    if strip == None:
        strip = Strip(length)
        
    # else, make sure it is a strip of the right length
    else:
        if not isinstance(strip, Strip):
            raise TypeError('strip must be a Strip')
        if strip.length != length:
            raise ValueError('strip and length must match')
    
    # base case - full strip, time to return
    if strip.filled.count('0') == 0:
        new_sol = [x.str_num for x in strip.plug_list]
        return [new_sol]
    
    # list of possible next plugs
    next_plug = []
    for key in plugs:
        if plugs[key] != 0:
            next_plug.append(key)
    
    # initialize list of solutions
    solutions = []
    
    # recursive case - try plugs in existing spaces
    for option in next_plug:
        
        # try the next plug in a copy of the strip
        new_strip = strip.copy()
        result = new_strip.add(option, style)
        
        # if the add was successful, pass the copy to next iteration
        if result == 'added':
            
            # remove used plug from list (if maximums have been implemented)
            new_plugs = plugs.copy()
            if new_plugs[option] != -1:
                new_plugs[option] -= 1
            
            # call flex
            recur = flex(length, new_plugs, new_strip, style)
            solutions.extend(recur)
            
    # remove doubles
    final = []
    for possible in solutions:
        if possible not in final:
            final.append(possible)
    
    return final


#####

# testing

if __name__ == '__main__':
    print('testing recursive solver...')
    
    # set up some test lists
    test_a1 = {'1': -1}
    test_a2 = ['1']
    test_b = {'3': -1, '5': -1}
    test_c = {'1': 1, '5': -1}
    
    # solutions
    solve_a = [['1', '1', '1']]
    solve_b3 = []
    solve_b6 = [['3', '3', '3'],
                ['3', '5', '5'],
                ['5', '5', '3']]
    solve_c2 = []
    solve_c7 = [['5', '1', '5', '5'],
                ['5', '5', '5', '1']]
    
    # answers from function
    ans_a1 = flex(3, test_a1)
    ans_a2 = flex(3, test_a2)
    ans_b3 = flex(3, test_b)
    ans_b6 = flex(6, test_b)
    ans_c2 = flex(2, test_c)
    ans_c7 = flex(7, test_c)
    
    tester = [('small dict', ans_a1, solve_a),
              ('small list', ans_a2, solve_a),
              ('empty, inf', ans_b3, solve_b3),
              ('some, inf', ans_b6, solve_b6),
              ('empty, lim', ans_c2, solve_c2),
              ('some, lim', ans_c7, solve_c7)]
    
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