
"""
code to calculate the prime to total and total to count
convolutions for an arbitrary integer sequence

last modified: 07/01/21

@author: Ethan Bolker
"""
import sys

def p2t( p ):
    ''' 
    input p is a list of prime counts
    output t is a list of total counts
    '''
    firstspot = p.index(next(filter(lambda x: x!=0, p))) 
    t = p[:firstspot+1] # copy p to t as far as first nonzero entry
    rr = range(1+firstspot, len(p))
#     print(rr)
    for i in rr:
        nextt = p[i]
        for j in range(i):
#               print(f"loop {j} {i-j-1} {p[j]}*{t[i-j-1]}")
            nextt += p[j]*t[i-j-1]
        t.append(nextt)
    return t


def t2p( t ):
    ''' 
    input t is a list of total counts
    output p is a list of prime counts
    '''
    p= []
    p.append(t[0])
    for i in range(len(t))[1:]:
        nextp = t[i]
        for j in range(i):
            nextp -= t[j]*p[i-j-1]        
        p.append(nextp)
    return p

def execute(x):
    print(f"input {x}")
    t = p2t(x)
    print(f"p2t: {t}")
    p = t2p(x)
    print(f"t2p {p}")
    check = t2p(t)
    print(f"should see True {x == check}")
#     print(f"p2t(t2p): {p2t(p)}\n")

#  Execute for testing
if __name__ == "__main__":

    if (len(sys.argv) == 1):
        print(f"usage: python {sys.argv[0]} a b c ...")
    else:
        new =  list(map(int, sys.argv[1:]))
        execute(new)

    ones = [1,1,1,1,1,1]
    powers = [1,2,4,8,16,32]
    ints = [1,2,3,4,5,6,7,8,9]
    plugt2 = [1,0,0,0,0,0,0]
    interesting = [0,0,0,1,0,2,0,1,0,1,0,1,0,1,0,1]
    binom = [1,5,10,10,5,1]
    unbells = [1, 1, 2, 6, 22, 92, 426, 214]
    bells = [1, 2, 5, 15, 52, 203, 877, 4140]
#     execute(interesting)
#     execute(ints)
#     execute(ones)
#     execute(powers)
#     execute(plugt2)


