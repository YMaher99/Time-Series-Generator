import unittest
from yaml_configuration_manager import YAMLConfigurationManager
from time_series_simulator import TimeSeriesGenerator
import pandas as pd
import numpy as np


class TestTimeSeriesSimulator(unittest.TestCase):

    def setUp(self) -> None:
        self.__config_manager = YAMLConfigurationManager()
        self.__generator = TimeSeriesGenerator(self.__config_manager)

    def test_generate_time_series_success(self):
        result = self.__generator.generate_time_series()
        self.assertEqual(len(result), 3, "generate_time_series did not return a tuple of length 3")
        self.assertIsInstance(result[0], pd.Series, msg="The time series is not a Pandas Series")
        self.assertIsInstance(result[1], pd.DatetimeIndex, msg="The date range is not a Pandas DateTimeIndex")
        self.assertIsInstance(result[2], np.ndarray, msg="The anomaly mask is not a NumPy nd-array")


if __name__ == '__main__':
    unittest.main()
