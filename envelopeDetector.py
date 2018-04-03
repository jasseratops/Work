#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  envelopeDetector.py
#  
#  Copyright 2017 Jasser Alshehri <jasser_alshehri@starkey.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import numpy as np
from scipy.signal import hilbert
from scipy import signal
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import math



def main(args):
  
  x = np.linspace(0,50,10001)
  freqs = np.logspace(0,4,num=1000)
  
  print len(x),np.shape(x)
  
  y = np.zeros(len(x))
  z = np.zeros(len(x))
  env = np.array(len(x),dtype=complex)
  envN = np.array(len(x),dtype=complex)
    
  
  print x,y,z
  for i in range(len(x)):
    y[i] = math.sin(2*math.pi*x[i])
    z[i] = y[i]*(1/math.exp(x[i]))
  
  envN = abs(signal.hilbert(z))
  env = np.convolve(envN,np.ones(len(envN)),'same')/float(len(envN))
  
  
  q_u = np.zeros(len(z))
  
  u_x = [0,]
  u_y = [z[0],]
  
  for k in xrange(1,len(z)-1):
    if (np.sign(z[k]-z[k-1])==1) and (np.sign(z[k]-z[k+1])==1):
        u_x.append(k)
        u_y.append(z[k])
        
  u_x.append(len(z)-1)
  u_y.append(z[-1])

  u_p = interp1d(u_x,u_y, kind = 'nearest',bounds_error = False, fill_value=0.0)
  
  for k in xrange(0,len(z)):
    q_u[k] = u_p(k)
  
  plt.figure()
  #plt.subplot(211)
  #plt.plot(x,y)
  plt.plot(x,z)
  #plt.plot(x,env)
  #plt.plot(x,envN)
  #plt.plot(x,q_u)

  #plt.subplot(212)
  #plt.semilogx(freqs,abs(specdecomp))
  plt.show()
  return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
