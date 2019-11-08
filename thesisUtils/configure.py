import configparser
import os
config = configparser.ConfigParser()
config_path = os.path.join(os.getcwd(), "CONFIG.ini")
config.read(config_path, encoding="utf-8")