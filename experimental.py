import pandas as pd
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QScrollArea,
    QSizePolicy,
    QWidget,
)
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline

from app_functions import get_error_header
from app_widgets import (
    HBoxLayout,
    VBoxLayout, Pad,
)
from custom_scaler import CustomScaler
from experimental_charts import PCAScatter
from experimental_dataframe import ExperimentalDataframe
from features import Features


class Experimental(QWidget):
    logMessage = Signal(str)
    # instance of internal panels
    panel_1 = None
    panel_2 = None
    #
    df = None
    col_chamber = None

    def __init__(self, features: Features):
        super().__init__()
        self.features = features
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        # initialize UI
        self.init_ui()

    def init_ui(self):
        """Initialize UI
        """
        layout_base = VBoxLayout()
        self.setLayout(layout_base)
        # row 0
        #row_0_layout = HBoxLayout()
        #layout_base.addLayout(row_0_layout)
        # panel_1: Dataframe Information
        self.panel_1 = ExperimentalDataframe()
        #row_0_layout.addWidget(self.panel_1)
        layout_base.addWidget(self.panel_1)
        # row 1
        self.panel_2 = TargetTolerance()
        layout_base.addWidget(self.panel_2)
        # row 2
        self.row_2_layout = row_2_layout = HBoxLayout()
        layout_base.addLayout(row_2_layout)

    def update_ui(self, df: pd.DataFrame, col_chamber: str, list_feature_selected: list):
        self.df = df
        self.col_chamber = col_chamber
        # _____________________________________________________________________
        # panel_1: ExperimentalDataframe
        # shape
        self.panel_1.set_df_shape(str(df.shape))
        # Wafer
        self.panel_1.set_info_wafer(df.shape[0])
        # Recipe
        list_recipe = self.features.getRecipe()
        self.panel_1.set_info_recipe(list_recipe)
        # Tool/Chamber
        list_chamber = sorted(list(set(df[col_chamber])))
        self.panel_1.set_info_chamber(list_chamber)
        # Features
        self.panel_1.set_info_feature(list_feature_selected)
        # _____________________________________________________________________
        # panel_2:
        #self.panel_2 =
        # _____________________________________________________________________
        # PCA
        pipe = Pipeline([
            ('scaler', CustomScaler()),
            ('PCA', PCA())
        ])
        x = df[list_feature_selected].values

        try:
            pipe.fit(x)
        except ValueError as error:
            self.logMessage.emit(get_error_header())
            self.logMessage.emit('@ PCA fitting model')
            self.logMessage.emit(str(error))
            return

        components = pipe.transform(x)
        df_pca = pd.DataFrame(
            data=components,
            columns=['PC{}'.format(i + 1) for i in range(components.shape[1])]
        )
        df_pca.insert(0, 'Tool/Chamber', df[col_chamber])
        # for test
        info = {
            'x': 'PC1',
            'y': 'PC2',
            'hue': 'Tool/Chamber',
            'title' : self.features.getRecipe()[0],
        }
        canvas = PCAScatter(
            df_pca[[info['hue'], info['x'], info['y']]],
            info
        )
        canvas.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.row_2_layout.addWidget(canvas)
        pad = Pad()
        self.row_2_layout.addWidget(pad)

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        self.logMessage.emit('> updated Experimental window.')

    def clear_ui(self):
        pass
class TargetTolerance(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        base = QFrame()
        base.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setWidget(base)