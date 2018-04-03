# JAscripts
# PWM
# Jasser Alshehri
# Starkey Hearing Technologies
# 2/5/2018


import numpy as np
import matplotlib.pyplot as plt
from numpy import pi, sin, cos, tan, exp
import scipy.signal as sig




def main(args):

    t = np.linspace(0,1,10100)
    fs = 44.1E3
    startTime = 0
    endTime = 1
    t = np.linspace(startTime, endTime, (endTime-startTime)*fs)
    print t

    tri= (sig.sawtooth((t*2*pi*100),width=0.5)+1)*0.5
    sine = ((sin(2*pi*t*3))+1)*0.5
    cmprtr = np.zeros(len(t))

    for i in range(len(t)):
        if sine[i] > tri[i]:
            cmprtr[i] = 1


    plt.figure()
    plt.plot(t,sine)
    plt.plot(t, tri)

    plt.figure()
    plt.plot(t,sine)
    plt.plot(t,cmprtr)
    plt.show()

    return 0


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))