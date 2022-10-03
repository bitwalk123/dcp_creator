import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PySide6.QtWidgets import QMainWindow, QScrollArea, QWidget, QHBoxLayout, QSizePolicy

from features import Features


class Scatter(FigureCanvas):
    df: pd.DataFrame = None

    def __init__(self, df):
        facetgrif = sns.FacetGrid(df, col='step', hue='*chamber')
        facetgrif.map(sns.scatterplot, '*start_time', 'value')
        super().__init__(facetgrif.fig)


class SensorChart(QMainWindow):
    def __init__(self, parent, features: Features, row: int):
        super().__init__(parent=parent)
        self.features = features
        sensor = self.init_ui(row)
        self.setWindowTitle(sensor)

    def init_ui(self, row):
        central = QScrollArea()
        central.setWidgetResizable(True)
        self.setCentralWidget(central)
        base = QWidget()
        base.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        central.setWidget(base)
        layout = QHBoxLayout()
        base.setLayout(layout)

        sensor = self.features.getSensors()[row]
        unit = self.features.getUnits()[sensor]
        stats = self.features.getStats()
        stat = stats[0]
        #
        list_df_step = list()
        steps = self.features.getSteps()
        for step in steps:
            features_full = '%s%s_%s_%s' % (sensor, unit, step, stat)
            if features_full in self.features.getSrcDfColumns():
                list_cols = [self.features.getSrcDfStart(),
                             self.features.getSrcDfChamberCol()]
                df_step = self.features.getSrcDf()[list_cols].copy()
                df_step['value'] = self.features.getSrcDf()[features_full].copy()
                df_step['step'] = step
                list_df_step.append(df_step)

        df = pd.concat(list_df_step)
        canvas = Scatter(df)
        layout.addWidget(canvas)

        return sensor
