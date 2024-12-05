#!/home/jake/anaconda3/envs/gem/bin/python
import time
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import itertools
import numpy as np
from scipy.signal import spectrogram
from riversound import image

sensitivity_infrasound = 0.01/125 * 3.2/12
sensitivity_seismic = 30 # V/m/s; probably order-of-magnitude accurate.
bitweight_V = 5/2**24 # differential measurement can go up to +/- 2.5V
gain_infrasound = 128
gain_seismic = 32
bitweight_infrasound = bitweight_V/gain_infrasound/sensitivity_infrasound
bitweight_seismic = bitweight_V/gain_seismic/sensitivity_seismic * 1e3 # um/s

N_full = 4096
N_sub = 128
overlap = 0.875
dt = 0.005

show_infrasound = True
show_seismic = True
show_traces = True

def data_gen_serial(): # this function must be iterable; every time it yields, what it yields is the input to run()
    infrasound = np.zeros(N_full) 
    seismic = np.zeros(N_full)
    print('startup')
    try:
        ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=20)  # Open port and read data.
    except:
        try:
            ser = serial.Serial('/dev/ttyUSB1', 115200, timeout=20)  # Open port and read data.
        except:
            raise(Exception('Could not open ttyUSB0 or ttyUSB1. Please confirm that pySerial is installed and device is plugged in.'))
            
    ser.reset_input_buffer()  # Flush input buffer, discarding all its contents.
    for i in range(100):
        line = ser.readline()
        #print(line)

    while True:
        for i in range(N_full):
            line = ser.readline().decode('utf-8').strip().split(',')
            infrasound[i] = float(line[-1]) * bitweight_infrasound
            seismic[i] = float(line[-2]) * bitweight_seismic
            if (i % N_sub) == 0:
                yield [infrasound, seismic, i]
        
def run(data): # this function accepts the "yields" of the data_gen function as its input, and must return a list of all artists (i.e., images and lines). If some feature in the plot isn't updating right, it may not be included in the returned list. note that axis.plot() returns a list of (typically 1) artists, not an artist itself. Seems like storing info in globals isn't an option.
    artists = []
    nplots = show_seismic+show_infrasound+show_traces
    current_time = data[2] * dt
    freqticks = [1, 3, 10, 30, 100]
    if show_infrasound:
        plt.subplot(nplots, 1, 1)
        freqs, times, sg = spectrogram(data[0], fs = 200, window = 'hamming', nperseg = N_sub, noverlap = overlap*N_sub, detrend = 'linear')#, axis = axes[0]) axis input doesn't work for some reason
        sg[sg == 0] = np.nan # prevent warnings when taking log(0)
        artists.append(image(np.log(sg.T[:,1:]), times, freqs[1:], log_y = True, ax = axes[0,0]))
        artists.append(axes[0,0].plot([current_time, current_time], axes[0,0].get_ylim(), 'k-')[0]) # axes[0,0].plot returns a list of artists, not just one
        axes[0,0].set_yticks(np.log10(freqticks), freqticks)
    if show_seismic:
        plt.subplot(nplots, 1, 1+show_infrasound)
        freqs, times, sg = spectrogram(data[1], fs = 200, window = 'hamming', nperseg = N_sub, noverlap = 0.5*N_sub, detrend = 'linear')#, axis = axes[0]) axis input doesn't work for some reason
        sg[sg == 0] = np.nan
        artists.append(image(np.log(sg.T[:,1:]), times, freqs[1:], log_y = True, ax = axes[show_infrasound+0,0]))
        artists.append(axes[show_infrasound+0,0].plot([current_time, current_time], axes[0,0].get_ylim(), 'k-')[0]) # axes[0,0].plot returns a list of artists, not just one
        axes[show_infrasound+0,0].set_yticks(np.log10(freqticks), freqticks)
    if show_traces:
        plt.subplot(nplots, 1, nplots)
        t = np.arange(N_full) * dt
        if show_infrasound:
            line_infrasound.set_data(t, data[0] - data[0][0]+0.25)
            artists.append(line_infrasound)
        if show_seismic:
            line_seismic.set_data(t, data[1] - data[1][0]-0.25)
            artists.append(line_seismic)
        axes[-1,0].set_ylim(-1, 1)
        artists.append(axes[-1,0].plot([current_time, current_time], [-1,1], 'k-')[0])
    return artists
    


if __name__ == '__main__':
    fig, axes = plt.subplots(show_seismic + show_infrasound + show_traces, 1, squeeze = False)  # Setup figure and axis
    if show_infrasound:
        axes[0,0].set_title('Infrasound')
    if show_seismic:
        axes[0+show_infrasound,0].set_title('Seismic')
    if show_infrasound or show_seismic:
        axes[-2,0].set_ylabel('Frequency (Hz)')
    if show_traces:
        line_infrasound, = axes[-1,0].plot([], [], color = 'red', lw = 1)  # Setup line
        line_seismic, = axes[-1,0].plot([], [], color = 'blue', lw = 1)  # Setup line

    #ax.set_ylim(-1, 1)  # Set limitation in y
    for j in range(len(axes)):
        axes[j,0].set_xlim(0, N_full * dt) # Set limitation in x

    fig.set_size_inches(12, 9)
    fig.tight_layout()
    fig.show()
    
    # Frames: Receives the generated data from the serial connection
    # Run: Provides the line data

    ani = animation.FuncAnimation(fig, run, frames=data_gen_serial, blit=True, interval=50, save_count = 0)
    plt.show()

