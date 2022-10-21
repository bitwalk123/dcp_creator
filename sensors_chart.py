import numpy as np

from PySide6.QtCharts import (
    QChart,
    QChartView,
    QDateTimeAxis,
    QScatterSeries,
    QValueAxis,
)
from PySide6.QtCore import (
    Qt,
    QDateTime,
    QMargins,
)
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QScrollArea,
    QSizePolicy,
    QStyle,
    QWidget,
)

from features import Features


class SensorChart(QMainWindow):
    def __init__(self, parent, features: Features, row: int):
        super().__init__(parent=parent)
        # Scroll Area for Central
        central = QScrollArea()
        central.setWidgetResizable(True)
        self.setCentralWidget(central)

        self.win = QWidget()
        self.win.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        central.setWidget(self.win)

        self.features = features
        sensor, unit, stat = self.init_ui(row)
        self.setWindowTitle('%s%s - %s' % (sensor, unit, stat))
        self.setWindowIcon(
            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward))
        )
        self.resize(1000, 200)

    def init_ui(self, row):
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.win.setLayout(layout)
        sensor = self.features.getSensors()[row]
        unit = self.features.getUnits()[sensor]
        stats = self.features.getStats()
        if 'Avg' in stats:
            stat = 'Avg'
        elif 'Median' in stats:
            stat = 'Median'
        else:
            stat = stats[0]
        steps = self.features.getSteps()

        list_y_max = list()
        list_y_min = list()
        for step in steps:
            features_full = '%s%s_%s_%s' % (sensor, unit, step, stat)  # full feature name
            if features_full in self.features.getSrcDfColumns():
                list_y_max.append(max(self.features.getSrcDf()[features_full]))
                list_y_min.append(min(self.features.getSrcDf()[features_full]))
        y_max = max(list_y_max)
        y_min = min(list_y_min)
        if y_max == y_min:
            y_max += 1
            y_min -= 1

        for step in steps:
            features_full = '%s%s_%s_%s' % (sensor, unit, step, stat)  # full feature name
            if features_full in self.features.getSrcDfColumns():
                list_cols = [self.features.getSrcDfStart(), self.features.getSrcDfChamberCol()]
                df_step = self.features.getSrcDf()[list_cols].copy()
                df_step['value'] = self.features.getSrcDf()[features_full].copy()
                df_step['step'] = step
                df_step['datetime'] = [QDateTime.fromString(str(dt), 'yyyy-MM-dd hh:mm:ss') for dt in df_step['*start_time']]

                series = QScatterSeries()
                for (dt, value) in zip(df_step['datetime'], df_step['value']):
                    series.append(np.int64(dt.toMSecsSinceEpoch()), float(value))
                series.setMarkerSize(10.0)

                chart = QChart()
                chart.setMargins(QMargins(0, 0, 0, 0))
                chart.setContentsMargins(0, 0, 0, 0)
                chart.layout().setContentsMargins(0, 0, 0, 0)
                chart.setBackgroundRoundness(0)
                chart.legend().hide()
                chart.setTitle('step %d' % step)
                chart.addSeries(series)

                axis_x = QDateTimeAxis()
                axis_x.setFormat('MM/dd')
                axis_x.setTitleText('date')
                chart.addAxis(axis_x, Qt.AlignBottom)
                series.attachAxis(axis_x)

                axis_y = QValueAxis()
                axis_y.setMax(y_max)
                axis_y.setMin(y_min)
                chart.addAxis(axis_y, Qt.AlignLeft)
                series.attachAxis(axis_y)

                chart_view = QChartView(chart)
                chart_view.setFixedWidth(200)
                chart_view.setStyleSheet('background-color:blue;')

                layout.addWidget(chart_view)

        return sensor, unit, stat
