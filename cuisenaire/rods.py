# -*- coding: utf-8 -*-
"""
last modified: aug 24, 2022

@author: katie

description:
    contains class for rod sets
    (for problems involving sets of cuisenaire rods)
    
    the Rodset class contains defining information for a group of rods.
    
    initiated with a dictionary of counts or list of rods in the set.
    
    represented by list (basic) descriptor.
    rodsets with the same basic representation are equivalent.
    
    attributes:
        basic - list of rod lengths
        counts - dict listing rod lengths (e.g. [2,3] = {1:0, 2:1, 3:1})
        coefs - list of coefs for the rod polynomial
        roots - all the roots (absolute value, rounded to 10 places)
        growth - max root
        order - degree of polynomial
        fullpoly - the full polynomial, written out
        facpoly - the full polynomial factored
        minimal - the minimal polynomial
        shift - the shift polynomial (fully expanded)
                
    methods:
        init, repr, eq
        copy - deep copy
        isminimal - is the rodset minimal?
        plotroots - plot the roots on the complex plane
        spotcon (helper) - switch between list and dictionary representations
        coefcon (helper) - switch between polynomial string and coef list
        
    dependencies:
        numpy as np
        matplotlib.pyplot as plt
        factor_list() from sympy
        polyroots() and polydiv() from numpy.polynomial.polynomial
        
"""
# dependencies
# packages
import numpy as np
import matplotlib.pyplot as plt

# functions
from sympy import factor_list
from numpy.polynomial.polynomial import polyroots
from numpy.polynomial.polynomial import polydiv


