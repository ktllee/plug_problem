# -*- coding: utf-8 -*-
"""
last modified: 06/15/21

@author: katie

description:
    contains class for plugs
    (for the plug problem where plugs go into strips)
    
    the plug class contains defining information for an individual plug.
    initiated with an integer (number rep) or string descriptor.
    represented by string descriptor.
    plugs with the same string representation and end behavior are equivalent.
    note that plugs are not reversible, meaning 1101 != 1011.
    methods:
        return reversed plug
        deep copy
        reset attributes based on zero_str, clean_ends
"""

class Plug:
    """ class for plug with defined prongs (any but 0) and gaps (0s)
        must input one of:
            number (int): base 10 equivalent of binary plug, e.g. 5 == '101'
            num_str (str): base 10 with leading zeros, e.g. '05' = '0101'
            zero_str (str): string representation with 0s, e.g. 'x0y' == '101'
            classic (int): total length for 1-2 prong plug, e.g. 3 == '101'
        optional:
            clean_ends (bool): only prongs to end a plug (T) or allow gaps (F)
            
        flip() method returns a reversed plug.
        copy() method returns a deep copy.
        reset() method re-aligns attributes based on zero_str and clean_ends.
        
        note: be aware that the number attribute does not account for
              leading 0s if clean_ends = False and zero_str used to init.
    """
    
    def __init__(self,
                 rep,
                 style = 'z',
                 clean_ends = True):
        ''' intitalizes from a descriptive attribute, based on style.
            also initializes:
                number, num_str, and zero_str if not given,
                length (int, total length),
                prongs (int, number of prongs),
                reverse (str, representation of the flipped plug),
                symmetrical (bool, true if reverse = zero_str),
                leading (int, number of leading 0s),
                trailing (int, number of trailing 0s)
        '''
        
        # raise error if exactly one defining argument not given
        if sum((x is None for x in
                [number, num_str, zero_str, classic])) != 3:
            raise TypeError('exactly one defining argument is required')
            
        # find which argument was given and fill others
        # also raise errors for invalid values and types
        if number is not None:
            if not isinstance(number, int):
                raise TypeError('number must be an int')
            
            # number to binary
            zero_str = bin(number)[2:]
            
            # number to string (note number starts have no leading 0s)
            num_str = str(number)
            
        elif num_str is not None:
            if not isinstance(num_str, str):
                raise TypeError('num_str must be a str')
                
            try:
                # string to number
                number = int(num_str)

            except ValueError:
                raise ValueError('num_str must represent an integer')
            
            # number to binary
            zero_str = '0' * num_str.index(str(number)) + bin(number)[2:]
            
        elif zero_str is not None:
            if not isinstance(zero_str, str):
                raise TypeError('zero_str must be a str')
                
            if len(zero_str.replace('0', '')) == 0:
                raise ValueError('zero_str must have 0s and other characters')
            
            # clean zero_str input (1s for any non-zero)
            zero_list = [x if x == '0' else '1' for x in zero_str]
            zero_str = ''.join(zero_list)
            
            # binary to number
            number = int(zero_str, 2)
            
            # number to string
            num_str = '0' * zero_str.index('1') + str(number)
            
        elif classic is not None:
            if not isinstance(classic, int):
                raise TypeError('classic must be an int')
                
            if classic < 1:
                raise ValueError('classic must be greater than 0')
                
            # classic to zero_str
            empty_list = ['0'] * classic
            empty_list[0], empty_list[-1] = '1', '1'
            zero_str = ''.join(empty_list)
            
            # binary to number
            number = int(zero_str, 2)
            num_str = str(number)
        
        if number < 1:
            raise ValueError('input must be positive')
        
        # remove 0s from beginning and end of zero_str if clean_ends
        # remove leading 0s from num_str
        if clean_ends:
            zero_str = zero_str.strip('0')
            
            # change number to agree with cleaned string
            number = int(zero_str, 2)
            num_str = str(number)
        
        # intialize given attributes
        self.number = number
        self.num_str = num_str
        self.zero_str = zero_str
        self.classic = classic
        self.clean_ends = clean_ends
        
        # initializing other attributes
        self.length = len(zero_str)
        self.prongs = zero_str.count('1')
        self.reverse = zero_str[::-1]
        self.symmetrical = (self.zero_str == self.reverse)
        self.leading = self.zero_str.index('1')
        self.trailing = self.reverse.index('1')
        
        
    def __repr__(self):
        ''' uses self.zero_str for representation.
        '''
        
        return self.zero_str
    
    
    def __eq__(self, other):
        ''' plugs are the same if they have the same zero_str and clean_ends.
            if other is not plug, return False.
        '''
        
        if not isinstance(other, Plug):
            return False
        
        if all((self.zero_str == other.zero_str,
                self.clean_ends == other.clean_ends)):
            return True
        else:
            return False
        
    
    def flip(self):
        ''' takes: self
            returns: another plug that is flipped version of self
        
            note that this method does not modify current plug.
        '''
        
        new = Plug(zero_str = self.reverse, clean_ends = self.clean_ends)
        
        return new
    
    
    def copy(self):
        ''' takes: self
            returns: a deep copy of self
            
            note that this carries over manually-created quirks
            reset if needed
        '''
        
        new = Plug(1)
        
        for key in self.__dict__:
            new.__dict__[key] = self.__dict__[key]
        
        return new
        
    
    def reset(self, attribute = 'z'):
        ''' takes:
                optional argument attribute takes str to force from.
                'z' or 'zero_str' for zero_str,
                's' or 'str_num' (*sigh*) for num_str,
                'n' or 'number' for number,
                'c' or 'classic' for classic
            returns: None
                
            resets based on zero_str or given descriptor attribute.
            always uses clean_ends behavior.
            
            note that this method directly modifies current plug.
        '''
        
        # check that attribute is valid
        if not isinstance(attribute, str):
            raise TypeError('attribute must be str')
          
        # use first character only
        attribute = attribute[0]
        
        # zero_str
        if attribute == 'z':
            new = Plug(zero_str = self.zero_str, clean_ends = self.clean_ends)
        
        # num_str
        elif attribute == 's':
            new = Plug(num_str = self.num_str, clean_ends = self.clean_ends)
        
        # number
        elif attribute == 'n':
            new = Plug(number = self.number, clean_ends = self.clean_ends)
        
        # classic
        elif attribute == 'c':
            new = Plug(classic = self.classic, clean_ends = self.clean_ends)
        
        # error if none of the above
        else:
            raise ValueError('attribute must correspond to descriptor')
        
        self.__dict__.update(new.__dict__)
        
        return


