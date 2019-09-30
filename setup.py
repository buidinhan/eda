import os
from sys import version_info
from setuptools import setup, find_packages

from utils import __name__, __package__, __version__, __author__


# This is a Python 3 package only
if version_info.major != 3:
    print("This package will only work with Python 3. \n"
          "If you already have Python 3 installed try 'pip3 install eda'.")

__desc__ = "A collection of tools for Exploratory Data Analysis"
__author_email__ = "buidinhan@live.com"
__license__ = "BSD"
__url__ = "https://github.com/buidinhan/eda"
__requires__ = ["numpy>=1.17.0",
                "pandas>=0.25.0",
                "matplotlib>=3.1.1",
                "scipy>=1.3.1",
                "statsmodels>=0.10.1"
]
__extras_require__= {
        'notebooks':  ["jupyter"]
    }
__python_requires__ = ">=3"
__keywords__ = [
    "statistics",
    "EDA",
    "plotting",
]
__classifiers__ = [
    "Development Status :: Under Development",
    "Programming Language :: Python :: 3",
    "Topic :: Education",
    "Topic :: Data Analysis",
    "Topic :: Statistics",
    "Intended Audience :: Education",
    "Intended Audience :: Engineers",
    "Intended Audience :: Scientists",
    "License :: OSI Approved :: BSD License",
]
__long_description__ = """
To be written
"""

setup(
    name=__name__,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    description=__desc__,
    long_description=__long_description__,
    long_description_content_type='text/markdown',
    license=__license__,
    keywords=__keywords__,
    url=__url__,
    packages=find_packages(),
    classifiers=__classifiers__,
    install_requires=__requires__,
    extras_require = __extras_require__,
    python_requires=__python_requires__,
)
