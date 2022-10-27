import json

from PySide6.QtCore import Qt

from app_object import AppObject
from util_filter import UtilFilter


class UIController(AppObject):
    """UI controller, especially for cross-tab management
    """

    def __init__(self, page: dict):
        super().__init__(page)
        # filters
        self.filter_utility = UtilFilter(page)
        # _____________________________________________________________________
        # for Summary page
        summary = self.getPanelSummary()
        # _____________________________________________________________________
        # for Sensor Selection page
        sensors = self.getPanelSensors()
        # _____________________________________________________________________
        # for Summary Stats Selection page
        stats = self.getPanelStats()
        # _____________________________________________________________________
        # Sensor Selection Modified
        n_sensor_step_valid = sensors.count_checkbox_checked()
        n_stat_valid = stats.count_checkbox_checked()
        # _____________________________________________________________________
        # for Summary page (update)
        # Recipe
        summary.setRecipe()
        # Chamber
        summary.setChambers()
        # Wafer
        summary.setWafers()
        # Features Original
        summary.setFeaturesOriginal()
        # Features Modified
        summary.setFeaturesModified(n_sensor_step_valid * n_stat_valid)
        # Sensor Selection
        summary.setSensor()
        # Step
        summary.setStep()
        # Stat
        summary.setStat()
        summary.setStatModified(n_stat_valid)

    def saveJSON4DCP(self, filename: str):
        """
        _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        save JSON file for DCP
        _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        """
        dict_dcp = {
            'sensor_steps': self.getDCPSensorStep(),
            'statistics': self.getDCPStats()
        }
        # _____________________________________________________________________
        # OUTPUT
        with open(filename, 'w') as f:
            json.dump(dict_dcp, f, indent=4)
        # for debug
        print(json.dumps(dict_dcp, indent=4))

    def getDCPSensorStep(self) -> list:
        """get sensor/tep currently selected.
        """
        model = self.getPanelSensorsModel()
        features = self.getPanelSensorsFeatures()
        rows = model.rowCount()
        cols_step = self.get_step_columns()
        list_sensor_steps = list()

        for row in range(rows):
            for col in cols_step:
                index = model.index(row, col)
                state = model.data(index, role=Qt.CheckStateRole)
                # check whether state is Qt.CheckState enum or int
                # This is measure in case that checkbox have Qt.CheckState or int.
                if isinstance(state, Qt.CheckState):
                    val = state.value
                else:
                    val = state
                # check comparing with int
                if val == Qt.CheckState.Checked.value:
                    name_sensor = features.getSensors()[row]
                    name_unit = features.getUnits()[name_sensor]
                    num_step = model.headerData(col, Qt.Horizontal, Qt.DisplayRole)
                    full_sensor = name_sensor + name_unit
                    dict_element = {'sensor': full_sensor, 'step': str(num_step)}
                    list_sensor_steps.append(dict_element)
        return list_sensor_steps

    def getDCPStats(self) -> list:
        list_checked = list()
        model = self.getPanelStatsModel()
        rows = model.rowCount()
        for row in range(rows):
            item = model.item(row, 0)
            if item.checkState() == Qt.CheckState.Checked:
                list_checked.append(item.text())
        return list_checked
