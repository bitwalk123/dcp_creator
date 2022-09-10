from PySide6.QtWidgets import QMainWindow

from feature_info import FeatureInfo


class DCPSummary(QMainWindow):
    def __init__(self, features: FeatureInfo):
        super().__init__()