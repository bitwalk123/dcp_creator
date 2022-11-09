from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow


class TabWindow(QMainWindow):
    """Tab Window/Panel/Tab
    """
    logMessage = Signal(str)

    def __init__(self):
        super().__init__()

    def showLog(self, msg: str):
        self.logMessage.emit(msg)
