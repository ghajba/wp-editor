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

    The algorithm is really a wood-cutter: replace all occurrences of the markers and correct the closing tags.

    If one tag is not closed, it gets closed at the end of the line -- so currently there are no multi-line tags
    available.

    :param line: the line to convert
    :return: the line formatted as XML
    """
    xmlline = line.strip()
    if len(xmlline) == 0:
        return xmlline

    for marker in configuration.get_configuration():
        config_element = configuration.get_configuration(marker)
        marker_count = xmlline.count(marker)
        if marker_count == 0:
            continue
        if marker_count == 1 and configuration.alter_multiline(marker):
            xmlline = xmlline.replace(marker, (
                config_element.get_begin() if configuration.is_multiline() else config_element.get_end()))
            return xmlline

        if configuration.is_multiline():
            return xmlline

        xmlline = xmlline.replace(marker, config_element.get_begin())
        if configuration.alter_multiline(marker):
            return xmlline
        if xmlline.count(config_element.get_begin()) % 2 != 0:
            xmlline += config_element.get_begin()
        marker_occurrences = [(a.start(), a.end()) for a in
                              list(re.finditer(re.escape(config_element.get_begin()), xmlline))]
        for i in marker_occurrences[1::2]:
            xmlline = xmlline[:i[0]] + config_element.get_end() + xmlline[i[1]:]
    if not xmlline.startswith('<') and not configuration.is_multiline():
        default_element = configuration.get_default()
        xmlline = default_element.get_begin() + xmlline + default_element.get_end()

    return xmlline


def read_mdfile(filename):
    input_file = open(filename)
    input_lines = input_file.readlines()
    input_file.close()

    output_file = open(filename.rsplit('.', 1)[0] + ".xml", 'w')
    for line in input_lines:
        if len(line.strip()) == 0:
            continue
        output_file.write(convert_line(line))
        output_file.write("\n")
        output_file.flush()
    output_file.close()


configuration = Configuration()
configuration.load_configuration()

# configuration.print_configuration()

read_mdfile("testfile.md")
read_mdfile("first_test_post.md")