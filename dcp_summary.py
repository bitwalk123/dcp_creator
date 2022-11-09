from PySide6.QtWidgets import QScrollArea

from base.tab_window import TabWindow
from features import Features
from summary import Summary


class DCPSummary(TabWindow):
    """
    Summary Window/Panel/Tab
    """
    summary: Summary = None

    def __init__(self, features: Features):
        super().__init__()
        self.features = features
        self.init_ui()

    def init_ui(self):
        """
        init_ui
        initialize UI
        :param info_log:
        """
        # Scroll Area for Central
        central = QScrollArea()
        central.setWidgetResizable(True)
        self.setCentralWidget(central)
        self.summary = Summary(self.features)
        self.summary.logMessage.connect(self.showLog)
        central.setWidget(self.summary)

    def getPanel(self) -> Summary:
        """
        get/return instance of this panel
        """
        return self.summary
