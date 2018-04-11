# JAscripts
# RT_graph2
# Jasser Alshehri
# Starkey Hearing Technologies
# 3/27/2018

import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import time
port = 'com4'
baud = 9600

if serial.Serial(port,baud).is_open:
    serial.Serial(port,baud).close()

ser = serial.Serial(port,baud,timeout=1)
ser.reset_input_buffer()
ser.readline()


class Scope(object):
    def __init__(self, ax, maxt=2, dt=0.04):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = [0]
        self.ydata = [0]
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(-.1, 2)
        self.ax.set_xlim(0, self.maxt)

    def update(self, y):

        lastt = self.tdata[-1]
        if lastt > self.tdata[0] + self.maxt:  # reset the arrays
            self.tdata = [self.tdata[-1]]
            self.ydata = [self.ydata[-1]]
            self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
            self.ax.figure.canvas.draw()

        t = self.tdata[-1] + self.dt
        self.tdata.append(t)
        self.ydata.append(y)
        self.line.set_data(self.tdata, self.ydata)
        return self.line,


def emitter():
    while True:
        #ser.reset_input_buffer()
        #ser.readline()

        val = ser.readline()
        allData = val.split(",")
        #for i in range(len(allData)):
            #print allData[i]

        yield allData[2]

fig, ax = plt.subplots()
scope = Scope(ax)

# pass a generator in "emitter" to produce data for the update func
ani = animation.FuncAnimation(fig, scope.update, emitter, interval=5,
                              blit=True)
plt.show()