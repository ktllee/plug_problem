# -*- coding: utf-8 -*-
"""
last modified: 06/22/21

@author: katie

description:
    contains class for strips
    (for the plug problem where plugs go into strips)
    
    the strip class contains a verbose list of (plug, id) tuples in order,
    a dictionary of total number of each type of plug on strip,
    and a list representation of total filled spots,
    as well as other defining attributes.
    
    initiated with a total size and an optional list of plugs.
    represented by spaces filled and number of plugs within.
    strips with the same list of plugs are equivalent.
    methods:
        add plug in first available position
        add several plugs
        remove last plug
        show current strip
        return flipped version of strip (refuses if not full)
        reset attributes based on list of plugs
        deep copy
        
    note: does not currently support plugs with hanging ends
"""

from plug_class import Plug

class Strip:
    """ class for strip with defined total length
        must input:
            length (int): total length of the strip
        optional:
            list_plugs (list of plugs to start with)
            list_style (how to initialize list_plugs)
            
        add(plug, style)
        add_multi(plug_list, style)
        remove()
        show()
        flip()
        reset()
        copy()
        is_prime()
        plug_count()
    """
    
    def __init__(self, length, list_plugs = [], list_style = 'n'):
        ''' intitalizes from length.
            can use optional list_plugs and list_style for starting Plugs,
            with styles as below:
                'z' or 'zero_str' for zero_str,
                's' or 'str_num' for str_num,
                'n' or 'number' for number (default),
                'c' or 'classic' for classic,
                'p' or 'plug' for full Plugs
            
            also initializes:
                plug_list (list, list of plugs from optional or empty),
                plug_verbose (list, list of Plugs in each space in strip),
                plug_dict (dict, dictionary of plugs and number used),
                filled (list, '1' or '0' for each position w/ or w/o Plug),
                thickness (list, "thicknesses" in each gap)
        '''
        
        # raise error if length or list isn't appropriate
        if not isinstance(length, int):
            raise TypeError('length must be an int')
            
        if length <= 0:
            raise ValueError('length must be > 0')
            
        if not all((isinstance(list_plugs, list),
                    isinstance(list_style, str))):
            raise TypeError('list_plugs and list_style must be list and str')
        
        # cut off extra style characters
        list_style = list_style[0]
        
        # applying given attributes
        plug_list = [x if list_style == 'p' else Plug(x, list_style) \
                     for x in list_plugs]
            
        # checking plug_list and creating plug_verbose and plug_dict
        plug_verbose = [None] * length
        plug_dict = {}
        
        for item in plug_list:
            
            # refuse if no more space
            if plug_verbose.count(None) == 0:
                raise ValueError('invalid inital list of plugs given')
            
            # find where prongs for next go
            current = plug_verbose.index(None)
            places = [i + current for i, x in enumerate(item.zero_str) \
                      if x == '1']
            
            # place each prong, refuse if not empty
            for pos in places:
                if pos >= length:
                    raise ValueError('invalid inital list of plugs given')
                elif plug_verbose[pos] != None:
                    raise ValueError('invalid inital list of plugs given')
                else:
                    plug_verbose[pos] = (item.copy(), current)
            
            # adding to dictionary
            if item.str_num not in plug_dict:
                plug_dict[item.str_num] = 1
            else:
                plug_dict[item.str_num] += 1
        
        # initialize given attributes
        self.length = length
        self.plug_list = plug_list
        self.plug_verbose = plug_verbose
        self.plug_dict = plug_dict
        
        # initialize other attributes
        self.filled = ['0' if x == None else '1' for x in plug_verbose]
        
        # calculate thickness
        # initialize thickness list, create list to find spread per plug
        thickness = [0] * (length - 1)
        thick_dict = {}
        
        # find distance from beginning to end of each plug
        for i in range(len(plug_verbose)):
            if plug_verbose[i] != None:
                if i == plug_verbose[i][1]:
                    thick_dict[i] = plug_verbose[i][0].length
                
        # add to thickness list appropriately from dict
        for start in thick_dict:
            for i in range(start, start + thick_dict[start] - 1):
                thickness[i] += 1
                
        # initialize
        self.thickness = thickness
            
    
    def __repr__(self):
        ''' uses self.filled and number of plugs for representation.
        '''
        
        plugs = str(len(self.plug_list))
            
        name = ''.join(self.filled) + ' with ' + plugs + ' plugs.'
        
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
        
    
    def add(self, plug_rep, style = 'n'):
        ''' takes: a plug representation with style as below
                'z' or 'zero_str' for zero_str,
                's' or 'str_num' for str_num,
                'n' or 'number' for number (default),
                'c' or 'classic' for classic,
                'p' or 'plug' for full Plugs
                
            returns: a string with outcome of method
                'added' if successfully added
                'incompatible' if the plug cannot be added
                'full' if strip is completely full
                
            note that the strip resets to where it was previously
            without manual oddities in the case of failure.
        '''
        
        # generate plug
        if style == 'p':
            new = plug_rep
        else:
            new = Plug(plug_rep, style)
            
        # refuse if no more space
        if self.plug_verbose.count(None) == 0:
            return 'full'
            
        # check if plug fits
        # find where prongs for next go
        current = self.plug_verbose.index(None)
        places = [i + current for i, x in enumerate(new.zero_str) \
                  if x == '1']
            
        # place each prong, refuse if not empty
        for pos in places:
            if pos >= self.length:
                self.reset()
                return 'incompatible'
            elif self.plug_verbose[pos] != None:
                self.reset()
                return 'incompatible'
            else:
                self.plug_verbose[pos] = (new.copy(), current)
                self.filled[pos] = '1'
        
        # add plug to list
        self.plug_list.append(new)
        
        # add plug to dict
        if new.str_num in self.plug_dict:
            self.plug_dict[new.str_num] += 1
        else:
            self.plug_dict[new.str_num] = 1
            
        # add to thickness
        for i in range(current, current + new.length - 1):
            self.thickness[i] += 1
        
        return 'added'
    
    
    def add_multi(self, list_plugs, list_style = 'n'):
        ''' takes: 
                a list of plug representations,
                one style as below:
                    'z' or 'zero_str' for zero_str,
                    's' or 'str_num' for str_num,
                    'n' or 'number' for number (default),
                    'c' or 'classic' for classic,
                    'p' or 'plug' for full Plugs
                
            returns: a string with outcome of method
                'added' if successfully added
                'incompatible' if a plug cannot be added
                'full' if strip is completely full (before adding)
                
            note that the strip resets to where it was previously
            without manual oddities in the case of failure.
        '''
        
        if not all((isinstance(list_plugs, list),
                    isinstance(list_style, str))):
            raise TypeError('list_plugs and list_style must be list and str')
        
        # cut off extra style characters
        list_style = list_style[0]
        old_list = self.plug_list.copy()
        
        # applying given attributes
        plug_list = [x if list_style == 'p' else Plug(x, list_style) \
                     for x in list_plugs]
            
        for item in plug_list:
            result = self.add(item, 'p')
            if result != 'added':
                self.plug_list = old_list
                self.reset()
                return result
            
        return 'added'
    
    
    def remove(self):
        ''' takes: self
            returns: None
            
            removes the last added plug,
            the plug with the rightmost start point.
            
            note that this method directly modifies the current strip.
        '''
        
        # remove last plug
        new_plugs = self.plug_list[:-1]
        
        # generate new strip
        new = Strip(self.length, new_plugs, 'p')
        self.__dict__.update(new.__dict__)
        
        return
        
        
    def show(self, style = 's'):
        ''' takes:
                self
                optional argument style takes str of type to print:
                    'z' or 'zero_str' for zero_str,
                    's' or 'str_num' for str_num
            returns: None
            
            prints representation of current strip with verbose notation.
        '''
        
        # error for improper style
        if not isinstance(style, str):
            raise TypeError('style must be a str')
        
        # use only first
        style = style[0]
        
        # print
        for item in self.plug_verbose:
            if item == None:
                line = 'empty'
            else:
                if style == 's':
                    line = '(' + str(item[1]) + ', ' + item[0].str_num + ')'
                elif style == 'z':
                    line = '(' + str(item[1]) + ', ' + item[0].zero_str + ')'
                else:
                    raise ValueError('style must be a valid descriptor')
                    
            print(line)
        
        return
        
    
    def flip(self):
        ''' takes: self
            returns: another strip that is flipped version of self
        
            note that this method does not modify current strip,
            and will fail if the strip is not full.
        '''
        
        # refuse if not full
        if self.filled.count('0') != 0:
            raise AssertionError('only full strips can be flipped')
        
        # reverse verbose
        new_verbose = self.plug_verbose[::-1]
        
        # create new list_plugs from reversed list
        new_list = []
        for item in new_verbose:
            if item[0] not in new_list:
                new_list.append(item[0].copy())
            
        # create new strip to return
        new_strip = Strip(self.length, new_list, 'p')
        
        return new_strip
    
    
    def reset(self):
        ''' takes: self
            returns: None
                
            resets based on plug_list.
            
            note that this method directly modifies current strip.
        '''
        
        new_plugs = [x.copy() for x in self.plug_list]
        new = Strip(self.length, new_plugs, 'p')
        self.__dict__.update(new.__dict__)
        
        return
    
    
    def copy(self):
        ''' takes: self
            returns: copy of self
            
            returns a deep copy of the strip.
            note that it takes no manual changes, e.g. it is equivalent to
            first reset(), then deep copy.
        '''
        
        new_plugs = [x.copy() for x in self.plug_list]
        new = Strip(self.length, new_plugs, 'p')
        
        return new
    
    
    def is_prime(self):
        ''' takes: self
            returns: bool for if the strip is prime
            
            strips are prime if the thickness is never 0.
            note that strips of length 1 are always prime.
        '''
        
        return self.thickness.count(0) == 0
    
    
    def plug_count(self):
        ''' takes: self
            returns: number of plugs currently in the strip
            
            a shortcut.
        '''
        
        return len(self.plug_list)
    
