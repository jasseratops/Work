# Work
# xlwtTest
# Jasser Alshehri
# Starkey Hearing Technologies
# 4/16/2018


import numpy as np
import matplotlib.pyplot as plt
from numpy import pi, sin, cos, tan, exp
import xlwt

def main(args):
    """"""
    book = xlwt.Workbook()
    sheet1 = book.add_sheet("PySheet1")

    cols = ["A", "B", "C", "D", "E"]
    dat  = [["-5.3","-8.6","3","7.2","0"],
            ['0.01', '0.25', '-0.97', '-0.41', '-0.66'],
            ['7.01', '0.25', '-0.96', '-0.39', '-0.33']]

    print np.shape(dat)
    noRows = np.shape(dat)[0] + 1
    noCols = len(cols)

    print noRows
    print noCols

    for num in range(noRows):      # accomodating for number of data rows + header row
        row = sheet1.row(num)                   # choosing a row to operate on
        if num == 0:
            for index in range(noCols):
                value = cols[index]
                row.write(index, value)
        else:
            for index in range(noCols):
                print "index: " + str(index)
                print "num:" + str(num-1)
                value = dat[num-1][index]
                #print(value)
                row.write(index, value)


    book.save("C:/Users/alshehrj/Data/tester9er.xls")
    return 0


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))