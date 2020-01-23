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

from wuhanncov.dingxiangyuan import DingXiangYuan
from wuhanncov.osx import notify

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

    def __init__(self):
        self.last_summary = None
        self.last_event_list = None
        self.last_state = None

    def _fetch(self):
        try:
            summary, event_list = DingXiangYuan().fetch()
            notify_title = None
            notify_message_list = list()
            last_msg = None
            if summary is None:
                time.sleep(2)
                self._fetch()
                return

            if self.last_summary is None:
                notify_title = summary.print_desc()
                notify_message_list = event_list.print_desc()
            else:
                notify_title = summary.print_desc(self.last_summary)
                notify_message_list = event_list.print_desc_with_compare(self.last_event_list)

            self.last_summary = summary
            self.last_event_list = event_list

            if notify_title is None:
                if len(notify_message_list) > 0:
                    last_msg = notify_message_list[0]
                    notify_title = last_msg
                else:
                    notify_title = None
            else:
                if len(notify_message_list) > 0:
                    last_msg = notify_message_list[0]
                else:
                    last_msg = "无新闻只有总数变化"

            if notify_title is not None:
                notify(title=notify_title,
                       subtitle=u"包含更新%d条" % len(notify_message_list),
                       message=u"最后一条: %s" % last_msg)

            self.last_state = "Refresh Success"
        except ConnectionError:
            self.last_state = "Connect Failed"

    def start(self):
        # first enter just print news
        self._fetch()
        random_min_interval = 5
        random_max_interval = 20

        i = 0
        interval_sec = randint(random_min_interval, random_max_interval)
        thread = None
        while True:
            try:
                if thread and thread.isAlive():
                    info = 'checking news.....              '
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
            except KeyboardInterrupt:
                exit(0)
