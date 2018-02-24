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
        'aba==0.2.1',
        'Flask',
        'chardet',
        'unidecode'
    ],
    'dependency_links': [
        'git+https://github.com/michaelsproul/python-aba.git@cbe3aa0d19a4642c9e75330b3f2624c9725d8898#egg=aba-0.2.1'
    ],
    'packages': ['bulk_pay'],
    'name': 'bulk_pay'
}

setup(**config)
