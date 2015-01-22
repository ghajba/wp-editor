This is a simple module meant to convert Markdown files to XML (XHTML).

The idea behind this is to make the base of an open-source offline WordPress.com blog entry editor -- and this is the part which converts the text written in a specific MarkDown language.
Because I write currently my books for LeanPub I align the main conversion to the LeanPub MarkDown.

However I aim to make this tool configurable: you can add your own mapping of MD -> XML in the configuration.py

Each configuration element has a starting and ending tag (although currently I am thinking about another way to solve this problem because XML files should be valid in the end...).

The main file is de ***mdxml.py***, you can start the application calling this file.

Currently I am under developing the first usable version, so stay tuned and do not complain about seeing test-code in the files :)
But feel free to create issues and change requests.