import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import seaborn as sns
from PySide6.QtWidgets import (
    QMainWindow,
    QScrollArea,
    QSizePolicy, QToolBar, QComboBox, QLabel, QStyle,
)

from app_functions import getAppLogger
from features import Features


class SensorStepScatter(FigureCanvas):
    def __init__(self, df):
        mpl.rcParams.update({'font.size': 9})
        facet = sns.FacetGrid(data=df, col='step', height=2, aspect=0.6)
        facet.map_dataframe(sns.scatterplot, x='*start_time', y='value', hue='*chamber')
        facet.set(xticklabels=[])
        facet.tight_layout()
        self.fig: Figure = facet.figure
        super().__init__(self.fig)


class SensorChart(QMainWindow):
    canvas: SensorStepScatter = None

    def __init__(self, parent, features: Features, row: int):
        super().__init__(parent=parent)
        self.features = features
        sensor, unit = self.init_ui(row)
        self.setWindowTitle('%s%s' % (sensor, unit))
        self.setWindowIcon(
            QIcon(self.style().standardIcon(QStyle.SP_ArrowForward))
        )
        self.resize(1000, 200)

    def init_ui(self, row):
        # _____________________________________________________________________
        # Toolbar
        toolbar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, toolbar)
        label_stat = QLabel('Summary Statistics')
        label_stat.setStyleSheet('margin:0 1em 0 0;')
        toolbar.addWidget(label_stat)
        combo_stat = QComboBox()
        toolbar.addWidget(combo_stat)
        # for combo
        stats = self.features.getStats()
        if 'Avg' in stats:
            stat = 'Avg'
        elif 'Median' in stats:
            stat = 'Median'
        else:
            stat = stats[0]
        combo_stat.addItems(stats)
        combo_stat.setCurrentText(stat)
        # _____________________________________________________________________
        # Central Widget
        central = QScrollArea()
        central.setWidgetResizable(True)
        self.setCentralWidget(central)
        base = QMainWindow()
        base.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        central.setWidget(base)
        # dataframe for facetgrid
        df, sensor, unit = self.get_df4facetgrid(row, stat)
        self.canvas = SensorStepScatter(df)
        base.setCentralWidget(self.canvas)

        return sensor, unit

    def get_df4facetgrid(self, row, stat):
        sensor = self.features.getSensors()[row]
        unit = self.features.getUnits()[sensor]
        list_df_step = list()
        steps = self.features.getSteps()
        for step in steps:
            # full feature name
            features_full = '%s%s_%s_%s' % (sensor, unit, step, stat)
            if features_full in self.features.getSrcDfColumns():
                list_cols = [self.features.getSrcDfStart(),
                             self.features.getSrcDfChamberCol()]
                df_step = self.features.getSrcDf()[list_cols].copy()
                df_step['value'] = self.features.getSrcDf()[features_full].copy()
                df_step['step'] = step
                list_df_step.append(df_step)
            else:
                try:
                    raise Exception
                except:
                    logger = getAppLogger(__name__)
                    logger.debug('Error in features_full = %s' % features_full)

        df = pd.concat(list_df_step)

        return df, sensor, unit

    def closeEvent(self, event):
        plt.close(self.canvas.fig)
        event.accept()
