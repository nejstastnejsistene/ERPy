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


def draw(data, t0, t1, ch0, ch1, scale=5000, pixel_density=1000):
    dt = t1 - t0
    dch = ch1 - ch0

    # Horizontal limits in terms of samples.
    s0 = max((t0 - dt) * sample_rate, 0)
    s1 = min((t1 + dt) * sample_rate, num_samples)
    ds = s1 - s0
    step = ds / pixel_density

    # Create the figure and axes.
    fig = plt.figure()
    axes = plt.subplot(111)

    # Plot the data.
    t = (np.arange(s0, s1, dtype=float) / sample_rate)[::step]
    for i in range(ch0 - 3, ch1 + 3):
        offset = i + 0.5
        axes.plot(t, scale*data[i][s0:s1:step]+offset)

    # Set our window limits.
    axes.set_xlim(t0, t1)
    axes.set_ylim(ch0, ch1)
    axes.set_xlabel('time (seconds)')

    if False:
        # Remove margins and axes.
        fig.subplots_adjust(left=0)
        fig.subplots_adjust(right=1)
        fig.subplots_adjust(bottom=0)
        fig.subplots_adjust(top=1)
        axes.get_xaxis().set_visible(False)
        axes.get_yaxis().set_visible(False)

    plt.show()

draw(data, 5, 8, 5, 8)
