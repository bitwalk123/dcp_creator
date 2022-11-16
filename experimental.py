import pandas as pd
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QSizePolicy,
    QWidget, QSplitter, QFrame,
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
from experimental_target_tolerance import TargetTolerance
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
        # row 0
        self.panel_info = ExperimentalDataframe()
        # row_0_layout.addWidget(self.panel_1)
        layout_base.addWidget(self.panel_info)
        # row 1
        splitter = QSplitter(Qt.Vertical)
        layout_base.addWidget(splitter)
        #
        self.panel_recipe = TargetTolerance()
        splitter.addWidget(self.panel_recipe)
        #
        self.panel_chart = panel_chart = QFrame()
        splitter.addWidget(panel_chart)

    def update_ui(self, df: pd.DataFrame, col_chamber: str, list_feature_selected: list):
        self.df = df
        self.col_chamber = col_chamber
        # _____________________________________________________________________
        # ExperimentalDataframe
        # shape
        self.panel_info.set_df_shape(str(df.shape))
        # Wafer
        self.panel_info.set_info_wafer(df.shape[0])
        # Recipe
        list_recipe = self.features.getRecipe()
        self.panel_info.set_info_recipe(list_recipe)
        # Tool/Chamber
        list_chamber = sorted(list(set(df[col_chamber])))
        self.panel_info.set_info_chamber(list_chamber)
        # Features
        self.panel_info.set_info_feature(list_feature_selected)
        # _____________________________________________________________________
        # TargetTolerance
        sensors = list()
        units = {}
        steps = list()  # dummy
        stats = list()  # dummy
        for feature in list_feature_selected:
            self.features.sensor_unit_step(feature, sensors, stats, steps, units)
        sensors = sorted(list(set(sensors)))
        steps = self.features.getSteps()
        info = {
            'sensors': sensors,
            'units': units,
            'steps': steps,
        }
        self.panel_recipe.set_dimension(info)
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
