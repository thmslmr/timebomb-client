from timebomb import __VERSION__, __DESCRIPTION__
from setuptools import setup, find_namespace_packages

with open("./README.md", encoding="utf-8") as f:
    LONG_DESC = "\n" + f.read()

CLASSIFIERS = [
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Topic :: Games/Entertainment",
    "Environment :: Console",
    "Intended Audience :: End Users/Desktop",
]


setup(
    name="timebomb-client",
    version=__VERSION__,
    description=__DESCRIPTION__,
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    author="Thomas Le Meur",
    author_email="thmslmr@gmail.com",
    url="https://github.com/thmslmr/timebomb-client",
    license="MIT",
    classifiers=CLASSIFIERS,
    python_requires=">=3.7.0",
    install_requires=["npyscreen", "python-socketio[client]"],
    extras_require={},
    packages=find_namespace_packages(),
    entry_points={"console_scripts": ["timebomb=timebomb.cli:main"]},
    include_package_data=True,
)
