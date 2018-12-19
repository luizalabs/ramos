import os

from setuptools import setup


def read(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    with open(path) as f:
        return f.read()


setup(
    name='ramos',
    version='1.1.0',
    description=(
        'Generic backend pool '
    ),
    long_description=read('README.rst'),
    author='LuizaLabs',
    author_email='pypi@luizalabs.com',
    url='https://github.com/luizalabs/ramos',
    keywords='django backends pool',
    packages=['ramos'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    extras_require={
        'django': ['Django>=1.8'],
        'simple_settings': ['simple_settings']
    }
)
