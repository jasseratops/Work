# JAscripts
# envDet3
# Jasser Alshehri
# Starkey Hearing Technologies
# 11/10/2017


import numpy as np
import matplotlib.pyplot as plt
from numpy import pi, sin, exp
import scipy.signal as sig


def main(args):

    fs = 44.1E3                     # sample rate
    endtime = 1.00                     # Time array end time
    noSamples = endtime*fs          # number of samples in time array
    t = np.linspace(0.00,endtime,noSamples)    # generate time array
    sPeriod = 1/fs
    sSamples = int(sPeriod*noSamples)


    freq = 100                      # Stimulus frequency.

    inp = sin(2*pi*freq*t)
    noise = (np.random.randn(len(inp))-0.5)/5 # Generate noise
    inpN = inp+noise                # Add noise to clean stimulus for real world modeling
    outp = np.zeros(len(inp))       # initialize hearing aid output array

    '''Create high and low input levels'''
    for i in range(len(inpN)):
        if i < sSamples:
            inpN[i] = noise[i]
        elif i < (len(inp)/2):
            inpN[i] = 2*inp[(i)] + noise[i]
        else:
            inpN[i] = inp[(i)] + noise[i]

    tau = 0.1                       # Time constant for both attack and release
    gain = 2                        # Hearing aid gain

    '''Grab hearing aid output'''
    for i in range(len(inpN)):
        if i < sSamples:
            outp[i] = gain*inpN[i]
        elif i < (len(inp)/2):
            outp[i] = inpN[i]*(gain+exp(-t[i-1000]/tau))        # Compression attack
        else:
            outp[i] = inpN[i]*(gain-exp(-t[i-(len(inp)/2)]/tau)) # Compression release

    env = abs(sig.hilbert(np.abs(outp)))  # envelope detection. go nuts!

    smooth = np.array(np.shape(env))

    b, a = sig.butter(3,(50/fs),btype="lowpass")

    zi = sig.lfilter_zi(b,a)
    z,_= sig.lfilter(b,a,env,zi=zi*env[0])

    plt.figure()
    plt.plot(t,inpN,label="input to hearing aid")
    #plt.plot(t,outp,label="output of hearing aid")
    #plt.plot(t,env,label="envelope")
    #plt.plot(t,z,label="filtered envelope")
    #plt.plot(t,filtinp,label="env of filt. input")
    plt.legend()
    plt.show()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))