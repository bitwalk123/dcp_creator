from PySide6.QtWidgets import QWidget, QSizePolicy

from app_widgets import GridLayout, LabelHead, LabelCell, LabelNumeric, ComboBox


class ExperimentalDataframe(QWidget):
    style_head = 'padding: 2px 5px; font-family: monospace;'
    style_cell = 'padding: 2px 5px; font-family: monospace; background-color: white;'
    style_combo = 'font-family: monospace;'
    width_combo_chamber = 200
    width_combo_feature = 400
    lab_df_shape = None

    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        layout = GridLayout()
        self.setLayout(layout)
        # DataFrame
        row = 0
        lab = LabelHead('DataFrame', self.style_head)
        layout.addWidget(lab, row, 0)
        self.lab_df_shape = LabelCell('', self.style_cell)
        layout.addWidget(self.lab_df_shape, row, 1)
        # Wafers
        row += 1
        lab = LabelHead('Wafers', self.style_head)
        layout.addWidget(lab, row, 0)
        self.lab_n_wafer = LabelNumeric('', self.style_cell)
        layout.addWidget(self.lab_n_wafer, row, 1)
        # Recipe(s)
        row += 1
        lab = LabelHead('Recipe', self.style_head)
        layout.addWidget(lab, row, 0)
        self.lab_n_recipe = LabelNumeric('', self.style_cell)
        layout.addWidget(self.lab_n_recipe, row, 1)
        self.combo_recipe = ComboBox()
        self.combo_recipe.setFixedWidth(self.width_combo_chamber)
        self.combo_recipe.setStyleSheet(self.style_combo)
        self.combo_recipe.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.combo_recipe, row, 2)
        # Tool/Chamber
        row += 1
        lab = LabelHead('Tool/Chamber', self.style_head)
        layout.addWidget(lab, row, 0)
        self.lab_n_chamber = LabelNumeric('', self.style_cell)
        layout.addWidget(self.lab_n_chamber, row, 1)
        self.combo_chamber = ComboBox()
        self.combo_chamber.setFixedWidth(self.width_combo_chamber)
        self.combo_chamber.setStyleSheet(self.style_combo)
        self.combo_chamber.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.combo_chamber, row, 2)
        # Features
        row += 1
        lab = LabelHead('Features', self.style_head)
        layout.addWidget(lab, row, 0)
        self.lab_n_feature = LabelNumeric('', self.style_cell)
        layout.addWidget(self.lab_n_feature, row, 1)
        self.combo_feature = ComboBox()
        self.combo_feature.setFixedWidth(self.width_combo_feature)
        self.combo_feature.setStyleSheet(self.style_combo)
        self.combo_feature.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.combo_feature, row, 2)

    def set_df_shape(self, shape: str):
        self.lab_df_shape.setText(shape)

    def set_info_wafer(self, n_wafer: int):
        self.lab_n_wafer.setValue(n_wafer)

    def set_info_recipe(self, list_recipe: list):
        n_recipe = len(list_recipe)
        self.lab_n_recipe.setValue(n_recipe)
        self.combo_recipe.addItems(list_recipe)

    def set_info_chamber(self, list_chamber: list):
        n_chamber = len(list_chamber)
        self.lab_n_chamber.setValue(n_chamber)
        self.combo_chamber.addItems(list_chamber)

    def set_info_feature(self, list_feature: list):
        n_feature = len(list_feature)
        self.lab_n_feature.setValue(n_feature)
        self.combo_feature.addItems(list_feature)
