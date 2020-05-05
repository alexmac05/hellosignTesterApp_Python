"""Setup script for realpython-reader"""

import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="hellosignTesterApp_Python",
    version="1.0.0",
    description="A console app for testing the python SDK",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/alexmac05/hellosignTesterApp_Python",
    author="Alex McFerron",
    author_email="alexmac2014@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["HiPyConsole"],
    include_package_data=True,
    install_requires=[
        "hellosign_sdk", "time", "requests", "yaml", "os", "json", "re"
    ],
    entry_points={"console_scripts": ["realpython=api_tester.__main__:main"]},
)

