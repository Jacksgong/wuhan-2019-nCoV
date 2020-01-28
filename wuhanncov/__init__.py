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
__version__ = '0.1.2'
__description__ = 'This tool is used for crawl Wuhan 2019nCov Info'

import argparse

from wuhanncov.check_loop import CheckLoop
from wuhanncov.dingxiangyuan import DingXiangYuan
from wuhanncov.fenghuang import FengHuang
from wuhanncov.output_helper import OutputHelper
from wuhanncov.toutiao import TouTiao
from wuhanncov.wangyi import WangYi
from wuhanncov.yanshixinwen import YanShiXinWen


def main():
    print("-------------------------------------------------------")
    print("                  WuHan 2019nCov v" + __version__)
    print("")
    print("     https://github.com/Jacksgong/wuhan-2019-nCoV   ")
    print("    This tool is used for crawl Wuhan 2019nCov Info   ")
    print("")
    print("                   Hope You Safe!")
    print("-------------------------------------------------------")

    dimensions = {
        'all': 'all',
        'lark': 'lark',
        'terminal': 'terminal',
        'mac': 'mac'
    }
    parser = argparse.ArgumentParser(description=__description__)

    parser.add_argument('dimension', nargs='*',
                        help='output dimensions: {}'.format(', '.join(dimensions)),
                        default=['terminal', 'mac'])
    parser.add_argument('-lark-url', '--lark-url', dest='lark_url',
                        help='the webhook or lark url for lark dimension for lark notify',
                        default='')
    parser.add_argument('--hide-terminal-process', dest='hide_terminal_process', action='store_true',
                        help='whether need to hide process waiting output')
    parser.add_argument('--ignore-first-two-note', dest='ignore_first_two_note', action='store_true',
                        help='whether need to ignore first two output')

    args = parser.parse_args()
    OutputHelper.lark_url = args.lark_url
    hide_terminal_process = args.hide_terminal_process
    ignore_first_two_note = args.ignore_first_two_note

    print ".........................."
    print "Output Dimensions: [%s]" % ', '.join(args.dimension)
    if len(OutputHelper.lark_url) > 0:
        print "Lark Url: " + OutputHelper.lark_url
    if hide_terminal_process:
        print "Hide terminal process waiting output"
    if ignore_first_two_note:
        print "Ignore first two output"
    print ".........................."

    for dimension in args.dimension:
        if dimension not in dimensions:
            print "supported dimensions are: %s" % ', '.join(dimensions)
            exit(-1)

        OutputHelper.is_terminal_output = (dimension == 'all' or dimension == 'terminal')
        OutputHelper.is_lark_output = (dimension == 'all' or dimension == 'lark')
        OutputHelper.is_mac_output = (dimension == 'all' or dimension == 'mac')

    CheckLoop([DingXiangYuan(), WangYi(), YanShiXinWen(), FengHuang(), TouTiao()]) \
        .start(hide_terminal_process, ignore_first_two_note)
