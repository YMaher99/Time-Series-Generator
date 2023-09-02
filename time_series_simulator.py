import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from configuration_manager import ConfigurationManager
from sklearn.preprocessing import MinMaxScaler
from abstract_time_series_generator import AbstractTimeSeriesGenerator


random.seed(22)


class TimeSeriesGenerator(AbstractTimeSeriesGenerator):

    def __init__(self, config_manager: ConfigurationManager):
        self.__time_series = None
        self.__date_range = None
        self.__anomaly_mask = None
        self.__config_manager = config_manager

    @property
    def time_series(self):
        return self.__time_series

    def __generate_data_range(self):
        date_rng = pd.date_range(start=self.__config_manager.start_date,
                                 end=self.__config_manager.start_date + timedelta(days=self.__config_manager.duration),
                                 freq=self.__config_manager.frequency)
        self.__time_series = date_rng
        self.__date_range = date_rng.copy(deep=True)

    def __add_daily_seasonality(self):
        if self.__config_manager.daily_seasonality == "exist":  # Daily Seasonality
            seasonal_component = np.sin(2 * np.pi * self.__time_series.hour / 24)
            seasonal_component += 1 if self.__config_manager.data_type == 'multiplicative' else 0
        else:
            seasonal_component = np.zeros(len(self.__time_series.hour)) \
                if self.__config_manager.data_type == 'additive' else np.ones(len(self.__time_series))
        return pd.Series(seasonal_component)

    def __add_weekly_seasonality(self):
        if self.__config_manager.weekly_seasonality == "exist":  # Weekly Seasonality
            seasonal_component = np.sin(2 * np.pi * self.__time_series.dayofweek / 7)
            seasonal_component += 1 if self.__config_manager.data_type == 'multiplicative' else 0
        else:
            seasonal_component = np.zeros(len(self.__time_series)) \
                if self.__config_manager.data_type == 'additive' else np.ones(len(self.__time_series))
        return pd.Series(seasonal_component)

    def __add_trend(self):
        if self.__config_manager.trend_level == "exist":
            slope = random.choice([1, -1])
            trend_component = np.linspace(0, self.__config_manager.duration / 30 * slope, len(self.__time_series))\
                if slope == 1 else np.linspace(-1 * self.__config_manager.duration / 30, 0, len(self.__time_series))
        else:  # No Trend
            trend_component = np.zeros(len(self.__time_series)) \
                if self.__config_manager.data_type == 'additive' else np.ones(len(self.__time_series))

        return pd.Series(trend_component)

    def __add_cycles(self):
        if self.__config_manager.cyclic_period == "exist":  # Quarterly
            cycle_component = 1 if self.__config_manager.data_type == 'multiplicative' else 0
            cycle_component += np.sin(2 * np.pi * (self.__time_series.quarter - 1) / 4)
        else:  # No Cyclic Periods
            cycle_component = 0 if self.__config_manager.data_type == 'additive' else 1

        return cycle_component

    def __add_noise(self):
        if self.__config_manager.noise_level == "small":
            noise_level = 0.1
            # noise = np.random.normal(0, 0.05, len(data))
        elif self.__config_manager.noise_level == "large":
            noise_level = 0.3
            # noise = np.random.normal(0, 0.1, len(data))
        else:  # No Noise
            noise_level = 0

        noise = np.zeros_like(self.__time_series)
        for i in range(len(self.__time_series)):
            noise[i] = np.random.normal(0, abs(self.__time_series[i]) * noise_level) if noise_level > 0 else 0
        return pd.Series((self.__time_series + noise)[:, 0])

    def __add_outliers(self):
        num_outliers = int(len(self.__time_series) * self.__config_manager.percentage_outliers)
        outlier_indices = np.random.choice(len(self.__time_series), num_outliers, replace=False)
        data_with_outliers = self.__time_series.copy()
        outliers = np.random.uniform(-1, 1, num_outliers)
        anomaly_mask = np.zeros(len(data_with_outliers), dtype=bool)
        if len(outliers) > 0:
            data_with_outliers[outlier_indices] = outliers
            anomaly_mask[outlier_indices] = True

        return data_with_outliers, anomaly_mask

    def __add_missing_values(self, percentage_missing=0.05):
        num_missing = int(len(self.__time_series) * percentage_missing)
        missing_indices = np.random.choice(len(self.__time_series), size=num_missing, replace=False)

        data_with_missing = self.__time_series.copy()
        data_with_missing[missing_indices] = np.nan

        return data_with_missing

    def generate_time_series(self):
        self.__generate_data_range()
        if self.__config_manager.data_type == "multiplicative":
            self.__time_series = (self.__add_daily_seasonality() * self.__add_weekly_seasonality() *
                                  self.__add_trend() * self.__add_cycles())
        else:
            self.__time_series = (self.__add_daily_seasonality() + self.__add_weekly_seasonality() +
                                  self.__add_trend() + self.__add_cycles())

        scaler = MinMaxScaler(feature_range=(-1, 1))
        self.__time_series = scaler.fit_transform(self.__time_series.values.reshape(-1, 1))
        self.__time_series = self.__add_noise()
        self.__time_series, self.__anomaly_mask = self.__add_outliers()
        self.__time_series = self.__add_missing_values()
        return self.__time_series, self.__date_range, self.__anomaly_mask












