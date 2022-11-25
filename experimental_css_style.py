class ExperimentalCSSStyle:
    # COLOR CONSTANT
    COLOR_TARGET_TOLERANCE = '#ccf'
    COLOR_MEAN_SIGMA = '#fcc'

    # CSS Style Sheet
    style_head = 'padding:2px 5px; font-family:monospace; background-color:#eee;'
    style_head2 = 'padding:2px 5px; font-family:monospace; font-size:7pt; background-color:#eee;'
    style_head_sensor = """
    QPushButton {
        padding:2px 5px;
        font-family:monospace;
        background-color:#eee;
        text-align:left;
    }
    QPushButton:hover {
        background-color:#fff;
    }
    QPushButton:pressed {
        background-color:#ddd;
    }
    """
    style_cell = """
    QPushButton {
        font-family:monospace;
        background-color:#beb;
    }
    QPushButton:hover {
        background-color:#dfd;
    }
    QPushButton:pressed {
        background-color:#aca;
    }
    """
    style_cell_label = """
    QLabel {
        font-family:monospace;
        background-color:#fff;
        padding:2px 5px;
    }
    QLabel:disabled {
        background-color:#ccc;
    }
    """
    style_cell_entry = """
    QLineEdit {
        font-family:monospace;
        padding:2px 5px;
    }
    QLineEdit:disabled {
        background-color:#ccc;
    }
    """
    style_cell_radio = """
    QLineEdit {
        font-family:monospace;
        padding:2px 5px;
    }
    """

    style_cell_target_tolerance = """
    QLabel {
        font-family:monospace;
        background-color:%s;
        padding:2px 5px;
    }
    """ % COLOR_TARGET_TOLERANCE
    style_cell_mean_sigma = """
    QLabel {
        padding:2px 5px;
        font-family:monospace;
        background-color:%s;
    }
    """ % COLOR_MEAN_SIGMA
    style_cell_none = """
    QLabel {
        padding:2px 5px;
        font-family:monospace;
    }
    """
    style_cell_disable = """
    QPushButton {
        font-family:monospace;
    }
    """

    def getStyle(self, name):
        return getattr(self, name)
