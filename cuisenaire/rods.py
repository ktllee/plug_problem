# -*- coding: utf-8 -*-
"""
last modified: jul 6, 2022

@author: katie

description:
    contains class for rod sets
    (for problems involving sets of cuisenaire rods)
    
    the Rodset class contains defining information for a group of rods.
    
    initiated with a string or list of rods in the set.
    (e.g. the padovans would be [2,3] or '011'.  note [2,2] is '02')
    
    represented by string descriptor.
    rodsets with the same string representation are equivalent.
    
    attributes:
        basic - list of rod lengths
        string - string listing rod lengths (e.g. 011 = [2,3])
    
    methods:
        init, repr, eq
        copy - deep copy
        spotcon (helper) - switch between basic and string representations
        
    dependencies:
        factor() from sympy, as factor
        
"""

class Rodset:
    """ class for set of cuisenaire rods
        must input one of below as represent:
            string (str): string containing number of rods at each length
            group (list): list of positive integer lengths of rods in set
            
        e.g. the padovans would be [2,3] or '011'.  note [2,2] is '02'
    """
    
    # dependencies
    from sympy import factor as factor
    
    # helper: string to basic converter
    # needed only for backwards compatibiity
    @staticmethod
    def spotcon(rep):
        ''' changes a string representaion of a rodset to a list
            or vice versa
            
            note: assumes rep is already correctly one or the other
        '''
        
        # string to list
        if isinstance(rep, str):
            converted = []
            for i in range(len(rep)):
                converted.extend([i + 1 for x in range(int(rep[i]))])
            
        # list to string
        elif isinstance(rep, list):
            converted = \
                ''.join([str(rep.count(x + 1)) for x in range(max(rep))])
        
        return converted
    
    
    def __init__(self, represent):
        ''' intitalizes from a descriptive attribute (represent),
            either list of lengths or bit string
                
            also initializes:
                growth
        '''
        
        # find which argument was given and fill others
        # also raise errors for invalid values and types
        # string (e.g. 011 == [2,3])
        if isinstance(represent, str):
            if represent.isnumeric():
                string = represent
                basic = self.spotcon(represent)
            else:
                raise ValueError('string representation must be numeric')
        
        # list of rod lengths
        elif isinstance(represent, list):
            if all(isinstance(x, int) for x in represent):
                represent.sort()
                basic = represent
                string = self.spotcon(represent)
            else:
                raise ValueError('list representation must contain ints')
        
        # neither
        else:
            raise TypeError('representation must be a list or string')
            
        # initialize attributes
        # given attributes
        self.string = string
        self.basic = basic
        
        # polynomials
        
        
        
    def __repr__(self):
        ''' basic (list) representation
        '''
        
        return self.basic
    
    
    def __eq__(self, other):
        ''' rodsets are the same if they have the same string
            if other is not Rodset, return False.
        '''
        
        if not isinstance(other, Rodset):
            return False
        
        if self.string == other.string:
            return True
        else:
            return False
        
    
    def copy(self):
        ''' takes: self
            returns: a deep copy of self
            
            note that this carries over any manually-created quirks
        '''
        
        new = Rodset('1')
        
        for key in self.__dict__:
            new.__dict__[key] = self.__dict__[key]
        
        return new


##### ##! testing in progress - below is a template for object testing

# testing

# if __name__ == '__main__':
#     print('testing Rodset class...')
    
#     # set up some test plugs
#     num = 91
#     nstr = '00218'
#     zstr = '00xx0xx0x0'
#     clssc = 6
    
#     corr_dict_num = {
#         'number': 91,
#         'str_num': '91',
#         'zero_str': '1011011',
#         'clean_ends': True,
#         'length': 7,
#         'prongs': 5,
#         'reverse': '1101101',
#         'symmetrical': False,
#         'trailing': 0,
#         'leading': 0}
    
#     corr_dict_zstr = {
#         'number': 109,
#         'str_num': '109',
#         'zero_str': '1101101',
#         'clean_ends': True,
#         'length': 7,
#         'prongs': 5,
#         'reverse': '1011011',
#         'symmetrical': False,
#         'trailing': 0,
#         'leading': 0}
    
#     corr_dict_clssc = {
#         'number': 33,
#         'str_num': '33',
#         'zero_str': '100001',
#         'clean_ends': True,
#         'length': 6,
#         'prongs': 2,
#         'reverse': '100001',
#         'symmetrical': True,
#         'trailing': 0,
#         'leading': 0}
    
#     corr_dict_ends = {
#         'number': 218,
#         'str_num': '00218',
#         'zero_str': '0011011010',
#         'clean_ends': False,
#         'length': 10,
#         'prongs': 5,
#         'reverse': '0101101100',
#         'symmetrical': False,
#         'trailing': 1,
#         'leading': 2}
    
#     plug_num = Plug(num)
#     plug_nstr = Plug(nstr, style = 's', clean_ends = False)
#     plug_nstr_c = Plug(nstr, style = 's')
#     plug_zstr = Plug(zstr, style = 'z')
#     plug_clssc = Plug(clssc, style = 'c')
#     plug_ends = Plug(zstr, style = 'z', clean_ends = False)
#     plug_flip = plug_num.flip()
    
#     tester = [('num', plug_num, corr_dict_num),
#               ('nstr', plug_nstr, corr_dict_ends),
#               ('nstr_c', plug_nstr_c, corr_dict_zstr),
#               ('zstr', plug_zstr, corr_dict_zstr),
#               ('clssc', plug_clssc, corr_dict_clssc),
#               ('ends', plug_ends, corr_dict_ends),
#               ('flip', plug_flip, corr_dict_zstr)]
    
#     # init list of failures
#     fails = []
    
#     for test in tester:
#         print(test[0] + '...')
        
#         for key in test[2]:
#             if test[1].__dict__[key] != test[2][key]:
#                 key_note = key + ', ' + test[0]
#                 fails.append(key_note)
    
#     # testing equivalency
#     print('equivalence...')
#     if any((plug_flip != plug_zstr,
#             plug_ends != plug_nstr,
#             plug_flip == plug_ends)):
#         fails.append('equivalence')
        
#     # testing the copy method
#     print('deep copy...')
#     plug_copy = plug_clssc.copy()
#     plug_clssc.__dict__['zero_str'] = '101'
    
#     for key in corr_dict_clssc:
#         if plug_copy.__dict__[key] != corr_dict_clssc[key]:
#             key_note = key + ', copy'
#             fails.append(key_note)
        
#     # testing the reset method
#     print('reset...')
#     plug_ends.clean_ends = True
#     plug_ends.reset()
    
#     for key in corr_dict_zstr:
#         if plug_ends.__dict__[key] != corr_dict_zstr[key]:
#             key_note = key + ', reset'
#             fails.append(key_note)
    
#     print('done.')
    
#     # showing failures
#     print()
#     print('failed tests:')
    
#     if fails == []:
#         print('none.')
        
#     else:
#         for x in fails:
#             print(x)