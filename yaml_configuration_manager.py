from datetime import datetime
from configuration_manager import ConfigurationManager
import yaml


class YAMLConfigurationManager(ConfigurationManager):

    def __init__(self):
        super().__init__()
        self.__yaml_data = None

    def load_config(self):
        with open("config.yaml", 'r') as file:
            self.__yaml_data = yaml.safe_load(file)

    def configure(self):
        self._start_date = datetime.strptime(self.__yaml_data['start_date'], "%d-%m-%Y")
        self._durations = self.__yaml_data['data_sizes']
        self._frequency = self.__yaml_data['frequencies']
        self._daily_seasonality = self.__yaml_data['daily_seasonality_options']
        self._weekly_seasonality = self.__yaml_data['weekly_seasonality_options']
        self._noise_level = self.__yaml_data['noise_levels']
        self._trend_level = self.__yaml_data['trend_levels']
        self._cyclic_periods = self.__yaml_data['cyclic_periods']
        self._data_type = self.__yaml_data["data_types"]
        self._percentage_outliers_options = self.__yaml_data["percentage_outliers_options"]
        self._datasets_num = self.__yaml_data["datasets_num"]
