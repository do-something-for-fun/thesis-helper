import configparser
import os
config = configparser.ConfigParser()
config_path = os.path.join(os.getcwd(), "CONFIG.ini")
# config_path = 'G:\\thesis-helper\\CONFIG.ini'
config.read(config_path, encoding="GBK")