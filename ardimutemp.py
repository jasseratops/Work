# JAscripts
# RT_graph2
# Jasser Alshehri
# Starkey Hearing Technologies
# 3/27/2018
# This was developed on matplotlib 2.0.2, and will not work with matplotlib 2.2.2

##### User Config #####
dataFolder = "C:/Users/alshehrj/Data/"
dataFile = "testTemp"

# Baseline
# 1p8dBV
# 11p08dBV


port = 'com7'  # Configure which port the Arduino is connected to.

mode = 2  # 0: Acc., 1: Gyro., 2: Temp.
axis = 2  # 0: x,    1: y,     2: z
####################################


import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import time
import re
import xlwt
from Tkinter import *

tArray = []
yArray = []


def createTimeStamp():
    ts = time.strftime("%c")
    ts = re.sub(" ", "_", ts)
    ts = re.sub("/", "-", ts)
    ts = re.sub(":", "-", ts)

    return ts


class Scope(object):
    def __init__(self, ax, maxt=60, dt=1.00):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = [-dt]
        self.ydata = [0]
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(yMin, yMax)
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
        tArray.append(t)
        self.ydata.append(y)
        self.line.set_data(self.tdata, self.ydata)
        return self.line,


def flush():
    # ser.reset_input_buffer()
    ser.readline()

i =0

def emitter():
    global i
    while True:
        if i > 60:
            StopIteration
            i = 0
            return
        # flush()
        val = ser.readline()
        allData = val.split(",")
        #print ser.in_waiting
        yArray.append(allData[:-1])  # discarding return line characters from the serial read.
        i +=1
        yield allData[ind]

def writeToXL(t, yD, path):
    book = xlwt.Workbook()
    sheet1 = book.add_sheet("data")

    hdrs = ["Time (s)", "accX [g]", "accY [g]", "accZ [g]",
            "gyroX[deg/s]", "gyroY[deg/s]", "gyroZ[deg/s]", "temp [C]"]
    accHdrs = hdrs[0:4]
    gyroHdrs = hdrs[0:1] + hdrs[4:7]
    tempHdrs = hdrs[0:1] + hdrs[7:]
    dat = yArray

    noRows = np.shape(dat)[0] + 1
    noCols = len(hdrs)

    for num in range(noRows):  # accomodating for number of data rows + header row
        row = sheet1.row(num)  # choosing a row to operate on
        if num == 0:
            for index in range(noCols):
                value = hdrs[index]
                row.write(index, value)
        else:
            for index in range(noCols):
                if index == 0:
                    value = float("{0:.2f}".format(t[num - 1]))
                    row.write(index, value)
                else:
                    value = float("{0:.2f}".format(float(yD[num - 1][index - 1])))
                    row.write(index, value)

    ###### Add AccData separately ######
    sheet2 = book.add_sheet("accData")
    noRows = np.shape(dat)[0] + 1
    noCols = len(accHdrs)

    for num in range(noRows):  # accomodating for number of data rows + header row
        row = sheet2.row(num)  # choosing a row to operate on
        if num == 0:
            for index in range(noCols):
                value = accHdrs[index]
                row.write(index, value)
        else:
            for index in range(noCols):
                if index == 0:
                    value = float("{0:.2f}".format(t[num - 1]))
                    row.write(index, value)
                else:
                    value = float("{0:.2f}".format(float(yD[num - 1][index - 1])))
                    row.write(index, value)

    ###### Add GyroData separately ######
    sheet3 = book.add_sheet("gyroData")
    noRows = np.shape(dat)[0] + 1
    noCols = len(gyroHdrs)

    for num in range(noRows):  # accomodating for number of data rows + header row
        row = sheet3.row(num)  # choosing a row to operate on
        if num == 0:
            for index in range(noCols):
                value = gyroHdrs[index]
                row.write(index, value)
        else:
            for index in range(noCols):
                if index == 0:
                    value = float("{0:.2f}".format(t[num - 1]))
                    row.write(index, value)
                else:
                    value = float("{0:.2f}".format(float(yD[num - 1][index - 1 + 3])))
                    row.write(index, value)

    ###### Add TempData separately ######
    sheet4 = book.add_sheet("tempData")
    noRows = np.shape(dat)[0] + 1
    noCols = len(tempHdrs)

    for num in range(noRows):  # accomodating for number of data rows + header row
        row = sheet4.row(num)  # choosing a row to operate on
        if num == 0:
            for index in range(noCols):
                value = tempHdrs[index]
                row.write(index, value)
        else:
            for index in range(noCols):
                if index == 0:
                    value = float("{0:.2f}".format(t[num - 1]))
                    row.write(index, value)
                else:
                    value = float("{0:.2f}".format(float(yD[num - 1][index - 1 + 6])))
                    row.write(index, value)

    book.save(path)
    print "-" * 10
    print "Data is stored in the following data path: "
    print path

