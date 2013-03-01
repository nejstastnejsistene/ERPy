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
_NTB_LEFT = wx.NewId()
_NTB_RIGHT = wx.NewId()
_NTB_UP = wx.NewId()
_NTB_DOWN = wx.NewId()

class ErpyNavigationToolbar(NavigationToolbar2Wx):

    def __init__(self, *args):
        NavigationToolbar2Wx.__init__(self, *args)

    def _init_toolbar(self, *args):
        NavigationToolbar2Wx._init_toolbar(self, *args)
        self.AddSimpleTool(_NTB_PLAY, _load_bitmap('forward.xpm'),
                           'Play', 'Start playing')
        self.AddSimpleTool(_NTB_LEFT, _load_bitmap('stock_left.xpm'),
                           'Left', 'Jump one screen to the left')
        self.AddSimpleTool(_NTB_RIGHT, _load_bitmap('stock_right.xpm'),
                           'Right', 'Jump one screen to the right')
        self.AddSimpleTool(_NTB_DOWN, _load_bitmap('stock_down.xpm'),
                           'Down', 'Go down one channel')
        self.AddSimpleTool(_NTB_UP, _load_bitmap('stock_up.xpm'),
                           'Up', 'Go up one channel')
        bind(self, wx.EVT_TOOL, self._onPlay, id=_NTB_PLAY)
        bind(self, wx.EVT_TOOL, self._onLeft, id=_NTB_LEFT)
        bind(self, wx.EVT_TOOL, self._onRight, id=_NTB_RIGHT)
        bind(self, wx.EVT_TOOL, self._onDown, id=_NTB_DOWN)
        bind(self, wx.EVT_TOOL, self._onUp, id=_NTB_UP)

    def _onPlay(self, *args):
        for axes in self.canvas.figure.get_axes():
            pass
        raise NotImplementedError

    def _onLeft(self, *args):
        for axes in self.canvas.figure.get_axes():
            t1, t2 = axes.get_xlim()
            axes.set_xlim(t1 - t2  + t1, t1)
        self.canvas.draw()

    def _onRight(self, *args):
        for axes in self.canvas.figure.get_axes():
            t1, t2 = axes.get_xlim()
            axes.set_xlim(t2, t2 + t2 - t1)
        self.canvas.draw()

    def _onDown(self, *args):
        for axes in self.canvas.figure.get_axes():
            ch1, ch2 = axes.get_ylim()
            axes.set_ylim(ch2, ch2 + ch2 - ch1)
        self.canvas.draw()

    def _onUp(self, *args):
        for axes in self.canvas.figure.get_axes():
            ch1, ch2 = axes.get_ylim()
            axes.set_ylim(ch2, ch2 + ch2 - ch1)
        self.canvas.draw()
