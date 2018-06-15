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

import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import time
import re
import xlwt
from Tkinter import *

baud = 19200

def DAQnDisplay(port,baud):
    if serial.Serial(port, baud).is_open:
        serial.Serial(port, baud).close()

    ser = serial.Serial(port, baud, timeout=1)
    ser.reset_input_buffer()
    ser.readline()

