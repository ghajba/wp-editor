__author__ = 'GHajba'
from distutils.core import setup

setup(
    name='wpedit',
    packages=['wpedit'],
    version='0.1',
    description='Sends (offline) articles written in MarkDown to WordPress via the XML-RPC API',
    author='Gabor Laszlo Hajba',
    author_email='gabor.hajba@gmail.com',
    url='https://github.com/ghajba/wp-edit',
    download_url='https://github.com/ghajba/wp-edit/tarball/0.1',
    keywords=['wordpress', 'offline', 'edit', 'markdown', 'xml'],
    classifiers=[],
    requires=[('Markdown'),("python.wordpress.xmlrpc")],
)