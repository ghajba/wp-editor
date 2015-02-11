__author__ = 'GHajba'

import argparse
import mdxml
from wordpress_xmlrpc import Client
from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc.methods import posts


def convert_file(filename):
    input_lines = mdxml.get_file_lines(filename)
    starter = 0
    title = None
    categories = None
    tags = None
    for line in input_lines:
        if not line.startswith("["):
            break
        starter += 1
        if line.startswith("[title]"):
            title = line[7:]
        elif line.startswith("[categories]"):
            categories = line[12:].split(",")
        elif line.startswith("[tags]"):
            tags = line[6:].split(",")
    content = mdxml.convert_lines(input_lines[starter:])
    return title, categories, tags, content


def send_to_wordpress(title, categories, tags, content, configuration):
    if len(content.strip()) == 0:
        return

    post = WordPressPost()
    post.content = content
    post.title = 'My post'
    if title is not None:
        post.title = title
    post.terms_names = {
        'post_tag': tags,
        'category': categories,
    }
    client = Client(configuration['endpoint'], configuration["username"], configuration['password'])
    post.id = client.call(posts.NewPost(post))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file",
                        help="The full path of the configuration file storing the XML-RPC endpoint, username and password.")
    parser.add_argument("post_file", help="The full path of the input file to send to WordPress.")
    parser.add_argument("-c", "--mdconf", help="The full path of the md-to-xml conversion-extension file")
    args = parser.parse_args()

    configuration = {}
    execfile(args.config_file, configuration)

    mdxml.init()
    title, categories, tags, content = convert_file(args.post_file)
    send_to_wordpress(title, categories, tags, content, configuration)