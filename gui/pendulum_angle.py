"""
    A simple application to plot the angle of an inverted pendulum from an
    Arduino, using a serial connection.

    By Ashleigh Wilson.
    https://github.com/AshleighWilson
"""

import sys
import pyqtgraph as pg
import numpy as np
import serial
from PyQt5 import QtGui

class ArduinoSerial:
    """ Class for data handling with a serial connection. """
    def __init__(self, port, baudrate):
        self.is_ready = False
        self.data_buffer = ''

        # Attempt a connection to the microcontroller, if we fail,
        # then quit the program.
        print('Connecting to ' + str(port) + '.. ', end='', flush=True)
        try:
            self.connection = serial.Serial(port, baudrate, timeout=None)
            print("Connected.")
        except:
            print("Failed. Quitting..")
            sys.exit()

        # Wait for a ready signal (RDY) from microcontroller to prevent
        # spurious data from being read.
        print('Waiting for RDY signal from controller.. ', end='', flush=True)
        while not self.is_ready:
            if self.connection.readline() == b'RDY\r\n':
                self.is_ready = True
                print('Received.')


    def read(self):
        ''' Read all complete lines of data from the Arduino. '''

        # If the connection is not ready, return empty list.
        if not self.is_ready:
            return []

        # Read all available data from arduino and append to buffer.
        self.data_buffer += self.connection.read(self.connection.inWaiting()).decode()

        # Check if at least one whole line of data has been received.
        if '\n' in self.data_buffer:
            data = []

            # Add all but the latest line of data to the data list.
            lines = self.data_buffer.split('\r\n')
            for line in lines[:-1]:
                data.append(line)

            # Clear the data buffer and add the remaining data to it.
            self.data_buffer = lines[-1]
            return data

        # No full lines of data received, so return empty list.
        return []


    def close(self):
        ''' Close the connection to the Arduino. '''
        self.is_ready = False
        self.connection.close()
        print("Disconnected.")


# Connect to the Arduino.
arduino = ArduinoSerial('/dev/tty.usbmodem14601', 115200)

# Always start by initializing Qt (only once per application).
app = QtGui.QApplication([])
pg.setConfigOptions(antialias=True, background="w")
win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('Pendulum Angle')

# Angle plot.
plot_angle = win.addPlot()
plot_angle.showGrid(x=True, y=True)
# plot_angle.setXRange(5,20, padding=0)
plot_angle.setYRange(-190, 190, padding=0)
plot_angle_x = np.zeros(500)
plot_angle_y = np.zeros(500)
plot_angle_curve = plot_angle.plot(
    plot_angle_x,
    plot_angle_y,
    pen=pg.mkPen('r', width=1.5)
)

def update_angle():
    ''' Update the plot(s) with fresh data. '''
    global plot_angle_x, plot_angle_y

    if (arduino_data := arduino.read()):
        for line in arduino_data:

            # Separate the individual values in the data.
            line = line.split()

            # Shift x and y values left in the list.
            plot_angle_x[:-1] = plot_angle_x[1:]
            plot_angle_y[:-1] = plot_angle_y[1:]

            # Add new data to the x and y lists, then update the curve.
            plot_angle_x[-1] = int(line[0]) / 1000
            plot_angle_y[-1] = line[1]
            plot_angle_curve.setData(plot_angle_x, plot_angle_y)

            # Update the GUI.
            QtGui.QApplication.processEvents()

    else: # No data was read from the arduino, so disconnect and exit.
        print('No data received, disconnecting.. ', end='', flush=True)
        arduino.close()
        sys.exit()
        return

# Run the GUI and update the plot every 20ms.
timer = pg.QtCore.QTimer()
timer.timeout.connect(update_angle)
timer.start(20)
app.exec_()
