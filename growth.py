
"""
code to calculate growth rate for plug puzzles using
arbitrary numbers of plugs R_k = 11....1

last modified: 07/17/21

@author: Ethan Bolker
"""
import sys
import math
from convolve import p2t

def mygcd(mylist):
    if len(mylist) == 1:
        return mylist[0]
    else:
        return math.gcd( mylist[0],mygcd(mylist[1:]))

def growthrate(d):
    ''' Calculate the growth rate for total solutions
    for the puzzle problem R(d). Here d is the  
    bit string specifying which R_k are allowed. 
    The algorithm pads with lots of 0s to stabilize growth.
    Return -1 if the allowed valuse of k have a nontrivial gcd.
    '''
    if isinstance(d, str): # d is a bitstring like "101"
        xd = list(map(int, list(d)))
    elif isinstance(d, int): # convert integer d to binary
        xd = [int(i) for i in bin(d)[2:]]
    else:
        print(f"type error {d}")
        return
    rplugnumbers = []
    for n in range(len(xd)):
        if xd[n] == 1:
            rplugnumbers.append(n+1)
    if mygcd(rplugnumbers) > 1 :
        return -1
    xd.extend([0]*1000)
    totals = p2t(xd)
    rate = totals[1000]/totals[999]
    return(rate)

    
#  Execute for testing
if __name__ == "__main__":

    if (len(sys.argv) == 1):
        print(f"usage: python {sys.argv[0]} N (for rates up to d = 2^N - 1)")
    else:
        N = int(sys.argv[1])
        print(N)
        print("d,  growth rate")
        for d in range(1, 1+2**N,2):
            print(f"{bin(d)[2:]}, {growthrate(d)}")
            print(f"{bin(2*d)[2:][::-1]}, {growthrate(bin(2*d)[2:][::-1])}")
            print(f"{bin(4*d)[2:][::-1]}, {growthrate(bin(4*d)[2:][::-1])}")


              
