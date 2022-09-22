from PySide6.QtWidgets import (
    QMainWindow,
    QScrollArea,
)

from features import Features
from recipe import Recipe


class DCPStepValueSetting(QMainWindow):
    recipe = None

    def __init__(self, features: Features):
        super().__init__()
        self.init_ui(features)

    def init_ui(self, features: Features):
        """
        init_ui
        initialize UI
        """
        # Scroll Area for Central
        central = QScrollArea()
        central.setWidgetResizable(True)
        self.setCentralWidget(central)
        recipe = Recipe(features)
        central.setWidget(recipe)
        #
        self.recipe = recipe

    def getPanel(self) -> Recipe:
        """
        getPanel
        get recipe instance
        """
        return self.recipe
