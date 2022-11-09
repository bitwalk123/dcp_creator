import pandas as pd
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QSizePolicy, QWidget

from app_widgets import (
    GridLayout,
    HBoxLayout,
    LabelCell,
    LabelHead,
    VBoxLayout,
)
from base.feature_matrix import FeatureMatrix


class Experimental(QWidget):
    logMessage = Signal(str)
    # instance of internal panels
    panel_1 = None
    #
    df = None

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
        self.panel_1 = ExperimentalDataframe()
        layout_row_0.addWidget(self.panel_1)

    def update_ui(self, df: pd.DataFrame):
        self.df = df
        # ExperimentalDataframe
        # shape
        self.panel_1.set_df_shape(str(df.shape))

class ExperimentalDataframe(QWidget):
    style_cell = 'padding:2px 5px; font-family:monospace;'
    lab_df_shape = None

    def __init__(self):
        super().__init__()
        layout = GridLayout()
        self.setLayout(layout)
        #
        row = 0
        lab = LabelHead('DataFrame', self.style_cell)
        layout.addWidget(lab, row, 0)
        self.lab_df_shape = LabelCell('', self.style_cell)
        layout.addWidget(self.lab_df_shape, row, 1)
        row += 1
        lab = LabelHead('', self.style_cell)
        layout.addWidget(lab, row, 0)

    def set_df_shape(self, shape: str):
        self.lab_df_shape.setText(shape)
