import struct

import numpy as np


filename = '5001.000.b.dat'

def draw(fig, axes, data, t0, t1, ch0, ch1, scale=5000, pixel_density=1000):
    dt = t1 - t0
    dch = int(ch1 - ch0)

    # Horizontal limits in terms of samples.
    s0 = max(int((t0 - dt) * fig.sample_rate), 0)
    s1 = min(int((t1 + dt) * fig.sample_rate), fig.num_samples)
    ds = s1 - s0
    step = ds / pixel_density

    # Create the figure and axes.
    #fig = pyplot.figure()
    #axes = pyplot.subplot(111)
    fig.data = data
    fig.xlim = t0 - dt, t1 + dt
    fig.ylim = ch0 - dch, ch1 + dch
    fig.scale = scale
    fig.pixel_density = pixel_density

    axes.cla()

    # Plot the data.
    t = (np.arange(s0, s1, dtype=float) / fig.sample_rate)[::step]
    off = ch0 % 1
    for i in range(int(ch0) - dch, int(ch1) + dch):
        offset = i + 0.5 + off
        #print offset, i, s0, s1, step
        #print 'dt', dt, ds/fig.sample_rate
        axes.plot(t, scale*data[i][s0:s1:step]+offset)
        
    # Set our window limits.
    axes.set_xlim(t0, t1)
    axes.set_ylim(ch0, ch1)
    axes.set_xlabel('time (seconds)')

    #if False:
        # Remove margins and axes.
        #fig.subplots_adjust(left=0)
        #fig.subplots_adjust(right=1)
        #fig.subplots_adjust(bottom=0)
        #fig.subplots_adjust(top=1)
        #axes.get_xaxis().set_visible(False)
        #axes.get_yaxis().set_visible(False)


if __name__ == '__main__':
    import matplotlib
    matplotlib.use('module://backend_wxagg_erpy')
    from matplotlib import pyplot

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

    fig = pyplot.figure()
    fig.sample_rate = sample_rate
    fig.num_samples = num_samples
    axes = pyplot.subplot(111)
    draw(fig, axes, data, 5, 8, 5, 8)
    pyplot.show()