class Rodset:
    """ class for set of cuisenaire rods
        must input one of below as represent:
            string (str): string containing number of rods at each length
            group (list): list of positive integer lengths of rods in set
            
        e.g. the padovans would be [2,3] or '011'.  note [2,2] is '02'
    """
    
    ########## helpers
    # helper: string to basic converter
    @staticmethod
    def spotcon(rep):
        ''' changes a dictionary representaion of a rodset to a list
            or vice versa.
            
            note:
                - assumes rep is already correctly one or the other
                - [1,-3,-3,4] <-> {1:1, 2:0, 3:-2, 4:1}
        '''
        
        # dict to list
        if isinstance(rep, str):
            converted = []
            for key in rep:
                converted.extend([key if rep[key] > 0 else -key for \
                                  x in range(abs(rep[key]))])
            
        # list to dict
        elif isinstance(rep, list):
            converted = {}
            for i in range(abs(max(rep, key = abs))):
                pos = rep.count(i + 1)
                neg = rep.count(-(i + 1))
                if pos >= neg:
                    converted[i + 1] = pos
                else:
                    converted[i + 1] = -neg
        
        return converted
    
    
    # helper: string to basic converter
    @staticmethod
    def coefcon(poly):
        ''' changes a string representaion of a polynomial to a list of coefs
            or vice versa.
            
            note:
                - assumes rep is already correctly one or the other
                - poly strings must be fully expanded
        '''
        
        # string to list
        if isinstance(poly, str):
            # find degrees and coefficients
            power = {}
            sign = 1
            poly = poly.replace('^', '**')
            for t in poly.split():
                if t == '-':
                    sign = -1
                elif t == '+':
                    sign = 1
                else:
                    term = t.split('*')
                    deg, coef = 1, 1
                    if '' in term:
                        deg = int(term[-1])
                    elif 'x' not in term:
                        deg = 0
                    if term[0] != 'x':
                        coef = int(term[0])
                    power[deg] = coef * sign
            # convert to coefficient list
            converted = [0] * (max(power.keys()) + 1)
            for i in range(len(converted)):
                if i in power.keys():
                    converted[i] = power[i]
            
        # list to string
        elif isinstance(poly, list):
            converted = ''
            top = len(poly) - 1
            if top == 0:
                converted = str(poly[0])
            else:
                # iterate through coefficients
                for deg, coef in enumerate(poly):
                    term = ''
                    # handle coefficient
                    if coef == 1:
                        term += ' + '
                    elif coef == -1:
                        term += ' - '
                    elif coef > 0:
                        term += f" + {coef}*"
                    elif coef < 0:
                        term += f" - {abs(coef)}*"
                    # handle degree
                    if coef != 0:
                        if deg == 0:
                            if abs(coef) == 1:
                                term += '1'
                            else:
                                term = term[:-1]
                        elif deg == top:
                            if coef == 1:
                                if deg == 1:
                                    term = "x"
                                else:
                                    term = f"x^{deg}"
                            elif coef == -1:
                                if deg == 1:
                                    term == "-x"
                                else:
                                    term = f"-x^{deg}"
                            else:
                                term = f"{coef}*x^{deg}"
                        elif deg == 1:
                            term += 'x'
                        elif deg < top:
                            term += f"x^{deg}"
                            
                    # add to converted
                    converted = term + converted
        
        return converted
    
    
    ########## class methods
    # initialize
    def __init__(self, represent):
        ''' intitalizes from a descriptive attribute (represent),
            either list of lengths (basic) or bit string (string).
                
            also initializes:
                coefs
                roots
                growth
                order
                fullpoly
                facpoly
                minimal
                shift
                
            note: ONLY works for rod polys.
        '''
        
        # find which argument was given and fill others
        # also raise errors for invalid values and types
        if isinstance(represent, dict):
            if represent.isnumeric():
                counts = represent
                basic = self.spotcon(represent)
            else:
                raise ValueError('string representation must be numeric')
        
        # list of rod lengths
        elif isinstance(represent, list):
            if all(isinstance(x, int) for x in represent):
                represent.sort(key = abs)
                basic = represent
                counts = self.spotcon(represent)
            else:
                raise ValueError('list representation must contain ints')
        
        # neither
        else:
            raise TypeError('representation must be a list or string')
            
        # initialize attributes
        # given attributes
        self.counts = counts
        self.basic = basic
        
        # polynomials
        # coefficients
        coefs = \
            [-counts[x + 1] for x in range(max(counts.keys()))][::-1] + [1]
        self.coefs = coefs
        
        # growth rate
        roots = np.round(np.abs(polyroots(coefs)), 10)
        growth = max(roots)
        order = len(coefs) - 1
        self.roots = roots
        self.growth = growth
        self.order = order
        
        # full polynomial
        fullpoly = self.coefcon(coefs)
        self.fullpoly = fullpoly
        
        # factored
        facpoly = [(str(x[0]).replace('**', '^'), x[1]) for x in \
                   factor_list(fullpoly)[1]]
        self.facpoly = facpoly
        
        # minimal and shift
        minimal = []
        for fac, deg in facpoly:
            if max(np.round(np.abs(polyroots(self.coefcon(fac))),
                            10)) == growth:
                minimal.append(fac)
        if len(minimal) == 1:
            minimal = minimal[0]
            shiftcoefs = [int(x) if x.is_integer else x for x in \
                          polydiv(coefs, self.coefcon(minimal))[0].tolist()]
            shift = self.coefcon(shiftcoefs)
        else:
            shift = 'minimal error'
        self.minimal = minimal
        self.shift = shift
        
        
    # represent
    def __repr__(self):
        ''' basic (list) representation.
        '''
        
        return str(self.basic)
    
    
    # equal
    def __eq__(self, other):
        ''' rodsets are the same if they have the same list of rods.
            if other is not Rodset, return False.
        '''
        
        if not isinstance(other, Rodset):
            return False
        
        if self.basic == other.basic:
            return True
        else:
            return False
        
    
    # (deep) copy
    def copy(self):
        ''' takes: self
            returns: a deep copy of self
            
            note that this carries over any manually-created quirks.
        '''
        
        new = Rodset('1')
        
        for key in self.__dict__:
            new.__dict__[key] = self.__dict__[key]
        
        return new
    
    
    # check if rodset is minimal
    def isminimal(self):
        ''' takes: self
            returns: bool of whether the rodset is minimal
        '''
        return self.shift == '1'
    
    
    # plot roots
    def plotroots(self):
        ''' takes: self
            returns: None
            
            shows plot of roots on the complex plane
        '''
        
        # find roots  
        data = polyroots(self.coefs)
        x = data.real
        y = data.imag
    
        # circle through roots of minimal poly
        circles = []
        if self.shift != 'minimal error':
            cdata = np.round(np.abs(polyroots(self.coefcon(self.minimal))), 10)
            for c in cdata:
                circles.append(plt.Circle((0,0), c, fill = False, ec = 'r'))
        
        # plot
        # roots
        fig, ax = plt.subplots()
        ax.plot(x, y, 'b*')
        if len(self.basic) < 10:
            plt.xlabel(str(self.basic))
        # circles
        for c in circles:
            ax.add_patch(c)
            
        # sizing
        ax.set_aspect('equal')
        gmax = self.growth * 1.1
        plt.xlim(-gmax, gmax)
        plt.ylim(-gmax, gmax)
    
        plt.show()
        
        return


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