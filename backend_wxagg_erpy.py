import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends import backend_wx
from matplotlib.backends.backend_wxagg import \
        FigureFrameWxAgg, FigureManagerWx, \
        NavigationToolbar2Wx, \
        backend_version, draw_if_interactive, show


def new_figure_manager(num, *args, **kwargs):
    """
    Create a new figure manager instance
    """
    backend_wx._create_wx_app()

    FigureClass = kwargs.pop('FigureClass', Figure)
    fig = FigureClass(*args, **kwargs)

    frame = ErpyFigureFrame(num, fig)
    manager = frame.get_figure_manager()
    if matplotlib.is_interactive():
        manager.frame.Show()
    return manager


class ErpyFigureFrame(FigureFrameWxAgg):

    def __init__(self, num, fig):
        FigureFrameWxAgg.__init__(self, num, fig)
        self.figmgr = ErpyFigureManager(self.canvas, num, self)

    def _get_toolbar(self, statbar):
        toolbar = ErpyNavigationToolbar(self.canvas)
        toolbar.set_status_bar(statbar)
        return toolbar


class ErpyFigureManager(FigureManagerWx):
    pass
    #def __init__(self, canvas, num, frame):
    #    FigureManagerWx.__init__(self, canvas, num, frame)


class ErpyNavigationToolbar(NavigationToolbar2Wx):

    def __init__(self, *args):
        NavigationToolbar2Wx.__init__(self, *args)

    def dynamic_update(self):
        #NavigationToolbar2Wx.dynamic_update(self)
        d = self._idle
        self._idle = False
        if d:
            fig = self.canvas.figure
            outer_x0, outer_x1 = fig.xlim
            outer_y0, outer_y1 = fig.ylim
            axes, = fig.get_axes()
            inner_x0, inner_x1 = axes.get_xlim()
            inner_y0, inner_y1 = axes.get_ylim()
            if inner_x0 < outer_x0 or inner_y0 < outer_y0 or \
                    inner_x1 > outer_x1 or inner_y1 > outer_y1:
                print 'reloading buffer'
                import mpl
                mpl.draw(fig, axes, fig.data, \
                        inner_x0, inner_x1, \
                        inner_y0, inner_y1, \
                        fig.scale, fig.pixel_density)
            self.canvas.draw()
            self._idle = True

