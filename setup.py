# -*- coding: utf-8 -*-

import setuptools

setuptools.setup(
    name="unapi",
    version="0.1.1",
    author="Donatus Herre",
    author_email="donatus.herre@slub-dresden.de",
    description="unAPI Client",
    license=open("LICENSE").read(),
    url="https://github.com/herreio/unapi",
    packages=["unapi"],
    install_requires=["requests", "lxml"],
    entry_points={
      'console_scripts': ['unapi = unapi.__main__:main'],
    },
)
