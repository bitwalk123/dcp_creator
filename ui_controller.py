import json
from collections import OrderedDict

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
        """get sensor/step currently selected.
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
        """get summary statistics currently selected.
        """
        list_checked = list()
        model = self.getPanelStatsModel()
        rows = model.rowCount()
        for row in range(rows):
            item = model.item(row, 0)
            if item.checkState() == Qt.CheckState.Checked:
                list_checked.append(item.text())
        return list_checked

    def readJSON4DCP(self, jsonfile):
        """
        _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        read JSON file for DCP
        _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        """
        with open(jsonfile) as f:
            dict_dcp = json.load(f)
        # for debug
        # print(json.dumps(dict_dcp, indent=4))
        # reset ChackState in Sensor/Stap and Summary Statistics
        self.clearDCPSensorStep()
        self.clearDCPStats()
        # reflect jason file on the CheckStates
        self.setDCPSensorStep(dict_dcp)
        self.setDCPStats(dict_dcp)

    def clearDCPSensorStep(self):
        """clear check status of sensor/step selection.
        """
        model = self.getPanelSensorsModel()
        rows = model.rowCount()
        cols_step = self.get_step_columns()

        for row in range(rows):
            for col in cols_step:
                index = model.index(row, col)
                model.setData(index, Qt.CheckState.Unchecked, role=Qt.CheckStateRole)

    def clearDCPStats(self):
        """clear check status of summary statistics.
        """
        model = self.getPanelStatsModel()
        rows = model.rowCount()
        for row in range(rows):
            item = model.item(row, 0)
            item.setData(Qt.CheckState.Unchecked, role=Qt.CheckStateRole)

    def setDCPSensorStep(self, dict_dcp: dict):
        """set sensor/step checked based on dict
        """
        features = self.getPanelSensorsFeatures()
        model = self.getPanelSensorsModel()

        for dict_sensor_step in dict_dcp['sensor_steps']:
            sensor_unit = dict_sensor_step['sensor']
            step = dict_sensor_step['step']

            sensor = None
            unit = None

            # Feature with [unit1][unit2]
            result1 = features.pattern_feature_2_units_nostepstat.match(sensor_unit)
            if result1:
                sensor = result1.group(1)
                unit = result1.group(2)
            else:
                # Feature with [unit]
                result2 = features.pattern_feature_1_unit_nostepstat.match(sensor_unit)
                if result2:
                    sensor = result2.group(1)
                    unit= result2.group(2)
                else:
                    # Feature w/o [unit]
                    result3 = features.pattern_feature_no_unit_nostepstat.match(sensor_unit)
                    if result3:
                        sensor = result3.group(1)
                        units = ''
                    else:
                        # No match!
                        print('ERROR @ %s' % sensor_unit)
            # set CheckState.Checked
            row = self.get_sensor_row(sensor)
            col = self.find_header_label(int(step))
            index = model.index(row, col)
            model.setData(index, Qt.CheckState.Checked, role=Qt.CheckStateRole)

    def setDCPStats(self, dict_dcp: dict):
        """set summary statistics checked based on dict
        """
        model = self.getPanelStatsModel()
        rows = model.rowCount()

        for name_stat in dict_dcp['statistics']:
            for row in range(rows):
                item = model.item(row, 0)
                if item.text() == name_stat:
                    # ** ATTENTION **
                    # Probably, this should be following:
                    # -> item.setData(Qt.CheckState.Checked, role=Qt.CheckStateRole)
                    item.setData(Qt.CheckState.Checked.value, role=Qt.CheckStateRole)

