from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QColor, QBrush


class RecipeItem(QStandardItem):
    status = 0

    def __init__(self, *args, status: int):
        super().__init__(*args)
        self.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.setStatus(status)

    def setStatus(self, status):
        if status == -1:
            # multiple values
            self.setValueMultiple()
        elif status == 0:
            # valid value
            self.setValueValid()
        elif status == 1:
            # setting data == 0
            self.setValueZero()
        else:
            pass
        #
        self.status = status

    def setValueMultiple(self):
        self.setBackground(QColor(255, 224, 224))

    def setValueValid(self):
        self.setBackground(QColor(240, 240, 255))
        self.setForeground(QBrush(QColor(0, 0, 32)))

    def setValueZero(self):
        self.setBackground(QColor(240, 240, 240))
        self.setForeground(QBrush(QColor(128, 128, 128)))
