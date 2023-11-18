# -*- coding: utf-8 -*-
"""
last modified: 06-29-2023

@author: katie

description:
    functions from class for rod sets made R-friendly
    class initialization transformed into functions for polynomials.
    
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
                
    methods:
        init, repr, eq
        copy - deep copy
        spotcon (helper) - switch between list and dictionary representations
        coefcon (helper) - switch between polynomial string and coef list
        
    dependencies:
        factor_list() from sympy
        round() and abs() from numpy
        polyroots() and polydiv() from numpy.polynomial.polynomial
        
"""
# dependencies
from sympy import factor_list
from numpy import round as np_round
from numpy import abs as np_abs
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
        if isinstance(rep, dict):
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
                
                REMOVED:
                minimal
                shift
                
            note: ONLY works for rod polys.
        '''
        
        # find which argument was given and fill others
        # also raise errors for invalid values and types
        if isinstance(represent, dict):
            if all(isinstance(x, int) for x in represent.keys()):
                basic = self.spotcon(represent)
                counts = self.spotcon(basic)
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
        roots = np_round(np_abs(polyroots(coefs)), 10)
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
