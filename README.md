This is a simple module meant to convert Markdown files to XML (XHTML) and send them to WordPress.com via REST.

The idea behind this all is to make the base of an open-source offline WordPress.com blog entry editor.

The first part converts the text written in a specific MarkDown language to XML (or XHTML).
Because I write currently my books for LeanPub I align the main conversion to the LeanPub MarkDown.

However I aim to make this tool configurable: you can add your own mapping of MD -> XML in the *configuration.py*

Each configuration element has a starting and ending tag (although currently I am thinking about another way to solve this problem because XML files should be valid in the end...).

The main file is currently the ***mdxml.py***, you can start the application calling this file without any parameters.
This will change as I get on with development.

Currently I am under developing the first usable version, so stay tuned and do not complain about seeing test-code in the files :)
But feel free to create issues and change requests.