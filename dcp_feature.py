import pandas as pd
import re

class FeatureInfo:
    """
    FeatureInfo
    """
    df_source = None
    steps = None
    sensors = None
    stats = None
    units = {}
    headers_feature = None
    # Regular Expression
    pattern_feature_2_units = re.compile(r'^([^_]+)(\[.+\]\[.+\])_([+-]?\d+)_(.+)$')
    pattern_feature_1_unit = re.compile(r'^([^_]+)(\[.+\])_([+-]?\d+)_(.+)$')
    pattern_feature_no_unit = re.compile(r'^([^_]+)_([+-]?\d+)_(.+)$')

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
        # _____________________________________________________________________
        # Step, Sensor, Stat
        sensors = list()
        units = {}
        steps = list()
        stats = list()
        for feature in self.headers_feature:
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

    def getSteps(self) -> list:
        return self.steps

    def getSensors(self) -> list:
        return self.sensors

    def getStats(self) -> list:
        return self.stats

    def getUnits(self) -> dict:
        return self.units
