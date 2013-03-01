import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_wx import \
        _create_wx_app, _load_bitmap, bind
from matplotlib.backends.backend_wxagg import \
        FigureFrameWxAgg, FigureManagerWx, \
        NavigationToolbar2Wx, \
        backend_version, draw_if_interactive, show

import wx

import threading
import time


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
        self.play_thread = PlayThread(self, self.canvas)
        self.play_thread.start()

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
        self.Bind(EVT_REDRAW, self._on_redraw)
        bind(self, wx.EVT_TOOL, self._on_play, id=_NTB_PLAY)
        bind(self, wx.EVT_TOOL, self._on_left, id=_NTB_LEFT)
        bind(self, wx.EVT_TOOL, self._on_right, id=_NTB_RIGHT)
        bind(self, wx.EVT_TOOL, self._on_down, id=_NTB_DOWN)
        bind(self, wx.EVT_TOOL, self._on_up, id=_NTB_UP)

    def _on_redraw(self, *args):
        self.canvas.draw()

    def _on_play(self, *args):
        self.playing = not self.playing

    def _on_left(self, *args):
        for axes in self.canvas.figure.get_axes():
            t1, t2 = axes.get_xlim()
            axes.set_xlim(t1 - t2  + t1, t1)
        self.canvas.draw()

    def _on_right(self, *args):
        for axes in self.canvas.figure.get_axes():
            t1, t2 = axes.get_xlim()
            axes.set_xlim(t2, t2 + t2 - t1)
        self.canvas.draw()

    def _on_down(self, *args):
        for axes in self.canvas.figure.get_axes():
            ch1, ch2 = axes.get_ylim()
            axes.set_ylim(ch1 - 1, ch2 - 1)
        self.canvas.draw()

    def _on_up(self, *args):
        for axes in self.canvas.figure.get_axes():
            ch1, ch2 = axes.get_ylim()
            axes.set_ylim(ch1 + 1, ch2 + 1)
        self.canvas.draw()

_EVT_REDRAW = wx.NewEventType()
EVT_REDRAW = wx.PyEventBinder(_EVT_REDRAW, 1)
class PlayThread(threading.Thread):
    interval = 0.1
    def __init__(self, parent, canvas):
        threading.Thread.__init__(self)
        self._parent = parent
        self._canvas = canvas
    def run(self):
        self._parent.playing = False
        while True:
            start_time = time.time()
            if self._parent.playing:
                for axes in self._canvas.figure.get_axes():
                    t1, t2 = axes.get_xlim()
                    axes.set_xlim(t1 + self.interval, t2 + self.interval)
                evt = wx.PyCommandEvent(_EVT_REDRAW, -1)
                wx.PostEvent(self._parent, evt)
            dt = time.time() - start_time
            if dt < self.interval:
                time.sleep(self.interval - dt)
