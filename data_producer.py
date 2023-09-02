from abc import ABC, abstractmethod
from configuration_manager import ConfigurationManager


class DataProducer(ABC):

    def __init__(self):
        self._metadata = []

    @abstractmethod
    def produce_data(self, time_series, date_range, anomaly_mask, filename, config_manager: ConfigurationManager):
        pass

    @abstractmethod
    def generate_metadata_file(self):
        pass
