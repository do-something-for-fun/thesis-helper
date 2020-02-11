import configparser
import os
import sys
config = configparser.ConfigParser()
config_path = os.path.join(os.getcwd(), "CONFIG.ini")
if sys.platform == "win32":
    config.read(config_path, encoding="utf-8")
else:
    config.read(config_path)