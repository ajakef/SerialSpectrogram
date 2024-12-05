#!/home/jake/anaconda3/envs/gem/bin/python
import time
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import itertools
import numpy as np
from utils import parse_line, baud_rate

def data_gen_serial():
    try:
        ser = serial.Serial('/dev/ttyUSB0', baud_rate, timeout=1)  # Open port and read data.
    except:
        try:
            ser = serial.Serial('/dev/ttyUSB1', baud_rate, timeout=1)  # Open port and read data.
        except:
            print('Could not open either ttyUSB0 or ttyUSB1. Please confirm that pySerial is installed and device is plugged in')
    ser.reset_input_buffer()  # Flush input buffer, discarding all its contents.
    for i in range(50):
        print(ser.readline())

    raw_data = np.zeros((n_chan, N_full))
    filtered_data = np.zeros((n_chan, N_full))
    while True:
        for i in range(N_full):
            filtered_data, raw_data = parse_line(ser, filtered_data, raw_data, n_chan, i) 
            if (i % N_sub) == 0:
                yield [filtered_data[j,:] for j in range(n_chan)]

def data_gen_no_serial():
    while True:
        time.sleep(1)
        yield np.arange(N_sub) + np.random.normal(0, 1, N_sub)
        
def run(data):
    line1.set_data(xdata, data[0] - data[0][0])  # Creating a data set for hand-over to plot
    if n_chan == 1:
        return line1,
    elif n_chan == 2:
        line2.set_data(xdata, data[1] - data[1][0])
        return line1, line2,
    

N_full = 1000
N_sub = 50
n_chan = 2
if __name__ == '__main__':
    fig, ax = plt.subplots()  # Setup figure and axis
    line1, = ax.plot([], [], color = 'red', lw = 2)  # Setup line
    line2, = ax.plot([], [], color = 'blue', lw = 2)  # Setup line

    ax.set_ylim(-1, 1)  # Set limitation in y
    ax.set_xlim(0, N_full) # Set limitation in x

    xdata, ydata = np.arange(N_full), np.zeros(N_sub)  # Create empty lists
    j = 0
    run_count = 0

    # Frames: Receives the generated data from the serial connection
    # Run: Provides the line data

    ani = animation.FuncAnimation(fig, run, frames=data_gen_serial, blit=True, interval=10)
    plt.show()

