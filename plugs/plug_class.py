# -*- coding: utf-8 -*-
"""
last modified: 06/22/21

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
        must input one of below as represent, and the name as style:
            number (int): base 10 equivalent of binary plug, e.g. 5 == '101'
            str_num (str): base 10 with leading zeros, e.g. '05' = '0101'
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
                 represent,
                 style = 'n',
                 clean_ends = True):
        ''' intitalizes from a descriptive attribute (represent),
            based on style from specific options:
                'z' or 'zero_str' for zero_str,
                's' or 'str_num' for str_num,
                'n' or 'number' for number (default),
                'c' or 'classic' for classic
                
            also initializes:
                number, str_num, and zero_str if not given,
                length (int, total length),
                prongs (int, number of prongs),
                reverse (str, representation of the flipped plug),
                symmetrical (bool, true if reverse = zero_str),
                leading (int, number of leading 0s),
                trailing (int, number of trailing 0s)
        '''
        
        # check that style is valid
        if not isinstance(style, str):
            raise TypeError('style must be str')
          
        # use first character only
        style = style[0]
        
        # find which argument was given and fill others
        # also raise errors for invalid values and types
        # zero_str
        if style == 'z':
            zero_str = represent
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
            str_num = '0' * zero_str.index('1') + str(number)
        
        # str_num
        elif style == 's':
            str_num = represent
            if not isinstance(str_num, str):
                raise TypeError('str_num must be a str')
                
            try:
                # string to number
                number = int(str_num)

            except ValueError:
                raise ValueError('str_num must represent an integer')
            
            # number to binary
            zero_str = '0' * str_num.index(str(number)) + bin(number)[2:]
        
        # number
        elif style == 'n':
            number = represent
            if not isinstance(number, int):
                raise TypeError('number must be an int')
            
            # number to binary
            zero_str = bin(number)[2:]
            
            # number to string (note number starts have no leading 0s)
            str_num = str(number)
        
        # classic
        elif style == 'c':
            classic = represent
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
            str_num = str(number)
            
        else:
            raise ValueError('style must be a valid descriptor')
        
        # last check
        if number < 1:
            raise ValueError('input must be positive')
        
        # remove 0s from beginning and end of zero_str if clean_ends
        # remove leading 0s from str_num
        if not isinstance(clean_ends, bool):
            raise TypeError('clean_ends must be a bool')
            
        if clean_ends:
            zero_str = zero_str.strip('0')
            
            # change number to agree with cleaned string
            number = int(zero_str, 2)
            str_num = str(number)
        
        # intialize given attributes
        self.number = number
        self.str_num = str_num
        self.zero_str = zero_str
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
        
        new = Plug(self.reverse, style = 'z', clean_ends = self.clean_ends)
        
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
        
    
    def reset(self, style = 'z'):
        ''' takes:
                optional argument style takes str to force from.
                'z' or 'zero_str' for zero_str,
                's' or 'str_num' for str_num,
                'n' or 'number' for number,
                'c' or 'classic' for classic
            returns: None
                
            resets based on zero_str or given descriptor style.
            always uses clean_ends behavior.
            
            note that this method directly modifies current plug.
        '''
        
        # check that style is valid
        if not isinstance(style, str):
            raise TypeError('style must be str')
          
        # use first character only
        style = style[0]
        
        # zero_str
        if style == 'z':
            new = Plug(self.zero_str,
                       style = 'z',
                       clean_ends = self.clean_ends)
        
        # str_num
        elif style == 's':
            new = Plug(self.str_num,
                       style = 's',
                       clean_ends = self.clean_ends)
        
        # number
        elif style == 'n':
            new = Plug(self.number,
                       style = 'n',
                       clean_ends = self.clean_ends)
        
        # classic
        elif style == 'c':
            new = Plug(self.classic,
                       style = 'c',
                       clean_ends = self.clean_ends)
        
        # error if none of the above
        else:
            raise ValueError('style must correspond to descriptor')
        
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
        'str_num': '91',
        'zero_str': '1011011',
        'clean_ends': True,
        'length': 7,
        'prongs': 5,
        'reverse': '1101101',
        'symmetrical': False,
        'trailing': 0,
        'leading': 0}
    
    corr_dict_zstr = {
        'number': 109,
        'str_num': '109',
        'zero_str': '1101101',
        'clean_ends': True,
        'length': 7,
        'prongs': 5,
        'reverse': '1011011',
        'symmetrical': False,
        'trailing': 0,
        'leading': 0}
    
    corr_dict_clssc = {
        'number': 33,
        'str_num': '33',
        'zero_str': '100001',
        'clean_ends': True,
        'length': 6,
        'prongs': 2,
        'reverse': '100001',
        'symmetrical': True,
        'trailing': 0,
        'leading': 0}
    
    corr_dict_ends = {
        'number': 218,
        'str_num': '00218',
        'zero_str': '0011011010',
        'clean_ends': False,
        'length': 10,
        'prongs': 5,
        'reverse': '0101101100',
        'symmetrical': False,
        'trailing': 1,
        'leading': 2}
    
    plug_num = Plug(num)
    plug_nstr = Plug(nstr, style = 's', clean_ends = False)
    plug_nstr_c = Plug(nstr, style = 's')
    plug_zstr = Plug(zstr, style = 'z')
    plug_clssc = Plug(clssc, style = 'c')
    plug_ends = Plug(zstr, style = 'z', clean_ends = False)
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
    if any((plug_flip != plug_zstr,
            plug_ends != plug_nstr,
            plug_flip == plug_ends)):
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