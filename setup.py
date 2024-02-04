try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'CSV to ABA Bulk Payment Website',
    'author': 'Michael Sproul',
    'url': 'https://sproul.xyz',
    'version': '0.1',
    'install_requires': [
        'aba @ git+https://github.com/michaelsproul/python-aba.git@cbe3aa0d19a4642c9e75330b3f2624c9725d8898',
        'Flask',
        'chardet',
        'unidecode'
    ],
    'packages': ['bulk_pay'],
    'name': 'bulk_pay'
}

setup(**config)
