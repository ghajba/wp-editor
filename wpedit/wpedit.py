__author__ = 'GHajba'

import argparse


def usage():
    print "wpedit -input file"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file", help="The full path of the configuration file storing the XML-RPC endpoint, username and password.")
    parser.add_argument("post_file", help="The full path of the input file to send to WordPress.")
    parser.add_argument("post_title", help="The title of the current blog post.") ## move this to the input file inkl. tags, categories
    parser.add_argument("-c", "--mdconf", help="The full path of the md-to-xml conversion-extension file")
    args = parser.parse_args()

    configuration = {}
    execfile(args.config_file, configuration)

    print configuration['username']
    # convert input file to XML
    # send XML content to WordPress
    pass