__author__ = 'GHajba'
from distutils.core import setup

setup(
    name='wpedit',
    packages=['wpedit'],
    version='0.3.4',
    description='Sends (offline) articles written in MarkDown to WordPress via the XML-RPC API, and loads the draft articles from WordPress to the local machine.',
    author='Gabor Laszlo Hajba',
    author_email='gabor.hajba@gmail.com',
    url='https://github.com/ghajba/wp-editor',
    download_url='https://github.com/ghajba/wp-editor/tarball/0.3.4',
    keywords=['wordpress', 'offline', 'edit', 'markdown', 'xml', 'editor'],
    classifiers=['Programming Language :: Python',
                 'License :: OSI Approved :: MIT License', ],
    requires=[('Markdown'), ("python.wordpress.xmlrpc")],
)