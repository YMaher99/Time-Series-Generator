# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
from yaml_configuration_manager import YAMLConfigurationManager
from time_series_simulator import TimeSeriesGenerator
from csv_data_producer import CSVDataProducer

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("INVALID ARGUMENTS! EXITING.")
        exit()

    if sys.argv[1] == "yaml":
        print("Configuring through \"config.yaml\" file")
        config_manager = YAMLConfigurationManager()
    else:
        print("Invalid first argument reverting to YAML config")
        config_manager = YAMLConfigurationManager()

    if sys.argv[2] == "csv":
        print("Producing data in .csv format")
        data_producer = CSVDataProducer()
    else:
        print("Invalid second argument reverting to CSV output")
        data_producer = CSVDataProducer()

    config_manager.load_config()
    config_manager.configure()
    generator = TimeSeriesGenerator(config_manager=config_manager)

    for series_num in range(config_manager.datasets_num):
        time_series, data_range, anomaly_mask = generator.generate_time_series()
        data_producer.produce_data(time_series, data_range, anomaly_mask, str(series_num), config_manager)

    data_producer.generate_metadata_file()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
