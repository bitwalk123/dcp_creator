import pandas as pd
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QSizePolicy,
    QWidget, QSplitter, QFrame, QLabel,
)
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline

from app_functions import get_error_header
from app_widgets import (
    HBoxLayout,
    VBoxLayout, Pad, LabelTitle,
)
from custom_scaler import CustomScaler
from experimental_charts import PCAScatter
from experimental_dataframe import ExperimentalDataframe
from experimental_dcp_menu import ExperimentalDCPMenu
from experimental_dcp_table import DCPTable
from features import Features


class Experimental(QWidget):
    logMessage = Signal(str)

    # instance of internal panels
    panel_info = None
    panel_recipe = None
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
        # Summary
        title_summary = LabelTitle('Summary of exported data')
        layout_base.addWidget(title_summary)
        # Summary table
        self.panel_info = ExperimentalDataframe()
        layout_base.addWidget(self.panel_info)
        # DCP
        title_dcp = LabelTitle('DCP')
        layout_base.addWidget(title_dcp)
        # DCP menubar
        menubar_dcp = ExperimentalDCPMenu()
        layout_base.addWidget(menubar_dcp)
        # DCP table
        self.panel_recipe = DCPTable()
        layout_base.addWidget(self.panel_recipe)
        # PCA
        title_pca = LabelTitle('PCA')
        layout_base.addWidget(title_pca)
        # PCA chart
        self.panel_chart = panel_chart = QFrame()
        panel_chart.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout_base.addWidget(panel_chart)

    def update_ui(self, df: pd.DataFrame, col_chamber: str, features_selected: list):
        self.df = df
        self.col_chamber = col_chamber
        # _____________________________________________________________________
        # ExperimentalDataframe
        # shape
        self.panel_info.set_df_shape(str(df.shape))
        # Wafer
        self.panel_info.set_info_wafer(df.shape[0])
        # Recipe
        recipes = self.features.getRecipe()
        self.panel_info.set_info_recipe(recipes)
        # Tool/Chamber
        chambers = sorted(list(set(df[col_chamber])))
        self.panel_info.set_info_chamber(chambers)
        # Features
        self.panel_info.set_info_feature(features_selected)
        # _____________________________________________________________________
        # TargetTolerance
        sensors = list()
        units = {}
        steps = list()  # dummy
        stats = list()  # dummy
        for feature in features_selected:
            self.features.sensor_unit_step(feature, sensors, stats, steps, units)
        sensors_dcp = sorted(list(set(sensors)))
        steps_recipe = self.features.getSteps()
        info = {
            'sensors': sensors_dcp,
            'units': units,
            'steps': steps_recipe,
            'feature': features_selected,
        }
        self.panel_recipe.gen_table(info, self.features)
        # _____________________________________________________________________
        # PCA
        pipe = Pipeline([
            ('scaler', CustomScaler()),
            ('PCA', PCA())
        ])
        x = df[features_selected].values

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
            'title': self.features.getRecipe()[0],
        }
        canvas = PCAScatter(
            df_pca[[info['hue'], info['x'], info['y']]],
            info
        )
        canvas.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        layout = HBoxLayout()
        self.panel_chart.setLayout(layout)
        layout.addWidget(canvas)
        # padding for right size
        pad = Pad()
        layout.addWidget(pad)

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        self.logMessage.emit('> updated Experimental window.')

    def clear_ui(self):
        pass
