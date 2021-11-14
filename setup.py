# -*- coding: utf-8 -*-

import setuptools

setuptools.setup(
    name="unapi",
    version="0.4.0",
    author="Donatus Herre",
    author_email="donatus.herre@slub-dresden.de",
    description="unAPI client for retrieving data from K10plus",
    license=open("LICENSE").read(),
    url="https://github.com/herreio/unapi",
    packages=["unapi"],
    install_requires=["requests", "lxml"],
    entry_points={
      'console_scripts': ['unapi = unapi.__main__:main'],
    },
)
