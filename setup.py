#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script for Healthcare Watch
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="healthcare-watch",
    version="1.0.0",
    author="Healthcare Watch",
    description="Automatisation de newsletters sanitaires avec Perplexity et Notion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/healthcare-watch",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "healthcare-watch=healthcare_watch.healthcare_watch:main",
        ],
    },
)
