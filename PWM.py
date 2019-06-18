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
    fs = 4*44.1E3
    startTime = 0
    endTime = 0.05
    f = 40.
    t = np.linspace(startTime, endTime, (endTime-startTime)*fs)
    print t

    tri= (sig.sawtooth((t*2*pi*1000.E3),width=0.5)+1)*0.5
    sine = ((sin(2*pi*t*f))+1)*0.5
    cmprtr = np.zeros(len(t))
    cmprtr2= np.zeros(len(t))
    for i in range(len(t)):
        if sine[i] > tri[i]:
            cmprtr[i] = 1

    sq = (sig.square((t*2*pi*10.E3))+1)*0.5

    for i in range(len(t)):
        if sine[i] > sq[i]:
            cmprtr2[i] = 1
    fc = 15.E3
    data1 = butter_lowpass_filter(cmprtr,fc,fs)
    data2 = butter_lowpass_filter(cmprtr2,fc,fs)

    plt.figure()
    plt.subplot(411)
    plt.plot(t,sine)
    plt.subplot(412)
    plt.plot(t,tri)
    plt.subplot(413)
    plt.plot(t,cmprtr)
    plt.subplot(414)
    plt.plot(t,data1)

    plt.figure()
    plt.subplot(411)
    plt.plot(t,sine)
    plt.subplot(412)
    plt.plot(t,sq)
    plt.subplot(413)
    plt.plot(t,cmprtr2)
    plt.subplot(414)
    plt.plot(t,data2)

    plt.show()

    return 0

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = sig.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = sig.lfilter(b, a, data)
    return y



if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))