# JAscripts
# SquareConstruction
# Jasser Alshehri
# Starkey Hearing Technologies
# 1/10/2018


import numpy as np
import matplotlib.pyplot as plt
from numpy import pi, sin, cos, tan, exp


def main(args):
    t = np.linspace(0,1,101)
    fund = sin(pi*t)
    cnstrct = fund

    n = 150

    plt.figure()
    plt.plot(t,fund,label= "fund")
    for i in range(2,n):
        harmonic = sin(pi * t * ((2 * i) - 1))
        plt.plot(t,harmonic,label= "n=" + str(i))
        cnstrct += harmonic
    plt.legend()

    plt.figure()
    plt.plot(t,cnstrct,label="cnstrct")
    plt.legend()
    plt.show()

    return 0


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))