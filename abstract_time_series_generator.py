from abc import ABC, abstractmethod


class AbstractTimeSeriesGenerator(ABC):

    @abstractmethod
    def generate_time_series(self):
        pass
