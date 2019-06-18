# Work
# Rome_MicFlex_Test
# Jasser Alshehri
# Starkey Hearing Technologies
# 4/11/2019


import numpy as np
import matplotlib.pyplot as plt
from numpy import pi, sin, cos, tan, exp
import pyupv

def main(args):
    sensTol=3
    einTol =3
    frqs = np.array([250.,1000.,7000.])
    sensLim = np.array([50.,60.,55.])

    einLim = np.array([20.,30.,40.])
    micSens = getSens()

    micNoise = getNoise()
    micEIN = micNoise - micSens

    if np.max(np.abs(micSens-sensLim))>=sensTol:
        print "Bad Sense"
    if np.max(np.abs(micEIN-einLim))>=einTol:
        print "Bad EIN"

    dataLimPlot(frqs,micSens,sensLim,sensTol)
    dataLimPlot(frqs, micEIN, einLim,einTol)


    return 0

def getSens():
    junk = np.array([50,62,53])
    sens = junk
    return sens

def getNoise():
    return 0

def dataLimPlot(frq,data,lim,tol):
    N = 3
    upLimLine = np.zeros(N*len(lim))
    loLimLine = np.zeros(N*len(lim))

    for i in range(len(lim)):
        for x in range(N):
            upLimLine[N*i+x] = lim[i]+tol
            loLimLine[N*i+x] = lim[i]-tol

    limFrq = np.zeros(N*len(frq))
    for i in range(len(lim)):
        limFrq[N*i:(N*(i+1))] = np.geomspace(0.9*frq[i],1.1*frq[i],N)



    plt.figure()
    for i in range(len(frq)):
        plt.semilogx(limFrq[N * i:(N * (i + 1))], loLimLine[N * i:(N * (i + 1))],color="red")
        plt.semilogx(limFrq[N * i:(N * (i + 1))], upLimLine[N * i:(N * (i + 1))],color="red")
        plt.semilogx(limFrq[N * i:(N * (i + 1))],data[i]*np.ones(N),color="blue",linestyle=":")

    plt.xlim(100,1E4)
    plt.show()


    return 0

if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))