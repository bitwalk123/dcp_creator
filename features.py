import pandas as pd
import re


class Features:
    """
    FeatureInfo
    """
    df_source = None
    src_chamber = '*chamber'
    src_start = '*start_time'
    steps = None
    sensors = None
    stats = None
    units = {}
    headers_feature = None
    headers_others = None
    # Regular Expression
    # example columns
    #   Wall Temperature (setting data)[degC]_2_Stddev
    #   Pulse Frequency (setting data)[kHz]_-1_Stddev
    pattern_feature_2_units = re.compile(r'^([^_]+\[.+\])(\[.+\])_([+-]?\d+)_(.+)$')
    pattern_feature_1_unit = re.compile(r'^([^_]+)(\[.+\])_([+-]?\d+)_(.+)$')
    pattern_feature_no_unit = re.compile(r'^([^_]+)_([+-]?\d+)_(.+)$')
    pattern_sensor_setting = re.compile(r'^(.+)\(setting\sdata\)$')
    pattern_sensor_general_counter = re.compile(r'^General Counter')
    pattern_sensor_dyp = re.compile(r'^Dynamic Process')
    pattern_sensor_epd = re.compile(r'^EPD DATA')
    pattern_sensor_oes = re.compile(r'^[0-9\.]{3,6}nm$')
    pattern_gas_flow = re.compile(r'^Gas\([0-9]{,2}\) Flow$')
    pattern_rf_power = re.compile(r'.*RF\sPower.*')
    #
    # This is for Sensor Table model
    check_states = dict()
    col_sensor = 'Sensor'
    col_unit = 'Unit'
    col_labels = [col_sensor, col_unit]

    def __init__(self, df: pd.DataFrame):
        self.df_source = df
        self.df_source[self.src_start] = pd.to_datetime(df[self.src_start], format='%Y/%m/%d %H:%M:%S')
        self.init_sensor()

    def init_sensor(self):
        """Initialize sensor dataset
        """
        print(self.df_source.shape)
        headers = self.df_source.columns
        # the header name starting with + is not feature
        self.headers_feature = [s for s in headers if not s.startswith('*')]
        self.headers_others = [s for s in headers if s.startswith('*')]
        # _____________________________________________________________________
        # Step, Sensor, Stat
        sensors = list()
        units = {}
        steps = list()
        stats = list()
        print('self.headers_feature ->', len(self.headers_feature))
        for feature in self.headers_feature:
            sensor = None
            # Feature with [unit1][unit2]
            result1 = self.pattern_feature_2_units.match(feature)
            if result1:
                sensor = result1.group(1)
                sensors.append(sensor)
                if sensor not in units:
                    units[sensor] = result1.group(2)
                steps.append(int(result1.group(3)))
                stats.append(result1.group(4))
            else:
                # Feature with [unit]
                result2 = self.pattern_feature_1_unit.match(feature)
                if result2:
                    sensor = result2.group(1)
                    sensors.append(sensor)
                    if sensor not in units:
                        units[sensor] = result2.group(2)
                    steps.append(int(result2.group(3)))
                    stats.append(result2.group(4))
                else:
                    # Feature w/o [unit]
                    result3 = self.pattern_feature_no_unit.match(feature)
                    if result3:
                        sensor = result3.group(1)
                        sensors.append(sensor)
                        if sensor not in units:
                            units[sensor] = ''
                        steps.append(int(result3.group(2)))
                        stats.append(result3.group(3))
                    else:
                        # No match!
                        print('ERROR @ %s' % feature)

        # _____________________________________________________________________
        # Unique, Sort
        steps = sorted(list(set(steps)))
        sensors = sorted(list(set(sensors)))
        stats = sorted(list(set(stats)))
        # Print
        print('STEPS', steps)
        print('SENSORS', sensors)
        print('STATS', stats)
        #
        self.steps = steps
        self.sensors = sensors
        self.stats = stats
        self.units = units

    def checkFeatureValid(self, sensor: str, step: int, stat: str = None) -> bool:
        """
        check if the feature is valid or not.
        """
        for stat in self.stats:
            feature = '%s%s_%d_%s' % (sensor, self.units[sensor], step, stat)
            if feature not in self.headers_feature:
                return False
        return True

    def getFeatureValue(self, sensor: str, step: int, stat: str = None):
        """
        get/return value of feature
        """
        if stat is None:
            stat = self.stats[0]
        feature = '%s%s_%d_%s' % (sensor, self.units[sensor], step, stat)
        return list(set(self.df_source[feature]))

    def getSteps(self) -> list:
        """
        get/return recipe steps
        """
        return self.steps

    def getSensors(self) -> list:
        """
        get/return sensor list
        """
        return self.sensors

    def getStats(self) -> list:
        """
        get/return stat list
        """
        return self.stats

    def getUnits(self) -> dict:
        """
        get/return unit dictionary
        """
        return self.units

    def getRecipe(self) -> list:
        """
        get/return recipe list
        """
        col_recipe = '*recipe'
        pattern_recipe = re.compile(r'.+/([^/]+)$')

        if col_recipe not in self.headers_others:
            return None
        list_recipe = list()
        for recipe_full in self.df_source[col_recipe]:
            result = pattern_recipe.match(recipe_full)
            if result:
                list_recipe.append(result.group(1))
        return sorted(list(set(list_recipe)))

    def getChambers(self) -> list:
        """
        get/return chamber list
        """
        return sorted(list(set(self.df_source[self.src_chamber])))

    def getWafers(self) -> int:
        """
        get/return number of wafer
        """
        return self.df_source.shape[0]

    def getFeaturesOriginal(self) -> int:
        """
        get/return original size of features
        """
        return len(self.headers_feature)

    def getSrcDf(self):
        return self.df_source

    def getSrcDfColumns(self):
        return self.df_source.columns

    def getSrcDfChamberCol(self):
        return self.src_chamber

    def getSrcDfStart(self):
        return self.src_start
    # _________________________________________________________________________
    # for Sensor Table Model
    def getCheckColStart(self):
        return len(self.col_labels)

    def getCols(self):
        return len(self.col_labels) + len(self.steps)

    def getColumnHeader(self, index: int):
        if index < len(self.col_labels):
            return self.col_labels[index]
        else:
            return self.steps[index - len(self.col_labels)]

    def getData(self, row: int, col: int):
        if col == 0:
            return self.sensors[row]
        elif col == 1:
            return self.units[self.sensors[row]]
        else:
            return None

    def getRowIndex(self, index: int):
        return str(index + 1)

    def getRows(self):
        return len(self.sensors)
