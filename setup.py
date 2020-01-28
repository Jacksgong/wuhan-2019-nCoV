#!/usr/bin/python -u

"""
Copyright (C) 2020 Jacksgong.com.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from setuptools import setup, find_packages

setup(
    name='Wuhan2019nCoV',
    version='0.1.4',
    packages=find_packages(exclude=['ats']),

    install_requires=['requests'],

    # metadata for upload to PyPI
    author="Jacksgong",
    author_email="igzhenjie@gmail.com",
    description="This tool is used for crawl Wuhan 2019nCov Info",
    long_description='This tool is used for crawl Wuhan 2019nCov Info',
    license="Apache2",
    keywords="crawler, wuhan, 2019nCov",
    url="https://github.com/jacksgong/wuhan-2019ncov",

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': [
            'whncov=wuhanncov:main'
        ]
    }

)
