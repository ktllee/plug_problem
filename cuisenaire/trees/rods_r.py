# -*- coding: utf-8 -*-
"""
last modified: aug 24, 2022

@author: katie

description:
    R-friendly version of rods.py
    
main difference is plotting function was removed
and all funcs are outside class.
        
"""
# dependencies
# packages
import numpy as np

# functions and aliases
from sympy import factor_list
polyroots =  np.polynomial.polynomial.polyroots
polydiv = np.polynomial.polynomial.polydiv


# helper: string to basic converter
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
    
    
# main
def Rodset(represent):
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
            basic = potcon(represent)
        else:
            raise ValueError('string representation must be numeric')
    
    # list of rod lengths
    elif isinstance(represent, list):
        if all(isinstance(x, int) for x in represent):
            represent.sort(key = abs)
            basic = represent
            counts = spotcon(represent)
        else:
            raise ValueError('list representation must contain ints')
    
    # neither
    else:
        raise TypeError('representation must be a list or string')
    
    # polynomials
    # coefficients
    coefs = \
        [-counts[x + 1] for x in range(max(counts.keys()))][::-1] + [1]
    
    # growth rate
    roots = np.round(np.abs(polyroots(coefs)), 10)
    growth = max(roots)
    order = len(coefs) - 1
    
    # full polynomial
    fullpoly = coefcon(coefs)
    
    # factored
    facpoly = [(str(x[0]).replace('**', '^'), x[1]) for x in \
               factor_list(fullpoly)[1]]
    
    # minimal and shift
    minimal = []
    for fac, deg in facpoly:
        if max(np.round(np.abs(polyroots(coefcon(fac))),
                        10)) == growth:
            minimal.append(fac)
    if len(minimal) == 1:
        minimal = minimal[0]
        shiftcoefs = [int(x) if x.is_integer else x for x in \
                      polydiv(coefs, coefcon(minimal))[0].tolist()]
        shift = coefcon(shiftcoefs)
    else:
        shift = 'minimal error'
    
    final =  {'basic': basic,
              'counts': counts,
              'coefs': coefs,
              'roots': roots,
              'growth': growth,
              'order': order,
              'fullpoly': fullpoly,
              'facpoly': facpoly,
              'minimal': minimal,
              'shift': shift}
    
    return final