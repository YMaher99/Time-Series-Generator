import unittest
from datetime import datetime
from unittest.mock import patch
from yaml_configuration_manager import YAMLConfigurationManager


class TestYAMLConfigurationManager(unittest.TestCase):

    def setUp(self) -> None:
        self.__config_manager = YAMLConfigurationManager()

    @patch('yaml_configuration_manager.yaml')
    def test_load_config_success(self, patched_yaml_object):
        self.__config_manager.load_config()
        patched_yaml_object.safe_load.assert_called()

    def test_configure_success(self):
        self.__config_manager.yaml_data = {
            "start_date": "1-7-2021",
            "frequencies": ["1D", "10T", "30T", "1H", "6H", "8H"],
            "daily_seasonality_options": ["no", "exist"],
            "weekly_seasonality_options": ["exist", "no"],
            "noise_levels": ["small"],
            "trend_levels": ["exist", "no"],
            "cyclic_periods": ["exist", "no"],
            "data_types": ["", "additive"],
            "percentage_outliers_options": [0.05],
            "data_sizes": [60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 365],
            "datasets_num": 10
        }
        self.__config_manager.configure()
        self.assertEqual(self.__config_manager.start_date,
                         datetime.strptime(self.__config_manager.yaml_data['start_date'], "%d-%m-%Y"),
                         msg="Incorrect start date")
        self.assertIn(self.__config_manager.duration,
                      self.__config_manager.yaml_data['data_sizes'],
                      msg="Incorrect duration")
        self.assertIn(self.__config_manager.frequency,
                      self.__config_manager.yaml_data['frequencies'],
                      msg="Incorrect frequency")
        self.assertIn(self.__config_manager.daily_seasonality,
                      self.__config_manager.yaml_data['daily_seasonality_options'],
                      msg="Incorrect daily seasonality")
        self.assertIn(self.__config_manager.weekly_seasonality,
                      self.__config_manager.yaml_data['weekly_seasonality_options'],
                      msg="Incorrect weekly seasonality")
        self.assertIn(self.__config_manager.noise_level,
                      self.__config_manager.yaml_data['noise_levels'],
                      msg="Incorrect noise level")
        self.assertIn(self.__config_manager.trend_level,
                      self.__config_manager.yaml_data['trend_levels'],
                      msg="Incorrect trend level")
        self.assertIn(self.__config_manager.cyclic_period,
                      self.__config_manager.yaml_data['cyclic_periods'],
                      msg="Incorrect cyclic period")
        self.assertIn(self.__config_manager.data_type,
                      self.__config_manager.yaml_data['data_types'],
                      msg="Incorrect data type")
        self.assertIn(self.__config_manager.percentage_outliers,
                      self.__config_manager.yaml_data['percentage_outliers_options'],
                      msg="Incorrect outlier percentage")
        self.assertEqual(self.__config_manager.datasets_num,
                         self.__config_manager.yaml_data['datasets_num'],
                         msg="Incorrect dataset number")


if __name__ == '__main__':
    unittest.main()
