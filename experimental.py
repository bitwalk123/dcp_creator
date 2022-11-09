from PySide6.QtCore import Signal
from PySide6.QtWidgets import QSizePolicy, QWidget

from app_widgets import (
    HBoxLayout,
    VBoxLayout, GridLayout, LabelHead,
)
from base.feature_matrix import FeatureMatrix


class Experimental(QWidget):
    logMessage = Signal(str)

    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        #
        self.init_ui()

    def init_ui(self):
        """
        init_ui
        initialize UI
        """
        layout_base = VBoxLayout()
        self.setLayout(layout_base)
        #
        layout_row_0 = HBoxLayout()
        layout_base.addLayout(layout_row_0)
        # Dataframe Information
        layout_row_0.addWidget(ExperimentalDataframe())


class ExperimentalDataframe(QWidget):
    style_cell = 'padding:2px 5px;'

    def __init__(self):
        super().__init__()
        layout = GridLayout()
        self.setLayout(layout)
        #
        row = 0
        lab = LabelHead('DataFrame', self.style_cell)
        layout.addWidget(lab, row, 0)
        row += 1
        lab = LabelHead('', self.style_cell)
        layout.addWidget(lab, row, 0)
