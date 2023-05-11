import numpy as np
import csv
import os
import pyqtgraph as pg
import serial
from pyqtgraph.Qt import QtCore

# Set serial
PORT_NAME = 'COM4'
BAUDRATE = '115200'
ser = serial.Serial(PORT_NAME, BAUDRATE)

# Set colour background
colour_background = 'black'   

# Set colour line
colour_line = '#00ffff'  

app = pg.mkQApp("Plotting Data")

win = pg.GraphicsLayoutWidget(show=True, title="Plotting Data")
win.resize(900, 700)
win.setWindowTitle('Plotting Data')
win.setBackground(colour_background)

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

# Set empty array
data_1 = []
data_2 = []
data_3 = []
data_4 = []
data_5 = []
data_6 = []

# Plot 1
p1 = win.addPlot(title="Data 1")
p1.showGrid(x=True, y=True)
p1.setLabel('bottom', 'Time (s)')
curve1 = p1.plot(pen=pg.mkPen(color=colour_line, width=1.25))

# Plot 2
p2 = win.addPlot(title="Data 2")
p2.showGrid(x=True, y=True)
p2.setLabel('bottom', 'Time (s)')
curve2 = p2.plot(pen=pg.mkPen(color=colour_line, width=1.25))

win.nextRow()

# Plot 3
p3 = win.addPlot(title="Data 3")
p3.showGrid(x=True, y=True)
p3.setLabel('bottom', 'Time (s)')
curve3 = p3.plot(pen=pg.mkPen(color=colour_line, width=1.25))

# Plot 4
p4 = win.addPlot(title="Data 4")
p4.showGrid(x=True, y=True)
p4.setLabel('bottom', 'Time (s)')
curve4 = p4.plot(pen=pg.mkPen(color=colour_line, width=1.25))

win.nextRow()

# Plot 5
p5 = win.addPlot(title="Data 5")
p5.showGrid(x=True, y=True)
p5.setLabel('bottom', 'Time (s)')
curve5 = p5.plot(pen=pg.mkPen(color=colour_line, width=1.25))

# Plot 6
p6 = win.addPlot(title="Data 6")
p6.showGrid(x=True, y=True)
p6.setLabel('bottom', 'Time (s)')
curve6 = p6.plot(pen=pg.mkPen(color=colour_line, width=1.25))

ptr = 0

# check for existing data files and increment index if necessary
index = 1
while os.path.exists(f'data/data_{index}.csv'):
    index += 1
filename = f'data/data_{index}.csv'

# main function
def update():
    global curve1, data_1, ptr, p1, p2, p3, p4, p5, p6

    # read a line of data from the serial port
    line = ser.readline().decode().strip()
    # print(line)
    line_split = line.split(",")
    # print(line_split)

    # write the data to the CSV file
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(line_split)

    # convert the data to floats and update the plots
    value1 = float(line_split[0])
    value2 = float(line_split[1])
    value3 = float(line_split[2])
    value4 = float(line_split[3])
    value5 = float(line_split[4])
    value6 = float(line_split[5])

    data_1.append(value1)
    curve1.setData(data_1)

    data_2.append(value2)
    curve2.setData(data_2)

    data_3.append(value3)
    curve3.setData(data_3)

    data_4.append(value4)
    curve4.setData(data_4)

    data_5.append(value5)
    curve5.setData(data_5)

    data_6.append(value6)
    curve6.setData(data_6)

    ptr += 1
    if ptr >= 1000:
        data_1.pop(0)
        data_2.pop(0)
        data_3.pop(0)
        data_4.pop(0)
        data_5.pop(0)
        data_6.pop(0)
        ptr -= 1
    if curve1.xData is None:
        p1.enableAutoRange('xy', False)
        p2.enableAutoRange('xy', False)
        p3.enableAutoRange('xy', False)
        p4.enableAutoRange('xy', False)
        p5.enableAutoRange('xy', False)
        p6.enableAutoRange('xy', False)


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

if __name__ == '__main__':
    pg.exec()
