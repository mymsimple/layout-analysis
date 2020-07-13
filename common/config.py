import configparser

class Config:

    def __init__(self, conf_file = 'recognizer.conf'):

        cf = configparser.ConfigParser()
        cf.read(conf_file)

        self.is_debug = cf.getboolean("common", "debug")