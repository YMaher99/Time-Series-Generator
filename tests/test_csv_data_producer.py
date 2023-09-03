import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock
import pandas as pd
import numpy as np
from csv_data_producer import CSVDataProducer
from configuration_manager import ConfigurationManager
import os


class TestCSVDataProducer(unittest.TestCase):
    def setUp(self) -> None:
        self.__mock_configuration_manager = Mock(spec=ConfigurationManager)
        self.__mock_configuration_manager.data_type.return_value = "additive"
        self.__mock_configuration_manager.daily_seasonality.return_value = "no"
        self.__mock_configuration_manager.weekly_seasonality.return_value = "no"
        self.__mock_configuration_manager.noise_level.return_value = "small"
        self.__mock_configuration_manager.trend_level.return_value = "no"
        self.__mock_configuration_manager.cyclic_period.return_value = "no"
        self.__mock_configuration_manager.duration.return_value = 60
        self.__mock_configuration_manager.percentage_outliers.return_value = 0.05
        self.__mock_configuration_manager.frequency.return_value = '1D'
        self.__producer = CSVDataProducer()
        self.__filename = "test"

        self.__date_range = pd.date_range(start=datetime(2017, 5, 10),
                                          end=datetime(2017, 5, 10) + timedelta(
                                              days=int(self.__mock_configuration_manager.duration())),
                                          freq=self.__mock_configuration_manager.frequency())
        self.__anomaly_mask = np.ndarray(shape=len(self.__date_range))
        self.__time_series = pd.Series(self.__anomaly_mask)

    def test_produce_data_success(self):
        self.__producer.produce_data(self.__time_series, self.__date_range, self.__anomaly_mask,
                                     self.__mock_configuration_manager,
                                     self.__filename)
        self.assertTrue(os.path.exists('./sample_datasets/test.csv'), "Time series file was not created successfully")

    def test_generate_metadata_file(self):
        self.__producer.metadata = [{'id': self.__filename,
                                     'data_type': self.__mock_configuration_manager.data_type,
                                     'daily_seasonality': self.__mock_configuration_manager.daily_seasonality,
                                     'weekly_seasonality': self.__mock_configuration_manager.weekly_seasonality,
                                     'noise': self.__mock_configuration_manager.noise_level,
                                     'trend': self.__mock_configuration_manager.trend_level,
                                     'cyclic_period (3 months)': self.__mock_configuration_manager.cyclic_period,
                                     'data_size': self.__mock_configuration_manager.duration,
                                     'percentage_outliers': self.__mock_configuration_manager.percentage_outliers,
                                     'percentage_missing': 0.05,
                                     'freq': self.__mock_configuration_manager.frequency}]
        self.__producer.generate_metadata_file()
        self.assertTrue(os.path.exists('./sample_datasets/meta_data.csv'), "Metadata file was not created successfully")


if __name__ == '__main__':
    unittest.main()
