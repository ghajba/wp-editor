This is a simple module meant to convert Markdown files to XML (XHTML) and send them to WordPress.com via ~~REST~~ XML-RPC.

The idea behind this all is to make the base of an open-source offline WordPress.com blog entry editor.

The first part converts the text written in a specific MarkDown language to XML (or XHTML).
Because I write currently my books for LeanPub I align the main conversion to the LeanPub MarkDown.
However MD to XML conversion is a bit bothersome and there are many libraries which do this, I'll stick to ***Markdown*** a Python library for converting MarkDown files to X(HT)ML.

The *mdxml.conf* file contains custom configuration which is not available in markdown. For example the *[sourcecode]* block for WordPress. For this behavior I skip the markdown conversion for these lines of code.
Currently language and other options cannot be added for source codes.

If you have other configuration extensions (for example if you want to override the *~~~~~~~~* for source-codes, you can define it in your own conversion file and provide it as an argument to the application.

Each configuration element has a starting and ending tag (although currently I am thinking about another way to solve this problem because XML files should be valid in the end...).

One problem with Markdown is, that you have to parse the whole text if you have multi-line elements (for example lists). If you do not do this, you'll end up with a bunch of lists.

Feel free to create issues and change requests.

The application looks for the configuration file (containing wordpress endpoint, username, password) in your home folder under the name *wpedit.conf*. Optionally you can provide it per commandline argument.


## Usage
    usage: wpedit.py [-h] [-c CONFIG] [-m MDCONF] [-l] post_file

    positional arguments:
    post_file             The full path of the input file to send to WordPress.
                        If used with the '-l' option it is the full path of
                        the folder to save the drafts from WordPress.

    optional arguments:
    -h, --help            show this help message and exit
    -c CONFIG, --config CONFIG
                        The full path of the configuration file storing the
                        XML-RPC endpoint, username and password. Per default
                        the application looks at your home folder and searches
                        for wpedit.conf
    -m MDCONF, --mdconf MDCONF
                        The full path of the md-to-xml conversion-extension
                        file
    -l, --load            Loads all draft posts into the folder where the
                        'post_file' resides. The 'post_file' will not be sent
                        to WordPress.

## File structure
The markdown file is parsed and you can place special lines at the beginning of the text. These special lines have to start with **[** (square bracket). Once the parser encounters a line which does not start with **[** the resulting text is treated as the content of the article.

### Accepted special lines
[id] 1001 -- the ID of the blog post, if you create a new post, you do not have to provide an ID, **Note** if you provide an ID, the application attempts to edit the post with this ID.

[title] Some title -- you can specify the post's title here, in the example "Some title" will be the title of the article. If you do not provide a title and the post does not have a title, the title will be set to "My post".

[categories] Category 1, Category 2 -- a comma separated list of categories for your post. Optional, if not provided there will be no categories set.

[tags] tag 1, tag 2, tag 3 -- a comma separated list for your post. Optional, if not provided there will be no tags set.

## Extra markdown
Currently these extra markdonw symbols are configured for wpedit:

~~~~~~~~ (tilde symbol 8 times) Surrounds code blocks which will be presented as *[sourcecode]* in WordPess. Source code blocks can be enriched with key-value pairs to represent parameters of **[sourcecode]** blocks.
~~~~~~~~{'language':'python', 'title':'Python source code example'} This line will be converted to: **[sourcecode language="python" title="Python source code example"]**

-------- (dash 8 times) Adds a read more tag to your article which will be presented as *<!--more-->* in WordPress.

@@@ (at symbol 3 times) Makes the surrounded text preformatted which will be presented as *&lt;pre&gt;* in WordPRess.

## Changes

### Version 0.3.1

 * force parameter added to update every draft even if it was changed locally later than on the server
 * number of fetched drafts is defineable from the command line as an argument, the default stays as 25

### Version 0.3

 *  Starting with version 0.3 you can download your draft posts (currently the latest 25 in reverse-chronological order (based on their publish date)) (I plan to add an option to configure the maximum number to load)
 * **tags** and **categories** are loaded with your posts
 * If you altered the draft locally it will not get overwritten (I plan to add a command line argument to force updates)
 * downloading of source code and "more"-tags work properly
