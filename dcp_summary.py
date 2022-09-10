from PySide6.QtWidgets import QMainWindow, QScrollArea

from features import Features
from summary import Summary


class DCPSummary(QMainWindow):
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
        summary = Summary(features)
        central.setWidget(summary)
