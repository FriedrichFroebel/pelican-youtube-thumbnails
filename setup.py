#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from pathlib import Path


ROOT_DIRECTORY = Path(__file__).parent.resolve()


setup(
    name="pelican-youtube-thumbnails",
    description="Pelican plugin to link to YouTube videos by their thumbnail",
    version="0.3.2",
    license="AGPL-3.0",
    long_description=(ROOT_DIRECTORY / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="FriedrichFröbel",
    url="https://github.com/FriedrichFroebel/pelican-youtube-thumbnails/",
    packages=find_packages(
        where=".",
        include=[
            "pelican.plugins.youtube_thumbnails",
            "pelican.plugins.youtube_thumbnails.*",
        ],
    ),
    include_package_data=True,
    python_requires=">=3.7, <4",
    install_requires=[
        "beautifulsoup4",
        "lxml",
        "Pillow",
        "requests",
        'importlib-resources; python_version<"3.9"',
    ],
    extras_require={
        "dev": [
            "flake8",
            "pep8-naming",
            "pelican>=4.5",
            "Markdown",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Framework :: Pelican",
        "Framework :: Pelican :: Plugins",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=["pelican", "plugin", "youtube"],
)
