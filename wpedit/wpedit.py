__author__ = 'GHajba'

import argparse
import mdxml
from wordpress_xmlrpc import Client
from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc.methods import posts
from os.path import expanduser


def convert_file(filename):
    input_lines = mdxml.get_file_lines(filename)
    starter = 0
    title = None
    categories = None
    tags = None
    id = None
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
        elif line.startswith("[id]"):
            id = line[4:]
    content = mdxml.convert_lines(input_lines[starter:])
    return id, title, categories, tags, content


def send_to_wordpress(id, title, categories, tags, content, configuration):
    if len(content.strip()) == 0:
        return

    client = Client(configuration['endpoint'], configuration["username"], configuration['password'])

    if id:
        post = client.call(posts.GetPost(id))
        pass
    else:
        post = WordPressPost()
    post.content = content
    if title is not None:
        post.title = title
    if post.title is None:
        post.title = 'My post'
    post.terms_names = {
        'post_tag': tags,
        'category': categories,
    }

    if id:
        client.call(posts.EditPost(post.id, post))
    else:
        post.id = client.call(posts.NewPost(post))

    print "Blog post with id " + post.id + " was successfully sent to WordPress."


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--config",
                        help="The full path of the configuration file storing the XML-RPC endpoint, username and password. Per default the application looks at your home folder and searches for wpedit.conf")
    parser.add_argument("post_file", help="The full path of the input file to send to WordPress.")
    parser.add_argument("-m", "--mdconf", help="The full path of the md-to-xml conversion-extension file")
    args = parser.parse_args()

    configuration = {}
    config_file = expanduser("~")+'/wpedit.conf'
    if args.config:
        config_file = args.config
    execfile(config_file, configuration)

    mdxml.init()
    id, title, categories, tags, content = convert_file(args.post_file)
    send_to_wordpress(id, title, categories, tags, content, configuration)