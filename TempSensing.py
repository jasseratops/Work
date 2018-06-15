# JAscripts
# RT_graph2
# Jasser Alshehri
# Starkey Hearing Technologies
# 3/27/2018
# This was developed on matplotlib 2.0.2, and will not work with matplotlib 2.2.2

##### User Config #####

dataFolder = "C:/Users/alshehrj/Data/"
dataFile = "testTemp"

port = 'com7'

noDataPnts = 3

###########################

import ardimutemp
import xlwt
import numpy as np
import time
import re


def createTimeStamp():
    ts = time.strftime("%c")
    ts = re.sub(" ", "_", ts)
    ts = re.sub("/", "-", ts)
    ts = re.sub(":", "-", ts)

    return ts

def main(args):

    timeStamp = createTimeStamp()
    dataPath = str(dataFolder) + str(dataFile) + "_" + str(timeStamp) + ".xls"
    book = xlwt.Workbook()
    sheet1 = book.add_sheet("data")
    noRows = 62

    ### write time

    for num in range(noRows):
        row = sheet1.row(num)  # choosing a row to operate on
        if num ==0:
            value = "Time(s)"
        else:
            value = num-1

        row.write(0,value)

    for count in range(noDataPnts):
        col = count + 1
        print "Collecting Temp Data" + str(col)

        _,tempDat = ardimutemp.runner(port)
        yD = tempDat

        for num in range(len(yD)):
            row = sheet1.row(num)  # choosing a row to operate on
            if num == 0:
                value = "temp data " + str(col)
            else:
                value = float("{0:.2f}".format(float(yD[(num-1)])))
            row.write(col,value)

    book.save(dataPath)
    print "-" * 10
    print "Data is stored in the following data path: "
    print dataPath

if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))