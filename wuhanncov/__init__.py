# coding=utf-8
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
__author__ = 'JacksGong'
__version__ = '0.0.5'
__description__ = 'This tool is used for crawl Wuhan 2019nCov Info'

from wuhanncov.check_loop import CheckLoop


def main():
    print("-------------------------------------------------------")
    print("                  WuHan 2019nCov v" + __version__)
    print("")
    print("     https://github.com/Jacksgong/wuhan-2019-nCoV   ")
    print("    This tool is used for crawl Wuhan 2019nCov Info   ")
    print("")
    print("                   Hope You Safe!")
    print("-------------------------------------------------------")

    CheckLoop().start()