#####

# testing

if __name__ == '__main__':
    print('testing Strip class...')
    
    # init list of failures
    fails = []
    
    # strips for testing
    strip_blank = Strip(7)
    strip_init = Strip(5, [9, 1])
    
    strip_multi = Strip(7, [5, 21, 5])
    strip_gap = Strip(4, [3, 3])
    
    strip_add = Strip(5, [9, 1])
    strip_add.add(5)
    
    strip_build = Strip(5)
    strip_build.add(9)
    strip_build.add(1)
    strip_build.add(5)
    
    strip_fast = Strip(7, [5])
    strip_fast.add_multi([21,5])
    
    strip_remove = strip_add.copy()
    strip_remove.remove()
    
    strip_flip = Strip(5, [9, 1, 5]).flip()
    
    # correct dictionaries
    corr_dict_blank = {
        'length': 7,
        'plug_list': [],
        'plug_verbose': [None, None, None, None, None, None, None],
        'plug_dict': {},
        'filled': ['0', '0', '0', '0', '0', '0', '0'],
        'thickness': [0, 0, 0, 0, 0, 0]}
    
    corr_dict_init = {
        'length': 5,
        'plug_list': [Plug(9), Plug(1)],
        'plug_verbose': [(Plug(9),0), (Plug(1),1), None, (Plug(9),0), None],
        'plug_dict': {'9': 1, '1': 1},
        'filled': ['1', '1', '0', '1', '0'],
        'thickness': [1, 1, 1, 0]}
    
    corr_dict_multi = {
        'length': 7,
        'plug_list': [Plug(5), Plug(21), Plug(5)],
        'plug_verbose': [(Plug(5),0),
                         (Plug(21),1),
                         (Plug(5),0),
                         (Plug(21),1),
                         (Plug(5),4),
                         (Plug(21),1),
                         (Plug(5),4)],
        'plug_dict': {'5': 2, '21': 1},
        'filled': ['1', '1', '1', '1', '1', '1', '1'],
        'thickness': [1, 2, 1, 1, 2, 1]}
    
    corr_dict_gap = {
        'length': 4,
        'plug_list': [Plug(3), Plug(3)],
        'plug_verbose': [(Plug(3),0),
                         (Plug(3),0),
                         (Plug(3),2),
                         (Plug(3),2)],
        'plug_dict': {'3': 2},
        'filled': ['1', '1', '1', '1'],
        'thickness': [1, 0, 1]}
    
    corr_dict_add = {
        'length': 5,
        'plug_list': [Plug(9), Plug(1), Plug(5)],
        'plug_verbose': [(Plug(9),0),
                         (Plug(1),1),
                         (Plug(5),2),
                         (Plug(9),0),
                         (Plug(5),2)],
        'plug_dict': {'9': 1, '1': 1, '5': 1},
        'filled': ['1', '1', '1', '1', '1'],
        'thickness': [1, 1, 2, 1]}
    
    corr_dict_flip = {
        'length': 5,
        'plug_list': [Plug(5), Plug(9), Plug(1)],
        'plug_verbose': [(Plug(5),0),
                         (Plug(9),1),
                         (Plug(5),0),
                         (Plug(1),3),
                         (Plug(9),1)],
        'plug_dict': {'9': 1, '1': 1, '5': 1},
        'filled': ['1', '1', '1', '1', '1'],
        'thickness': [1, 2, 1, 1]}
    
    corr_dict_reset = {
        'length': 5,
        'plug_list': [],
        'plug_verbose': [None, None, None, None, None],
        'plug_dict': {},
        'filled': ['0', '0', '0', '0', '0'],
        'thickness': [0, 0, 0, 0]}
    
    
    # all tests
    tester = [('blank', strip_blank, corr_dict_blank),
              ('init', strip_init, corr_dict_init),
              ('multi', strip_multi, corr_dict_multi),
              ('gap', strip_gap, corr_dict_gap),
              ('add', strip_add, corr_dict_add),
              ('build', strip_build, corr_dict_add),
              ('fast', strip_fast, corr_dict_multi),
              ('remove', strip_remove, corr_dict_init),
              ('flip', strip_flip, corr_dict_flip)]
    
    # iterate over tester
    for test in tester:
        print(test[0] + '...')
        
        for key in test[2]:
            if test[1].__dict__[key] != test[2][key]:
                key_note = key + ', ' + test[0]
                fails.append(key_note)
    
    # testing the copy method
    print('copy...')
    strip_reset = strip_build.copy()
    strip_reset.plug_list = []
    
    for key in corr_dict_add:
        if strip_build.__dict__[key] != corr_dict_add[key]:
            key_note = key + ', copy'
            fails.append(key_note)
    
    # testing the reset method
    print('reset...')
    strip_reset.reset()
    
    for key in corr_dict_reset:
        if strip_reset.__dict__[key] != corr_dict_reset[key]:
            key_note = key + ', reset'
            fails.append(key_note)
            
    # testing equivalency
    print('equivalence...')
    if any((strip_add != strip_build,
            strip_flip.flip() != strip_add,
            strip_blank == strip_reset)):
        fails.append('equivalence')
        
    print('shortcuts...')
    if any((strip_add.plug_count() != 3,
            strip_add.is_prime() == False,
            strip_gap.is_prime())):
        fails.append('shortcuts')
    
    print('done.')
    
    # showing failures
    print()
    print('failed tests:')
    
    if fails == []:
        print('none.')
        
    else:
        for x in fails:
            print(x)
    


































