import json

from app_object import AppObject
from dcp_sensor_selection import DCPSensorSelection
from dcp_sensor_selection_dock import DCPSensorSelectionDock
from dcp_stats_selection import DCPStats
from dcp_step_value_setting import DCPStepValueSetting
from dcp_summary import DCPSummary
from recipe import Recipe
from sensors import Sensors
from stats import Stats
from summary import Summary
from util_filter import UtilFilter


class UIController(AppObject):
    """UI controler, especially for cross-tab management
    """

    def __init__(self, page: dict):
        super().__init__(page)
        # self.page = page
        # filters
        self.filter_utility = UtilFilter(page)
        # self.filter_event_handling()
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
        # SENSOR/STEP
        sensors = self.getPanelSensors()
        dict_dcp = sensors.getDCP()
        # _____________________________________________________________________
        # OUTPUT
        with open(filename, 'w') as f:
            json.dump(dict_dcp, f, indent=4)
        # for debug
        print(json.dumps(dict_dcp, indent=4))

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
        #dock_sensors.excludeNoSetting.connect(self.exclude_sensor_no_setting)
        #dock_sensors.excludeSetting0.connect(self.exclude_sensor_step_setting_0)
        #dock_sensors.excludeSensorDYP.connect(self.exclude_sensor_dyp)
        #dock_sensors.excludeStepMinus1.connect(self.exclude_step_minus_1)
        #dock_sensors.excludeStepDechuck.connect(self.exclude_step_dechuck)
        #dock_sensors.excludeSensorSetting.connect(self.exclude_sensor_for_setting)
        #dock_sensors.excludeSensorTimeDependent.connect(self.exclude_sensor_time_dependent)
        #dock_sensors.excludeSensorEPD.connect(self.exclude_sensor_epd)
        #dock_sensors.excludeSensorOES.connect(self.exclude_sensor_oes)

    #def exclude_sensor_no_setting(self, flag: bool):
    #    recipe = self.getPanelRecipe()
    #    list_sensor_setting = recipe.getSensorWithSetting()
    #    sensors = self.getPanelSensors()
    #    sensors.excludeSensorWithoutSetting(flag, list_sensor_setting)
    #    self.updateFeatures()

    def exclude_sensor_step_setting_0(self, flag: bool):
        recipe = self.getPanelRecipe()
        dict_sensor_step_setting_0 = recipe.getSensorStepSetting0()
        sensors = self.getPanelSensors()
        sensors.excludeSetting0(flag, dict_sensor_step_setting_0)
        self.updateFeatures()

    def exclude_sensor_dyp(self, flag: bool):
        sensors = self.getPanelSensors()
        sensors.excludeSensorDYP(flag)
        self.updateFeatures()

    #def exclude_step_minus_1(self, flag: bool):
    #    sensors = self.getPanelSensors()
    #    sensors.excludeStepMinus1(flag)
    #    self.updateFeatures()

    #def exclude_step_dechuck(self, flag: bool):
    #    sensors = self.getPanelSensors()
    #    sensors.excludeStepDechuck(flag)
    #    self.updateFeatures()

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
