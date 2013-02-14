import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_wx import \
        _create_wx_app, _load_bitmap, bind
from matplotlib.backends.backend_wxagg import \
        FigureFrameWxAgg, FigureManagerWx, \
        NavigationToolbar2Wx, \
        backend_version, draw_if_interactive, show

import wx


def new_figure_manager(num, *args, **kwargs):
    """
    Create a new figure manager instance
    """
    _create_wx_app()

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


_NTB_PLAY = wx.NewId()

class ErpyNavigationToolbar(NavigationToolbar2Wx):

    def __init__(self, *args):
        NavigationToolbar2Wx.__init__(self, *args)

    def _init_toolbar(self, *args):
        NavigationToolbar2Wx._init_toolbar(self, *args)
        self.AddSimpleTool(_NTB_PLAY, _load_bitmap('forward.xpm'),
                           'Play', 'Start playing')
        bind(self, wx.EVT_TOOL, self._onPlay, id=_NTB_PLAY)

    def _onPlay(self, *args):
        pass
