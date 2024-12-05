#!/home/jake/anaconda3/envs/gem/bin/python
import time
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import itertools
import numpy as np

sensitivity_infrasound = 0.01/125 * 3.2/12
sensitivity_seismic = 30 # V/m/s; probably order-of-magnitude accurate.
bitweight_V = 5/2**24 # differential measurement can go up to +/- 2.5V
gain_infrasound = 128
gain_seismic = 32
bitweight_infrasound = bitweight_V/gain_infrasound/sensitivity_infrasound
bitweight_seismic = bitweight_V/gain_seismic/sensitivity_seismic * 1e3 # um/s


def data_gen_serial():
    try:
        ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  # Open port and read data.
    except:
        try:
            ser = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)  # Open port and read data.
        except:
            print('Could not open either ttyUSB0 or ttyUSB1. Please confirm that pySerial is installed and device is plugged in')
    ser.reset_input_buffer()  # Flush input buffer, discarding all its contents.
    for i in range(50):
        print(ser.readline())

    data1 = np.zeros(N_full)
    data2 = np.zeros(N_full)
    while True:
        for i in range(N_full):
            line = ser.readline().decode('utf-8').strip().split(',')
            data1[i] = float(line[-1]) * bitweight_infrasound
            data2[i] = float(line[-2]) * bitweight_seismic
            if (i % N_sub) == 0:
                if n_chan == 1:
                    yield [data1]
                elif n_chan == 2:
                    yield [data1, data2]

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

