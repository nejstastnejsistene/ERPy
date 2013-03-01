import struct

import numpy as np

from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.figure import Figure

filename = '5001.000.b.dat'


class ErpyAxes(Axes):
    '''
    New keyword arguments:
        memmap
        sample_rate
        num_samples
        limits
        scale
        pixel_density
    '''

    default_scale = 5000
    default_pixel_density = 1000

    def __init__(self, *args, **kwargs):
        self._memmap = kwargs.pop('memmap')
        self._sample_rate = kwargs.pop('sample_rate')
        self._num_samples = kwargs.pop('num_samples')
        limits = kwargs.pop('limits')
        self._limits = self._get_buffer_bounds(*limits)
        self._scale = kwargs.pop('scale', self.default_scale)
        self._pixel_density = kwargs.pop('pixel_density',
                                         self.default_pixel_density)
        Axes.__init__(self, *args, **kwargs)
        self._reload_buffer()

    @staticmethod
    def _get_buffer_bounds(x0, x1, y0, y1):
        '''
        Calculates the bounds of the buffer given the
        viewing window.
        '''
        dx, dy = x1 - x0, y1 - y0
        return x0 - dx, x1 + dx, y0 - dy, y1 + dy

    def _check_buffer(self):
        '''
        Reloads the buffer if the viewing window has left
        the buffered region.
        '''
        outer_x0, outer_x1, outer_y0, outer_y1 = self._limits
        inner_x0, inner_x1 = self.get_xlim()
        inner_y0, inner_y1 = self.get_ylim()
        if inner_x0 < outer_x0 or inner_y0 < outer_y0 or \
                inner_x1 > outer_x1 or inner_y1 > outer_y1:
            self._limits = self._get_buffer_bounds(inner_x0, inner_x1, \
                                                   inner_y0, inner_y1)
            self._reload_buffer()

    def _reload_buffer(self):
        '''
        Reloads the buffer to the region indicated by self._limits.
        It does not modify the current view window, so it assumes
        that the window is within the given bounds.
        '''
        x0, x1, y0, y1 = self._limits

        # Horizontal limits in terms of samples.
        s0 = max(int(x0 * self._sample_rate), 0)
        s1 = min(int(x1 * self._sample_rate), self._num_samples)
        ds = s1 - s0
        step = ds / self._pixel_density

        # Clear axes.
        self.cla()

        # Plot the data.
        t = (np.arange(s0, s1, dtype=float) / self._sample_rate)[::step]
        off = y0 % 1 
        ymin = max(int(y0), 0)
        ymax = min(int(y1), len(self._memmap))
        lines = []
        for i in range(ymin, ymax):
            offset = i + 0.5 + off
            data = self._scale * self._memmap[i][s0:s1:step] + offset
            lines.append(zip(t, data))
        self.add_collection(LineCollection(lines))

    def draw(self, *args):
        '''Override Axes.draw() to first consider our buffer.'''
        self._check_buffer()
        Axes.draw(self, *args)


if __name__ == '__main__':
    import matplotlib
    matplotlib.use('module://backend_wxagg_erpy')
    #matplotlib.use('WXAgg')
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

    limits = 5, 8, 5, 8
    fig = pyplot.figure()

    #for i in range(4):
    #    x0 = (i % 2) * 0.5
    #    y0 = (i / 2) * 0.5
    axes = ErpyAxes(
            fig, [0.1, 0.1, 0.8, 0.8],
            memmap=data,
            sample_rate=sample_rate,
            num_samples=num_samples,
            limits=limits,
            )
    axes.set_xlim(*limits[:2])
    axes.set_ylim(*limits[2:])
    axes.set_xlabel('time (seconds)')
    fig.add_axes(axes)

    pyplot.show()
