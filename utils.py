import numpy as np
import scipy.signal

sensitivity_infrasound = 0.01/125 * 3.2/12 # V/Pa
sensitivity_seismic = 30 # V/m/s; probably order-of-magnitude accurate.
bitweight_V = 5/2**24 # differential measurement can go up to +/- 2.5V
gain_infrasound = 128 / 16 # FW divides by 16 to avoid writing noise bits
gain_seismic = 32 / 16
bitweight_infrasound = bitweight_V/gain_infrasound/sensitivity_infrasound
bitweight_seismic = bitweight_V/gain_seismic/sensitivity_seismic * 1e3 # mm/s

baud_rate = 500000

dt = 0.005
corner_freq = 1 # Hz
nyquist = 0.5/dt
[b, a] = scipy.signal.butter(1, corner_freq/nyquist, 'highpass')
    
def parse_line(ser, filtered_data, raw_data, n_chan, i):
    bitweights = [bitweight_infrasound] + [bitweight_seismic for i in range(n_chan - 1)]
    while True:
        try:
            line = ser.readline().decode('utf-8').strip().split(',')
            float(line[0]) # raises an exception if the first character isn't numeric
            raw_data[:,i] = np.array([float(line[j+1]) * bitweights[j] for j in range(n_chan)]) + raw_data[:,i-1] # integrate it before filtering
            filtered_data[:,i] = -a[1] * filtered_data[:,i-1] + b[0] * raw_data[:,i] + b[1] * raw_data[:,i-1]
            return filtered_data, raw_data
        except Exception as e:
            print(line)
            #print(e)

        
