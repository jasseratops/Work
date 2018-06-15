# Work
# clock
# Jasser Alshehri
# Starkey Hearing Technologies
# 5/21/2018


import numpy as np
import matplotlib.pyplot as plt
from numpy import pi, sin, cos, tan, exp

'''
def main(args):
    hours = range(12)
    mins = np.linspace(0,60,241)

    for h in hours:
        for m in mins:
            hangle = (h+(m/60.0))*(360.0/12.0)
            mangle = (m/60.0)*360.0
            angDif = abs(hangle - mangle)


            print hangle
            print mangle
            print angDif

            if angDif < 181 and angDif > 179:
                print str(h) + ':' + str(m)
                print angDif
                print "bingo"
    return 0
'''

def main(args):
    hours = range(12)
    for h in hours:
        m = abs((((180.0*12.0)/360.0)-h)*(1.0/((1.0/60.0)-(1.0/5.0))))
        s = (m-int(m))*60
        print str(h) + ":" + str(int(m))+":" +str(int(s))
    return 0

if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))