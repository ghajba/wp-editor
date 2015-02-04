This is a simple module meant to convert Markdown files to XML (XHTML) and send them to WordPress.com via ~~REST~~ XML-RPC.

The idea behind this all is to make the base of an open-source offline WordPress.com blog entry editor.

The first part converts the text written in a specific MarkDown language to XML (or XHTML).
Because I write currently my books for LeanPub I align the main conversion to the LeanPub MarkDown.
However MD to XML conversion is a bit bothersome and there are many libraries which do this, I'll stick to ***markdown*** a Python library for converting MarkDown files to X(HT)ML.

In the *mdxml.conf* file you can add your own configuration which is not available in markdown. For example the *[sourcecode]* block for WordPress. For this behavior I skip the markdown conversion for these lines of code.
Currently language and other options cannot be added for source codes.

Each configuration element has a starting and ending tag (although currently I am thinking about another way to solve this problem because XML files should be valid in the end...).

One problem with markdown is, that you have to parse the whole text if you have multi-line elements (for example lists). If you do not do this, you'll end up with a bunch of lists.

The main file is currently the ***mdxml.py***, you can start the application calling this file without any parameters.
This will change as I get on with development.

Currently I am under developing the first usable version, so stay tuned and do not complain about seeing test-code in the files :)
But feel free to create issues and change requests.