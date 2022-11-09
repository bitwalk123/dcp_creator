from PySide6.QtGui import QIcon, QTextCursor
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPlainTextEdit, QSizePolicy, QPushButton, QStyle

from app_widgets import VBoxLayout


class LogConsole(QWidget):
    prompt = '> '
    eol = '\n'

    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        layout_horiz = QHBoxLayout()
        layout_horiz.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout_horiz)
        # log
        self.log = QPlainTextEdit()
        self.log.setFixedHeight(100)
        self.log.setStyleSheet(
            'font-family: monospace; '
            'font-size: 9pt; '
            'padding: 5px 5px;'
        )
        self.log.setReadOnly(True)
        self.log.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout_horiz.addWidget(self.log)
        # control
        self.control = QWidget()
        layout_horiz.addWidget(self.control)
        #
        layout_vert = VBoxLayout()
        self.control.setLayout(layout_vert)
        # save log
        but_file = QPushButton(
            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogStart)),
            None
        )
        but_file.setToolTip('save log to file.')
        but_file.setContentsMargins(0, 0, 0, 0)
        layout_vert.addWidget(but_file)
        layout_vert.setContentsMargins(0, 0, 0, 0)
        # padding
        vpad = QWidget()
        vpad.setContentsMargins(0, 0, 0, 0)
        layout_vert.addWidget(vpad)
        vpad.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        # trash log
        but_trash = QPushButton(
            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon)),
            None
        )
        but_trash.setContentsMargins(0, 0, 0, 0)
        but_trash.setToolTip('clear log on the console.')
        layout_vert.addWidget(but_trash)

    def insertLine(self, line):
        self.log.insertPlainText(line)
        self.log.moveCursor(QTextCursor.End)

    def insertIn(self, msg):
        line = msg + self.eol
        self.insertLine(line)

    def insertOut(self, msg):
        line = self.prompt + msg + self.eol
        self.insertLine(line)

    def insertCompleted(self, elapsed: float):
        line = 'done. (elapsed {:.3f} sec)'.format(elapsed) + self.eol
        self.insertLine(line)

    def insertAttention(self):
        line = '■■■ ATTENTION ■■■' + self.eol
        self.insertLine(line)
