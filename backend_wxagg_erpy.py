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

    def _get_toolbar(self, statbar):
        toolbar = ErpyNavigationToolbar(self.canvas)
        toolbar.set_status_bar(statbar)
        return toolbar


class ErpyNavigationToolbar(NavigationToolbar2Wx):

    def __init__(self, *args):
        NavigationToolbar2Wx.__init__(self, *args)
