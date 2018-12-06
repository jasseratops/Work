# Work
# TCoilCoeff
# Jasser Alshehri
# Starkey Hearing Technologies
# 11/26/2018


import numpy as np
import matplotlib.pyplot as plt
from numpy import pi, sin, cos, tan, exp
import scipy.signal as sig


def main(args):
    b = [0.605,-1.194,0.766,-0.169,0.013]
    a = [1.000,-1.799,0.834]
    w,h = sig.freqz(b,a)

    mag = 20*np.log10(abs(h))
    mag = abs(h)


    plt.figure()
    plt.plot(w,mag)
    plt.show()
    return 0


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))