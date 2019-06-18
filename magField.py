# Work
# magField
# Jasser Alshehri
# Starkey Hearing Technologies
# 6/18/2019


import numpy as np
import matplotlib.pyplot as plt
from numpy import pi, sin, cos, tan, exp


def main(args):
    r = np.linspace(1.,5.,101)
    g = [2.E3,4.E3,100.]


    plt.figure()
    plt.plot(r, GvR(g[0],r))
    plt.plot(r, GvR(g[1],r))
    plt.plot(r, GvR(g[2],r))

    plt.show()
    return 0

def GvR(gauss,dist):
    return gauss/(dist**2)

if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))