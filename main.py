# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
from yaml_configuration_manager import YAMLConfigurationManager
from time_series_simulator import TimeSeriesGenerator

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
        pass

    config_manager.load_config()

    generator = TimeSeriesGenerator(config_manager=config_manager)

    for _ in range(config_manager.datasets_num):
        generator.generate_time_series()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
