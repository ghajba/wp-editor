"""
This file loads and maintains the configuration of the application
"""


class ConfigurationElement:
    def __init__(self, marker, begin, end=None):
        self.__marker = marker
        self.__begin = begin
        self.__end = end

    def __str__(self):
        return self.__marker + " --> " + self.__begin + " " + self.__end

    def get_begin(self):
        return self.__begin

    def get_marker(self):
        return self.__marker

    def get_end(self):
        return self.__end


class Configuration:
    def __init__(self):
        self.__sourcecode_added = False
        self.__configuration = {}
        self.__markers = []

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
                end = params[2]
            else:
                end = None
            self.__configuration[marker] = (ConfigurationElement(marker, begin, end))

    def get_configuration(self, marker=None):
        """
        :param marker: the marker to look up in the configuration
        :return: the loaded Configuration element or None if the marker is not present
        """
        if marker is None:
            return sorted(self.__configuration, key=len, reverse=True)
        if marker in self.__configuration:
            return self.__configuration[marker]
        return None

    def get_markers(self):
        for marker in self.__configuration:
            pass
        pass

    def print_configuration(self):
        for key in self.__configuration:
            print self.__configuration[key]
