"""
This file loads and maintains the configuration of the application
"""


class ConfigurationElement:
    def __init__(self, marker, begin, end=None, multiline=False):
        self.__marker = marker
        self.__begin = begin
        self.__end = end
        self.__multiline = multiline

    def __str__(self):
        return self.__marker + " --> " + self.__begin + " " + self.__end + ( " multi-line" if self.__multiline else "")

    def get_begin(self):
        return self.__begin

    def get_marker(self):
        return self.__marker

    def get_end(self):
        return self.__end

    def is_multiline(self):
        return self.__multiline


#TODO add possibility to have multiple categories of configurations like starter, complex and multiline
class Configuration:
    def __init__(self):
        self.__multiline_added = False
        self.__multiline_marker = None
        self.__configuration = {}
        self.__markers = []
        self.__default = None

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
            multiline = False
            if len(params) >= 3:
                end = params[2]
            else:
                end = None
        # TODO add variable configuration for fourth parameter, for example M for multiline, S for starter, C for complex
            if len(params) > 3:
                multiline = True
            if "default" == marker:
                self.__default = ConfigurationElement(marker, begin, end)
            else:
                self.__configuration[marker] = ConfigurationElement(marker, begin, end, multiline)

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

    def get_default(self):
        return self.__default

    def print_configuration(self):
        for key in self.__configuration:
            print self.__configuration[key]

    def is_multiline(self):
        return self.__multiline_added

    def alter_multiline(self, actual_marker):
        if not self.__configuration[actual_marker].is_multiline():
            return False
        if self.__multiline_added and not self.__multiline_marker == actual_marker:
            return False
        if self.__multiline_added:
            self.__multiline_marker = None
        else:
            self.__multiline_marker = actual_marker
        self.__multiline_added = not self.__multiline_added
        return True