# ## This is the main module of the markdown to XML converter python module
# ## (c) Gabor Laszlo Hajba 2015
"""
The main idea behind this app is to take a markdown file, parse it line-by-line and create an XML output
along the defined rules of the conversion.
"""

from configuration import Configuration
import re


def convert_line(line):
    """
    This method converts a line of markdown to specified XML. Currently hard-coded.

    First it looks if the line has some propeties at the beginning and changes the structure according to this.
    Than it goes through the line and parses known in-line markdowns and changes them to XML.

    :param line: the line to convert
    :return: the line formatted as XML
    """
    xmlline = line.strip()
    if len(xmlline) == 0:
        return xmlline

    for marker in sorted(configuration.configuration, key=len, reverse=True):
        config_element = configuration.get_configuration(marker)
        xmlline = xmlline.replace(marker, config_element.begin)
        if xmlline.count(config_element.begin) % 2 != 0:
            xmlline += config_element.begin
        marker_occurrences = [(a.start(), a.end()) for a in list(re.finditer(re.escape(config_element.begin), xmlline))]
        for i in marker_occurrences[1::2]:
            xmlline = xmlline[:i[0]] + config_element.end + xmlline[i[1]:]
    if not xmlline.startswith('<'):
        xmlline = configuration.get_configuration('default').begin + xmlline + configuration.get_configuration(
            'default').end

    return xmlline


def read_mdfile(filename):
    input_file = open(filename)
    input_lines = input_file.readlines()
    input_file.close()

    output_file = open(filename.rsplit('.', 1)[0]+".xml", 'w')
    for line in input_lines:
        if len(line.strip()) == 0:
            continue
        output_file.write(convert_line(line))
        output_file.write("\n")
        output_file.flush()
    output_file.close()


configuration = Configuration()
configuration.load_configuration()

read_mdfile("testfile.md")