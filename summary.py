from PySide6.QtWidgets import QSizePolicy

from app_widgets import (
    ComboBox,
    FeatureMatrix,
    GridLayout,
    LabelCell,
    LabelHead,
    LabelNumeric,
)
from features import Features


class Summary(FeatureMatrix):
    style_cell = 'padding:2px 5px;'

    def __init__(self, features: Features):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # source
        self.features = features
        #
        self.init_ui()

    def init_ui(self):
        """
        init_ui
        initialize UI
        """
        layout = GridLayout()
        self.setLayout(layout)
        #
        row = 0
        lab = LabelHead('Recipe', self.style_cell)
        layout.addWidget(lab, row, 0)
        lab_recipe = ComboBox()
        layout.addWidget(lab_recipe, row, 1)
        #
        row += 1
        lab = LabelHead('Chamber', self.style_cell)
        layout.addWidget(lab, row, 0)
        lab_chamber = LabelNumeric(0, self.style_cell)
        layout.addWidget(lab_chamber, row, 1)
        #
        row += 1
        lab = LabelHead('Wafers', self.style_cell)
        layout.addWidget(lab, row, 0)
        lab_wafer = LabelNumeric(0, self.style_cell)
        layout.addWidget(lab_wafer, row, 1)
