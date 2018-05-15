# JAscripts
# RT_graph2
# Jasser Alshehri
# Starkey Hearing Technologies
# 3/27/2018
# This was developed on matplotlib 2.0.2, and will not work with matplotlib 2.2.2

##### User Config #####
dataFolder = "C:/Users/alshehrj/Data/"
dataFile = "IMUdata"

port = 'com4'       # Configure which port the Arduino is connected to.

mode = 2            # 0: Acc., 1: Gyro., 2: Temp.
axis = 2            # 0: x,    1: y,     2: z
####################################


import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.pylab import *
from mpl_toolkits.axes_grid1 import host_subplot
import serial
import time
import re
import xlwt
from Tkinter import *



baud = 19200

if serial.Serial(port,baud).is_open:
    serial.Serial(port,baud).close()

ser = serial.Serial(port,baud,timeout=1)
ser.reset_input_buffer()
ser.readline()
axisStr = ["x","y","z"]

ind = []

def figConfig():
    global ind
    if mode == 0:
        ind = range(0,3)
        yMin = -16.0
        yMax = 16.0

        f0 = figure(num=0, figsize=(12, 8))  # , dpi = 100)
        f0.suptitle("Acc. Data", fontsize=12)
        ax01 = subplot2grid((3, 1), (0, 0))
        ax02 = subplot2grid((3, 1), (1, 0))
        ax03 = subplot2grid((3, 1), (2, 0))

        ax01.set_title('Acc. X')
        ax02.set_title('Acc. Y')
        ax03.set_title('Acc. Z')

        ax01.set_ylim(yMin, yMax)
        ax02.set_ylim(yMin, yMax)
        ax03.set_ylim(yMin, yMax)



        print "Displaying ACC Data [g]"
        print axisStr[axis] + "-axis"

    elif mode == 1:
        ind = range(3,6)
        yMin = -10
        yMax = 10

        f0 = figure(num=0, figsize=(12, 8))  # , dpi = 100)
        f0.suptitle("Gyro. Data", fontsize=12)
        ax01 = subplot2grid((3, 1), (0, 0))
        ax02 = subplot2grid((3, 1), (1, 0))
        ax03 = subplot2grid((3, 1), (2, 0))

        ax01.set_title('Gyro X')
        ax02.set_title('Gyro Y')
        ax03.set_title('Gyro Z')

        ax01.set_ylim(yMin, yMax)
        ax02.set_ylim(yMin, yMax)
        ax03.set_ylim(yMin, yMax)

        print "Displaying GYRO Data [deg/s]"
        print axisStr[axis] + "-axis"
    else:
        ind = [6]
        yMin = 10
        yMax = 35

        f0 = figure(num=0, figsize=(12, 8))  # , dpi = 100)
        f0.suptitle("Acc. Data", fontsize=12)

        ax01 = subplot2grid((1, 1), (0, 0))

        ax01.set_title('Temp')

        ax01.set_ylim(yMin, yMax)

        print "Displaying TEMP Data [C]"


tArray = []
yArray = []


def createTimeStamp():
    ts = time.strftime("%c")
    ts = re.sub(" ", "_", ts)
    ts = re.sub("/", "-", ts)
    ts = re.sub(":", "-", ts)

    return ts

timeStamp = createTimeStamp()
dataPath = dataFolder+dataFile + "_" + str(timeStamp)

class Scope(object):
    def __init__(self, ax, maxt=4, dt=0.04):
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
    ser.reset_input_buffer()
    ser.readline()


def dataWriter():
    while True:
        #flush()
        val = ser.readline()
        allData = val.split(",")
        yArray.append(allData[:-1])     # discarding return line characters from the serial read.
        dispArray = np.zeros(len(ind))
        for i in range(len(ind)):
            dispArray[i] = allData(ind[i])

        yield dispArray


figConfig()

fig, ax = plt.subplots()
scope = Scope(ax01)

# pass a generator in "emitter" to produce data for the update func
ani = animation.FuncAnimation(fig, scope.update, dataWriter, interval=10,blit=True)
plt.show()


def writeToXL(t,yD):
    book = xlwt.Workbook()
    sheet1 = book.add_sheet("data")

    hdrs = ["Time (s)","accX [g]","accY [g]","accZ [g]",
            "gyroX[deg/s]","gyroY[deg/s]","gyroZ[deg/s]","temp [C]"]
    accHdrs = hdrs[0:4]
    gyroHdrs = hdrs[0:1]+hdrs[4:7]
    tempHdrs = hdrs[0:1]+hdrs[7:]
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
                    value = float("{0:.2f}".format(t[num-1]))
                    row.write(index, value)
                else:
                    value = float("{0:.2f}".format(float(yD[num-1][index-1])))
                    row.write(index, value)

    ###### Add AccData separately ######
    sheet2 = book.add_sheet("accData")
    noRows = np.shape(dat)[0] + 1
    noCols = len(accHdrs)

    for num in range(noRows):               # accomodating for number of data rows + header row
        row = sheet2.row(num)               # choosing a row to operate on
        if num == 0:
            for index in range(noCols):
                value = accHdrs[index]
                row.write(index, value)
        else:
            for index in range(noCols):
                if index == 0:
                    value = float("{0:.2f}".format(t[num-1]))
                    row.write(index, value)
                else:
                    value = float("{0:.2f}".format(float(yD[num-1][index-1])))
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

    book.save(dataPath+".xls")
    print "-" * 10
    print "Data is stored in the following data path: "
    print dataPath

writeToXL(tArray,yArray)(sys.argv))