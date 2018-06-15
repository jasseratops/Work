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

import Arduino_IMU_RTD


def main():

    tDat,yDat = Arduino_IMU_RTD.runner(dataFolder,dataFile,port)
