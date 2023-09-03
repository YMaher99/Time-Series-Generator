from abc import ABC, abstractmethod
from configuration_manager import ConfigurationManager
import os


class DataProducer(ABC):

    def __init__(self):
        self._metadata = []
        if not os.path.exists('sample_datasets'):
            os.mkdir('sample_datasets')

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        self._metadata = value

    @abstractmethod
    def produce_data(self, time_series, date_range, anomaly_mask, filename, config_manager: ConfigurationManager):
        pass

    @abstractmethod
    def generate_metadata_file(self):
        pass
