"""
This file loads and maintains the configuration of the application
"""


class Configuration:
    def __init__(self, marker, begin, end=None):
        self.marker = marker
        self.begin = begin
        self.end = end

    def __str__(self):
        return self.marker + " --> " + self.begin + " " +  self.end

sourcecode_added = False
configuration = {}


def load_configuration(config_file="mdxml.conf"):
    config = open(config_file)
    config_lines = config.readlines()
    for line in config_lines:
        if len(line.strip()) == 0:
            continue
        params = line.split()
        marker = params[0]
        begin = params[1]
        if len(params) >= 3:
            end =params[2]
        else:
            end =None
        configuration[marker] = (Configuration(marker, begin, end))

def print_configuration():
    for key in configuration:
        print configuration[key]
