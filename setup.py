#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Dec 24, 2012

@author: daniel
"""

from setuptools import find_packages, setup

setup(
    name="ghostdev.pyform",
    version="1.0.5",
    package_dir={"": "src"},
    packages=find_packages("src"),
)

if __name__ == "__main__":
    pass
