from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QStandardItemModel,
    QStandardItem,
)
from PySide6.QtWidgets import (
    QHeaderView,
    QSizePolicy,
)

from app_widgets import (
    TableView,
    VBoxLayout, CheckBoxDelegate,
)
from base.feature_matrix import FeatureMatrix
from features import Features


class Stats(FeatureMatrix):
    """
    DCPMatrix class
    manage sensor selection
    """

    def __init__(self, features: Features):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # source
        self.features = features
        self.init_ui()

    def init_ui(self):
        """
        init_ui
        initialize UI
        """
        layout = VBoxLayout()
        self.setLayout(layout)
        #
        table = TableView()
        model = QStandardItemModel()

        # headers QHeaderView,
        headers = [self.name_stat]
        model.setHorizontalHeaderLabels(headers)
        model.itemChanged.connect(self.on_check_item)
        table.setModel(model)
        table.verticalHeader().setDefaultAlignment(Qt.AlignRight)
        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        delegate = CheckBoxDelegate(table)
        table.setItemDelegateForColumn(1, delegate)
        layout.addWidget(table)

        for stat in self.features.getStats():
            list_row = list()
            # stat name
            item = QStandardItem()
            item.setText(stat)
            # checkbox
            item.setCheckable(True)
            item.setEditable(False)
            # In initial selection, Avg and Stddev are selected.
            if stat == 'Avg' or stat == 'Stddev':
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)
            #
            list_row.append(item)
            #
            model.appendRow(list_row)
        # set the model to member variable
        self.model = model
