__author__ = 'GHajba'

from codecs import open
from os.path import dirname, abspath, isfile, getmtime
from time import ctime
from datetime import datetime


def write_line_at_beginning(filename, line):
    input_file = open(filename, mode="r+", encoding="utf-8")
    content = input_file.read()
    input_file.seek(0, 0)
    input_file.write(line + "\n" + content)
    input_file.close()


def read_file_as_one(filename):
    input_file = open(filename, mode="r", encoding="utf-8")
    file_content = input_file.read()
    input_file.close()
    return file_content


def read_file_lines(filename):
    input_file = open(filename, mode="r", encoding="utf-8")
    input_lines = input_file.readlines()
    input_file.close()
    return input_lines


def get_folder_name(filename):
    filepath = abspath(filename)
    if isfile(filepath):
        return dirname(filepath)
    return filepath


def write_file(folder, filename, content):
    output_file = open(folder + "/" + filename, mode="w", encoding="utf-8")
    output_file.writelines(content)
    output_file.close()


def user_edited_later(folder, filename, modified):
    folder_filename = folder + '/' + filename
    if not isfile(folder_filename):
        return False
    return modified < datetime.strptime(ctime(getmtime(folder_filename)), "%a %b %d %H:%M:%S %Y")