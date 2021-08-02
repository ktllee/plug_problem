"""

Utilities for plug puzzle python.

last modified: 07/29/21

@author: Ethan Bolker

These are not as pythonic as they ought to be. 
Too many loops, too little list comprehension.

No error checking for input values.
"""
import sys

def spots2bits(spots):
    '''expects list like [2,3] with positions of 1 bits
       returns bit list like [0, 1, 1]
    '''
    bits = [0]*max(spots)
    for i in spots:
        bits[i-1] = 1
    return bits

def bits2spots(bits):
    '''expects bit list like [0, 1, 1] 
       returns list of positions like [2,3]
    '''
    spots = []
    for i in range(len(bits)):
        if bits[i] == 1:
            spots.append(i+1)
    return spots

def bits2bitstring(bits):
    '''expects bit list like [0, 1, 1] 
       returns bitstring like '011'
    '''
    bitstring = ''
    for bit in bits:
        bitstring += str(bit)
    return bitstring
    
def spots2bitstring(spots):
    '''expects list like [2,3] 
       returns bitstring '011'
    '''
    return bits2bitstring(spots2bits(spots))

def bitstring2spots(bitstring):
    '''expects bitstring '011'
       returns list [2,3] 
    '''
    return bits2spots(bitstring2bits(bitstring))

# 
def bitstring2bits(bitstring):
    '''expects bitstring like '011'
       returns bit list like [0, 1, 1] 
    '''
    return [int(bit) for bit in bitstring]


#  Execute 
if __name__ == "__main__":

    bits = [0, 1, 1]
    spots = [2,3]
    bitstring = '011'
    
    print(f"bits {bits}, bits2spots {bits2spots(bits)}")
    print(f"spots {spots}, spots2bits {spots2bits(spots)}")
    print(f"bits {bits}, bits2bitstring {bits2bitstring(bits)}")
    print(f"bitstring {bitstring}, bitstring2bits {bitstring2bits(bitstring)}")    
    print(f"spots {spots}, spots2bitstring {spots2bitstring(spots)}")
    print(f"bitstring {bitstring}, bitstring2spots {bitstring2spots(bitstring)}")
