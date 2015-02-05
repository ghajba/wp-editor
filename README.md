This is a simple module meant to convert Markdown files to XML (XHTML) and send them to WordPress.com via ~~REST~~ XML-RPC.

The idea behind this all is to make the base of an open-source offline WordPress.com blog entry editor.

The first part converts the text written in a specific MarkDown language to XML (or XHTML).
Because I write currently my books for LeanPub I align the main conversion to the LeanPub MarkDown.
However MD to XML conversion is a bit bothersome and there are many libraries which do this, I'll stick to ***Markdown*** a Python library for converting MarkDown files to X(HT)ML.

The *mdxml.conf* file contains custom configuration which is not available in markdown. For example the *[sourcecode]* block for WordPress. For this behavior I skip the markdown conversion for these lines of code.
Currently language and other options cannot be added for source codes.

If you have other configuration extensions (for example if you want to override the *~~~~~~~~* for sourcecodes, you can define it in your own conversion file and provide it as an argument to the application.

Each configuration element has a starting and ending tag (although currently I am thinking about another way to solve this problem because XML files should be valid in the end...).

One problem with Markdown is, that you have to parse the whole text if you have multi-line elements (for example lists). If you do not do this, you'll end up with a bunch of lists.

Feel free to create issues and change requests.

usage: wpedit.py [-h] [-c MDCONF] config_file post_file post_title

positional arguments:
  config_file           The full path of the configuration file storing the XML-RPC endpoint, username and password.
  post_file             The full path of the input file to send to WordPress.
  post_title            The title of the current blog post.

optional arguments:
  -h, --help            show this help message and exit
  -c MDCONF, --mdconf MDCONF
                        The full path of the md-to-xml conversion-extension file