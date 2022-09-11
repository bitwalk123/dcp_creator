import pandas as pd
import re


class Features:
    """
    FeatureInfo
    """
    df_source = None
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

    def __init__(self, df: pd.DataFrame):
        self.df_source = df
        self.init_sensor()

    def init_sensor(self):
        """
        init_sensor
        initialize sensor dataset
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

        count = 0
        headers_feature = self.headers_feature.copy()
        for sensor in self.sensors:
            for step in self.steps:
                for stat in self.stats:
                    feature = '%s%s_%d_%s' % (sensor, self.units[sensor], step, stat)
                    if feature in headers_feature:
                        headers_feature.remove(feature)
                    count += 1
        print('count', count)
        print(headers_feature)
        print('remaining', len(headers_feature))

    def checkFeatureVaid(self, sensor: str, step: int, stat: str = None) -> bool:
        #if stat is None:
        #    stat = self.stats[0]
        for stat in self.stats:
            feature = '%s%s_%d_%s' % (sensor, self.units[sensor], step, stat)
            if feature not in self.headers_feature:
                return False
        return True

    def getFeatureValue(self, sensor: str, step: int, stat: str = None):
        # print(sensor, step)
        #   Pulse Frequency (setting data)[kHz]_-1_Stddev
        if stat is None:
            stat = self.stats[0]
        feature = '%s%s_%d_%s' % (sensor, self.units[sensor], step, stat)
        return list(set(self.df_source[feature]))

    def getSteps(self) -> list:
        return self.steps

    def getSensors(self) -> list:
        return self.sensors

    def getStats(self) -> list:
        return self.stats

    def getUnits(self) -> dict:
        return self.units

    def getRecipe(self) -> list:
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
        col_chamber = '*chamber'
        return sorted(list(set(self.df_source[col_chamber])))

    def getWafers(self) -> int:
        return self.df_source.shape[0]

    def getFeaturesOriginal(self) -> int:
        return len(self.headers_feature)
