# -*- coding: utf-8 -*-
"""
last modified: 06/15/21

@author: katie

description:
    contains class for strips
    (for the plug problem where plugs go into strips)
    
    the strip class contains a verbose list of (plug, id) tuples in order,
    a dictionary of total number of each type of plug on strip,
    and a string representation of total filled spots,
    as well as other defining attributes.
    
    initiated with a total size and (currently) no plugs.
    represented by current ordered list of plugs.
    strips with the same list of plugs are equivalent.
    methods (not ready yet):
        add plug in first available position
        remove plug from specific index or by name
        show current strip (verbose as compared to __repr__)
        return flipped version of strip (really not ready yet)
        check plug list compliance
        
"""

from plug_class import Plug

class Strip:
    """ class for strip with defined total length
        must input:
            length (int): total length of the strip
        optional:
            plug_list (not ready yet, list of plugs to start with)
            plug_init (not ready yet, how to initialize plug_list)
            
        add(plug)
        remove(index, plug)
        show()
        flip()
        check()
    """
    
    def __init__(self, length):
        ''' intitalizes from length.
            also initializes:
                number and zero_str if not given,
                length (int, total length),
                
                full (bool, true if the strip is full),
        '''
        
        # raise error if length isn't appropriate
        if not isinstance(length, int):
            raise TypeError('length must be an int')
            
        if length <= 0:
            raise ValueError('length must be > 0')
        
        # length attribute
        self.length = length
        
        # other defining attributes (empty lists, dicts, str)
        self.plug_verbose = [None] * length
        self.plug_dict = {}
        self.filled = '0' * length
        self.plug_list = []
        
        # additional attributes
        self.gap_count = [0] * (length - 1)
        self.full = self.filled.count('1')
        self.empty = self.filled.count('0')
        # not ready yet
        # self.reverse = plug_verbose[::-1]
        # self.symmetrical = (self.plug_verbose == self.reverse)
    
    
    def __repr__(self):
        ''' uses self.plug_list and self.filled for representation.
        '''
        
        if self.plug_list == []:
            plugs = 'None'
        else:
            plugs = ','.join(self.plug_list)
            
        name = self.filled + ' with ' + plugs + '.'
        
        return name
    
    
    def __eq__(self, other):
        ''' strips are the same if they have the same plug_list and length.
            if other is not strip, return False.
        '''
        
        if not isinstance(other, Strip):
            return False
        
        if all((self.plug_list == other.plug_list,
                self.length == other.length)):
            return True
        else:
            return False
        
    
    def add(self, plug):
        ''' takes:
                a Plug object
            returns: a string with outcome of method
                'added' if successfully added
                'incompatible' if the plug cannot be added
                'full' if strip is completely full

        '''
        
        # not ready yet
        
        return
    
#####

# testing

if __name__ == '__main__':
    print('testing Strip class...')
    
    # init list of failures
    fails = []
    
    # testing initial strip
    strip_init = Strip(7)
    
    # correct dictionaries
    corr_dict_init = {
        'length': 7,
        'plug_verbose': [None, None, None, None, None, None, None],
        'plug_dict': {},
        'filled': '0000000',
        'plug_list': [],
        'gap_count': [0, 0, 0, 0, 0, 0],
        'full': 0,
        'empty': 7}
    
    # all tests
    tester = [('init', strip_init, corr_dict_init)]
    
    # iterate over tester
    for test in tester:
        print(test[0] + '...')
        
        for key in test[2]:
            if test[1].__dict__[key] != test[2][key]:
                key_note = key + ', ' + test[0]
                fails.append(key_note)
                
    print('done.')
    
    # showing failures
    print()
    print('failed tests:')
    
    if fails == []:
        print('none.')
        
    else:
        for x in fails:
            print(x)
    


































