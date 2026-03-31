from krita import Krita, DockWidgetFactory, DockWidgetFactoryBase
from .gesture_2_grid import GestureToGrid

instance = Krita.instance()

dock_widget_factory = DockWidgetFactory(
    "gesture_2_grid_docker",
    DockWidgetFactoryBase.DockRight,
    GestureToGrid
)

instance.addDockWidgetFactory(dock_widget_factory)