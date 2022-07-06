"""
Call plug puzzle solver from command line

last modified: 07/14/2021

@author: Ethan Bolker
"""
import sys
import flex_solver

if __name__ == "__main__":

    if (len(sys.argv) < 3):
        print(f"usage: python {sys.argv[0]} striplength plug# plug# ...\nor")
        print(f"       python {sys.argv[0]} loop maxlength plug# plug# ...")
    elif (sys.argv[1] == "loop"):
        out = []
        for n in range(int(sys.argv[2]))[1:]:
            out.append(len(flex_solver.flex(n, sys.argv[3:])))
        print(out)
    else:
        answer = flex_solver.flex(int(sys.argv[1]), sys.argv[2:])
        for x in answer:
            print(x)


# python3.6 solve.py 20 3 7
# [0, 1, 1, 1, 2, 2, 3, 4, 5, 7, 9, 12, 16, 21, 28, 37, 49, 65, 86]



#         answer = flex_solver.flex(int(sys.argv[1]), sys.argv[2:], result_style='f')
#         print(answer)
#         for strip in answer:
#             print(strip)
#             for plug in strip.getplugs():
#                 print(f"{plug.format(style='something'}")
#                 print(f"isprime? {plug.isprime()}")



# 0 0 1 0 1 1 0 2 1 1 3 1 3 4 2 6 5 5 10
