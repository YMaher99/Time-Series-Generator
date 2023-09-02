from data_producer import DataProducer
import pandas as pd


class CSVDataProducer(DataProducer):
    def produce_data(self, time_series, date_range, anomaly_mask, filename, config_manager):

        df = pd.DataFrame({'value': time_series, 'timestamp': date_range, 'anomaly': anomaly_mask})
        df.to_csv(f"./sample_datasets/{filename}.csv", encoding='utf-8', index=False)
        self._metadata.append({'id': str(filename),
                               'data_type': config_manager.data_type,
                               'daily_seasonality': config_manager.daily_seasonality,
                               'weekly_seasonality': config_manager.weekly_seasonality,
                               'noise': config_manager.noise_level,
                               'trend': config_manager.trend_level,
                               'cyclic_period (3 months)': config_manager.cyclic_period,
                               'data_size': config_manager.duration,
                               'percentage_outliers': config_manager.percentage_outliers,
                               'percentage_missing': 0.05,
                               'freq': config_manager.frequency})

    def generate_metadata_file(self):
        """
            Generates a .csv file containing the metadata of the generated time series
        """
        pd.DataFrame.from_records(self._metadata).to_csv('sample_datasets/meta_data.csv', encoding='utf-8', index=False)
