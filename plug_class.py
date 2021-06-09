# -*- coding: utf-8 -*-
"""
last modified: 06/08/21

@author: katie

description:
    contains classes for plug and strip
    (for the plug problem where plugs go into strips)
    
    the plug class contains defining information for an individual plug.
    initiated with an integer (number rep) or string descriptor.
    represented by string descriptor.
    plugs with the same string representation and end behavior are equivalent.
    note that plugs are not reversible, meaning 1101 != 1011.
    methods:
        return reversed plug
        reset attributes based on zero_str, clean_ends
    
    the strip class contains a list of plugs in order
    and a dictionary of total number of each type of plug on strip.
    initiated with a total size and no plugs.
    represented by current ordered list of plugs.
    strips with the same list of plugs are equivalent.
    methods:
        none
"""

class plug:
    """ class for plug with defined prongs (any but 0) and gaps (0s)
        must input one of:
            number (int): base 10 equivalent of binary plug, e.g. 5 == '101'
            zero_str (str): string representation with 0s, e.g. 'x0y' == '101'
            classic (int): total length for 1-2 prong plug, e.g. 3 == '101'
        optional:
            clean_ends (bool): only prongs to end a plug (T) or allow gaps (F)
            
        flip() method reverses plug direction.
        reset() method re-aligns attributes based on zero_str and clean_ends.
        
        note: be aware that the number attribute does not account for
              leading 0s if clean_ends = False and zero_str used to init.
    """
    
    def __init__(self,
                 number = None,
                 zero_str = None,
                 classic = None,
                 clean_ends = True):
        ''' intitalizes from one of number, zero_str, or classic.
            also initializes:
                number and zero_str if not given,
                length (int, total length),
                prongs (int, number of prongs),
                reverse (str, representation of the flipped plug),
                symmetrical (bool, true if reverse = zero_str)
        '''
        
        # raise error if exactly one defining argument not given
        if sum((x is None for x in [number, zero_str, classic])) != 2:
            raise TypeError('exactly one defining argument is required')
            
        # find which argument was given and fill others
        # also raise errors for invalid values and types
        if number is not None:
            if not isinstance(number, int):
                raise TypeError('number must be an int')
                
            if number < 1:
                raise ValueError('number must be greater than 0')
            
            # number to binary
            zero_str = bin(number)[2:]
            
        elif zero_str is not None:
            if not isinstance(zero_str, str):
                raise TypeError('zero_str must be a str')
                
            if any((zero_str.count('0') == 0,
                    len(zero_str.replace('0', '')) == 0)):
                raise ValueError('zero_str must have 0s and other characters')
            
            # clean zero_str input (1s for any non-zero)
            zero_list = [x if x == '0' else '1' for x in zero_str]
            zero_str = ''.join(zero_list)
            
            # binary to number
            number = int(zero_str, 2)
            
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
        
        # remove 0s from beginning and end of zero_str if clean_ends
        if clean_ends:
            zero_str = zero_str.strip('0')
            
            # change number to agree with cleaned string
            number = int(zero_str, 2)
        
        # intialize given attributes
        self.number = number
        self.zero_str = zero_str
        self.classic = classic
        self.clean_ends = clean_ends
        
        # initializing other attributes
        self.length = len(zero_str)
        self.prongs = zero_str.count('1')
        self.reverse = zero_str[::-1]
        self.symmetrical = (self.zero_str == self.reverse)
        
        
    def __repr__(self):
        ''' uses self.zero_str for representation.
        '''
        
        return self.zero_str
    
    
    def __eq__(self, other):
        ''' plugs are the same if they have the same zero_str and clean_ends.
            if other is not plug, return False.
        '''
        
        if not isinstance(other, plug):
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
        
        new = plug(zero_str = self.reverse, clean_ends = self.clean_ends)
        
        return new
        
    
    def reset(self, attribute = 'z'):
        ''' takes:
                optional argument attribute takes str to force from.
                'z' or 'zero_str' for zero_str,
                'n' or 'number' for number,
                'c' or 'classic' for classic
            returns: None
                
            resets based on zero_str or given descriptor attribute.
            always uses clean_ends behavior
            
            note that this method directly modifies current plug.
        '''
        
        # check that attribute is valid
        if not isinstance(attribute, str):
            raise TypeError('attribute must be str')
          
        # use first character only
        attribute = attribute[0]
        
        # zero_str
        if attribute == 'z':
            new = plug(zero_str = self.zero_str, clean_ends = self.clean_ends)
        
        # number
        elif attribute == 'n':
            new = plug(number = self.number, clean_ends = self.clean_ends)
        
        # classic
        elif attribute == 'c':
            new = plug(classic = self.classic, clean_ends = self.clean_ends)
        
        # error if none of the above
        else:
            raise ValueError('attribute must correspond to descriptor')
        
        self.__dict__.update(new.__dict__)
        
        return





































