# Work
# TwosComp
# Jasser Alshehri
# Starkey Hearing Technologies
# 5/4/2018


import numpy as np
import matplotlib.pyplot as plt
from numpy import pi, sin, cos, tan, exp

MSB = 0b0111;
LSB = 0b1111;

def main(args):
    print twosCompConv(MSB,LSB,4)
    return 0


def twosCompConv(MSB,LSB,length=8):                 # Length is how many bits is in EACH MSB and LSB
    conc = (MSB<<length)|LSB                        # Concatenate MSB and LSB

    if len(str(bin(conc))) < ((length*2)+2):        # Checks if the number has been shortened due to leading zeros (i.e. the MS bit is 0)
        answer = conc                               # Answer is positive representation from binary
    else:                                           # If the MS bit is NOT zero,
        answer = -1 * ((2 ** (length * 2)) - conc)  # the number is translated from two's compliment.

    return answer


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))