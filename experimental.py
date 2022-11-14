import pandas as pd
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QSizePolicy,
    QWidget, QFrame,
)
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline

from app_widgets import (
    HBoxLayout,
    VBoxLayout,
)
from custom_scaler import CustomScaler
from experimental_charts import Scatter
from experimental_dataframe import ExperimentalDataframe
from features import Features


class Experimental(QWidget):
    logMessage = Signal(str)
    # instance of internal panels
    panel_1 = None
    #
    df = None
    col_chamber = None

    def __init__(self, features: Features):
        super().__init__()
        self.features = features
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # initialize UI
        self.init_ui()

    def init_ui(self):
        """Initialize UI
        """
        layout_base = VBoxLayout()
        self.setLayout(layout_base)
        # row 0
        row_0_layout = HBoxLayout()
        layout_base.addLayout(row_0_layout)
        # panel_1: Dataframe Information
        self.panel_1 = ExperimentalDataframe()
        row_0_layout.addWidget(self.panel_1)
        # row 1
        self.row_1_layout = row_2_layout = HBoxLayout()
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
        # PCA
        pipe = Pipeline([
            ('scaler', CustomScaler()),
            ('PCA', PCA())
        ])
        x = df[list_feature_selected].values
        components = pipe.fit_transform(x)
        df_pca = pd.DataFrame(
            data=components,
            columns=['PC{}'.format(i + 1) for i in range(components.shape[1])]
        )
        df_pca.insert(0, 'Tool/Chamber', df[col_chamber])
        canvas = Scatter(df_pca[['Tool/Chamber', 'PC1', 'PC2']], x='PC1', y='PC2', hue='Tool/Chamber')
        canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.row_1_layout.addWidget(canvas)

    def clear_ui(self):
        pass
