try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'CSV to ABA Bulk Payment Website',
    'author': 'Michael Sproul',
    'url': 'https://sproul.xyz',
    'version': '0.1',
    'install_requires': ['aba', 'Flask', 'chardet', 'unidecode'],
    'packages': ['bulk_pay'],
    'name': 'bulk_pay'
}

setup(**config)