#####

# testing

if __name__ == '__main__':
    print('testing Plug class...')
    
    # set up some test plugs
    num = 91
    nstr = '00218'
    zstr = '00xx0xx0x0'
    clssc = 6
    
    corr_dict_num = {
        'number': 91,
        'num_str': '91',
        'zero_str': '1011011',
        'classic': None,
        'clean_ends': True,
        'length': 7,
        'prongs': 5,
        'reverse': '1101101',
        'symmetrical': False,
        'trailing': 0,
        'leading': 0}
    
    corr_dict_zstr = {
        'number': 109,
        'num_str': '109',
        'zero_str': '1101101',
        'classic': None,
        'clean_ends': True,
        'length': 7,
        'prongs': 5,
        'reverse': '1011011',
        'symmetrical': False,
        'trailing': 0,
        'leading': 0}
    
    corr_dict_clssc = {
        'number': 33,
        'num_str': '33',
        'zero_str': '100001',
        'classic': 6,
        'clean_ends': True,
        'length': 6,
        'prongs': 2,
        'reverse': '100001',
        'symmetrical': True,
        'trailing': 0,
        'leading': 0}
    
    corr_dict_ends = {
        'number': 218,
        'num_str': '00218',
        'zero_str': '0011011010',
        'classic': None,
        'clean_ends': False,
        'length': 10,
        'prongs': 5,
        'reverse': '0101101100',
        'symmetrical': False,
        'trailing': 1,
        'leading': 2}
    
    plug_num = Plug(num)
    plug_nstr = Plug(num_str = nstr, clean_ends = False)
    plug_nstr_c = Plug(num_str = nstr)
    plug_zstr = Plug(zero_str = zstr)
    plug_clssc = Plug(classic = clssc)
    plug_ends = Plug(zero_str = zstr, clean_ends = False)
    plug_flip = plug_num.flip()
    
    tester = [('num', plug_num, corr_dict_num),
              ('nstr', plug_nstr, corr_dict_ends),
              ('nstr_c', plug_nstr_c, corr_dict_zstr),
              ('zstr', plug_zstr, corr_dict_zstr),
              ('clssc', plug_clssc, corr_dict_clssc),
              ('ends', plug_ends, corr_dict_ends),
              ('flip', plug_flip, corr_dict_zstr)]
    
    # init list of failures
    fails = []
    
    for test in tester:
        print(test[0] + '...')
        
        for key in test[2]:
            if test[1].__dict__[key] != test[2][key]:
                key_note = key + ', ' + test[0]
                fails.append(key_note)
    
    # testing equivalency
    print('equivalence...')
    if plug_flip != plug_zstr or plug_ends != plug_nstr:
        fails.append('equivalence')
        
    # testing the copy method
    print('deep copy...')
    plug_copy = plug_clssc.copy()
    plug_clssc.__dict__['zero_str'] = '101'
    
    for key in corr_dict_clssc:
        if plug_copy.__dict__[key] != corr_dict_clssc[key]:
            key_note = key + ', copy'
            fails.append(key_note)
        
    # testing the reset method
    print('reset...')
    plug_ends.clean_ends = True
    plug_ends.reset()
    
    for key in corr_dict_zstr:
        if plug_ends.__dict__[key] != corr_dict_zstr[key]:
            key_note = key + ', reset'
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