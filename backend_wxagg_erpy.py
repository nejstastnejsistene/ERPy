import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends import backend_wx
from matplotlib.backends.backend_wxagg import \
        FigureFrameWxAgg, FigureManagerWx, \
        backend_version, draw_if_interactive, show


def new_figure_manager(num, *args, **kwargs):
    """
    Create a new figure manager instance
    """
    backend_wx._create_wx_app()

    FigureClass = kwargs.pop('FigureClass', Figure)
    figure = FigureClass(*args, **kwargs)

    frame = ErpyFigureFrame(num, figure)
    manager = frame.get_figure_manager()
    if matplotlib.is_interactive():
        manager.frame.Show()
    return manager


class ErpyFigureFrame(FigureFrameWxAgg):
    pass


class ErpyFigureManager(FigureManagerWx):
    pass
