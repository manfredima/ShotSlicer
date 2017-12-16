#ilunga_menu#Shot slicer;show()
from . import mayaShotSlicerQT, mayaShotSlicer
reload(mayaShotSlicerQT)
reload(mayaShotSlicer)
# from .widgets import shotSlicer_UIs
# reload(shotSlicer_UIs)

def show():
    w = mayaShotSlicerQT.shotSlicerClass()
    w.show()