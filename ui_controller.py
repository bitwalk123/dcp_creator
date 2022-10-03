import json

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem

from dcp_sensor_selection import DCPSensorSelection
from dcp_sensor_selection_dock import DCPSensorSelectionDock
from dcp_stats_selection import DCPStats
from dcp_step_value_setting import DCPStepValueSetting
from dcp_summary import DCPSummary
from recipe import Recipe
from sensors import Sensors
from stats import Stats
from summary import Summary


class UIController:
    """
    UI controler, especially for cross-tab management
    """

    def __init__(self, page: dict):
        self.page = page
        # filter
        self.filter_event_handling()

    def Init(self):
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

    def getPanelSummary(self) -> Summary:
        """
        getPanelSummary
        get summary instance
        """
        page_summary: DCPSummary = self.page['summary']
        summary: Summary = page_summary.getPanel()
        return summary

    def getPanelSensors(self) -> Sensors:
        """
        getPanelSensors
        get sensors instance
        """
        page_sensors: DCPSensorSelection = self.page['sensors']
        sensors: Sensors = page_sensors.getPanel()
        return sensors

    def getPanelRecipe(self) -> Recipe:
        """
        getPanelRecipe
        get recipe instance
        """
        page_recipe: DCPStepValueSetting = self.page['recipe']
        recipe: Recipe = page_recipe.getPanel()
        return recipe

    def getPanelStats(self) -> Stats:
        """
        getPanelRecipe
        get recipe instance
        """
        page_stats: DCPStats = self.page['stats']
        stats: Stats = page_stats.getPanel()
        return stats

    def updateFeatures(self):
        """
        update_features
        """
        # _____________________________________________________________________
        # for Summary page
        summary = self.getPanelSummary()
        # _____________________________________________________________________
        # for Sensor Selection page
        sensors = self.getPanelSensors()
        # _____________________________________________________________________
        # for Summary Stats Selection page
        stats = self.getPanelStats()
        # Sensor Selection Modified
        n_sensor_step_valid = sensors.count_checkbox_checked()
        n_stat_valid = stats.count_checkbox_checked()
        # Features Modified
        summary.setFeaturesModified(n_sensor_step_valid * n_stat_valid)
        summary.setStatModified(n_stat_valid)

    def saveJSON4DCP(self, filename: str):
        """
        _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        save JSON file for DCP
        _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        """
        # SENSOR/STEP
        sensors = self.getPanelSensors()
        rows = sensors.model.rowCount()

        key_sensor = sensors.name_sensor
        col_sensor = sensors.find_header_label(key_sensor)
        key_unit = sensors.name_unit
        col_unit = sensors.find_header_label(key_unit)

        cols_step = sensors.get_step_columns()
        list_sensor_steps = list()
        for row in range(rows):
            for col in cols_step:
                item: QStandardItem = sensors.model.item(row, col)
                if item.isCheckable():
                    if item.checkState() == Qt.CheckState.Checked:
                        name_sensor = sensors.model.item(row, col_sensor).text()
                        name_unit = sensors.model.item(row, col_unit).text()
                        full_sensor = name_sensor + name_unit
                        name_step = sensors.model.horizontalHeaderItem(col).text()
                        dic_element = {'sensor': full_sensor, 'step': name_step}
                        list_sensor_steps.append(dic_element)
        # _____________________________________________________________________
        # STATS
        stats = self.getPanelStats()
        rows = stats.model.rowCount()
        col_stat = stats.find_header_label(stats.name_stat)
        col_sel = stats.find_header_label(stats.name_sel)
        list_stats = list()
        for row in range(rows):
            item: QStandardItem = stats.model.item(row, col_sel)
            if item.isCheckable():
                if item.checkState() == Qt.CheckState.Checked:
                    name_stat = stats.model.item(row, col_stat).text()
                    list_stats.append(name_stat)
        # _____________________________________________________________________
        # OUTPUT
        dict_dcp = {'sensor_steps': list_sensor_steps, 'statistics': list_stats}
        with open(filename, 'w') as f:
            json.dump(dict_dcp, f, indent=4)
        # for debug
        print(json.dumps(dict_dcp, indent=4))
        print('total features (%d) = %d sensor_steps x %d statistics' % (
            len(list_sensor_steps) * len(list_stats),
            len(list_sensor_steps),
            len(list_stats)
        ))

    # =========================================================================
    #  SENSOR FILTERING RELATED
    # =========================================================================
    def filter_event_handling(self):
        """
        _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        filter_event_handling
        event handling of filter button on the dock in the sensor panel.
        _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        """
        dock_sensors: DCPSensorSelectionDock = self.page['sensors'].getDock()
        # _____________________________________________________________________
        # binding
        dock_sensors.excludeNoSetting.connect(self.exclude_sensor_no_setting)
        dock_sensors.excludeSetting0.connect(self.exclude_sensor_step_setting_0)
        dock_sensors.excludeGasFlow0.connect(self.exclude_sensor_step_gas_flow_0)
        dock_sensors.excludeRFPower0.connect(self.exclude_sensor_step_rf_power_0)
        dock_sensors.excludeSensorDYP.connect(self.exclude_sensor_dyp)
        dock_sensors.excludeStepMinus1.connect(self.exclude_step_minus_1)
        dock_sensors.excludeStepDechuck.connect(self.exclude_step_dechuck)
        dock_sensors.excludeSensorSetting.connect(self.exclude_sensor_for_setting)
        dock_sensors.excludeSensorTimeDependent.connect(self.exclude_sensor_time_dependent)
        dock_sensors.excludeSensorEPD.connect(self.exclude_sensor_epd)
        dock_sensors.excludeLargeUnit.connect(self.exclude_sensor_large_unit)
        dock_sensors.excludeSensorOES.connect(self.exclude_sensor_oes)

    def exclude_sensor_no_setting(self, flag: bool):
        recipe = self.getPanelRecipe()
        list_sensor_setting = recipe.getSensorWithSetting()
        sensors = self.getPanelSensors()
        sensors.excludeSensorWithoutSetting(flag, list_sensor_setting)
        self.updateFeatures()

    def exclude_sensor_step_setting_0(self, flag: bool):
        recipe = self.getPanelRecipe()
        dict_sensor_step_setting_0 = recipe.getSensorStepSetting0()
        sensors = self.getPanelSensors()
        sensors.excludeSetting0(flag, dict_sensor_step_setting_0)
        self.updateFeatures()

    def exclude_sensor_step_gas_flow_0(self, flag: bool):
        recipe = self.getPanelRecipe()
        list_sensor_step = recipe.excludeGasFlow0(flag)
        sensors = self.getPanelSensors()
        sensors.setSensorStep(flag, list_sensor_step)
        self.updateFeatures()

    def exclude_sensor_step_rf_power_0(self, flag: bool):
        recipe = self.getPanelRecipe()
        list_sensor_step = recipe.excludeRFPower0(flag)
        sensors = self.getPanelSensors()
        sensors.setSensorStep(flag, list_sensor_step)
        self.updateFeatures()

    def exclude_sensor_dyp(self, flag: bool):
        sensors = self.getPanelSensors()
        sensors.excludeSensorDYP(flag)
        self.updateFeatures()

    def exclude_step_minus_1(self, flag: bool):
        sensors = self.getPanelSensors()
        sensors.excludeStepMinus1(flag)
        self.updateFeatures()

    def exclude_step_dechuck(self, flag: bool):
        sensors = self.getPanelSensors()
        sensors.excludeStepDechuck(flag)
        self.updateFeatures()

    def exclude_sensor_for_setting(self, flag: bool):
        sensors = self.getPanelSensors()
        sensors.excludeSensorSetting(flag)
        self.updateFeatures()

    def exclude_sensor_time_dependent(self, flag: bool):
        sensors = self.getPanelSensors()
        sensors.excludeSensorGeneralCounter(flag)
        self.updateFeatures()

    def exclude_sensor_epd(self, flag: bool):
        sensors = self.getPanelSensors()
        sensors.excludeSensorEPD(flag)
        self.updateFeatures()

    def exclude_sensor_large_unit(self, flag: bool):
        sensors = self.getPanelSensors()
        sensors.excludeLargeUnit(flag)
        self.updateFeatures()

    def exclude_sensor_oes(self, flag: bool):
        sensors = self.getPanelSensors()
        sensors.excludeSensorOES(flag)
        self.updateFeatures()

