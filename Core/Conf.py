import sys
import configparser

print(sys.argv)
if len(sys.argv) == 2:
    CONFIG_FILE = sys.argv[1]
else:
    CONFIG_FILE = "config.ini"


print("Logging to: ", CONFIG_FILE)
cfg = configparser.ConfigParser()
cfg.read(CONFIG_FILE)
