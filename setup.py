# _*_ coding: utf-8 _*_
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kobopost',
    version='1.0.1',

    description="""Package to post-process surveys that were created with kobotoolbox.
    Currently this provides one command line script: mark_skipped.
    """,
    long_description=long_description,
    url='https://github.com/eawag-rdm/kobo-post',
    author='Harald von Waldow @ Eawag',
    author_email='harald.vonwaldow@eawag.ch',
    # Choose your license
    license='GNU AFFERO GENERAL PUBLIC LICENSE',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU AFFERO GENERAL PUBLIC LICENSE',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='kobotoolbox csv post-processing',
    packages=['kobopost'],
    install_requires=['docopt', 'pandas', 'xlrd', 'ply', 'openpyxl'],
    entry_points={
        'console_scripts': ['mark_skipped=kobopost.mark_skipped:main']
    },
)
