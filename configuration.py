"""
This file loads and maintains the configuration of the application
"""


class ConfigurationElement:
    def __init__(self, marker, begin, end=None):
        self.marker = marker
        self.begin = begin
        self.end = end

    def __str__(self):
        return self.marker + " --> " + self.begin + " " + self.end


class Configuration:
    def __init__(self):
        self.sourcecode_added = False
        self.configuration = {}
        self.markers = []

    def load_configuration(self, config_file="mdxml.conf"):
        """
        :param config_file: the file where the configuration is stored
        """
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
            self.configuration[marker] = (ConfigurationElement(marker, begin, end))

    def get_configuration(self, marker):
        """
        :param marker: the marker to look up in the configuration
        :return: the loaded Configuration element or None if the marker is not present
        """
        if marker in self.configuration:
            return self.configuration[marker]
        return None

    def get_markers(self):
        for marker in self.configuration:
            pass
        pass

    def print_configuration(self):
        for key in self.configuration:
            print self.configuration[key]
