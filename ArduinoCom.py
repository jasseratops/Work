# JAscripts
# ArduinoCom
# Jasser Alshehri
# Starkey Hearing Technologies
# 3/27/2018


import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

port = 'com4'
baud = 9600

if serial.Serial(port,baud).is_open:
    serial.Serial(port,baud).close()

ser = serial.Serial(port,baud,timeout=1)


def main(args):
    #fig = plt.figure()
    #ax1 = fig.add_subplot(1, 1, 1)
    count = 0

    xar = []
    yar = []

    ser.reset_input_buffer()
    ser.readline()
    while True:

        start = time.time()

        val = ser.readline()
        allData = val.split(",")



        '''
        xar.append(count)
        yar.append(int(val))
        count += 1
        '''

        print (time.time()-start)

    ser.close()

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))