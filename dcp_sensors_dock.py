from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QDockWidget,
    QSizePolicy,
    QWidget, QScrollArea,
)

from app_widgets import (
    VBoxLayout,
)


class DCPSensorSelectionDock(QDockWidget):
    """Dock for sensor filtering
    """
    def __init__(self):
        super().__init__('Filter')
        sarea = QScrollArea()
        sarea.setWidgetResizable(True)
        self.setWidget(sarea)
        base = QWidget()
        base.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sarea.setWidget(base)

        # Layout for the dock
        self.layout = VBoxLayout()
        base.setLayout(self.layout)

    def getLayout(self):
        return self.layout