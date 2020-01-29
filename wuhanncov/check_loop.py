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
import time
from random import randint
from sys import stdout
from threading import Thread

from requests import ConnectionError
from requests.exceptions import ChunkedEncodingError

from wuhanncov.dingxiangyuan import Summary
from wuhanncov.output_helper import notify_mac_msg

bar = [
    " [=     ]",
    " [ =    ]",
    " [  =   ]",
    " [   =  ]",
    " [    = ]",
    " [     =]",
    " [    = ]",
    " [   =  ]",
    " [  =   ]",
    " [ =    ]",
]


class CheckLoop:

    def __init__(self, cache_path, source_list):
        self.last_summary = None
        self.last_event_list = None
        self.last_state = None
        # todo use for fetch data and compare, need a unified compare
        self.source_list = source_list
        self.cache_path = cache_path

    def _fetch(self, ignore_first_two_note=False):
        try:
            summary, event_list = self.source_list[0].fetch()
            if summary is None:
                time.sleep(5)
                self._fetch(ignore_first_two_note)
                return

            notify_title = None
            notify_message_list = list()

            if self.last_summary is None:
                if not ignore_first_two_note:
                    notify_title = summary.print_desc()
                    notify_message_list = event_list.print_desc()
            else:
                notify_title = summary.print_desc(self.last_summary)
                notify_message_list = event_list.print_desc_with_compare(self.last_event_list)

            if notify_title is not None or self.last_summary is None:
                # valid summary
                summary.write_to_file(self.cache_path)
                self.last_summary = summary

            if len(notify_message_list) > 0 or self.last_event_list is None:
                # valid event list
                self.last_event_list = event_list

            if not ignore_first_two_note:
                notify_mac_msg(notify_title, notify_message_list)

            self.last_state = "Refresh Success"
        except ConnectionError:
            self.last_state = "Connect Failed"
        except ChunkedEncodingError:
            self.last_state = "Chunked Encoding Failed"

    def start(self, hide_terminal_process, ignore_first_two_note):
        summary = Summary().restore_from_file(self.cache_path)
        if summary:
            self.last_summary = summary

        # first enter just print news
        self._fetch(ignore_first_two_note)

        random_min_interval = 5
        random_max_interval = 20

        i = 0
        interval_sec = randint(random_min_interval, random_max_interval)
        thread = None
        while True:
            try:
                if not hide_terminal_process:
                    if thread and thread.isAlive():
                        info = 'checking news.....                                            '

                    else:
                        interval_sec -= .2
                        info = "waiting next check less %ds     " % interval_sec
                        if self.last_state:
                            info = "[Last %s] %s" % (self.last_state, info)

                    print(bar[i % len(bar)] + ' ' + info + '\r'),
                    i += 1
                    stdout.flush()
                    time.sleep(.2)
                    if interval_sec <= 0:
                        thread = Thread(target=self._fetch)
                        thread.start()
                        interval_sec = randint(random_min_interval, random_max_interval)
                else:
                    info = "waiting %ds for next check      " % interval_sec
                    info = "[Last %s] %s" % (self.last_state, info)
                    print(info + '\r'),
                    stdout.flush()
                    time.sleep(interval_sec)
                    interval_sec = randint(random_min_interval, random_max_interval)
                    print('checking news.....                                            \r'),
                    stdout.flush()
                    self._fetch()

            except KeyboardInterrupt:
                exit(0)
