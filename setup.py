from distutils.core import setup

setup (
    name = 'django-feedstream',
    packages = [
        'feedstream',
        'feedstream.management',
        'feedstream.management.commands'
    ],
    version = '0.1',
    description = 'Yet Another Django lifestream thingy',
    author = 'Simon Willison',
    author_email = 'simon@simonwillison.net',
    url = 'http://github.com/simonw/django-feedstream',
)

