from PySide6.QtWidgets import (
    QMainWindow,
    QScrollArea,
)

from feature_info import FeatureInfo
from dcp_recipe import DCPRecipe


class DCPStepValueSetting(QMainWindow):
    def __init__(self, features: FeatureInfo):
        super().__init__()
        self.init_ui(features)

    def init_ui(self, features: FeatureInfo):
        """
        init_ui
        initialize UI
        :param info_log:
        """
        # Scroll Area for Central
        central = QScrollArea()
        central.setWidgetResizable(True)
        self.setCentralWidget(central)
        recipe = DCPRecipe(features)
        central.setWidget(recipe)
