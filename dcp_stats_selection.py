from PySide6.QtWidgets import (
    QMainWindow,
    QScrollArea,
)

from features import Features
from stats import Stats


class DCPStats(QMainWindow):
    """
    Panel for Summary Statistics
    """
    stats = None

    def __init__(self, features: Features):
        super().__init__()
        self.init_ui(features)

    def init_ui(self, features: Features):
        """
        init_ui
        initialize UI
        :param info_log:
        """
        # Scroll Area for Central
        central = QScrollArea()
        central.setWidgetResizable(True)
        self.setCentralWidget(central)
        # widget on the Scroll Area
        self.stats = stats = Stats(features)
        central.setWidget(stats)

    def getPanel(self) -> Stats:
        """
        get/return instance of this panel
        """
        return self.stats
