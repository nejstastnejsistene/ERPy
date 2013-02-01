import struct

import numpy as np

import matplotlib.pyplot as plt

filename = '5001.000.b.dat'

# Read the header for information about data.
with open(filename, 'rb') as f:
    header = struct.unpack('>20f', f.read(80))
num_channels = int(header[3])
sample_rate = header[7]
total_time = header[9]
num_samples = int(sample_rate * total_time)

# Load data into numpy memmap.
shape = num_channels, num_samples
data = np.memmap(filename, '>f', 'r', 80, shape, 'F')

def draw(data, t0, t1, ch0, ch1, scale=5000):
    t0 *= sample_rate
    t1 *= sample_rate
    dt = t1 - t0
    t = np.arange(dt, dtype=float) / sample_rate
    for i in range(ch0, ch1):
        offset = i + 0.5
        plt.plot(t, scale*data[i][:2000]+offset)
    plt.ylim(ch0, ch1)
    plt.xlabel('time (seconds)')
    plt.show()

draw(data, 0, 1, 2, 5)
