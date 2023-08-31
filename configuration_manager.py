from abc import ABC, abstractmethod
from datetime import datetime


class ConfigurationManager(ABC):

    def __init__(self):
        self._start_date = datetime(2021, 7, 1)
        self._durations = [60]
        self._frequency = ['1D']
        self._daily_seasonality = ["no"]
        self._weekly_seasonality = ["no"]
        self._noise_level = ["small"]
        self._trend_level = ["no"]
        self._cyclic_periods = ["no"]
        self._data_type = ["additive"]
        self._percentage_outliers_options = [0.05]
        self._datasets_num = 1

    @property
    def datasets_num(self):
        return self._datasets_num

    @property
    def daily_seasonality(self):
        return self._daily_seasonality

    @property
    def cyclic_periods(self):
        return self._cyclic_periods

    @property
    def noise_level(self):
        return self._noise_level

    @property
    def durations(self):
        return self._durations

    @property
    def start_date(self):
        return self._start_date

    @property
    def weekly_seasonality(self):
        return self._weekly_seasonality

    @property
    def frequency(self):
        return self._frequency

    @property
    def trend_level(self):
        return self._trend_level

    @property
    def percentage_outliers_options(self):
        return self._percentage_outliers_options

    @property
    def data_type(self):
        return self._data_type

    @abstractmethod
    def load_config(self):
        pass

    @abstractmethod
    def configure(self):
        pass
