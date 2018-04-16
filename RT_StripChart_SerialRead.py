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
import re
import xlwt


port = 'com4'
baud = 9600

mode = 0            # 0: Acc., 1: Gyro., 2: Temp.
axis = 2            # 0: x,    1: y,     2: z


if serial.Serial(port,baud).is_open:
    serial.Serial(port,baud).close()

ser = serial.Serial(port,baud,timeout=1)
ser.reset_input_buffer()
ser.readline()

if mode == 0:
    ind = 0 + axis
    yMin = -16.0
    yMax = 16.0
elif mode == 1:
    ind = 3 + axis
    yMin = -10
    yMax = 10
else:
    ind = 6
    yMin = 10
    yMax = 35

tArray = []
yArray = []


def createTimeStamp():
    ts = time.strftime("%c")
    ts = re.sub(" ", "_", ts)
    ts = re.sub("/", "-", ts)
    ts = re.sub(":", "-", ts)

    return ts

timeStamp = createTimeStamp()

startTime = time.time()

class Scope(object):
    def __init__(self, ax, maxt=4, dt=0.04):
        print "going into scope INIT"
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = [0]
        self.ydata = [0]
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(yMin, yMax)
        self.ax.set_xlim(0, self.maxt)

    def update(self, y):
        print "going into scope UPDATE"
        lastt = self.tdata[-1]
        if lastt > self.tdata[0] + self.maxt:  # reset the arrays
            self.tdata = [self.tdata[-1]]
            self.ydata = [self.ydata[-1]]
            self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
            self.ax.figure.canvas.draw()

        t = time.time() - startTime #self.tdata[-1] + self.dt
        print t
        self.tdata.append(t)
        tArray.append(t)
        self.ydata.append(y)
        self.line.set_data(self.tdata, self.ydata)
        return self.line,

def flush():
    ser.reset_input_buffer()
    ser.readline()


def emitter():
    print "hello from EMITTER"
    while True:
        #print "hello from while loop"
        #flush()
        val = ser.readline()
        print ser.in_waiting
        allData = val.split(",")

        yArray.append(allData)


        yield allData[ind]

fig, ax = plt.subplots()
scope = Scope(ax)

# pass a generator in "emitter" to produce data for the update func
ani = animation.FuncAnimation(fig, scope.update, emitter, interval=10,blit=True)
plt.show()

dataFolder = "C:/Users/alshehrj/Data/"
dataFile = "IMUdata"
dataPath = dataFolder+dataFile + "_" + str(timeStamp)
print(dataPath)

print np.shape(yArray)

def writeToXL(t,yD):
    book = xlwt.Workbook()
    sheet1 = book.add_sheet("data")

    hdrs = ["Time (s)","accX [g]","accY [g]","accZ [g]",
            "gyroX[d/s]","gyroY[d/s]","gyroZ[d/s]","temp [C]"]
    dat = yArray

    noRows = np.shape(dat)[0] + 1
    noCols = len(hdrs)

    for num in range(noRows):               # accomodating for number of data rows + header row
        row = sheet1.row(num)               # choosing a row to operate on
        if num == 0:
            for index in range(noCols):
                value = hdrs[index]
                row.write(index, value)
        else:
            for index in range(noCols):
                if index == 0:
                    value = t[num-1]
                    row.write(index, value)
                else:
                    value = yD[num-1][index-1]
                    row.write(index, value)
        book.save(dataPath+".xls")

writeToXL(tArray,yArray)

print timeStamp
print(tArray)
print(yArray)