# def main():
#     # # Define simulation parameters
#     # start_date = datetime(2021, 7, 1)
#     # frequencies = ["1D", "10T", "30T", "1H", "6H", "8H"]
#     # daily_seasonality_options = ["no", "exist"]
#     # weekly_seasonality_options = ["exist", "no"]
#     # noise_levels = ["small"]  # , "large"]
#     # trend_levels = ["exist", "no"]
#     # cyclic_periods = ["exist", "no"]
#     # data_types = [""
#     #               "", "additive"]
#     # percentage_outliers_options = [0.05]  # , 0]
#     # data_sizes = [60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 365]
#     # meta_data = []
#     # counter = 0
#     # for freq in frequencies:
#     for daily_seasonality in daily_seasonality_options:
#         for weekly_seasonality in weekly_seasonality_options:
#             for noise_level in noise_levels:
#                 for trend in trend_levels:
#                     for cyclic_period in cyclic_periods:
#                         for percentage_outliers in percentage_outliers_options:
#                             for data_type in data_types:
#                                 for _ in range(16):
#                                     # for data_size in data_sizes:
#                                     data_size = random.choice(data_sizes)
#                                     freq = random.choice(frequencies)
#                                     counter += 1
#                                     file_name = f"TimeSeries_daily_{daily_seasonality}_weekly_{weekly_seasonality}_noise_{noise_level}_trend_{trend}_cycle_{cyclic_period}_outliers_{int(percentage_outliers * 100)}%_freq_{freq}_size_{data_size}Days.csv"
#                                     print(f"File '{file_name}' generated.")
#                                     # Generate time index
#                                     date_rng = generate_time_series(start_date, start_date + timedelta(days=data_size),
#                                                                     freq)
#                                     # Create components
#                                     daily_seasonal_component = add_daily_seasonality(date_rng, daily_seasonality,
#                                                                                      season_type=data_type)
#                                     weekly_seasonal_component = add_weekly_seasonality(date_rng, weekly_seasonality,
#                                                                                        season_type=data_type)
#                                     trend_component = add_trend(date_rng, trend, data_size=data_size,
#                                                                 data_type=data_type)
#                                     cyclic_period = "exist"
#                                     cyclic_component = add_cycles(date_rng, cyclic_period, season_type=data_type)
#
#                                     # Combine components and add missing values and outliers
#                                     if data_type == 'multiplicative':
#                                         data = daily_seasonal_component * weekly_seasonal_component * trend_component * cyclic_component
#                                     else:
#                                         data = daily_seasonal_component + weekly_seasonal_component + trend_component + cyclic_component
#                                     # Create a MinMaxScaler instance
#                                     scaler = MinMaxScaler(feature_range=(-1, 1))
#                                     data = scaler.fit_transform(data.values.reshape(-1, 1))
#                                     data = add_noise(data, noise_level)
#                                     data, anomaly = add_outliers(data, percentage_outliers)
#                                     data = add_missing_values(data, 0.05)
#
#                                     # Save the data to a CSV file
#                                     df = pd.DataFrame({'value': data, 'timestamp': date_rng, 'anomaly': anomaly})
#                                     df.to_csv('sample_datasets/' + str(counter) + '.csv', encoding='utf-8', index=False)
#
#                                     """
#                                     import matplotlib.pyplot as plt
#                                     plt.figure(figsize=(10, 6))
#                                     # Plot the time series data
#                                     plt.plot(df['timestamp'], df['value'], marker='o', linestyle='-', color='b',
#                                              label='Time Series Data')
#                                     # Add labels and title
#                                     plt.xlabel('Time')
#                                     plt.ylabel('Value')
#                                     plt.title('Time Series Plot')
#                                     plt.legend()
#                                     # Display the plot
#                                     plt.tight_layout()
#                                     plt.show()
#                                     break
#                                     """
#
#                                     meta_data.append({'id': str(counter) + '.csv',
#                                                       'data_type': data_type,
#                                                       'daily_seasonality': daily_seasonality,
#                                                       'weekly_seasonality': weekly_seasonality,
#                                                       'noise (high 30% - low 10%)': noise_level,
#                                                       'trend': trend,
#                                                       'cyclic_period (3 months)': cyclic_period,
#                                                       'data_size': data_size,
#                                                       'percentage_outliers': percentage_outliers,
#                                                       'percentage_missing': 0.05,
#                                                       'freq': freq})
#                                     # generate_csv(list(zip(date_rng, data)), file_name)
#
#     meta_data_df = pd.DataFrame.from_records(meta_data)
#     meta_data_df.to_csv('sample_datasets/meta_data.csv', encoding='utf-8', index=False)
#
#
# if __name__ == "__main__":
#     main()
