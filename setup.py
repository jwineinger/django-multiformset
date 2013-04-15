import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'django-multiformset',
    version = '1.0',
    packages = ['multiformset', 'multiformset.templatetags'],
    include_package_data = True,
    #license = 'BSD License',
    description = 'A Django app to use multiple formsets on the same page.',
    long_description = README,
    url = 'https://github.com/jwineinger/django-multiformset',
    author = 'Jay Wineinger',
    author_email = 'jay.wineinger@gmail.com',
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        #'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
