__author__ = 'GHajba'

import argparse
import mdxml
from wordpress_xmlrpc import Client
from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc.methods import posts, taxonomies
from os.path import expanduser
from xml2md import xml2md
from file_utils import write_line_at_beginning, read_file_lines, get_folder_name, write_file, read_file_as_one

import inspect

def convert_file(filename):
    input_lines = read_file_lines(filename)
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


def get_client(configuration):
    client = Client(configuration['endpoint'], configuration["username"], configuration['password'])
    return client


def send_to_wordpress(id, title, categories, tags, content, configuration):
    if len(content.strip()) == 0:
        return

    client = get_client(configuration)

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
    return post.id


def add_post_id_to_original(filename, id):
    write_line_at_beginning(filename, "[id] " + id)


def create_filename(title):
    """Converts the title of the post to a filename."""
    filename = title.replace(" ", "_") + ".md"
    return filename


def load_drafts(configuration):
    """Loads all draft posts from WordPress"""
    client = get_client(configuration)
    draft_posts = client.call(posts.GetPosts({'post_status': 'draft'}))
    return draft_posts


def get_draft_parameters(draft):
    categories = []
    tags = []
    terms = draft.terms
    if terms:
        for term in terms:
            if "categoriy" == term.taxonomy:
                categories.append(term.id)
            if "post_tag" == term.taxonomy:
                tags.append(term.id)
    return draft.id, draft.title, categories, tags, draft.content


def convert_to_markdown(id, title, categories, tags, content):
    result = "[id] " + id + "\n"
    result += "[title] " + title + "\n"
    if categories:
        result += "[categories] " + ','.join(categories) + "\n"
    if tags:
        result += "[tags] " + ','.join(tags) + "\n"
    result += "\n"
    result += xml2md(content)
    return result

def load_tags(configuration):
    client = get_client(configuration)
    tags = client.call(taxonomies.GetTerms('post_tag'))
    #print tags

def load_categories(configuration):
    client = get_client(configuration)
    categories = client.call(taxonomies.GetTerms('category'))
    #print categories

def export_drafts(configuration, target_folder):
    drafts = load_drafts(configuration)
    for draft in drafts:
        id, title, categories, tags, content = get_draft_parameters(draft)
        filename = create_filename(title)
        markdown_content = convert_to_markdown(id, title, categories, tags, content)
        write_file(target_folder, filename, markdown_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config",
                        help="The full path of the configuration file storing the XML-RPC endpoint, username and password. Per default the application looks at your home folder and searches for wpedit.conf")
    parser.add_argument("post_file", help="The full path of the input file to send to WordPress.")
    parser.add_argument("-m", "--mdconf", help="The full path of the md-to-xml conversion-extension file")
    parser.add_argument("-l", "--load",
                        help="Loads all draft posts into the folder where the 'post_file' resides. The 'post_file' will not be sent to WordPress.", action="store_true")
    args = parser.parse_args()

    configuration = {}
    config_file = expanduser("~") + '/wpedit.conf'
    if args.config:
        config_file = args.config
    execfile(config_file, configuration)

    mdxml.init()
    load_tags(configuration)
    load_categories(configuration)
    if args.load:
        import os
        content = read_file_as_one(os.path.join(os.path.dirname(__file__), "../testfile.xml"))
        target_folder = get_folder_name(args.post_file)
        export_drafts(configuration, target_folder)
    else:
        id, title, categories, tags, content = convert_file(args.post_file)
        post_id = send_to_wordpress(id, title, categories, tags, content, configuration)
        if not id and post_id:
            add_post_id_to_original(args.post_file, post_id)