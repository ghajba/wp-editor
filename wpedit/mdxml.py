# ## This is the main module of the markdown to XML converter python module
# ## (c) Gabor Laszlo Hajba 2015
"""
The main idea behind this app is to take a markdown file, parse it line-by-line and create an XML output
along the defined rules of the conversion.
"""

import re

from markdown import markdown

from configuration import Configuration
from file_utils import read_file_lines

configuration = Configuration()


def convert_line(line):
    """
    This method converts a line of markdown to specified XML. Currently hard-coded.

    The algorithm is really a wood-cutter: replace all occurrences of the markers and correct the closing tags.

    If one tag is not closed, it gets closed at the end of the line -- so currently there are no multi-line tags
    available.

    :param line: the line to convert
    :return: the line formatted as XML
    """
    global configuration
    xmlline = line

    for marker in configuration.get_normal():
        config_element = configuration.get_configuration(marker)
        marker_count = line.count(marker)

        if marker_count == 1 and configuration.alter_multiline(marker):
            xmlline = config_element.get_begin() if configuration.is_multiline() else config_element.get_end()
            xmlline += "\n"
            placeholder = ""
            if len(line.strip()[len(marker):]) > 0:
                conf = eval(line.strip()[len(marker):])
                for key in conf:
                    placeholder += " " + key + "=\"" + conf[key] + "\""
            return xmlline.format(placeholder), True

        if configuration.is_multiline():
            return line, True

        if marker_count == 0:
            continue
        xmlline = line.strip().replace(marker, config_element.get_begin())
        if xmlline.count(config_element.get_begin()) % 2 != 0:
            xmlline += config_element.get_begin()
            marker_occurrences = find_marker_occurrences(xmlline, config_element.get_begin())
            for i in marker_occurrences[1::2]:
                xmlline = xmlline[:i[0]] \
                          + (config_element.get_end() if config_element.get_end() is not None else "") + xmlline[i[1]:]

    return xmlline, False


def convert_lines(lines):
    final_text = ""
    temp = ""
    for line in lines:
        result, final = convert_line(line)
        if final:
            if len(temp) != 0:
                final_text += markdown(temp) + "\n"
                temp = ""
            final_text += result
        else:
            temp += result

    if len(temp) != 0:
        final_text += markdown(temp) + "\n"
    return final_text


def find_marker_occurrences(xmlline, marker):
    return [(a.start(), a.end()) for a in list(re.finditer(re.escape(marker), xmlline))]


def convert_md_file(filename):
    return convert_lines(read_file_lines(filename))


def write_xml_file(filename, content):
    output_file = codecs.open(filename, "w",
                              encoding="utf-8",
                              errors="xmlcharrefreplace")
    output_file.write(content)
    output_file.flush()
    output_file.close()


def init():
    global configuration
    configuration.load_configuration()


if __name__ == "__main__":
    init()
    import os

    write_xml_file(os.path.join(os.path.dirname(__file__), "../testfile.xml"),
                   convert_md_file(os.path.join(os.path.dirname(__file__), "../testfile.md")))