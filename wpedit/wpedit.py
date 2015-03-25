__author__ = 'GHajba'

import argparse
import mdxml
from wordpress_xmlrpc import Client
from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc.methods import posts, taxonomies
from os.path import expanduser
from xml2md import xml2md
from file_utils import write_line_at_beginning, read_file_lines, get_folder_name, write_file, read_file_as_one, \
    user_edited_later

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


def load_drafts(configuration, draft_count):
    """Loads all draft posts from WordPress"""
    client = get_client(configuration)
    draft_posts = client.call(posts.GetPosts({'post_status': 'draft', 'number': str(draft_count)}))
    return draft_posts


def get_draft_parameters(draft):
    """
    Loads all parameters from the draft
    :param draft: the draft which is loaded
    :return: the id, title, categories, tags, content and modified date of the draft
    """
    categories = []
    tags = []
    terms = draft.terms
    if terms:
        for term in terms:
            if "category" == term.taxonomy:
                categories.append(term.name)
            if "post_tag" == term.taxonomy:
                tags.append(term.name)

    return draft.id, draft.title, categories, tags, draft.content, draft.date_modified


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
    """
    Loads already defined and used tags from WordPress.
    :param configuration:  the configuration to enable a connection with WordPress.
    :return: the list of defined tags
    """
    client = get_client(configuration)
    return client.call(taxonomies.GetTerms('post_tag'))


def load_categories(configuration):
    """
    Loads already defined categories from WordPress.
    :param configuration: the configuration to enable a connection with WordPress.
    :return: the list of defined categories
    """
    client = get_client(configuration)
    return client.call(taxonomies.GetTerms('category'))


def export_drafts(configuration, target_folder, draft_count, update):
    drafts = load_drafts(configuration, draft_count)
    for draft in drafts:
        id, title, categories, tags, content, modified = get_draft_parameters(draft)
        filename = create_filename(title)
        if update or not user_edited_later(target_folder, filename, modified):
            markdown_content = convert_to_markdown(id, title, categories, tags, content)
            write_file(target_folder, filename, markdown_content)
        else:
            print(
                "The file {0} has beed modified locally later than at the blog, it won't be overwritten.".format(
                    filename))


def verify_categories(categories, defined_categories):
    """
    Verifies each category of the post if it is already defined or not. Categories have to be defined.
    :param categories: the categories of the post
    :param defined_categories: the defined categories in the blog
    :return: True if the categories are empty or are already defined, False if the category is unknown
    """
    for category in categories:
        if category not in defined_categories:
            print(
            'Category "{0}" is not defined for this blog. Please define it through the WordPress User Interface.'.format(
                category))
            return False
    return True


def verify_tags(tags, defined_tags):
    """
    Verifies each tag of the post if it is already defined or not. Tags do not have to be defined per default.
    :param tags: the tags of the post
    :param defined_tags: the already defined and used tags of the blog
    :return: True if the tags are empty or are already defined, False if the tag is unknown
    """
    for tag in tags:
        if tag not in defined_tags:
            print('Tag "{0}" is not defined for this blog.'.format(category))
            return False
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config",
                        help="The full path of the configuration file storing the XML-RPC endpoint, username and password. Per default the application looks at your home folder and searches for wpedit.conf")
    parser.add_argument("post_file",
                        help="The full path of the input file to send to WordPress.  If used with the '-l' option it is the full path of the folder to save the drafts from WordPress.")
    parser.add_argument("-m", "--mdconf", help="The full path of the md-to-xml conversion-extension file")
    parser.add_argument("-l", "--load",
                        help="Loads all draft posts into the folder where the 'post_file' resides. The 'post_file' will not be sent to WordPress.",
                        action="store_true")
    parser.add_argument('-n', '--number',
                        help="The number of draft posts to load. Works only in combination with the '-l' argument.",
                        default=25)
    parser.add_argument('-U', '--update',
                        help="Forces update of every draft loaded, the check for local modifications is disabled. Works only in combination with the '-l' argument.",
                        action="store_true")
    parser.add_argument('-V', '--verify',
                        help="Enables verification of tags. If the blog post contains tags which are not defined, the article will not be sent to WordPress.",
                        action='store_true')
    args = parser.parse_args()

    configuration = {}
    config_file = expanduser("~") + '/wpedit.conf'
    if args.config:
        config_file = args.config
    execfile(config_file, configuration)

    mdxml.init()

    if args.load:
        draft_count = args.number
        target_folder = get_folder_name(args.post_file)
        export_drafts(configuration, target_folder, draft_count, args.update)
    else:
        defined_tags = load_tags(configuration)
        defined_categories = load_categories(configuration)
        id, title, categories, tags, content = convert_file(args.post_file)
        if not verify_categories(categories, defined_categories):
            print("Category-verification failed for {0}, post is not sent to WordPress.".format(args.post_file))
            exit()
        if args.verify and not verify_tags(tags, defined_tags):
            print("Tag-verification failed for {0}, post is not sent to WordPress.".format(args.post_file))
            exit()
        post_id = send_to_wordpress(id, title, categories, tags, content, configuration)
        if not id and post_id:
            add_post_id_to_original(args.post_file, post_id)