def writeToXLTemp(t, yD, path):
    book = xlwt.Workbook()
    sheet1 = book.add_sheet("data")

    hdrs = ["Time (s)", "accX [g]", "accY [g]", "accZ [g]",
            "gyroX[deg/s]", "gyroY[deg/s]", "gyroZ[deg/s]", "temp [C]"]
    accHdrs = hdrs[0:4]
    gyroHdrs = hdrs[0:1] + hdrs[4:7]
    tempHdrs = hdrs[0:1] + hdrs[7:]
    dat = yArray

    noRows = np.shape(dat)[0] + 1
    noCols = len(hdrs)

    for num in range(noRows):  # accomodating for number of data rows + header row
        row = sheet1.row(num)  # choosing a row to operate on
        if num == 0:
            for index in range(noCols):
                value = hdrs[index]
                row.write(index, value)
        else:
            for index in range(noCols):
                if index == 0:
                    value = float("{0:.2f}".format(t[num - 1]))
                    row.write(index, value)
                else:
                    value = float("{0:.2f}".format(float(yD[num - 1][index - 1])))
                    row.write(index, value)

    ###### Add TempData separately ######
    sheet4 = book.add_sheet("tempData")
    noRows = np.shape(dat)[0] + 1
    noCols = len(tempHdrs)

    for num in range(noRows):  # accomodating for number of data rows + header row
        row = sheet4.row(num)  # choosing a row to operate on
        if num == 0:
            for index in range(noCols):
                value = tempHdrs[index]
                row.write(index, value)
        else:
            for index in range(noCols):
                if index == 0:
                    value = float("{0:.2f}".format(t[num - 1]))
                    row.write(index, value)
                else:
                    value = float("{0:.2f}".format(float(yD[num - 1][index - 1 + 6])))
                    row.write(index, value)

    book.save(path)
    print "-" * 10
    print "Data is stored in the following data path: "
    print path


baud = 19200

axisStr = ["x", "y", "z"]

if mode == 0:
    ind = 0 + axis
    yMin = -16.0
    yMax = 16.0
    print "Displaying ACC Data [g]"
    print axisStr[axis] + "-axis"
elif mode == 1:
    ind = 3 + axis
    yMin = -10
    yMax = 10
    print "Displaying GYRO Data [deg/s]"
    print axisStr[axis] + "-axis"
else:
    ind = 6
    yMin = 10
    yMax = 35
    print "Displaying TEMP Data [C]"


def runner(comPort=port):
    global yArray,tArray
    yArray = []
    tArray = []
    if serial.Serial(port, baud).is_open:
        print ""
        serial.Serial(port, baud).close()

    global ser  # globalizing variable "ser" so it can be used by emitter and flush functions

    ser = serial.Serial(port, baud, timeout=1)
    ser.reset_input_buffer()
    ser.readline()
    fig, ax = plt.subplots()
    scope = Scope(ax)

    # pass a generator in "emitter" to produce data for the update func
    ani = animation.FuncAnimation(fig, scope.update, emitter, interval=1, blit=True, repeat=False)
    plt.show()

    ser.close()

    # writeToXL(tArray,yArray,dataPath)


    tempArray = np.asarray(yArray)[:,6]
    timeArray = np.asarray(tArray)

    return timeArray, tempArray


def main(args):
    runner(dataFolder, dataFile)


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))